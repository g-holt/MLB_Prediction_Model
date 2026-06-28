import json

import pytest

from mlb_prediction_model.mlb_statsapi_schedule import (
    DuplicateCanonicalGameIdError,
    build_canonical_game_identity,
    filter_schedule_game,
    validate_unique_canonical_game_ids,
)


def raw_completed_schedule_game() -> dict[str, object]:
    return {
        "gamePk": 746123,
        "gameGuid": "abc-123",
        "gameDate": "2024-04-01T17:10:00Z",
        "officialDate": "2024-04-01",
        "season": "2024",
        "gameType": "R",
        "gameNumber": 1,
        "doubleHeader": "N",
        "dayNight": "day",
        "scheduledInnings": 9,
        "seriesDescription": "Regular Season",
        "status": {"abstractGameState": "Final", "detailedState": "Final"},
        "link": "/api/v1.1/game/746123/feed/live",
        "linescore": {"currentInning": 9},
        "decisions": {"winner": {"id": 1}},
        "teams": {
            "away": {
                "score": 9,
                "isWinner": True,
                "leagueRecord": {"wins": 1, "losses": 0},
                "team": {"id": 111, "name": "Away Team"},
                "probablePitcher": {"id": 444, "fullName": "Away Pitcher"},
            },
            "home": {
                "score": 0,
                "isWinner": False,
                "leagueRecord": {"wins": 0, "losses": 1},
                "team": {"id": 222, "name": "Home Team"},
                "probablePitcher": {"id": 555, "fullName": "Home Pitcher"},
            },
        },
        "venue": {"id": 333, "name": "Example Park"},
    }


def test_filter_schedule_game_keeps_only_allowed_score_blind_fields() -> None:
    filtered = filter_schedule_game(raw_completed_schedule_game())
    assert filtered == {
        "game_pk": 746123,
        "game_guid": "abc-123",
        "game_date_utc": "2024-04-01T17:10:00Z",
        "official_date": "2024-04-01",
        "season": "2024",
        "game_type": "R",
        "game_number": 1,
        "double_header": "N",
        "day_night": "day",
        "scheduled_innings": 9,
        "series_description": "Regular Season",
        "away_team_id": 111,
        "away_team_name": "Away Team",
        "home_team_id": 222,
        "home_team_name": "Home Team",
        "away_probable_pitcher_id": 444,
        "away_probable_pitcher_name": "Away Pitcher",
        "home_probable_pitcher_id": 555,
        "home_probable_pitcher_name": "Home Pitcher",
        "venue_id": 333,
        "venue_name": "Example Park",
    }
    encoded = json.dumps(filtered)
    for denied_text in (
        "score",
        "isWinner",
        "leagueRecord",
        "status",
        "linescore",
        "decisions",
        "link",
    ):
        assert denied_text not in encoded


def test_build_canonical_game_identity_uses_filtered_score_blind_record() -> None:
    filtered = filter_schedule_game(raw_completed_schedule_game())
    identity = build_canonical_game_identity(filtered)
    assert identity == {
        "canonical_game_id": 746123,
        "mlb_game_pk": 746123,
        "mlb_game_guid": "abc-123",
        "official_date": "2024-04-01",
        "game_date_utc": "2024-04-01T17:10:00Z",
        "season": "2024",
        "game_type": "R",
        "game_number": 1,
        "double_header": "N",
        "away_team_id": 111,
        "home_team_id": 222,
        "venue_id": 333,
        "blocked": False,
        "blocked_reason": None,
    }
    encoded = json.dumps(identity)
    for denied_text in (
        "score",
        "isWinner",
        "leagueRecord",
        "status",
        "linescore",
        "decisions",
        "link",
    ):
        assert denied_text not in encoded


def test_missing_game_pk_blocks_identity_instead_of_inferring() -> None:
    filtered = filter_schedule_game(raw_completed_schedule_game())
    filtered["game_pk"] = None
    assert build_canonical_game_identity(filtered) == {
        "canonical_game_id": None,
        "blocked": True,
        "blocked_reason": "missing_game_pk",
    }


def test_duplicate_canonical_game_ids_fail_validation() -> None:
    filtered = filter_schedule_game(raw_completed_schedule_game())
    identity = build_canonical_game_identity(filtered)
    with pytest.raises(DuplicateCanonicalGameIdError, match="duplicate canonical_game_id: 746123"):
        validate_unique_canonical_game_ids([identity, identity])
