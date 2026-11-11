"""Local response validation."""

import json
from typing import Literal

from pydantic import Field, ValidationError

from brief_otter.domain import StrictRecord

Intent = Literal[
    'project_request',
    'job_vacancy',
    'executor_ad',
    'resume',
    'editorial',
    'uncertain',
]
Topic = Literal['match', 'no_match', 'uncertain']


class Classification(StrictRecord):
    """Three field response."""

    intent: Intent
    topic: Topic
    reason: str = Field(min_length=1, max_length=240, pattern=r'\S')


class ClassificationError(ValueError):
    """Sanitized response failure."""


def reject_constant(value: str) -> object:
    """Reject nonfinite literals."""
    raise ClassificationError('invalid_json_constant')


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject duplicate keys."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ClassificationError('duplicate_json_key')
        result[key] = value
    return result


def parse_classification(text: str) -> Classification:
    """Validate untrusted response."""
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
        return Classification.model_validate(value)
    except ValueError, TypeError, RecursionError, ValidationError:
        raise ClassificationError('invalid_classification') from None
