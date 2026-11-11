"""Pure collection contracts."""

from datetime import UTC, datetime, timedelta
from enum import IntEnum, StrEnum
from typing import Annotated, Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

DISPLAY_TIMEZONE = 'Europe/Minsk'
READING_DAYS = 7
NonnegativeCount = Annotated[int, Field(strict=True, ge=0)]


class ExitCode(IntEnum):
    """Command exit meanings."""

    COMPLETE = 0
    INVALID_INPUT = 2
    PARTIAL = 3
    SOURCE_UNAVAILABLE = 4
    FAILED = 5


class RunOutcome(StrEnum):
    """Terminal run states."""

    COMPLETE = 'complete'
    PARTIAL = 'partial'
    SOURCE_UNAVAILABLE = 'source_unavailable'
    FAILED = 'failed'


class StrictRecord(BaseModel):
    """Strict local values."""

    model_config = ConfigDict(
        strict=True, extra='forbid', frozen=True, hide_input_in_errors=True
    )


class MessageIdentity(StrictRecord):
    """Stable message identity."""

    source_id: int
    message_id: int = Field(gt=0)

    @field_validator('source_id')
    @classmethod
    def reject_zero_source(cls, value: int) -> int:
        """Reject absent identity."""
        if value == 0:
            raise ValueError('invalid_source_identity')
        return value


class ReadingWindow(StrictRecord):
    """Exclusive upper interval."""

    start: AwareDatetime
    end: AwareDatetime

    @model_validator(mode='after')
    def require_ordered_bounds(self) -> Self:
        """Validate interval order."""
        if self.start >= self.end:
            raise ValueError('invalid_interval')
        return self

    @classmethod
    def last_seven_days(cls, end: datetime) -> Self:
        """Freeze recent interval."""
        if end.tzinfo is None or end.utcoffset() is None:
            raise ValueError('timezone_required')
        end = end.astimezone(UTC)
        return cls(start=end - timedelta(days=READING_DAYS), end=end)

    def contains(self, instant: datetime) -> bool:
        """Check interval membership."""
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError('timezone_required')
        return self.start <= instant < self.end


class DispositionCounts(StrictRecord):
    """Disjoint normal dispositions."""

    analysed: NonnegativeCount
    projects: NonnegativeCount
    vacancies: NonnegativeCount
    uncertain: NonnegativeCount
    excluded_intent: NonnegativeCount
    excluded_topic: NonnegativeCount

    @model_validator(mode='after')
    def require_reconciled_total(self) -> Self:
        """Validate disposition total."""
        total = (
            self.projects
            + self.vacancies
            + self.uncertain
            + self.excluded_intent
            + self.excluded_topic
        )
        if self.analysed != total:
            raise ValueError('unreconciled_counts')
        return self
