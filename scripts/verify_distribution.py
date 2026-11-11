"""Inspect local distributions."""

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SAFE_ENVIRONMENT = ('PATH', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TZ', 'TMPDIR')


def run(arguments: list[str], cwd: Path, extra: dict[str, str]) -> None:
    """Run isolated qualification."""
    environment = {
        key: os.environ[key] for key in SAFE_ENVIRONMENT if key in os.environ
    }
    environment.update(extra)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    subprocess.run(arguments, cwd=cwd, env=environment, check=True)


def checked_name(name: str) -> PurePosixPath:
    """Validate archive member."""
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('unsafe_archive_member')
    return path


def qualify_import(expected: Path, cwd: Path, pythonpath: str) -> None:
    """Verify actual imports."""
    run(
        [
            sys.executable,
            '-c',
            'import sys; from pathlib import Path; import brief_otter; '
            'module_file = Path(brief_otter.__file__); '
            'assert module_file.is_relative_to(sys.argv[1]); '
            'print("Qualified module origin:", module_file); '
            'from brief_otter.cli import main; main(["--help"])',
            str(expected),
        ],
        cwd,
        {'PYTHONPATH': pythonpath},
    )


def require_same_bytes(actual: bytes, expected: Path) -> None:
    """Verify product bytes."""
    if (
        hashlib.sha256(actual).digest()
        != hashlib.sha256(expected.read_bytes()).digest()
    ):
        raise ValueError('archive_content_mismatch')


def inspect_wheel(wheel: Path, distribution: str) -> None:
    """Verify wheel contents."""
    configuration = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    selected = configuration['tool']['hatch']['build']['targets']['wheel'][
        'only-include'
    ]
    product = {
        Path(name).relative_to('src').as_posix(): ROOT / name
        for name in selected
    }
    metadata = distribution + '.dist-info/'
    allowed = set(product) | {
        metadata + suffix
        for suffix in (
            'METADATA',
            'WHEEL',
            'entry_points.txt',
            'RECORD',
            'licenses/LICENSE',
        )
    }
    with zipfile.ZipFile(wheel) as archive:
        entries = archive.infolist()
        members = {info.filename for info in entries}
        if len(entries) != len(members):
            raise ValueError('duplicate_wheel_member')
        if members != allowed:
            raise ValueError(f'unexpected_wheel_members: {members ^ allowed}')
        for info in archive.infolist():
            checked_name(info.filename)
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('archive_link_forbidden')
        for name, source in product.items():
            require_same_bytes(archive.read(name), source)
        require_same_bytes(
            archive.read(metadata + 'licenses/LICENSE'), ROOT / 'LICENSE'
        )
    print(f'Wheel: {len(members)} approved members')


def source_members() -> dict[str, Path]:
    """Declare source contents."""
    configuration = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    selected = configuration['tool']['hatch']['build']['targets']['sdist'][
        'only-include'
    ]
    members: dict[str, Path] = {}
    for name in selected:
        checked_name(name)
        source = ROOT / name
        if source.is_symlink() or not source.is_file() or name in members:
            raise ValueError('invalid_explicit_source_selection')
        members[name] = source
    python_sources = {
        path.relative_to(ROOT).as_posix()
        for folder in ['src', 'tests']
        for path in (ROOT / folder).rglob('*.py')
    }
    if not python_sources <= set(members):
        raise ValueError('unselected_python_source')
    return members


def inspect_source(archive_path: Path, destination: Path) -> Path:
    """Verify source contents."""
    expected = source_members()
    with tarfile.open(archive_path) as archive:
        actual: dict[str, tarfile.TarInfo] = {}
        prefix: str | None = None
        for info in archive.getmembers():
            path = checked_name(info.name)
            if prefix is None:
                prefix = path.parts[0]
            if path.parts[0] != prefix:
                raise ValueError('multiple_archive_roots')
            if info.isdir():
                continue
            if not info.isfile():
                raise ValueError('archive_link_forbidden')
            relative = PurePosixPath(*path.parts[1:]).as_posix()
            if relative in actual:
                raise ValueError('duplicate_archive_member')
            actual[relative] = info
        if set(actual) != set(expected) | {'PKG-INFO'}:
            raise ValueError(
                f'unexpected_source_members: '
                f'{set(actual) ^ (set(expected) | {"PKG-INFO"})}'
            )
        for name, source in expected.items():
            stream = archive.extractfile(actual[name])
            if stream is None:
                raise ValueError('missing_archive_content')
            require_same_bytes(stream.read(), source)
        archive.extractall(destination, filter='data')
    if prefix is None:
        raise ValueError('empty_source_archive')
    print(f'Source: {len(actual)} approved members')
    return destination / prefix


def main() -> None:
    """Qualify built artifacts."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--tests', action='store_true')
    arguments = parser.parse_args()
    metadata = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']
    distribution = re.sub(r'[-_.]+', '_', metadata['name'])
    distribution += '-' + metadata['version']
    wheel = ROOT / 'dist' / (distribution + '-py3-none-any.whl')
    source = ROOT / 'dist' / (distribution + '.tar.gz')
    inspect_wheel(wheel, distribution)
    with tempfile.TemporaryDirectory(prefix='brief-otter-package-') as temp:
        temporary = Path(temp)
        extracted = inspect_source(source, temporary / 'source')
        uv = str(Path(sys.executable).parent / 'uv')
        target = temporary / 'installed'
        run(
            [
                uv,
                'pip',
                'install',
                '--offline',
                '--no-deps',
                '--python',
                sys.executable,
                '--target',
                str(target),
                str(wheel),
            ],
            temporary,
            {},
        )
        qualify_import(target, temporary, str(target))
        run(
            [
                uv,
                'build',
                '--wheel',
                '--offline',
                '--no-build-isolation',
                '--python',
                sys.executable,
                '--out-dir',
                str(temporary / 'rebuilt'),
                str(extracted),
            ],
            temporary,
            {},
        )
        print('Wheel import and source rebuild passed')
        if arguments.tests:
            source_path = os.pathsep.join(
                [str(extracted / 'src'), str(extracted)]
            )
            qualify_import(extracted / 'src', extracted, source_path)
            run(
                [
                    sys.executable,
                    '-m',
                    'pytest',
                    'tests/',
                ],
                extracted,
                {'PYTHONPATH': source_path},
            )


if __name__ == '__main__':
    main()
