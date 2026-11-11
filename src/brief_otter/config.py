"""Explicit configuration validation."""

import os
import re
import stat
import tomllib
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Annotated, Self

from pydantic import BeforeValidator, Field, ValidationError, field_validator
from pydantic import model_validator as validate_model

from brief_otter.domain import StrictRecord

PROJECT_NAME = 'brief-otter'
AI_ENDPOINT = 'https://api.z.ai/api/paas/v4/chat/completions'
AI_MODEL = 'glm-5.3-flash'
MAX_HISTORY_PAGE = 100
PositiveCount = Annotated[int, Field(strict=True, gt=0)]
PositiveSeconds = Annotated[float, Field(gt=0, allow_inf_nan=False)]


class ConfigurationError(ValueError):
    """Sanitized configuration failure."""


def decimal_budget(value: object) -> Decimal:
    """Parse explicit budget."""
    if not isinstance(value, str):
        raise ValueError('decimal_string_required')
    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise ValueError('invalid_budget') from None
    if not amount.is_finite() or amount <= 0:
        raise ValueError('invalid_budget')
    return amount


def explicit_path(value: object) -> Path:
    """Parse explicit path."""
    if not isinstance(value, str | Path):
        raise ValueError('path_required')
    result = Path(value)
    if not result.is_absolute():
        raise ValueError('absolute_path_required')
    return result


PrivatePath = Annotated[Path, BeforeValidator(explicit_path)]
Budget = Annotated[Decimal, BeforeValidator(decimal_budget)]


class SourceSettings(StrictRecord):
    """Single source settings."""

    username: str = Field(repr=False)
    expected_id: int | None = Field(default=None, repr=False)

    @field_validator('username')
    @classmethod
    def require_one_username(cls, value: str) -> str:
        """Normalize source username."""
        value = value.removeprefix('@')
        if re.fullmatch(r'[A-Za-z0-9_]{1,32}', value) is None:
            raise ValueError('invalid_source_username')
        return value.lower()

    @field_validator('expected_id')
    @classmethod
    def reject_zero_identity(cls, value: int | None) -> int | None:
        """Reject absent identity."""
        if value == 0:
            raise ValueError('invalid_source_identity')
        return value


class ReportSettings(StrictRecord):
    """Private report destination."""

    path: PrivatePath = Field(repr=False)
    excerpt_characters: PositiveCount = 400


class CollectionSettings(StrictRecord):
    """Bounded traversal settings."""

    max_messages: PositiveCount = 5000
    page_size: PositiveCount = Field(default=100, le=MAX_HISTORY_PAGE)
    max_pages: PositiveCount = 50
    page_interval_seconds: PositiveSeconds = 3.0
    max_seconds: PositiveSeconds = 180.0
    request_timeout_seconds: PositiveSeconds = 15.0

    @validate_model(mode='after')
    def require_bounded_timeout(self) -> Self:
        """Validate nested deadline."""
        if self.request_timeout_seconds > self.max_seconds:
            raise ValueError('invalid_collection_deadline')
        return self


class AISettings(StrictRecord):
    """Admitted route settings."""

    endpoint: str
    model: str
    max_calls: PositiveCount
    deadline_seconds: PositiveSeconds
    budget_usd: Budget
    state_path: PrivatePath = Field(repr=False)

    @field_validator('endpoint')
    @classmethod
    def require_selected_endpoint(cls, value: str) -> str:
        """Reject alternate endpoint."""
        if value != AI_ENDPOINT:
            raise ValueError('unapproved_endpoint')
        return value

    @field_validator('model')
    @classmethod
    def require_selected_model(cls, value: str) -> str:
        """Reject alternate model."""
        if value != AI_MODEL:
            raise ValueError('unapproved_model')
        return value


class Settings(StrictRecord):
    """Explicit application settings."""

    source: SourceSettings
    report: ReportSettings
    ai: AISettings
    collection: CollectionSettings = Field(default_factory=CollectionSettings)


def require_owner_only(path: Path) -> None:
    """Validate private ownership."""
    info = path.stat()
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
        raise ConfigurationError('unsafe_permissions')


def private_destination(path: Path, project_root: Path) -> Path:
    """Validate private destination."""
    try:
        if not path.is_absolute() or path.is_symlink():
            raise ConfigurationError('unsafe_path')
        parent = path.parent.resolve(strict=True)
        if not parent.is_dir():
            raise ConfigurationError('unsafe_path')
        resolved = parent / path.name
        if resolved.is_relative_to(project_root.resolve(strict=True)):
            raise ConfigurationError('path_inside_checkout')
        require_owner_only(parent)
        if path.exists():
            if not path.is_file():
                raise ConfigurationError('unsafe_path')
            require_owner_only(path)
        return resolved
    except OSError, RuntimeError:
        raise ConfigurationError('unsafe_path') from None


def validate_settings(payload: object, project_root: Path) -> Settings:
    """Validate supplied settings."""
    try:
        settings = Settings.model_validate(payload)
    except ValidationError, TypeError, ValueError:
        raise ConfigurationError('invalid_configuration') from None
    report = private_destination(settings.report.path, project_root)
    state = private_destination(settings.ai.state_path, project_root)
    if report.suffix.lower() != '.html':
        raise ConfigurationError('invalid_report_extension')
    if report == state:
        raise ConfigurationError('conflicting_destinations')
    return settings


def load_settings(path: Path, project_root: Path) -> Settings:
    """Load explicit settings."""
    location = private_destination(path, project_root)
    try:
        with location.open('rb') as stream:
            payload = tomllib.load(stream)
    except OSError, ValueError:
        raise ConfigurationError('invalid_configuration_file') from None
    settings = validate_settings(payload, project_root)
    outputs = (settings.report.path, settings.ai.state_path)
    if any(location == destination.resolve() for destination in outputs):
        raise ConfigurationError('conflicting_configuration_path')
    return settings


def find_project_root(start: Path) -> Path:
    """Locate checkout boundary."""
    try:
        location = start.resolve(strict=True)
        for candidate in (location, *location.parents):
            manifest = candidate / 'pyproject.toml'
            if not manifest.is_file():
                continue
            with manifest.open('rb') as stream:
                metadata = tomllib.load(stream)
            project = metadata.get('project')
            if (
                isinstance(project, dict)
                and project.get('name') == PROJECT_NAME
            ):
                return candidate
    except OSError, ValueError, RuntimeError:
        raise ConfigurationError('project_boundary_unavailable') from None
    raise ConfigurationError('project_boundary_unavailable')
