# MLB Stats API Schedule Limited-Use Fallback Acceptance Review

Status: `ACCEPTED_FALLBACK`

Review date: 2026-07-03

## Decision

- Game schedule from the MLB Stats API schedule endpoint is accepted as `FALLBACK` only for the canonical identity fields allowed by the limited-use fallback contract.
- Canonical game IDs from the same endpoint are accepted as `FALLBACK` within the same limited scope.
- The endpoint is not `PROVEN_SAFE` because no durable source-issued representation timestamp has been proven.
- Downstream crosswalks remain required before multi-source joins and do not broaden the accepted fallback scope.

## Accepted scope

The fallback is limited to forward-captured snapshots collected before an explicitly configured prediction cutoff, or deterministic replay of a stored snapshot originally captured before that cutoff.

Eligible output is restricted to the canonical identity allowlist implemented in `mlb_statsapi_schedule_fallback_asof.py`.

The acceptance excludes packet schema, probable pitchers, confirmed lineups, scores, game results, and every other unaudited model input.

## Evidence reviewed

- Historical schedule response sample for 2024-04-01.
- Future schedule probe covering 2026-06-28 through 2026-07-27.
- Read-only as-of and live collector audits.
- Targeted GET and HEAD timestamp probe showing no durable source-issued representation timestamp.
- Score-blind schedule filtering and canonical identity implementation.
- As-of snapshot manifest and collector implementation.
- Limited-use fallback contract.
- PR #20 merge commit `34372c9e1a0049331e9c7a8e5c5cbe2487cd99ee`.
- PR #21 merge commit `5f37ddf622d50bfb2dfb0141658c1086dc549b4c`.
- 34 targeted fallback tests and 52 full repository tests passing after PR #21.

## Contract acceptance gates

1. Pre-cutoff stored snapshot passes: PASS.
2. Snapshot received after cutoff fails: PASS.
3. Game at or before cutoff fails: PASS.
4. Missing game_pk blocks: PASS.
5. Duplicate canonical game IDs fail: PASS.
6. Payload hash mismatch fails: PASS.
7. Missing, non-integer, Boolean, or non-2xx response status fails: PASS.
8. Source-issued as-of remains null and unproven: PASS.
9. Derived output exactly matches the canonical identity allowlist: PASS.
10. Postgame retrieval cannot be backdated into pregame evidence: PASS.
11. Replay of the same stored payload and manifest is deterministic: PASS.

Additional negative controls cover missing, empty, invalid, and timezone-naive configured cutoff, response-received, collector-observed, and game timestamps.

## Leakage and operational restrictions

- Raw schedule fields must not flow directly into prediction inputs.
- Score-blind filtering and canonical identity reconstruction are mandatory.
- Collector and HTTP timestamps must never be relabeled as source-issued timestamps.
- A response retrieved after the relevant cutoff cannot serve as historical pregame evidence.
- The raw payload hash must validate before derived output is allowed.

## Classification effect

- Game schedule: `FALLBACK`.
- Canonical game IDs: `FALLBACK`.
- All broader uses of the endpoint remain unaccepted unless separately audited and approved.
