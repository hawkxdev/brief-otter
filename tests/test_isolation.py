"""Offline containment checks."""

import asyncio
import os
import socket
import subprocess
import sys
from pathlib import Path

import httpx
import pytest

from tests import offline_support
from tests.offline_support import (
    OfflineViolation,
    admit_command,
    check_environment_file,
    check_socket_family,
    safe_environment,
    scrub_environment,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('family', [socket.AF_INET6])
def test_policy_rejects_network_families(family: int) -> None:
    with pytest.raises(OfflineViolation, match='external_network_blocked'):
        check_socket_family(family)


def test_dns_is_blocked_before_resolution() -> None:
    with pytest.raises(OfflineViolation, match='external_dns_blocked'):
        socket.getaddrinfo('example.invalid', 443)


def test_tcp_is_blocked_before_connect() -> None:
    with (
        socket.socket() as connection,
        pytest.raises(OfflineViolation, match='external_network_blocked'),
    ):
        connection.connect(('192.0.2.1', 443))


def test_udp_is_blocked_before_send() -> None:
    with (
        socket.socket(type=socket.SOCK_DGRAM) as connection,
        pytest.raises(OfflineViolation, match='external_network_blocked'),
    ):
        connection.sendto(b'synthetic', ('192.0.2.1', 443))


@pytest.mark.skipif(
    not hasattr(socket.socket, 'sendmsg'), reason='sendmsg_not_on_platform'
)
def test_udp_messages_are_blocked_before_send() -> None:
    with (
        socket.socket(type=socket.SOCK_DGRAM) as connection,
        pytest.raises(OfflineViolation, match='external_network_blocked'),
    ):
        connection.sendmsg([b'synthetic'], [], 0, ('192.0.2.1', 443))


def test_http_transport_cannot_leave_process() -> None:
    with pytest.raises(OfflineViolation, match='external_dns_blocked'):
        httpx.get('https://example.invalid', trust_env=False)


def test_mock_transport_remains_usable() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        """Supply local response."""
        return httpx.Response(200, json={'local': True})

    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        result = client.get('https://example.invalid')
    assert result.json() == {'local': True}


def test_process_guard_rejects_request_binary() -> None:
    with pytest.raises(OfflineViolation, match='external_process_blocked'):
        subprocess.run(['curl', 'https://example.invalid'], check=True)


def test_positional_executable_cannot_bypass_process_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def reject_delegate(*args: object, **kwargs: object) -> None:
        """Prevent any execution."""
        raise AssertionError('unsafe_process_delegation')

    monkeypatch.setattr(offline_support, '_POPEN', reject_delegate)
    with pytest.raises(OfflineViolation, match='external_process_blocked'):
        subprocess.Popen(
            [sys.executable, 'https://example.invalid'], -1, '/usr/bin/curl'
        )


@pytest.mark.parametrize('flag', ['-I', '-E', '-S', '-IS'])
def test_python_cannot_disable_child_containment(flag: str) -> None:
    with pytest.raises(OfflineViolation, match='uncontained_python_blocked'):
        admit_command([sys.executable, flag, '-c', 'print(1)'])


def test_shell_cannot_hide_request_command() -> None:
    with pytest.raises(OfflineViolation, match='external_process_blocked'):
        subprocess.run('curl https://example.invalid', shell=True, check=True)


def test_native_shell_is_blocked() -> None:
    with pytest.raises(OfflineViolation, match='external_process_blocked'):
        os.system('curl https://example.invalid')


def test_environment_file_reads_are_blocked(tmp_path: Path) -> None:
    path = tmp_path / '.env'
    path.write_text('SYNTHETIC_KEY=synthetic_value')
    with pytest.raises(OfflineViolation, match='environment_file_blocked'):
        path.read_text()


def test_environment_file_policy_blocks_implicit_reads() -> None:
    with pytest.raises(OfflineViolation, match='environment_file_blocked'):
        check_environment_file('.env', 'r')


def test_low_level_environment_read_is_blocked(tmp_path: Path) -> None:
    path = tmp_path / '.env'
    path.write_text('SYNTHETIC_KEY=synthetic_value')
    with pytest.raises(OfflineViolation, match='environment_file_blocked'):
        descriptor = os.open(path, os.O_RDONLY)
        os.close(descriptor)


def test_child_environment_contains_no_inherited_credentials() -> None:
    result = safe_environment(
        {
            'PATH': os.defpath,
            'BRIEF_OTTER_AI_API_KEY': 'synthetic_key_marker',
            'BRIEF_OTTER_SESSION': 'synthetic_session_marker',
            'OPENAI_API_KEY': 'synthetic_other_marker',
        }
    )
    assert 'BRIEF_OTTER_AI_API_KEY' not in result
    assert 'BRIEF_OTTER_SESSION' not in result
    assert 'OPENAI_API_KEY' not in result
    assert result['PATH'] == os.defpath


def test_parent_environment_is_scrubbed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('BRIEF_OTTER_AI_API_KEY', 'synthetic_scrub_marker')
    scrub_environment()
    assert os.getenv('BRIEF_OTTER_AI_API_KEY') is None


def test_local_child_process_is_usable() -> None:
    result = subprocess.run(
        [sys.executable, '-c', 'print(42)'],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == '42\n'


def test_child_bootstrap_blocks_dns_and_removes_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('BRIEF_OTTER_AI_API_KEY', 'synthetic_parent_marker')
    code = (
        'import os,socket\n'
        "assert 'BRIEF_OTTER_AI_API_KEY' not in os.environ\n"
        'try:\n'
        " socket.getaddrinfo('example.invalid',443)\n"
        'except RuntimeError as error:\n'
        ' print(str(error))\n'
        'else:\n'
        " raise AssertionError('network_guard_missing')\n"
    )
    result = subprocess.run(
        [sys.executable, '-c', code],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == 'external_dns_blocked\n'
    assert 'synthetic_parent_marker' not in result.stdout + result.stderr


def test_collection_guard_precedes_module_import(tmp_path: Path) -> None:
    module = tmp_path / 'test_import_canary.py'
    module.write_text(
        'import socket\n'
        'import pytest\n'
        'with pytest.raises(RuntimeError, match="external_dns_blocked"):\n'
        '    socket.getaddrinfo("example.invalid",443)\n'
        'def test_local():\n'
        '    assert 1 == 1\n'
    )
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'pytest',
            '-p',
            'tests.conftest',
            '--collect-only',
            str(module),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert '1 test collected' in result.stdout


def test_full_mode_fails_explicitly_before_collection(tmp_path: Path) -> None:
    marker = tmp_path / 'collected'
    module = tmp_path / 'test_should_not_import.py'
    module.write_text(
        'from pathlib import Path\n'
        f'Path({str(marker)!r}).write_text("unexpected")\n'
    )
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'pytest',
            '-p',
            'tests.conftest',
            '--run-ai',
            str(module),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 4, result.stdout + result.stderr
    assert 'real_model_group_not_implemented' in result.stderr
    assert not marker.exists()


def test_asyncio_and_unix_socketpair_remain_usable() -> None:
    async def round_trip() -> bytes:
        """Exercise local eventloop."""
        left, right = socket.socketpair()
        try:
            left.setblocking(False)
            right.setblocking(False)
            loop = asyncio.get_running_loop()
            await loop.sock_sendall(left, b'local')
            return await loop.sock_recv(right, 5)
        finally:
            left.close()
            right.close()

    assert asyncio.run(round_trip()) == b'local'


async def test_async_mock_transport_remains_usable() -> None:
    async def respond(request: httpx.Request) -> httpx.Response:
        """Supply local response."""
        await asyncio.sleep(0)
        return httpx.Response(200, json={'local': True})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(respond)
    ) as client:
        result = await client.get('https://example.invalid')
    assert result.json() == {'local': True}
