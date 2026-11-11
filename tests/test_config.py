"""Explicit settings checks."""

import os
import traceback
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from brief_otter.config import (
    ConfigurationError,
    find_project_root,
    load_settings,
    validate_settings,
)
from tests.helpers import make_payload, write_config


def test_valid_settings_are_explicit_and_normalized(
    private_dir: Path, project_root: Path
) -> None:
    value = validate_settings(make_payload(private_dir), project_root)
    assert value.source.username == 'sample_channel'
    assert value.ai.budget_usd == Decimal('1.00')
    assert value.collection.max_messages == 5000
    assert value.collection.request_timeout_seconds == 15


@pytest.mark.parametrize(
    'section,key,value',
    [
        ('source', 'username', ''),
        ('source', 'username', 'https://t.me/sample_channel/5'),
        ('source', 'username', 'first,second'),
        ('source', 'username', '@@sample_channel'),
        ('source', 'expected_id', 0),
        ('source', 'expected_id', True),
        ('report', 'path', 'relative.html'),
        ('report', 'excerpt_characters', 0),
        ('ai', 'endpoint', 'https://example.invalid/completions'),
        ('ai', 'model', 'other-model'),
        ('ai', 'max_calls', True),
        ('ai', 'max_calls', 0),
        ('ai', 'deadline_seconds', float('inf')),
        ('ai', 'deadline_seconds', float('nan')),
        ('ai', 'budget_usd', '-1'),
        ('ai', 'budget_usd', 'NaN'),
        ('ai', 'budget_usd', 'Infinity'),
        ('ai', 'budget_usd', 1),
        ('ai', 'budget_usd', 'not-a-decimal'),
        ('collection', 'page_size', 101),
        ('collection', 'max_pages', 0),
        ('collection', 'max_messages', '5'),
        ('collection', 'request_timeout_seconds', 181),
    ],
)
def test_invalid_settings_fail_before_access(
    private_dir: Path,
    project_root: Path,
    section: str,
    key: str,
    value: Any,
) -> None:
    payload = make_payload(private_dir)
    payload.setdefault(section, {})[key] = value
    with pytest.raises(ConfigurationError, match='^invalid_configuration$'):
        validate_settings(payload, project_root)


@pytest.mark.parametrize('section', ['source', 'report', 'ai'])
def test_missing_section_is_rejected(
    private_dir: Path, project_root: Path, section: str
) -> None:
    payload = make_payload(private_dir)
    del payload[section]
    with pytest.raises(ConfigurationError, match='invalid_configuration'):
        validate_settings(payload, project_root)


def test_small_message_budget_does_not_claim_completion(
    private_dir: Path, project_root: Path
) -> None:
    payload = make_payload(private_dir)
    payload['collection'] = {'max_messages': 2, 'page_size': 100}
    assert (
        validate_settings(payload, project_root).collection.max_messages == 2
    )


def test_checkout_output_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    payload = make_payload(private_dir)
    payload['report']['path'] = str(project_root / 'report.html')
    with pytest.raises(ConfigurationError, match='path_inside_checkout'):
        validate_settings(payload, project_root)
    assert not (project_root / 'report.html').exists()


def test_symlink_parent_cannot_hide_checkout_destination(
    private_dir: Path, project_root: Path
) -> None:
    link = private_dir / 'redirect'
    link.symlink_to(project_root, target_is_directory=True)
    payload = make_payload(private_dir)
    payload['report']['path'] = str(link / 'report.html')
    with pytest.raises(ConfigurationError, match='path_inside_checkout'):
        validate_settings(payload, project_root)


def test_symlink_destination_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    destination = private_dir / 'latest.html'
    destination.symlink_to(private_dir / 'missing.html')
    with pytest.raises(ConfigurationError, match='unsafe_path'):
        validate_settings(make_payload(private_dir), project_root)
    assert destination.is_symlink()


def test_shared_output_directory_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    private_dir.chmod(0o755)
    with pytest.raises(ConfigurationError, match='unsafe_permissions'):
        validate_settings(make_payload(private_dir), project_root)


def test_shared_existing_output_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    path = private_dir / 'latest.html'
    path.write_text('previous report')
    path.chmod(0o644)
    with pytest.raises(ConfigurationError, match='unsafe_permissions'):
        validate_settings(make_payload(private_dir), project_root)
    assert path.read_text() == 'previous report'


