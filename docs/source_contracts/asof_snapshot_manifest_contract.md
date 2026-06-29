# As-Of Snapshot Manifest Contract

Status: draft contract, not implementation acceptance.

Purpose:

Define the minimum manifest required for raw source snapshots when a source does not provide a durable source-issued as-of timestamp.

Background:

- The MLB Stats API schedule as-of audit observed HTTP retrieval/cache headers.
- The audit did not prove durable MLB source-issued as-of timestamp behavior.
- A collector-captured retrieval timestamp is not the same as a source-issued timestamp.
- A source row must not be marked proven-safe solely because a collector timestamp exists.

Required manifest fields:

- manifest_version
- source_name
- source_url
- request_method
- requested_at_utc
- response_received_at_utc
- collector_observed_asof_utc
- source_issued_asof_utc
- source_issued_asof_proven
- response_http_status
- response_headers_selected
- raw_payload_sha256
- raw_payload_path
- score_blind_filter_required
- leakage_risk
- acceptance_status

Rules:

- collector_observed_asof_utc must be captured by the collector at runtime.
- source_issued_asof_utc must be null unless the source itself provides a proven durable as-of timestamp.
- source_issued_asof_proven must be false unless a source-issued timestamp contract and audit prove it.
- response_headers_selected may preserve retrieval/cache headers, but those headers must not be relabeled as source-issued timestamps without proof.
- raw payloads that may contain final-truth fields must never be used directly as prediction packet input.
- score-blind derived records must be newly constructed from allowlisted fields.
- acceptance_status must remain UNPROVEN until all source-specific gates pass.

Acceptance gates:

- A fixture manifest must include every required field.
- Missing required manifest fields must fail validation.
- source_issued_asof_proven true must fail validation when source_issued_asof_utc is null.
- source_issued_asof_utc must not be populated from collector timestamps or generic HTTP cache headers.
- raw_payload_sha256 must match the referenced raw payload bytes.
- The source capability matrix must remain UNPROVEN until implementation tests and source-specific acceptance gates pass.

Not accepted yet:

- implementation code
- production source status
- source-issued as-of timestamp behavior for MLB Stats API schedule
- packet schema
