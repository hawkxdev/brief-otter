"""Offline command behavior."""

import subprocess
import sys
from pathlib import Path

import pytest

from brief_otter import cli
from tests.helpers import make_payload, write_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('arguments', [['--help'], ['collect', '--help']])
def test_help_does_not_resolve_configuration(
    monkeypatch: pytest.MonkeyPatch, arguments: list[str]
) -> None:
    def unexpected_access(*args: object) -> None:
        """Reject premature access."""
        raise AssertionError('configuration_was_read')

    monkeypatch.setattr(cli, 'find_project_root', unexpected_access)
    with pytest.raises(SystemExit) as result:
        cli.main(arguments)
    assert result.value.code == 0


def test_installed_command_help_works_outside_checkout(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(Path(sys.executable).parent / 'brief-otter'),
            '--help',
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert 'Local opportunity review foundation' in result.stdout


@pytest.mark.parametrize(
    'arguments', [[], ['collect'], ['unknown'], ['--synthetic_secret_marker']]
)
def test_invalid_arguments_exit_two_without_echoing_values(
    arguments: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as result:
        cli.main(arguments)
    assert result.value.code == 2
    output = capsys.readouterr()
    assert 'invalid_arguments' in output.err
    assert 'synthetic_secret_marker' not in output.err


def test_runtime_ai_opt_in_is_required(
    private_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    result = cli.main(['collect', '--config', str(private_dir / 'missing')])
    assert result == 2
    assert 'ai_opt_in_required' in capsys.readouterr().err


def test_invalid_explicit_config_never_claims_success(
    private_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(ROOT)
    result = cli.main(
        [
            'collect',
            '--allow-ai',
            '--config',
            str(private_dir / 'missing'),
        ]
    )
    assert result == 2
    assert 'invalid_configuration_file' in capsys.readouterr().err


def test_valid_setup_stops_before_collection_or_output(
    private_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(ROOT)
    path = write_config(
        private_dir / 'settings.toml', make_payload(private_dir)
    )
    old = private_dir / 'latest.html'
    old.write_text('previous artifact')
    old.chmod(0o600)
    result = cli.main(['collect', '--allow-ai', '--config', str(path)])
    output = capsys.readouterr()
    assert result == 5
    assert output.out == ''
    assert 'collection_not_implemented' in output.err
    assert old.read_text() == 'previous artifact'
    assert not (private_dir / 'attempt.json').exists()


def test_module_entry_preserves_failure_exit(private_dir: Path) -> None:
    path = write_config(
        private_dir / 'settings.toml', make_payload(private_dir)
    )
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'brief_otter',
            'collect',
            '--allow-ai',
            '--config',
            str(path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 5
    assert 'collection_not_implemented' in result.stderr