def test_owner_only_output_is_not_replaced(
    private_dir: Path, project_root: Path
) -> None:
    path = private_dir / 'latest.html'
    path.write_text('previous report')
    path.chmod(0o600)
    validate_settings(make_payload(private_dir), project_root)
    assert path.read_text() == 'previous report'


def test_missing_parent_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    payload = make_payload(private_dir)
    payload['report']['path'] = str(private_dir / 'missing' / 'latest.html')
    with pytest.raises(ConfigurationError, match='unsafe_path'):
        validate_settings(payload, project_root)


def test_file_cannot_be_an_output_parent(
    private_dir: Path, project_root: Path
) -> None:
    parent = private_dir / 'not_directory'
    parent.write_text('unchanged')
    parent.chmod(0o600)
    payload = make_payload(private_dir)
    payload['report']['path'] = str(parent / 'latest.html')
    with pytest.raises(ConfigurationError, match='unsafe_path'):
        validate_settings(payload, project_root)


def test_foreign_owner_is_rejected(
    private_dir: Path,
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = os.getuid()
    monkeypatch.setattr(os, 'getuid', lambda: owner + 1)
    with pytest.raises(ConfigurationError, match='unsafe_permissions'):
        validate_settings(make_payload(private_dir), project_root)


def test_directory_destination_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    (private_dir / 'latest.html').mkdir(mode=0o700)
    with pytest.raises(ConfigurationError, match='unsafe_path'):
        validate_settings(make_payload(private_dir), project_root)


def test_wrong_report_extension_is_rejected(
    private_dir: Path, project_root: Path
) -> None:
    payload = make_payload(private_dir)
    payload['report']['path'] = str(private_dir / 'latest.txt')
    with pytest.raises(ConfigurationError, match='invalid_report_extension'):
        validate_settings(payload, project_root)


def test_state_cannot_replace_report(
    private_dir: Path, project_root: Path
) -> None:
    payload = make_payload(private_dir)
    payload['ai']['state_path'] = payload['report']['path']
    with pytest.raises(ConfigurationError, match='conflicting_destinations'):
        validate_settings(payload, project_root)


def test_configuration_cannot_replace_itself(
    private_dir: Path, project_root: Path
) -> None:
    path = private_dir / 'settings.toml'
    payload = make_payload(private_dir)
    payload['ai']['state_path'] = str(path)
    write_config(path, payload)
    with pytest.raises(ConfigurationError, match='conflicting_configuration'):
        load_settings(path, project_root)


def test_secret_markers_stay_out_of_repr_and_errors(
    private_dir: Path, project_root: Path
) -> None:
    marker = 'synthetic_secret_marker'
    payload = make_payload(private_dir)
    payload['source']['username'] = marker
    settings = validate_settings(payload, project_root)
    assert marker not in repr(settings)
    payload['ai']['unexpected_secret'] = marker
    with pytest.raises(ConfigurationError) as error:
        validate_settings(payload, project_root)
    assert marker not in ''.join(traceback.format_exception(error.value))


def test_explicit_toml_loads_without_an_environment_carrier(
    private_dir: Path,
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('BRIEF_OTTER_AI_API_KEY', 'synthetic_ambient_marker')
    path = write_config(
        private_dir / 'settings.toml', make_payload(private_dir)
    )
    settings = load_settings(path, project_root)
    assert settings.ai.max_calls == 100
    assert not (private_dir / 'attempt.json').exists()


def test_invalid_toml_diagnostic_is_sanitized(
    private_dir: Path, project_root: Path
) -> None:
    path = private_dir / 'settings.toml'
    path.write_text('secret = "synthetic_unclosed_marker')
    path.chmod(0o600)
    with pytest.raises(ConfigurationError) as error:
        load_settings(path, project_root)
    assert str(error.value) == 'invalid_configuration_file'
    assert 'synthetic_unclosed_marker' not in ''.join(
        traceback.format_exception(error.value)
    )


def test_checkout_boundary_is_found_from_a_child(project_root: Path) -> None:
    child = project_root / 'nested'
    child.mkdir()
    assert find_project_root(child) == project_root


def test_unbound_checkout_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(
        ConfigurationError, match='project_boundary_unavailable'
    ):
        find_project_root(tmp_path)


def test_invalid_project_metadata_is_rejected(project_root: Path) -> None:
    (project_root / 'pyproject.toml').write_text(
        'project = "synthetic_invalid_project"\n'
    )
    with pytest.raises(
        ConfigurationError, match='project_boundary_unavailable'
    ):
        find_project_root(project_root)
