import json
from pathlib import Path

import httpx

from mlb_prediction_model.asof_snapshot_manifest import validate_asof_snapshot_manifest
from mlb_prediction_model.mlb_statsapi_schedule_snapshot import (
    SCHEDULE_ENDPOINT,
    build_schedule_snapshot_url_params,
    collect_mlb_statsapi_schedule_snapshot,
)


class FakeClient:
    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        self.calls: list[tuple[str, dict[str, str | int]]] = []

    def get(self, url: str, params: dict[str, str | int]) -> httpx.Response:
        self.calls.append((url, params))
        return self.response


def response_with_payload(payload: dict[str, object]) -> httpx.Response:
    return httpx.Response(
        200,
        json=payload,
        headers={
            "date": "Sun, 28 Jun 2026 22:15:45 GMT",
            "cache-control": "max-age=20, public",
            "age": "22",
            "x-cache": "HIT, MISS",
            "ignored-header": "not persisted",
        },
        request=httpx.Request("GET", SCHEDULE_ENDPOINT),
    )


def test_build_schedule_snapshot_url_params_matches_audited_endpoint() -> None:
    assert build_schedule_snapshot_url_params("2026-07-01") == {
        "sportId": 1,
        "date": "2026-07-01",
        "hydrate": "probablePitcher",
    }


def test_collect_schedule_snapshot_writes_raw_payload_and_valid_manifest(tmp_path: Path) -> None:
    payload = {"dates": [{"date": "2026-07-01", "games": []}]}
    client = FakeClient(response_with_payload(payload))
    result = collect_mlb_statsapi_schedule_snapshot("2026-07-01", tmp_path, http_client=client)
    raw_payload_path = result["raw_payload_path"]
    manifest_path = result["manifest_path"]
    manifest = result["manifest"]
    assert client.calls == [
        (SCHEDULE_ENDPOINT, {"sportId": 1, "date": "2026-07-01", "hydrate": "probablePitcher"})
    ]
    assert raw_payload_path.is_file()
    assert manifest_path.is_file()
    assert json.loads(raw_payload_path.read_text(encoding="utf-8")) == payload
    assert json.loads(manifest_path.read_text(encoding="utf-8")) == manifest
    validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_manifest_preserves_unproven_source_issued_asof_status(tmp_path: Path) -> None:
    result = collect_mlb_statsapi_schedule_snapshot(
        "2026-07-01",
        tmp_path,
        http_client=FakeClient(response_with_payload({"dates": []})),
    )
    manifest = result["manifest"]
    assert manifest["collector_observed_asof_utc"] == manifest["response_received_at_utc"]
    assert manifest["source_issued_asof_utc"] is None
    assert manifest["source_issued_asof_proven"] is False
    assert manifest["acceptance_status"] == "UNPROVEN"
    assert manifest["score_blind_filter_required"] is True
    assert manifest["leakage_risk"] == "HIGH"


def test_manifest_preserves_selected_headers_only(tmp_path: Path) -> None:
    result = collect_mlb_statsapi_schedule_snapshot(
        "2026-07-01",
        tmp_path,
        http_client=FakeClient(response_with_payload({"dates": []})),
    )
    headers = result["manifest"]["response_headers_selected"]
    assert headers == {
        "date": "Sun, 28 Jun 2026 22:15:45 GMT",
        "cache-control": "max-age=20, public",
        "age": "22",
        "x-cache": "HIT, MISS",
    }
