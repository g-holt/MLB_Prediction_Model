"""Score-blind MLB Stats API schedule filtering and game identity helpers."""

from collections.abc import Iterable, Mapping
from typing import Any


class DuplicateCanonicalGameIdError(ValueError):
    """Raised when a generated game index contains duplicate canonical game IDs."""


def _nested_value(data: Mapping[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = data
    for part in path:
        if not isinstance(current, Mapping):
            return None
        current = current.get(part)
        if current is None:
            return None
    return current


def filter_schedule_game(raw_game: Mapping[str, Any]) -> dict[str, Any]:
    """Build a score-blind pregame schedule record from one raw schedule game object."""
    return {
        "game_pk": raw_game.get("gamePk"),
        "game_guid": raw_game.get("gameGuid"),
        "game_date_utc": raw_game.get("gameDate"),
        "official_date": raw_game.get("officialDate"),
        "season": raw_game.get("season"),
        "game_type": raw_game.get("gameType"),
        "game_number": raw_game.get("gameNumber"),
        "double_header": raw_game.get("doubleHeader"),
        "day_night": raw_game.get("dayNight"),
        "scheduled_innings": raw_game.get("scheduledInnings"),
        "series_description": raw_game.get("seriesDescription"),
        "away_team_id": _nested_value(raw_game, ("teams", "away", "team", "id")),
        "away_team_name": _nested_value(raw_game, ("teams", "away", "team", "name")),
        "home_team_id": _nested_value(raw_game, ("teams", "home", "team", "id")),
        "home_team_name": _nested_value(raw_game, ("teams", "home", "team", "name")),
        "away_probable_pitcher_id": _nested_value(
            raw_game, ("teams", "away", "probablePitcher", "id")
        ),
        "away_probable_pitcher_name": _nested_value(
            raw_game, ("teams", "away", "probablePitcher", "fullName")
        ),
        "home_probable_pitcher_id": _nested_value(
            raw_game, ("teams", "home", "probablePitcher", "id")
        ),
        "home_probable_pitcher_name": _nested_value(
            raw_game, ("teams", "home", "probablePitcher", "fullName")
        ),
        "venue_id": _nested_value(raw_game, ("venue", "id")),
        "venue_name": _nested_value(raw_game, ("venue", "name")),
    }


def build_canonical_game_identity(filtered_game: Mapping[str, Any]) -> dict[str, Any]:
    """Build canonical game identity from a score-blind filtered schedule record."""
    game_pk = filtered_game.get("game_pk")
    if game_pk is None:
        return {
            "canonical_game_id": None,
            "blocked": True,
            "blocked_reason": "missing_game_pk",
        }
    return {
        "canonical_game_id": game_pk,
        "mlb_game_pk": game_pk,
        "mlb_game_guid": filtered_game.get("game_guid"),
        "official_date": filtered_game.get("official_date"),
        "game_date_utc": filtered_game.get("game_date_utc"),
        "season": filtered_game.get("season"),
        "game_type": filtered_game.get("game_type"),
        "game_number": filtered_game.get("game_number"),
        "double_header": filtered_game.get("double_header"),
        "away_team_id": filtered_game.get("away_team_id"),
        "home_team_id": filtered_game.get("home_team_id"),
        "venue_id": filtered_game.get("venue_id"),
        "blocked": False,
        "blocked_reason": None,
    }


def validate_unique_canonical_game_ids(records: Iterable[Mapping[str, Any]]) -> None:
    """Validate that non-blocked canonical game records have unique IDs."""
    seen: set[Any] = set()
    for record in records:
        if record.get("blocked"):
            continue
        canonical_game_id = record.get("canonical_game_id")
        if canonical_game_id in seen:
            raise DuplicateCanonicalGameIdError(f"duplicate canonical_game_id: {canonical_game_id}")
        seen.add(canonical_game_id)
