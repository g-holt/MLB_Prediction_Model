# MLB Stats API Schedule As-Of Timestamp Read-Only Audit

Status: evidence artifact, not source acceptance.

Purpose:

Audit whether the MLB Stats API schedule endpoint provides durable source-issued as-of or timestamp evidence usable for pregame source acceptance.

Audit cases:

- Historical completed schedule date 2024-04-01 returned HTTP 200 and 14 games.
- Future schedule date 2026-07-01 returned HTTP 200 and 14 games.

Observed timestamp-related evidence:

- Selected HTTP headers included date, cache-control, age, and x-cache.
- No selected last-modified, etag, expires, or source-generated timestamp header was observed in the audit output.
- JSON timestamp-like fields shown by the audit were copyright, dates, gameDate, officialDate, and status.startTimeTBD fields.
- Those JSON fields describe schedule/game timing or metadata; they do not prove a durable source-issued as-of timestamp for the response.

Conclusion:

- The endpoint provided response retrieval/cache header evidence during this run.
- The audit did not prove durable MLB source-issued as-of timestamp behavior.
- Game schedule and canonical game IDs must remain UNPROVEN pending an accepted as-of strategy or replacement source behavior.

Artifacts:

- docs/source_audits/mlb_statsapi_schedule_asof_readonly_summary_2026-06-28.json
