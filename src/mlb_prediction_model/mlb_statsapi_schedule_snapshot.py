"""MLB Stats API schedule raw snapshot collector with as-of manifest validation."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import httpx

from mlb_prediction_model.asof_snapshot_manifest import validate_asof_snapshot_manifest

SCHEDULE_ENDPOINT = "https://statsapi.mlb.com/api/v1/schedule"
SELECTED_RESPONSE_HEADERS: tuple[str, ...] = (
    "date",
    "last-modified",
    "etag",
    "cache-control",
    "expires",
    "age",
    "x-cache",
    "cf-cache-status",
)


class SupportsGet(Protocol):
    """Minimal HTTP client protocol for schedule snapshot collection."""

    def get(self, url: str, params: Mapping[str, str | int]) -> httpx.Response:
        """Return one HTTP response for the requested URL and query params."""


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _safe_date_token(schedule_date: str) -> str:
    return schedule_date.replace("/", "-").replace("\\", "-").replace(":", "-")


def _selected_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        header_name: headers[header_name]
        for header_name in SELECTED_RESPONSE_HEADERS
        if header_name in headers
    }


def build_schedule_snapshot_url_params(schedule_date: str) -> dict[str, str | int]:
    """Build the audited MLB Stats API schedule endpoint params."""
    return {"sportId": 1, "date": schedule_date, "hydrate": "probablePitcher"}


def collect_mlb_statsapi_schedule_snapshot(
    schedule_date: str,
    output_dir: Path,
    http_client: SupportsGet | None = None,
) -> dict[str, Any]:
    """Collect one raw schedule snapshot and write a validating as-of manifest."""
    output_dir.mkdir(parents=True, exist_ok=True)
    params = build_schedule_snapshot_url_params(schedule_date)
    requested_at_utc = _utc_now_iso()
    if http_client is None:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.get(SCHEDULE_ENDPOINT, params=params)
    else:
        response = http_client.get(SCHEDULE_ENDPOINT, params=params)
    response_received_at_utc = _utc_now_iso()
    response.raise_for_status()
    payload = response.json()
    payload_bytes = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    raw_payload_sha256 = hashlib.sha256(payload_bytes).hexdigest()
    date_token = _safe_date_token(schedule_date)
    raw_payload_path = output_dir / f"mlb_statsapi_schedule_{date_token}_raw.json"
    manifest_path = output_dir / f"mlb_statsapi_schedule_{date_token}_manifest.json"
    raw_payload_path.write_bytes(payload_bytes)
    manifest: dict[str, Any] = {
        "manifest_version": 1,
        "source_name": "MLB Stats API schedule endpoint",
        "source_url": SCHEDULE_ENDPOINT,
        "request_method": "GET",
        "requested_at_utc": requested_at_utc,
        "response_received_at_utc": response_received_at_utc,
        "collector_observed_asof_utc": response_received_at_utc,
        "source_issued_asof_utc": None,
        "source_issued_asof_proven": False,
        "response_http_status": response.status_code,
        "response_headers_selected": _selected_headers(response.headers),
        "raw_payload_sha256": raw_payload_sha256,
        "raw_payload_path": raw_payload_path.name,
        "score_blind_filter_required": True,
        "leakage_risk": "HIGH",
        "acceptance_status": "UNPROVEN",
        "request_params": params,
    }
    validate_asof_snapshot_manifest(manifest, raw_payload_root=output_dir)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "raw_payload_path": raw_payload_path,
    }
