# MLB Stats API Schedule Source Audit

Status: read-only source capability audit.

This audit does not accept MLB Stats API as a production source yet.

Request:
https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-04-01&hydrate=probablePitcher

Output files:
C:\Users\gholt\Desktop\mlb_pred_source_audit_schedule_20260627\mlb_statsapi_schedule_raw_2024-04-01.json
C:\Users\gholt\Desktop\mlb_pred_source_audit_schedule_20260627\mlb_statsapi_schedule_summary_2024-04-01.json
C:\Users\gholt\Desktop\mlb_pred_source_audit_schedule_20260627\mlb_statsapi_schedule_audit_report_2024-04-01.md

Observed:
date_count=1
game_count=14
score_fields_present_any=True
probable_pitcher_present_any=True

Preliminary leakage note:
If score_fields_present_any=True, the raw historical schedule response contains score data and needs a score-blind filtering layer before it can feed prediction packets.
