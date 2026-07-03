import hashlib
from pathlib import Path

import pytest

from mlb_prediction_model.mlb_statsapi_schedule import DuplicateCanonicalGameIdError
from mlb_prediction_model.mlb_statsapi_schedule_fallback_asof import (
    CANONICAL_GAME_IDENTITY_FIELDS,
    ScheduleFallbackAsofValidationError,
    build_schedule_fallback_canonical_identities,
    build_schedule_fallback_canonical_identity,
)


def write_raw_payload(tmp_path: Path, content: bytes = b'{"dates": []}\n') -> tuple[str, str]:
    raw_path = tmp_path / "raw_payload.json"
    raw_path.write_bytes(content)
    return raw_path.name, hashlib.sha256(content).hexdigest()


def valid_manifest(tmp_path: Path) -> dict[str, object]:
    raw_payload_path, raw_payload_sha256 = write_raw_payload(tmp_path)
    return {
        "manifest_version": 1,
        "source_name": "MLB Stats API schedule endpoint",
        "source_url": "https://statsapi.mlb.com/api/v1/schedule",
        "request_method": "GET",
        "requested_at_utc": "2026-06-30T14:59:58Z",
        "response_received_at_utc": "2026-06-30T15:00:00Z",
        "collector_observed_asof_utc": "2026-06-30T15:00:00Z",
        "source_issued_asof_utc": None,
        "source_issued_asof_proven": False,
        "response_http_status": 200,
        "response_headers_selected": {"date": "Tue, 30 Jun 2026 15:00:00 GMT"},
        "raw_payload_sha256": raw_payload_sha256,
        "raw_payload_path": raw_payload_path,
        "score_blind_filter_required": True,
        "leakage_risk": "HIGH",
        "acceptance_status": "UNPROVEN",
    }


def raw_game(
    game_pk: int | None = 777001,
    game_date_utc: str | None = "2026-07-01T18:10:00Z",
) -> dict[str, object]:
    return {
        "gamePk": game_pk,
        "gameGuid": "guid-777001",
        "gameDate": game_date_utc,
        "officialDate": "2026-07-01",
        "season": "2026",
        "gameType": "R",
        "gameNumber": 1,
        "doubleHeader": "N",
        "status": {"abstractGameState": "Final"},
        "linescore": {"currentInning": 9},
        "teams": {
            "away": {
                "score": 9,
                "isWinner": True,
                "team": {"id": 111, "name": "Away Team"},
            },
            "home": {
                "score": 0,
                "isWinner": False,
                "team": {"id": 222, "name": "Home Team"},
            },
        },
        "venue": {"id": 333, "name": "Example Park"},
    }


def test_pre_cutoff_stored_snapshot_passes_with_exact_identity_allowlist(
    tmp_path: Path,
) -> None:
    identity = build_schedule_fallback_canonical_identity(
        raw_game(),
        valid_manifest(tmp_path),
        "2026-06-30T16:00:00Z",
        raw_payload_root=tmp_path,
    )
    assert tuple(identity) == CANONICAL_GAME_IDENTITY_FIELDS
    assert identity["canonical_game_id"] == 777001
    assert "score" not in identity
    assert "status" not in identity
    assert "linescore" not in identity


def test_snapshot_received_after_cutoff_fails(tmp_path: Path) -> None:
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="response_received_at_utc must be at or before",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            valid_manifest(tmp_path),
            "2026-06-30T14:59:59Z",
            raw_payload_root=tmp_path,
        )


def test_game_at_cutoff_fails(tmp_path: Path) -> None:
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="game_date_utc must be strictly after",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(game_date_utc="2026-07-01T18:10:00Z"),
            valid_manifest(tmp_path),
            "2026-07-01T18:10:00Z",
            raw_payload_root=tmp_path,
        )


