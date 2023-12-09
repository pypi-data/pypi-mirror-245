"""
Utilities for working with docker compose.
"""
from contextlib import contextmanager, ExitStack
import enum
import io
import os.path
import pathlib
import shlex
import subprocess
import tarfile
import tempfile
from typing import Iterable, Iterator

import docker
import docker.errors
import docker.models
from unholy.junk_drawer import tarfile_add

from .config import app_dirs
from .docker import get_client, smart_pull, mount, inject_and_run, container_run, wait_for_status


class Label(enum.StrEnum):
    # From https://github.com/docker/compose/blob/7daa2a5325c2fe2608db90e6f4500fac21bd53b7/pkg/api/labels.go#L28-L59
    #: allow to track resource related to a compose project
    Project = "com.docker.compose.project"
    #: allow to track resource related to a compose service
    Service = "com.docker.compose.service"
    #: stores configuration hash for a compose service
    ConfigHash = "com.docker.compose.config-hash"
    #: stores the container index of a replicated service
    ContainerNumber = "com.docker.compose.container-number"
    #: allow to track resource related to a compose volume
    Volume = "com.docker.compose.volume"
    #: allow to track resource related to a compose network
    Network = "com.docker.compose.network"
    #: stores absolute path to compose project working directory
    WorkingDir = "com.docker.compose.project.working_dir"
    #: stores absolute path to compose project configuration files
    ConfigFiles = "com.docker.compose.project.config_files"
    #: stores absolute path to compose project env file set by `- -env-file`
    EnvironmentFile = "com.docker.compose.project.environment_file"
    #: stores value 'True' for one-off containers created by `compose run`
    OneOff = "com.docker.compose.oneoff"
    #: stores unique slug used for one-off container identity
    Slug = "com.docker.compose.slug"
    #: stores digest of the container image used to run service
    ImageDigest = "com.docker.compose.image"
    #: stores service dependencies
    Dependencies = "com.docker.compose.depends_on"
    #: stores the compose tool version used to build/run application
    Version = "com.docker.compose.version"
    #: stores the builder(classic or BuildKit) used to produce the image.
    ImageBuilder = "com.docker.compose.image.builder"
    #: is set when container is created to replace another container(recreated)
    ContainerReplace = "com.docker.compose.replace"


class Compose:
    """
    Wrapper around a docker client that does all the extra compose bits.

    (Mostly labelling.)
    """

    def __init__(self, name, unholy_config):
        self.config = unholy_config
        self.name = name
        self.project_name = \
            unholy_config.get('compose', {}).get('project') \
            or name

        self.client = get_client(self.config.get('context', None))

    def volume_list(self) -> Iterator[docker.models.volumes.Volume]:
        """
        Enumerate realized volumes associated with this project.
        """
        for vol in self.client.volumes.list():
            if vol.attrs['Labels'] and \
                    vol.attrs['Labels'].get(Label.Project) == self.project_name:
                yield vol

    def volume_create(self, name, *, labels=None) -> docker.models.volumes.Volume:
        """
        Create a volume in the compose project
        """
        labels = labels or {}
        return self.client.volumes.create(
            name=f"{self.project_name}_{name}",
            labels={
                Label.Project: self.project_name,
                Label.Volume: name,
            } | labels,
        )

    def _socket_mount_opts(self):
        """
        Get the options needed for a container to access the docker socket.
        """
        # TODO: Use https://github.com/Tecnativa/docker-socket-proxy instead?
        return {
            'environment': {
                'DOCKER_HOST': 'unix:///var/run/docker.sock',
            },
            'mounts': [
                docker.types.Mount(
                    target='/var/run/docker.sock',
                    source='/var/run/docker.sock',  # FIXME: Detect this
                    type='bind',
                )
            ],
            # 'privledged': True,
        }

    def container_list(self) -> Iterator[docker.models.containers.Container]:
        """
        Enumerate realized containers associated with this project.
        """
        for con in self.client.containers.list(all=True):
            if con.labels.get(Label.Project) == self.project_name:
                yield con

    def container_create(
        self, service, image, *,
        one_off=None, labels=None, mount_docker_socket=False,
        environment=None, mounts=None,
        **opts
    ):
        # FIXME: Implement service increment
        default_labels = {
            Label.Project: self.project_name,
            Label.Service: service,
        }
        if one_off is not None:
            default_labels[Label.OneOff] = repr(bool(one_off))
        if labels is not None:
            labels = default_labels | labels
        else:
            labels = default_labels
        if mount_docker_socket:
            socket_bits = self._socket_mount_opts()
            if environment is None:
                environment = {}
            environment |= socket_bits.pop('environment', {})
            if mounts is None:
                mounts = []
            mounts += socket_bits.pop('mounts', [])
            opts |= socket_bits

        return self.client.containers.create(
            name=f"{self.project_name}-{service}-1",
            image=image,
            labels=labels,
            environment=environment,
            mounts=mounts,
            **opts
        )

    def docker_cmd(self, *cmd: str | docker.models.containers.Container):
        """
        Builds the command to invoke docker locally.
        """
        prefix = ['docker']
        if 'context' in self.config:
            prefix += ['--context', self.config['context']]
        return [*prefix, *(
            bit.name if isinstance(bit, docker.models.containers.Container)
            else str(bit)
            for bit in cmd
        )]

    @contextmanager
    def docker_script(self, *cmd: str | docker.models.containers.Container, **opts):
        """
        Writes out a script to invoke docker itself.
        """
        with tempfile.NamedTemporaryFile('wt+', delete_on_close=False, **opts) as ntf:
            ntf.write("#!/bin/bash\n")  # We use a bashism below
            ntf.write('exec ')
            ntf.write(shlex.join(self.docker_cmd(*cmd)))
            ntf.write(' "$@"\n')
            ntf.flush()

            os.chmod(ntf.name, 0o755)

            # Gotta close the file, else "text file busy"
            ntf.close()
            yield ntf.name


