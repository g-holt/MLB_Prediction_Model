# MLB Stats API Schedule Limited-Use Fallback As-Of Contract

Status: draft contract; not source acceptance.

## Purpose

Define a limited-use fallback for MLB schedule and canonical game identity when the source does not provide a durable source-issued as-of timestamp.

## Proven source behavior

- The schedule endpoint provides JSON schedule responses without a proven durable source-issued representation timestamp.
- HTTP Date, Age, Cache-Control, Vary, and cache routing headers are retrieval or cache evidence and must not populate source_issued_asof_utc.
- The accepted snapshot collector records requested_at_utc, response_received_at_utc, collector_observed_asof_utc, a payload SHA-256, source_issued_asof_utc null, source_issued_asof_proven false, score_blind_filter_required true, leakage_risk HIGH, and acceptance_status UNPROVEN.

## Limited scope

This fallback is limited to:

- forward-captured snapshots collected before a configured prediction cutoff; or
- deterministic replay from a stored snapshot that was originally captured before that cutoff.

It must not be used to convert a response retrieved after a game or after the configured cutoff into historical pregame evidence.

Eligible derived output is limited to the existing canonical game identity fields:

- canonical_game_id
- mlb_game_pk
- mlb_game_guid
- official_date
- game_date_utc
- season
- game_type
- game_number
- double_header
- away_team_id
- home_team_id
- venue_id
- blocked
- blocked_reason

All other raw or filtered schedule fields are outside this fallback contract unless separately audited and accepted.

## Required cutoff rules

A snapshot is eligible only when all of the following are true:

- configured_asof_cutoff_utc is explicitly supplied;
- collector_observed_asof_utc is at or before configured_asof_cutoff_utc;
- the target game_date_utc is strictly after configured_asof_cutoff_utc;
- source_issued_asof_utc remains null;
- source_issued_asof_proven remains false;
- response_http_status is successful;
- raw_payload_sha256 matches the stored payload bytes;
- score_blind_filter_required is true;
- the derived record is newly constructed through the accepted score-blind and canonical identity helpers.

Collector timestamps must never be relabeled as source-issued timestamps. A current or postgame retrieval must never be backdated to represent a historical pregame snapshot.

## Blocking rules

The record must block or fail when:

- the snapshot was received after the configured cutoff;
- game_date_utc is missing, invalid, or not strictly later than the cutoff;
- game_pk is missing;
- duplicate canonical game IDs are present;
- the payload hash does not validate;
- source_issued_asof_utc is populated without separate source-issued proof;
- raw payload fields are passed directly into prediction input;
- the only available historical response was retrieved after the relevant cutoff.

## Required acceptance tests

Before this fallback can receive source-specific acceptance:

1. A pre-cutoff stored snapshot must pass.
2. A snapshot received after the cutoff must fail.
3. A game at or before the cutoff must fail.
4. Missing game_pk must block.
5. Duplicate canonical game IDs must fail.
6. Payload hash mismatch must fail.
7. source_issued_asof_utc must remain null and source_issued_asof_proven must remain false.
8. Derived output must match the canonical identity allowlist exactly.
9. A postgame historical retrieval must fail as a pregame snapshot even after score-blind filtering.
10. Replaying the same stored payload and manifest must produce deterministic canonical identity output.

## Status effect

- Game schedule and canonical game IDs remain UNPROVEN while this contract is draft-only.
- Passing implementation tests and source-specific review may support a FALLBACK classification.
- A collector-observed timestamp alone must never justify PROVEN_SAFE status.
- This draft does not accept packet schema, probable pitchers, lineups, scores, or other model inputs.
