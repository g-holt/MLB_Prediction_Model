# MLB Stats API Schedule Future-Date Probe

Status: read-only source capability audit.

This probe does not accept MLB Stats API as a production source yet.

Probe window: 2026-06-28 through 2026-07-27

Files copied into repo:
- docs/source_audits/mlb_statsapi_schedule_future_probe_2026-06-28_to_2026-07-27.csv
- docs/source_audits/mlb_statsapi_schedule_future_probe_2026-06-28_to_2026-07-27.json
- docs/source_audits/mlb_statsapi_schedule_future_probe_report_2026-06-28_to_2026-07-27.md

Observed:
- dates_probed=30
- dates_with_games=28
- dates_with_score_fields=0
- dates_with_winner_fields=0
- dates_with_probable_pitchers=5
- first_usable_future_date=2026-06-28
- first_usable_future_game_count=15
- first_usable_future_probable_pitcher_present_any=True

Preliminary finding:
The future-date probe found upcoming schedule rows with game identity and no score/winner fields in the sampled responses.

Important limitation:
The historical audit already proved completed historical schedule responses can include score and winner fields. Therefore, MLB Stats API schedule responses still require a score-blind filtering layer before they can feed prediction packets.

Not accepted yet:
- production source status
- source schema contract
- score-blind filtering contract
- collector implementation
- packet schema
