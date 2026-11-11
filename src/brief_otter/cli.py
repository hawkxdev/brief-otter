"""Offline command lifecycle."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn

from brief_otter.config import (
    ConfigurationError,
    find_project_root,
    load_settings,
)
from brief_otter.domain import ExitCode


class SafeParser(argparse.ArgumentParser):
    """Sanitized argument failures."""

    def error(self, message: str) -> NoReturn:
        """Hide untrusted arguments."""
        self.print_usage(sys.stderr)
        self.exit(ExitCode.INVALID_INPUT, 'brief-otter: invalid_arguments\n')


def build_parser() -> argparse.ArgumentParser:
    """Describe offline command."""
    parser = SafeParser(
        prog='brief-otter', description='Local opportunity review foundation.'
    )
    commands = parser.add_subparsers(dest='command', required=True)
    collect = commands.add_parser('collect', help='Validate collection setup')
    collect.add_argument('--config', type=Path, required=True)
    collect.add_argument('--allow-ai', action='store_true')
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run offline preflight."""
    args = build_parser().parse_args(argv)
    if not args.allow_ai:
        print('brief-otter: ai_opt_in_required', file=sys.stderr)
        return ExitCode.INVALID_INPUT
    try:
        root = find_project_root(Path.cwd())
        load_settings(args.config, root)
    except ConfigurationError as error:
        print(f'brief-otter: {error}', file=sys.stderr)
        return ExitCode.INVALID_INPUT
    print('brief-otter: collection_not_implemented', file=sys.stderr)
    return ExitCode.FAILED
