# MLB Stats API Schedule Snapshot Collector Live Audit

Status: evidence artifact, not source acceptance.

Purpose:

Record a read-only live run of the accepted MLB Stats API schedule snapshot collector and preserve the manifest evidence without committing the raw payload.

Audit case:

- Schedule date: 2026-07-01
- Request params: {"date": "2026-07-01", "hydrate": "probablePitcher", "sportId": 1}
- HTTP status: 200
- Raw payload SHA-256: 56bd4f8a43416765d3d011c8eeca5fe113c769e43af4df2e7061efa2a3e8ff02

Observed as-of evidence:

- requested_at_utc: 2026-07-02T03:20:50.112098Z
- response_received_at_utc: 2026-07-02T03:20:50.426194Z
- collector_observed_asof_utc: 2026-07-02T03:20:50.426194Z
- source_issued_asof_utc: None
- source_issued_asof_proven: False
- selected response headers: {"age": "15", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 03:20:52 GMT", "x-cache": "HIT, MISS"}

Conclusion:

- The accepted collector wrote a raw payload and validating manifest during this live run.
- The manifest preserves source_issued_asof_utc as null and source_issued_asof_proven as false.
- This audit does not prove durable MLB source-issued as-of timestamp behavior.
- Game schedule must remain UNPROVEN pending source-specific acceptance review.

Artifacts:

- docs/source_audits/mlb_statsapi_schedule_snapshot_live_summary_2026-07-02.json