class UnholyCompose(Compose):
    """
    Adds unholy-specific resource concepts to Compose.
    """

    # There's three resources that unholy cares about:
    # * The workspace--the persistent place to keep the project
    # * The devenv--A semi-ephemeral container the user actually works in
    # * Bootstrap container--Ephemeral container used for some operations when
    #   a devenv might not be available

    BOOTSTRAP_IMAGE = 'ghcr.io/astraluma/unholy/bootstrap:trunk'
    WORKSPACE_MOUNTPOINT = '/workspace'
    DEVENV_SERVICE = 'devenv'

    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self.workspace_name = self.config.get('dev', {}).get('volume')

    def workspace_get(self) -> None | docker.models.volumes.Volume:
        """
        Searches for the workspace, or returns None
        """
        for vol in self.volume_list():
            if vol.attrs['Labels'].get(Label.Volume) == self.workspace_name:
                return vol

    def workspace_create(self) -> docker.models.volumes.Volume:
        """
        Creates a fresh workspace
        """
        assert self.workspace_get() is None
        return self.volume_create(self.workspace_name)

    def workspace_delete(self):
        """
        Deletes the workspace
        """
        vol = self.workspace_get()
        if vol is not None:
            vol.remove()

    def _inject_config(self, cont: docker.models.containers.Container):
        """
        Copy some specific user config files to the container
        """
        real_home = pathlib.Path.home()
        cont_home = container_run(
            cont, ['/bin/sh', '-c', 'echo ~'],
            stdout=subprocess.PIPE, encoding='utf-8',
        ).stdout.strip()

        files_to_try = [
            real_home / '.gitconfig',
            real_home / '.ssh' / 'known_hosts',
            *(real_home / '.ssh').glob('*.pub'),
            # real_home / '.ssh' / 'config',  # XXX: Include this?
        ]

        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode='w:') as tf:
            for file in files_to_try:
                if file.exists():
                    st = file.stat()
                    tarfile_add(
                        tf, str(file.relative_to(real_home)), file.read_bytes(),
                        mode=st.st_mode,
                    )

        buf.seek(0)
        cont.put_archive(cont_home, buf)

    @contextmanager
    def bootstrap_spawn(self, accessories=True) -> docker.models.containers.Container:
        """
        Start a bootstrap container and clean it up when done.

        Args:
            accessories: Whether to include config blobs, ssh agent, and other bits
        """
        img = smart_pull(self.client, self.BOOTSTRAP_IMAGE)
        proj = self.workspace_get()
        assert proj is not None
        cont = self.container_create(
            'bootstrap', img,
            one_off=True,
            init=True,
            auto_remove=True,
            mounts=[
                mount(self.WORKSPACE_MOUNTPOINT, proj),
            ],
            working_dir=self.WORKSPACE_MOUNTPOINT,
            mount_docker_socket=accessories,
            environment={
                'SSH_AUTH_SOCK': self.agent_path(),
            },
        )
        print("Starting")
        cont.start()
        if accessories:
            self._inject_config(cont)
            wait_for_status(cont, 'running')
            self.ensure_agent_forward(cont)
        try:
            yield cont
        finally:
            cont.stop()
            try:
                cont.remove()
            except docker.errors.APIError:
                # This usually happens, because auto_remove
                pass

    def devenv_get(self) -> None | docker.models.containers.Container:
        """
        Get the devenv container, if it exists.
        """
        for con in self.container_list():
            if con.labels.get(Label.Service) == self.DEVENV_SERVICE:
                if not con.status != 'running':
                    con.start()
                return con

    def devenv_create(self, scripts: Iterable[str]):
        """
        Create the devenv container.

        Args:
            scripts: The list of configuration scripts to run.
        """
        img = smart_pull(self.client, self.config['dev']['image'])
        proj = self.workspace_get()
        assert proj is not None
        cont = self.container_create(
            self.DEVENV_SERVICE, img,
            command=['sleep', 'infinity'],
            hostname=self.name,  # FIXME: read from config
            init=True,
            mounts=[
                mount(self.WORKSPACE_MOUNTPOINT, proj),
                # TODO: Other mounts
            ],
            tmpfs={
                '/tmp': '',
            },
            working_dir=self.WORKSPACE_MOUNTPOINT,
            mount_docker_socket=True,
            environment={
                'SSH_AUTH_SOCK': self.agent_path(),
            },
            # TODO: Networks
        )
        cont.start()
        self._inject_config(cont)
        for i, script in enumerate(scripts):
            if script:
                inject_and_run(
                    cont, fix_script(script),
                    cwd=self.WORKSPACE_MOUNTPOINT,
                    name=f'unholyscript-{i}'
                )
        return cont

    def get_unholyfile(self) -> str:
        """
        Gets the config file from the workspace.
        """
        with ExitStack() as stack:
            if (cont := self.devenv_get()) is not None:
                pass
            else:
                cont = stack.enter_context(self.bootstrap_spawn(accessories=False))

            try:
                tarblob, _ = cont.get_archive(f'{self.WORKSPACE_MOUNTPOINT}/Unholyfile')
            except docker.errors.NotFound as exc:
                raise FileNotFoundError("Unholyfile not in workspace") from exc
            buffer = io.BytesIO()
            for bit in tarblob:
                buffer.write(bit)
            buffer.seek(0)
            with tarfile.open(fileobj=buffer, mode='r|') as tf:
                for member in tf:
                    name = os.path.basename(member.name)
                    if name == 'Unholyfile':
                        assert member.isfile()
                        return tf.extractfile(member).read().decode('utf-8')

        raise RuntimeError("Unable to find Unholyfile in workspace.")

    def compose_cmd(self, *cmd) -> list[str]:
        """
        Builds the command to invoke compose in the devenv
        """
        return [
            'docker', 'compose',
            '--file', pathlib.PurePosixPath(self.WORKSPACE_MOUNTPOINT) / self.config['compose']['file'],
            '--project-name', self.config['compose']['project'],
            # '--project-directory', self.WORKSPACE_MOUNTPOINT,
            *cmd
        ]

    def compose_run(self, *cmd, container=None, **opts):
        """
        Run compose in the devenv
        """
        if container is None:
            container = self.devenv_get()
        assert container is not None

        opts.setdefault('cwd', self.WORKSPACE_MOUNTPOINT)
        opts.setdefault('check', True)

        return container_run(
            container, self.compose_cmd(*cmd),
            **opts
        )

    def _ssh_lockfile(self):
        """
        Path to use for socat lockfile
        """
        path = pathlib.Path(app_dirs().user_config_dir)
        if not path.exists():
            path.mkdir(parents=True)
        return path / f"{self.name}.agent-lock"

    def agent_path(self):
        """
        The path of the agent socket inside the container.
        """
        return "/var/run/ssh-agent.sock"

    def ensure_agent_forward(self, cont=None):
        if 'SSH_AUTH_SOCK' not in os.environ:
            # No agent in the parent environment
            return
        lf = self._ssh_lockfile()
        if lf.exists():
            # FIXME: Actually check that socat is still running
            # (The lock file contains the PID, so we can look up
            # if the process still exists and if it looks like
            # one of ours)
            # Forward is already running
            return
        if cont is None:
            cont = self.devenv_get()
        cmd = self.docker_cmd(
            'exec', '--interactive', cont,
            'socat',
            'STDIO',
            f'UNIX-LISTEN:{self.agent_path()},unlink-early,forever,fork,max-children=1',
        )
        subprocess.Popen(
            [
                'socat', f"-L{lf}",
                f"UNIX-CONNECT:{os.environ['SSH_AUTH_SOCK']}",
                f'EXEC:"{" ".join(cmd)}"'
            ]
        )


def fix_script(script: str) -> str:
    if not script.startswith('#!'):
        script = '#!/bin/sh\n' + script
    return script
