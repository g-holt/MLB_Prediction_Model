MLB Stats API schedule source-issued timestamp probe
Status: read-only probe, not source acceptance

Case: historical_completed
- GET status: 200
- GET selected headers: {"age": "0", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "MISS, MISS"}
- HEAD status: 200
- HEAD selected headers: {"age": "0", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "MISS, HIT"}
- Conditional request attempted: False
- Timestamp-like JSON fields first twenty: [{"path": "dates", "value_type": "list"}, {"path": "dates[0].date", "value": "2024-04-01"}, {"path": "dates[0].games[0].gameDate", "value": "2024-04-01T18:10:00Z"}, {"path": "dates[0].games[0].officialDate", "value": "2024-04-01"}, {"path": "dates[0].games[0].status.startTimeTBD", "value": false}, {"path": "dates[0].games[1].gameDate", "value": "2024-04-01T18:20:00Z"}, {"path": "dates[0].games[1].officialDate", "value": "2024-04-01"}, {"path": "dates[0].games[1].status.startTimeTBD", "value": false}]
- Durable source-issued response timestamp candidate from selected headers: NOT OBSERVED

Case: future_schedule
- GET status: 200
- GET selected headers: {"age": "24", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "HIT, MISS"}
- HEAD status: 200
- HEAD selected headers: {"age": "24", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "HIT, MISS"}
- Conditional request attempted: False
- Timestamp-like JSON fields first twenty: [{"path": "dates", "value_type": "list"}, {"path": "dates[0].date", "value": "2026-07-01"}, {"path": "dates[0].games[0].gameDate", "value": "2026-07-01T16:35:00Z"}, {"path": "dates[0].games[0].officialDate", "value": "2026-07-01"}, {"path": "dates[0].games[0].status.startTimeTBD", "value": false}, {"path": "dates[0].games[1].gameDate", "value": "2026-07-01T17:10:00Z"}, {"path": "dates[0].games[1].officialDate", "value": "2026-07-01"}, {"path": "dates[0].games[1].status.startTimeTBD", "value": false}]
- Durable source-issued response timestamp candidate from selected headers: NOT OBSERVED

Case: future_schedule_no_hydrate
- GET status: 200
- GET selected headers: {"age": "20", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "HIT, HIT"}
- HEAD status: 200
- HEAD selected headers: {"age": "20", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "HIT, HIT"}
- Conditional request attempted: False
- Timestamp-like JSON fields first twenty: [{"path": "dates", "value_type": "list"}, {"path": "dates[0].date", "value": "2026-07-01"}, {"path": "dates[0].games[0].gameDate", "value": "2026-07-01T16:35:00Z"}, {"path": "dates[0].games[0].officialDate", "value": "2026-07-01"}, {"path": "dates[0].games[0].status.startTimeTBD", "value": false}, {"path": "dates[0].games[1].gameDate", "value": "2026-07-01T17:10:00Z"}, {"path": "dates[0].games[1].officialDate", "value": "2026-07-01"}, {"path": "dates[0].games[1].status.startTimeTBD", "value": false}]
- Durable source-issued response timestamp candidate from selected headers: NOT OBSERVED

Case: future_schedule_range
- GET status: 200
- GET selected headers: {"age": "0", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "MISS, MISS"}
- HEAD status: 200
- HEAD selected headers: {"age": "0", "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400", "date": "Thu, 02 Jul 2026 19:36:19 GMT", "vary": "accept-encoding, Accept-Encoding", "x-cache": "MISS, HIT"}
- Conditional request attempted: False
- Timestamp-like JSON fields first twenty: [{"path": "dates", "value_type": "list"}, {"path": "dates[0].date", "value": "2026-07-01"}, {"path": "dates[0].games[0].gameDate", "value": "2026-07-01T16:35:00Z"}, {"path": "dates[0].games[0].officialDate", "value": "2026-07-01"}, {"path": "dates[0].games[0].status.startTimeTBD", "value": false}, {"path": "dates[0].games[1].gameDate", "value": "2026-07-01T17:10:00Z"}, {"path": "dates[0].games[1].officialDate", "value": "2026-07-01"}, {"path": "dates[0].games[1].status.startTimeTBD", "value": false}]
- Durable source-issued response timestamp candidate from selected headers: NOT OBSERVED

Conclusion:
- At least one probed case did not expose durable selected source-issued timestamp headers.
- JSON timestamp-like fields must still be reviewed as schedule/game timing fields versus response as-of fields.
- Do not change source status from this probe alone.

Method interpretation:

- RFC 9110 section 6.6.1 defines Date as message-origination time, not a representation modification or durable data-version timestamp.
- RFC 9111 sections 4.2.3 and 5.1 define Age as estimated cache age since origin generation or validation.
- Date, Age, cache-control, vary, and x-cache remain retrieval/cache evidence and must not populate source_issued_asof_utc.
- No ETag, Last-Modified, or Expires header was observed in any of the four GET/HEAD probe variants.

Acceptance effect:

- This evidence does not promote Game schedule from UNPROVEN.
- A separate limited-use fallback as-of strategy must be drafted and accepted before source-specific acceptance review.
