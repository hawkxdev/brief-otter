"""Synthetic configuration fixtures."""

import json
from pathlib import Path
from typing import Any


def make_payload(directory: Path) -> dict[str, Any]:
    """Build explicit settings."""
    return {
        'source': {'username': '@Sample_Channel'},
        'report': {'path': str(directory / 'latest.html')},
        'ai': {
            'endpoint': 'https://api.z.ai/api/paas/v4/chat/completions',
            'model': 'glm-5.3-flash',
            'max_calls': 100,
            'deadline_seconds': 900,
            'budget_usd': '1.00',
            'state_path': str(directory / 'attempt.json'),
        },
    }


def write_config(path: Path, payload: dict[str, Any]) -> Path:
    """Write synthetic TOML."""
    lines: list[str] = []
    for section, values in payload.items():
        lines.append(f'[{section}]')
        lines.extend(
            f'{key} = {json.dumps(value)}' for key, value in values.items()
        )
        lines.append('')
    path.write_text('\n'.join(lines))
    path.chmod(0o600)
    return path