@pytest.mark.parametrize("game_date_utc", [None, "not-a-timestamp", "2026-07-01T18:10:00"])
def test_missing_invalid_or_naive_game_timestamp_fails(
    tmp_path: Path,
    game_date_utc: str | None,
) -> None:
    with pytest.raises(ScheduleFallbackAsofValidationError, match="game_date_utc"):
        build_schedule_fallback_canonical_identity(
            raw_game(game_date_utc=game_date_utc),
            valid_manifest(tmp_path),
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_missing_game_pk_blocks(tmp_path: Path) -> None:
    identity = build_schedule_fallback_canonical_identity(
        raw_game(game_pk=None),
        valid_manifest(tmp_path),
        "2026-06-30T16:00:00Z",
        raw_payload_root=tmp_path,
    )
    assert identity == {
        "canonical_game_id": None,
        "blocked": True,
        "blocked_reason": "missing_game_pk",
    }


def test_duplicate_canonical_game_ids_fail(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    with pytest.raises(DuplicateCanonicalGameIdError, match="duplicate canonical_game_id"):
        build_schedule_fallback_canonical_identities(
            [raw_game(), raw_game()],
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_payload_hash_mismatch_fails(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["raw_payload_sha256"] = "0" * 64
    with pytest.raises(ScheduleFallbackAsofValidationError, match="raw_payload_sha256 mismatch"):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


@pytest.mark.parametrize("response_http_status", [None, "200", 199, 300, True])
def test_missing_non_integer_or_non_2xx_status_fails(
    tmp_path: Path,
    response_http_status: object,
) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["response_http_status"] = response_http_status
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="response_http_status must be an integer from 200 through 299",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_source_issued_asof_must_remain_null_and_unproven(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["source_issued_asof_utc"] = "2026-06-30T14:00:00Z"
    manifest["source_issued_asof_proven"] = True
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="source_issued_asof_utc must remain null",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_score_blind_filter_requirement_must_be_true(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["score_blind_filter_required"] = False
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="score_blind_filter_required must be true",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_postgame_historical_retrieval_cannot_be_backdated(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["collector_observed_asof_utc"] = "2026-07-02T12:00:00Z"
    manifest["response_received_at_utc"] = "2026-07-02T12:00:00Z"
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="response_received_at_utc must be at or before",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(game_date_utc="2024-04-01T17:10:00Z"),
            manifest,
            "2024-04-01T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_replay_is_deterministic(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    first = build_schedule_fallback_canonical_identities(
        [raw_game()],
        manifest,
        "2026-06-30T16:00:00Z",
        raw_payload_root=tmp_path,
    )
    second = build_schedule_fallback_canonical_identities(
        [raw_game()],
        manifest,
        "2026-06-30T16:00:00Z",
        raw_payload_root=tmp_path,
    )
    assert first == second


def test_response_received_after_cutoff_fails_even_when_collector_observed_is_before(
    tmp_path: Path,
) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["response_received_at_utc"] = "2026-06-30T17:00:00Z"
    manifest["collector_observed_asof_utc"] = "2026-06-30T15:00:00Z"
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="response_received_at_utc must be at or before",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


@pytest.mark.parametrize(
    "response_received_at_utc",
    [None, "not-a-timestamp", "2026-06-30T15:00:00"],
)
def test_missing_invalid_or_naive_response_received_timestamp_fails(
    tmp_path: Path,
    response_received_at_utc: object,
) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["response_received_at_utc"] = response_received_at_utc
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="response_received_at_utc",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )


def test_collector_observed_after_cutoff_fails_even_when_response_received_is_before(
    tmp_path: Path,
) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["response_received_at_utc"] = "2026-06-30T15:00:00Z"
    manifest["collector_observed_asof_utc"] = "2026-06-30T17:00:00Z"
    with pytest.raises(
        ScheduleFallbackAsofValidationError,
        match="collector_observed_asof_utc must be at or before",
    ):
        build_schedule_fallback_canonical_identity(
            raw_game(),
            manifest,
            "2026-06-30T16:00:00Z",
            raw_payload_root=tmp_path,
        )
