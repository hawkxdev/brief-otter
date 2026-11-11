"""Offline process containment."""

import builtins
import inspect
import io
import os
import shutil
import socket
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / 'tests' / 'offline_bootstrap'
SAFE_ENVIRONMENT = frozenset(
    {
        'PATH',
        'LANG',
        'LC_ALL',
        'LC_CTYPE',
        'TZ',
        'TERM',
        'TMPDIR',
        'PYTHONPATH',
        'PYTHONDONTWRITEBYTECODE',
        'PYTHONIOENCODING',
        'PYTHONUTF8',
        'PYTHONNOUSERSITE',
        'VIRTUAL_ENV',
        'PYTEST_CURRENT_TEST',
        'PYTEST_DISABLE_PLUGIN_AUTOLOAD',
    }
)
NETWORK_FAMILIES = frozenset({socket.AF_INET, socket.AF_INET6})
LOCAL_PROGRAMS = frozenset({'/usr/bin/true', '/usr/bin/false'})
_INSTALLED = False
_POPEN = subprocess.Popen
_POPEN_SIGNATURE = inspect.signature(subprocess.Popen)
_OPEN = builtins.open
_IO_OPEN = io.open
_OS_OPEN = os.open


class OfflineViolation(RuntimeError):
    """Blocked external operation."""


def check_socket_family(family: int) -> None:
    """Reject network sockets."""
    if family in NETWORK_FAMILIES:
        raise OfflineViolation('external_network_blocked')


def deny_lookup(*args: Any, **kwargs: Any) -> Any:
    """Block name resolution."""
    raise OfflineViolation('external_dns_blocked')


def socket_guard(original: Any) -> Any:
    """Wrap socket operation."""

    def guarded(sock: socket.socket, *args: Any, **kwargs: Any) -> Any:
        """Enforce socket boundary."""
        check_socket_family(sock.family)
        return original(sock, *args, **kwargs)

    return guarded


def safe_environment(environment: Mapping[str, str]) -> dict[str, str]:
    """Copy nonsensitive environment."""
    result = {
        key: environment[key] for key in SAFE_ENVIRONMENT if key in environment
    }
    paths = [str(BOOTSTRAP)]
    paths.extend(filter(None, result.get('PYTHONPATH', '').split(os.pathsep)))
    paths.append(str(ROOT))
    result['PYTHONPATH'] = os.pathsep.join(dict.fromkeys(paths))
    result['PYTHONDONTWRITEBYTECODE'] = '1'
    return result


def admit_command(command: Any, shell: bool = False) -> Sequence[Any]:
    """Admit guarded children."""
    if shell or isinstance(command, str | bytes):
        raise OfflineViolation('external_process_blocked')
    if not isinstance(command, Sequence) or not command:
        raise OfflineViolation('external_process_blocked')
    program = os.fsdecode(command[0])
    executable = shutil.which(program)
    if executable is None:
        raise OfflineViolation('external_process_blocked')
    resolved = str(Path(executable).resolve())
    if resolved in LOCAL_PROGRAMS:
        return command
    if Path(resolved) != Path(sys.executable).resolve():
        raise OfflineViolation('external_process_blocked')
    for argument in command[1:]:
        argument = os.fsdecode(argument)
        if argument in {'-c', '-m'} or not argument.startswith('-'):
            break
        if argument.startswith('--') or any(
            flag in argument[1:] for flag in 'IESX'
        ):
            raise OfflineViolation('uncontained_python_blocked')
    return command


def guarded_popen(*args: Any, **kwargs: Any) -> Any:
    """Contain subprocess execution."""
    bound = _POPEN_SIGNATURE.bind(*args, **kwargs)
    command = admit_command(
        bound.arguments.get('args'), bool(bound.arguments.get('shell'))
    )
    executable = bound.arguments.get('executable')
    if executable is not None:
        admit_command([executable])
        if (
            Path(os.fsdecode(executable)).resolve()
            != Path(os.fsdecode(command[0])).resolve()
        ):
            raise OfflineViolation('alternate_executable_blocked')
    environment = bound.arguments.get('env')
    if environment is None:
        environment = os.environ
    bound.arguments['env'] = safe_environment(environment)
    return _POPEN(*bound.args, **bound.kwargs)


def deny_shell(*args: Any, **kwargs: Any) -> Any:
    """Reject raw shells."""
    raise OfflineViolation('external_process_blocked')


def spawn_guard(original: Any) -> Any:
    """Contain native spawning."""

    def guarded(
        executable: Any, argv: Any, environment: Any, **kwargs: Any
    ) -> Any:
        """Validate native child."""
        admit_command(argv)
        admit_command([executable])
        if (
            Path(os.fsdecode(executable)).resolve()
            != Path(os.fsdecode(argv[0])).resolve()
        ):
            raise OfflineViolation('alternate_executable_blocked')
        return original(
            executable, argv, safe_environment(environment), **kwargs
        )

    return guarded


def check_environment_file(file: Any, mode: str) -> None:
    """Block implicit environment."""
    if isinstance(file, str | bytes | os.PathLike):
        name = Path(os.fsdecode(file)).name
        if (name == '.env' or name.startswith('.env.')) and (
            'r' in mode or '+' in mode
        ):
            raise OfflineViolation('environment_file_blocked')


def guarded_open(file: Any, mode: str = 'r', *args: Any, **kw: Any) -> Any:
    """Guard builtin reads."""
    check_environment_file(file, mode)
    return _OPEN(file, mode, *args, **kw)


def guarded_io_open(file: Any, mode: str = 'r', *args: Any, **kw: Any) -> Any:
    """Guard pathlib reads."""
    check_environment_file(file, mode)
    return _IO_OPEN(file, mode, *args, **kw)


def guarded_os_open(
    path: Any, flags: int, mode: int = 0o777, *, dir_fd: int | None = None
) -> int:
    """Guard descriptor reads."""
    access = 'r+' if flags & os.O_RDWR else 'w' if flags & os.O_WRONLY else 'r'
    check_environment_file(path, access)
    return _OS_OPEN(path, flags, mode, dir_fd=dir_fd)


def scrub_environment() -> None:
    """Remove inherited credentials."""
    for key in list(os.environ):
        if key not in SAFE_ENVIRONMENT:
            del os.environ[key]


def install() -> None:
    """Install offline boundary."""
    global _INSTALLED
    if _INSTALLED:
        return
    scrub_environment()
    for method in [
        'connect',
        'connect_ex',
        'send',
        'sendall',
        'sendto',
        'sendmsg',
        'sendfile',
    ]:
        if not hasattr(socket.socket, method):
            continue
        setattr(
            socket.socket,
            method,
            socket_guard(getattr(socket.socket, method)),
        )
    for method in [
        'getaddrinfo',
        'gethostbyname',
        'gethostbyname_ex',
        'gethostbyaddr',
    ]:
        setattr(socket, method, deny_lookup)
    patch.object(subprocess, 'Popen', guarded_popen).start()
    os.system = deny_shell
    for method in [
        'execv',
        'execve',
        'execvp',
        'execvpe',
        'execl',
        'execle',
        'execlp',
        'execlpe',
    ]:
        setattr(os, method, deny_shell)
    for method in ['posix_spawn', 'posix_spawnp']:
        if hasattr(os, method):
            setattr(os, method, spawn_guard(getattr(os, method)))
    builtins.open = guarded_open
    io.open = guarded_io_open
    os.open = guarded_os_open
    _INSTALLED = True
