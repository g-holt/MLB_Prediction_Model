# MLB Stats API Schedule Score-Blind Filter Contract

Status: draft contract with initial implementation tests accepted; not production source acceptance.

Purpose:

Define the only MLB Stats API schedule fields that may survive into a pregame schedule record.

Evidence:

- Historical audit 2024-04-01 proved raw completed schedule responses can include score and winner fields.
- Future probe 2026-06-28 through 2026-07-27 proved upcoming schedule responses can expose game identity without score or winner fields in the sampled window.
- Therefore raw schedule JSON is never accepted directly as a prediction packet input.

Allowed output fields:

| Output field | Raw source path | Notes |
|---|---|---|
| game_pk | gamePk | Canonical MLB game identifier candidate. |
| game_guid | gameGuid | Secondary MLB game identifier candidate. |
| game_date_utc | gameDate | Scheduled game datetime from schedule response. |
| official_date | officialDate | MLB official date. |
| season | season | Season label. |
| game_type | gameType | Regular season/playoff/etc. |
| game_number | gameNumber | Schedule metadata only. |
| double_header | doubleHeader | Schedule metadata only. |
| day_night | dayNight | Schedule metadata only. |
| scheduled_innings | scheduledInnings | Schedule metadata only. |
| series_description | seriesDescription | Schedule metadata only. |
| away_team_id | teams.away.team.id | Team identity only. |
| away_team_name | teams.away.team.name | Team identity only. |
| home_team_id | teams.home.team.id | Team identity only. |
| home_team_name | teams.home.team.name | Team identity only. |
| away_probable_pitcher_id | teams.away.probablePitcher.id | Optional; null if absent. |
| away_probable_pitcher_name | teams.away.probablePitcher.fullName | Optional; null if absent. |
| home_probable_pitcher_id | teams.home.probablePitcher.id | Optional; null if absent. |
| home_probable_pitcher_name | teams.home.probablePitcher.fullName | Optional; null if absent. |
| venue_id | venue.id | Venue identity only. |
| venue_name | venue.name | Venue identity only. |

Denied raw fields:

- teams.away.score
- teams.home.score
- teams.away.isWinner
- teams.home.isWinner
- teams.away.leagueRecord
- teams.home.leagueRecord
- status
- status.*
- isTie
- linescore
- decisions
- winningPitcher
- losingPitcher
- savePitcher
- content
- link
- any live-feed link or live game feed payload

Filter rule:

A schedule collector may read raw schedule JSON, but the persisted pregame schedule record must be newly constructed from the allowlist above. It must not copy raw game objects or nested team objects wholesale.

Acceptance gates:

- A test fixture must include a raw historical response with score and winner fields present.
- The filtered output must contain every required allowed field when present in raw input.
- The filtered output must contain none of the denied raw fields.
- The filtered output must be valid JSON-serializable data.
- The source capability matrix must remain UNPROVEN until issued/as-of timestamp behavior is accepted and all remaining source gates pass.

Not accepted yet:

- production source status
- packet schema
- issued/as-of timestamp behavior
