"""Response shape checks."""

import json
from pathlib import Path

import pytest

from brief_otter.classification import (
    Classification,
    ClassificationError,
    parse_classification,
)

SCHEMA = (
    Path(__file__).resolve().parents[1]
    / 'docs/specs/001-local-candidates/classification.schema.json'
)
VALID = {
    'intent': 'project_request',
    'topic': 'match',
    'reason': 'The available text describes a software task.',
}


def test_runtime_shape_matches_normative_schema() -> None:
    expected = json.loads(SCHEMA.read_text())
    actual = Classification.model_json_schema()
    assert actual['additionalProperties'] is False
    assert set(actual['required']) == set(expected['required'])
    for name in expected['properties']:
        for key, value in expected['properties'][name].items():
            assert actual['properties'][name][key] == value


@pytest.mark.parametrize(
    'intent', json.loads(SCHEMA.read_text())['properties']['intent']['enum']
)
@pytest.mark.parametrize('topic', ['match', 'no_match', 'uncertain'])
def test_all_declared_labels_are_structurally_valid(
    intent: str, topic: str
) -> None:
    text = json.dumps({**VALID, 'intent': intent, 'topic': topic})
    result = parse_classification(text)
    assert result.intent == intent
    assert result.topic == topic


@pytest.mark.parametrize(
    'text',
    [
        'null',
        '[]',
        'true',
        '1',
        '',
        '{}',
        json.dumps({**VALID, 'extra': True}),
        json.dumps({**VALID, 'intent': 'other'}),
        json.dumps({**VALID, 'topic': 'other'}),
        json.dumps({**VALID, 'reason': None}),
        json.dumps({**VALID, 'reason': 1}),
        json.dumps({**VALID, 'reason': True}),
        json.dumps({**VALID, 'reason': ''}),
        json.dumps({**VALID, 'reason': ' \n\t'}),
        json.dumps({**VALID, 'reason': 'x' * 241}),
        json.dumps(
            {key: value for key, value in VALID.items() if key != 'topic'}
        ),
        '```json\n' + json.dumps(VALID) + '\n```',
        json.dumps(VALID) + '{}',
        '{"intent":"uncertain","intent":"project_request",'
        '"topic":"match","reason":"A concrete task."}',
        '{"intent":"uncertain","topic":"match","reason":NaN}',
        '{"intent":"uncertain","topic":"match","reason":Infinity}',
    ],
    ids=[
        'null',
        'array',
        'boolean',
        'number',
        'empty',
        'missing',
        'extra',
        'intent',
        'topic',
        'reason-null',
        'reason-int',
        'reason-bool',
        'reason-empty',
        'reason-blank',
        'reason-long',
        'missing-topic',
        'fenced',
        'trailing',
        'duplicate-key',
        'nan',
        'infinity',
    ],
)
def test_invalid_responses_are_rejected(text: str) -> None:
    with pytest.raises(ClassificationError, match='^invalid_classification$'):
        parse_classification(text)


@pytest.mark.parametrize('reason', ['x' * 240, '🙂' * 240])
def test_reason_limit_counts_unicode_characters(reason: str) -> None:
    result = parse_classification(json.dumps({**VALID, 'reason': reason}))
    assert result.reason == reason


def test_error_does_not_echo_untrusted_payload() -> None:
    marker = 'synthetic_response_secret'
    with pytest.raises(ClassificationError) as error:
        parse_classification(marker)
    assert marker not in str(error.value)


def test_surrounding_whitespace_is_allowed() -> None:
    result = parse_classification(' \n' + json.dumps(VALID) + '\t')
    assert result.reason == VALID['reason']
