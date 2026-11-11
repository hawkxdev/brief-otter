"""Pure domain contracts."""

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from brief_otter.domain import (
    DispositionCounts,
    ExitCode,
    MessageIdentity,
    ReadingWindow,
    RunOutcome,
)


def test_identity_uses_both_source_and_message() -> None:
    first = MessageIdentity(source_id=12, message_id=3)
    assert first == MessageIdentity(source_id=12, message_id=3)
    assert first != MessageIdentity(source_id=13, message_id=3)
    assert first != MessageIdentity(source_id=12, message_id=4)
    assert first != MessageIdentity(source_id=-12, message_id=3)


@pytest.mark.parametrize(
    'source,message', [(0, 1), (1, 0), (1, -1), (True, 1), (1, True), ('1', 1)]
)
def test_invalid_identity_is_rejected(source: object, message: object) -> None:
    with pytest.raises(ValidationError):
        MessageIdentity.model_validate(
            {'source_id': source, 'message_id': message}
        )


def test_recent_window_freezes_exact_bounds() -> None:
    end = datetime(2026, 1, 8, 10, 20, 30, 500000, tzinfo=UTC)
    window = ReadingWindow.last_seven_days(end)
    assert window.start == datetime(2026, 1, 1, 10, 20, 30, 500000, tzinfo=UTC)
    assert window.end == end


@pytest.mark.parametrize(
    'offset,expected', [(-1, False), (0, True), (1, True)]
)
def test_lower_boundary(offset: int, expected: bool) -> None:
    end = datetime(2026, 1, 8, tzinfo=UTC)
    window = ReadingWindow.last_seven_days(end)
    assert (
        window.contains(window.start + timedelta(microseconds=offset))
        is expected
    )


def test_upper_boundary_is_exclusive_at_subsecond_precision() -> None:
    end = datetime(2026, 1, 8, 0, 0, 0, 500000, tzinfo=UTC)
    window = ReadingWindow.last_seven_days(end)
    assert window.contains(datetime(2026, 1, 8, tzinfo=UTC)) is True
    assert window.contains(end) is False


def test_naive_time_is_rejected() -> None:
    with pytest.raises(ValueError, match='timezone_required'):
        ReadingWindow.last_seven_days(datetime(2026, 1, 8))
    window = ReadingWindow.last_seven_days(datetime(2026, 1, 8, tzinfo=UTC))
    with pytest.raises(ValueError, match='timezone_required'):
        window.contains(datetime(2026, 1, 1))


@pytest.mark.parametrize('offset', [0, -1])
def test_reversed_or_empty_window_is_rejected(offset: int) -> None:
    instant = datetime(2026, 1, 1, tzinfo=UTC)
    with pytest.raises(ValidationError, match='invalid_interval'):
        ReadingWindow(start=instant, end=instant + timedelta(seconds=offset))


def test_counts_reconcile_disjoint_categories() -> None:
    counts = DispositionCounts(
        analysed=15,
        projects=1,
        vacancies=2,
        uncertain=3,
        excluded_intent=4,
        excluded_topic=5,
    )
    assert counts.analysed == 15


@pytest.mark.parametrize(
    'analysed,projects', [(14, 1), (15, -1), (15, True), ('15', 1)]
)
def test_invalid_counts_are_rejected(
    analysed: object, projects: object
) -> None:
    with pytest.raises(ValidationError):
        DispositionCounts.model_validate(
            {
                'analysed': analysed,
                'projects': projects,
                'vacancies': 2,
                'uncertain': 3,
                'excluded_intent': 4,
                'excluded_topic': 5,
            }
        )


def test_outcomes_keep_distinct_exit_meanings() -> None:
    assert [item.value for item in ExitCode] == [0, 2, 3, 4, 5]
    assert [item.value for item in RunOutcome] == [
        'complete',
        'partial',
        'source_unavailable',
        'failed',
    ]
