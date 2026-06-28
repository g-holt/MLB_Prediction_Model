# MLB Stats API Canonical Game ID Mapping Contract

Status: draft contract, not implementation acceptance.

Purpose:

Define how MLB Stats API schedule identity fields may be mapped into this project canonical game identity record.

Evidence:

- The source capability matrix records that gamePk and gameGuid fields are proven in the historical sample and future game IDs were observed in the future probe.
- The MLB Stats API schedule score-blind filter contract allows identity fields including game_pk, game_guid, game_date_utc, official_date, season, game_type, game_number, double_header, team IDs, team names, probable pitcher IDs/names, and venue fields.
- This contract does not prove implementation, uniqueness across all seasons, cross-source joins, or issued/as-of timestamp behavior.

Canonical identity fields:

| Output field | Source field | Required? | Rule |
|---|---|---:|---|
| canonical_game_id | gamePk | yes | Primary project game key for MLB Stats API schedule-derived game identity. |
| mlb_game_pk | gamePk | yes | Preserve raw MLB Stats API numeric gamePk value. |
| mlb_game_guid | gameGuid | no | Preserve raw MLB Stats API gameGuid when present; do not use as sole primary key unless gamePk is absent and an accepted fallback rule exists. |
| official_date | officialDate | yes | MLB official date for slate grouping. |
| game_date_utc | gameDate | yes | Scheduled game datetime from schedule response. |
| season | season | yes | Season label from schedule response. |
| game_type | gameType | yes | Game type label from schedule response. |
| game_number | gameNumber | no | Preserve when present for doubleheader/schedule disambiguation. |
| double_header | doubleHeader | no | Preserve when present for doubleheader handling. |
| away_team_id | teams.away.team.id | yes | Away team identity only. |
| home_team_id | teams.home.team.id | yes | Home team identity only. |
| venue_id | venue.id | no | Venue identity only when present. |

Mapping rules:

- Build canonical game identity only from the score-blind schedule-filter output, not from raw schedule game objects.
- Use gamePk as canonical_game_id when present.
- Preserve gameGuid as secondary identity evidence when present.
- Do not infer missing gamePk values from team names, dates, or game order.
- If gamePk is missing, mark the game identity as blocked unless a future accepted fallback contract exists.
- For doubleheaders, preserve game_number and double_header; do not collapse games with the same teams and official_date.
- For postponed, suspended, neutral-site, or otherwise irregular games, preserve identity fields but do not infer final handling until those cases are separately audited.
- Do not include score, winner, league record, status, linescore, decisions, live-feed links, or final-truth fields in canonical identity records.

Acceptance gates:

- A test fixture must include at least one normal scheduled game.
- A test fixture must include either a doubleheader example or a documented missing-source reason for not testing doubleheaders yet.
- The canonical identity output must contain required identity fields when present in filtered schedule input.
- The canonical identity output must not contain denied score/final-truth fields.
- Duplicate canonical_game_id values within one generated game index must fail validation.
- Missing required identity fields must produce a blocked/degraded reason instead of inferred IDs.
- The source capability matrix must remain UNPROVEN until implementation tests pass, as-of timestamp behavior is accepted, and downstream source crosswalk behavior is separately accepted where needed.

Not accepted yet:

- implementation code
- production source status
- issued/as-of timestamp behavior
- cross-source mapping to FanGraphs, Baseball Savant, Odds API, Retrosheet, or other sources
- handling rules for postponed, suspended, or neutral-site games beyond preserving identity fields
