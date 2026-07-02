# Source Capability Matrix

This document tracks candidate data sources and what must be proven before each source can be used.

No source is accepted until the required proof artifacts exist.

## Status values

Use one of these values for each row:

- `UNPROVEN`
- `PROVEN_SAFE`
- `PROVEN_UNSAFE`
- `FALLBACK`
- `FINAL_TRUTH_ONLY`
- `EXCLUDED`

## Leakage risk values

Use one of these values for each row:

- `LOW`
- `MEDIUM`
- `HIGH`
- `UNKNOWN`

## Source capability table

| Data category | Candidate source | Historical available? | As-of / timestamped? | Can be derived only from prior games? | Requires login/API key? | Raw format | Leakage risk | Required proof artifact | Status |
|---|---|---:|---:|---:|---:|---|---|---|---|
| Game schedule | MLB Stats API schedule endpoint | Historical response sample proven; future schedule probe proven | HTTP retrieval/cache headers observed in read-only as-of audit, live collector audit, and targeted GET/HEAD variant probe; no ETag, Last-Modified, Expires, or durable source-issued representation timestamp observed | N/A for schedule identity; historical raw responses require score-blind filtering | No login/API key observed in audits | JSON | HIGH | Merged audits: historical 2024-04-01, future probe 2026-06-28 to 2026-07-27, as-of read-only audit 2026-06-28, score-blind filter contract, initial schedule filter implementation tests, initial as-of manifest implementation tests, schedule snapshot collector tests, live schedule snapshot collector audit 2026-07-02, and targeted source-issued timestamp probe 2026-07-02, and draft limited-use fallback as-of contract; implementation tests and negative controls are still required before source-specific acceptance review | UNPROVEN |
| Canonical game IDs | MLB Stats API schedule endpoint | gamePk/gameGuid fields proven in historical sample; future game IDs observed in probe | Future-date game identity partially proven; HTTP retrieval/cache headers observed in read-only as-of audit; durable source-issued as-of timestamp not proven | N/A for schedule identity; historical raw responses require score-blind filtering | No login/API key observed in audits | JSON | HIGH | Merged audits: historical 2024-04-01, future probe 2026-06-28 to 2026-07-27, and as-of read-only audit 2026-06-28; ID mapping contract documented; initial implementation tests accepted; as-of snapshot manifest contract drafted; initial manifest implementation tests accepted; draft limited-use fallback as-of contract added; implementation tests, negative controls, and downstream crosswalks still required | UNPROVEN |
| Odds snapshots | The Odds API | Not proven for account | Not proven for account | No | Likely yes, not proven locally | Not proven | UNKNOWN | API response sample, endpoint proof, market list, timestamp fields | UNPROVEN |
| Starting pitchers | MLB data / lineup source / FanGraphs / other | Not proven | Not proven | No | Not proven | Not proven | UNKNOWN | Historical/current sample with timestamp or as-of rule | UNPROVEN |
| Confirmed lineups | MLB data / lineup source / other | Not proven | Not proven | No | Not proven | Not proven | UNKNOWN | Historical/current lineup sample with timestamp or as-of rule | UNPROVEN |
| Team batting stats | FanGraphs | Not proven | Not proven | Maybe, not proven | User has membership, exact access not proven | Not proven | UNKNOWN | Export sample, headers, date filter proof, as-of behavior proof | UNPROVEN |
| Team batting stats | Baseball Savant / Statcast-derived | Not proven | Not proven | Maybe, not proven | Not proven | Not proven | UNKNOWN | Export sample, headers, query proof, derivation proof | UNPROVEN |
| Player batting stats | FanGraphs | Not proven | Not proven | Maybe, not proven | User has membership, exact access not proven | Not proven | UNKNOWN | Export sample, headers, date filter proof, as-of behavior proof | UNPROVEN |
| Player batting stats | Baseball Savant / Statcast-derived | Not proven | Not proven | Maybe, not proven | Not proven | Not proven | UNKNOWN | Export sample, headers, query proof, derivation proof | UNPROVEN |
| Starting pitcher stats | FanGraphs | Not proven | Not proven | Maybe, not proven | User has membership, exact access not proven | Not proven | UNKNOWN | Export sample, headers, date filter proof, as-of behavior proof | UNPROVEN |
| Starting pitcher stats | Baseball Savant / Statcast-derived | Not proven | Not proven | Maybe, not proven | Not proven | Not proven | UNKNOWN | Export sample, headers, query proof, derivation proof | UNPROVEN |
| Bullpen usage | Prior game logs / MLB data / Retrosheet / other | Not proven | Not proven | Likely possible, not proven | Not proven | Not proven | UNKNOWN | Prior-game-only derivation sample and pitcher usage fields | UNPROVEN |
| Team defense | FanGraphs / Savant / derived source | Not proven | Not proven | Maybe, not proven | Not proven | Not proven | UNKNOWN | Export sample, headers, date filter proof | UNPROVEN |
| Park factors | FanGraphs / Statcast / other | Not proven | Not proven | Not proven | Not proven | Not proven | UNKNOWN | Source sample, date/version behavior, field definitions | UNPROVEN |
| Weather forecast | Weather provider to be selected | Not proven | Not proven | No | Not proven | Not proven | UNKNOWN | Historical forecast sample with issued timestamp | UNPROVEN |
| Weather observed | Weather provider to be selected | Not proven | Not proven | No | Not proven | Not proven | MEDIUM | Historical observed sample and clear label as observed, not forecast | UNPROVEN |
| Injuries | Injury source to be selected | Not proven | Not proven | No | Not proven | Not proven | UNKNOWN | Historical injury status sample with timestamp/as-of rule | UNPROVEN |
| Roster status | MLB data / roster source / other | Not proven | Not proven | No | Not proven | Not proven | UNKNOWN | Historical roster sample with transaction/status timing | UNPROVEN |
| Final scores | MLB data / Retrosheet / Baseball Savant / other | Not proven | Not applicable for prediction | No | Not proven | Not proven | HIGH if used before grading | Final score sample isolated to grading phase only | UNPROVEN |
| Postgame grading truth | MLB data / Retrosheet / Baseball Savant / other | Not proven | Not applicable for prediction | No | Not proven | Not proven | HIGH if used before grading | Final truth sample and proof it is isolated from packet builder | UNPROVEN |

## Required proof artifact checklist

For each source, collect and store proof of:

- source name;
- access method;
- endpoint or export path;
- authentication requirement;
- rate limit or plan restriction if known;
- raw response or raw export sample;
- file headers or JSON keys;
- timestamp behavior;
- timezone behavior;
- historical availability;
- whether data is true as-of or reconstructed;
- whether final scores or postgame labels appear;
- allowed use category:
  - pregame input;
  - derived pregame feature;
  - fallback;
  - final-truth only;
  - excluded.

## Source decision rule

A source can only become canonical for a category after it has:

1. a raw proof artifact;
2. documented schema or headers;
3. leakage review;
4. reproducibility review;
5. acceptance in the project list.

## Initial audit priority

Start with these categories:

1. Game schedule and canonical game IDs.
2. Odds snapshots.
3. Starting pitchers.
4. Team/player batting stats.
5. Starting pitcher stats.
6. Bullpen usage.
7. Lineups.
8. Weather.
9. Park factors.
10. Final scores for grading only.

## Current status

No source is accepted yet.

All rows are currently `UNPROVEN`.
