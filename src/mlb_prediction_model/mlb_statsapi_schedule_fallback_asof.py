"""Limited-use fallback as-of validation for MLB schedule canonical identities."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mlb_prediction_model.asof_snapshot_manifest import (
    AsofSnapshotManifestValidationError,
    validate_asof_snapshot_manifest,
)
from mlb_prediction_model.mlb_statsapi_schedule import (
    build_canonical_game_identity,
    filter_schedule_game,
    validate_unique_canonical_game_ids,
)

CANONICAL_GAME_IDENTITY_FIELDS: tuple[str, ...] = (
    "canonical_game_id",
    "mlb_game_pk",
    "mlb_game_guid",
    "official_date",
    "game_date_utc",
    "season",
    "game_type",
    "game_number",
    "double_header",
    "away_team_id",
    "home_team_id",
    "venue_id",
    "blocked",
    "blocked_reason",
)


class ScheduleFallbackAsofValidationError(ValueError):
    """Raised when a schedule snapshot is ineligible for limited-use fallback."""


def _parse_aware_datetime(value: object, field_name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ScheduleFallbackAsofValidationError(
            f"{field_name} must be a non-empty ISO 8601 timestamp string"
        )
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ScheduleFallbackAsofValidationError(
            f"{field_name} must be a valid ISO 8601 timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ScheduleFallbackAsofValidationError(f"{field_name} must include a UTC offset")
    return parsed.astimezone(UTC)


def _validate_fallback_manifest(
    manifest: Mapping[str, Any],
    configured_asof_cutoff_utc: str,
    raw_payload_root: Path | None,
) -> datetime:
    try:
        validate_asof_snapshot_manifest(manifest, raw_payload_root=raw_payload_root)
    except AsofSnapshotManifestValidationError as exc:
        raise ScheduleFallbackAsofValidationError(str(exc)) from exc

    response_http_status = manifest.get("response_http_status")
    if (
        not isinstance(response_http_status, int)
        or isinstance(response_http_status, bool)
        or not 200 <= response_http_status <= 299
    ):
        raise ScheduleFallbackAsofValidationError(
            "response_http_status must be an integer from 200 through 299 inclusive"
        )
    if manifest.get("source_issued_asof_utc") is not None:
        raise ScheduleFallbackAsofValidationError(
            "source_issued_asof_utc must remain null for limited-use fallback"
        )
    if manifest.get("source_issued_asof_proven") is not False:
        raise ScheduleFallbackAsofValidationError(
            "source_issued_asof_proven must remain false for limited-use fallback"
        )
    if manifest.get("score_blind_filter_required") is not True:
        raise ScheduleFallbackAsofValidationError(
            "score_blind_filter_required must be true for limited-use fallback"
        )

    cutoff = _parse_aware_datetime(configured_asof_cutoff_utc, "configured_asof_cutoff_utc")
    response_received = _parse_aware_datetime(
        manifest.get("response_received_at_utc"),
        "response_received_at_utc",
    )
    collector_observed = _parse_aware_datetime(
        manifest.get("collector_observed_asof_utc"),
        "collector_observed_asof_utc",
    )
    if response_received > cutoff:
        raise ScheduleFallbackAsofValidationError(
            "response_received_at_utc must be at or before configured_asof_cutoff_utc"
        )
    if collector_observed > cutoff:
        raise ScheduleFallbackAsofValidationError(
            "collector_observed_asof_utc must be at or before configured_asof_cutoff_utc"
        )
    return cutoff


def _build_identity_for_cutoff(
    raw_game: Mapping[str, Any],
    cutoff: datetime,
) -> dict[str, Any]:
    filtered_game = filter_schedule_game(raw_game)
    game_date = _parse_aware_datetime(filtered_game.get("game_date_utc"), "game_date_utc")
    if game_date <= cutoff:
        raise ScheduleFallbackAsofValidationError(
            "game_date_utc must be strictly after configured_asof_cutoff_utc"
        )

    identity = build_canonical_game_identity(filtered_game)
    if not identity.get("blocked") and tuple(identity) != CANONICAL_GAME_IDENTITY_FIELDS:
        raise ScheduleFallbackAsofValidationError(
            "derived canonical identity fields do not match the accepted allowlist"
        )
    return identity


def build_schedule_fallback_canonical_identity(
    raw_game: Mapping[str, Any],
    manifest: Mapping[str, Any],
    configured_asof_cutoff_utc: str,
    raw_payload_root: Path | None = None,
) -> dict[str, Any]:
    """Build one eligible limited-use canonical identity or raise."""
    cutoff = _validate_fallback_manifest(
        manifest,
        configured_asof_cutoff_utc,
        raw_payload_root,
    )
    return _build_identity_for_cutoff(raw_game, cutoff)


def build_schedule_fallback_canonical_identities(
    raw_games: Iterable[Mapping[str, Any]],
    manifest: Mapping[str, Any],
    configured_asof_cutoff_utc: str,
    raw_payload_root: Path | None = None,
) -> list[dict[str, Any]]:
    """Build deterministic eligible canonical identities and reject duplicates."""
    cutoff = _validate_fallback_manifest(
        manifest,
        configured_asof_cutoff_utc,
        raw_payload_root,
    )
    identities = [_build_identity_for_cutoff(raw_game, cutoff) for raw_game in raw_games]
    validate_unique_canonical_game_ids(identities)
    return identities
