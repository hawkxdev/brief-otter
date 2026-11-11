"""Runtime import qualification."""

import importlib
import importlib.metadata
import sys

import pytest


def test_selected_python_is_running() -> None:
    assert sys.version_info[:3] == (3, 14, 10)


@pytest.mark.parametrize(
    'module,distribution,version',
    [
        ('telethon', 'telethon', '1.45.0'),
        ('httpx', 'httpx', '0.28.1'),
        ('pydantic', 'pydantic', '2.14.3'),
    ],
)
def test_selected_dependencies_import_without_network(
    module: str, distribution: str, version: str
) -> None:
    assert importlib.import_module(module) is not None
    assert importlib.metadata.version(distribution) == version


def test_distribution_exposes_the_command() -> None:
    entry = next(
        entry
        for entry in importlib.metadata.distribution(
            'brief-otter'
        ).entry_points
        if entry.group == 'console_scripts' and entry.name == 'brief-otter'
    )
    assert entry.value == 'brief_otter.cli:main'
    assert callable(entry.load())
