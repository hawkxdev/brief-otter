"""Synthetic test boundary."""

from pathlib import Path

import pytest

from tests.offline_support import install, scrub_environment

install()


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register model option."""
    parser.addoption('--run-ai', action='store_true', default=False)


def pytest_configure(config: pytest.Config) -> None:
    """Reject unavailable admission."""
    if config.getoption('--run-ai'):
        raise pytest.UsageError('real_model_group_not_implemented')


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Keep model cases gated."""
    for item in items:
        if item.get_closest_marker('ai'):
            item.add_marker(pytest.mark.skip(reason='real_model_not_admitted'))


@pytest.fixture(autouse=True)
def isolated_environment() -> None:
    """Reset synthetic environment."""
    scrub_environment()


@pytest.fixture
def private_dir(tmp_path: Path) -> Path:
    """Create private fixture."""
    directory = tmp_path / 'private'
    directory.mkdir(mode=0o700)
    return directory


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """Create synthetic checkout."""
    directory = tmp_path / 'checkout'
    directory.mkdir(mode=0o700)
    (directory / 'pyproject.toml').write_text(
        "[project]\nname = 'brief-otter'\n"
    )
    return directory
