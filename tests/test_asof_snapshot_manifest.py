import hashlib
from pathlib import Path

import pytest

from mlb_prediction_model.asof_snapshot_manifest import (
    REQUIRED_MANIFEST_FIELDS,
    AsofSnapshotManifestValidationError,
    validate_asof_snapshot_manifest,
)


def write_raw_payload(tmp_path: Path, content: bytes = b'{"games": []}\n') -> tuple[str, str]:
    raw_path = tmp_path / "raw_payload.json"
    raw_path.write_bytes(content)
    return raw_path.name, hashlib.sha256(content).hexdigest()


def valid_manifest(tmp_path: Path) -> dict[str, object]:
    raw_payload_path, raw_payload_sha256 = write_raw_payload(tmp_path)
    return {
        "manifest_version": 1,
        "source_name": "MLB Stats API schedule endpoint",
        "source_url": "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-07-01",
        "request_method": "GET",
        "requested_at_utc": "2026-06-28T22:15:42Z",
        "response_received_at_utc": "2026-06-28T22:15:45Z",
        "collector_observed_asof_utc": "2026-06-28T22:15:45Z",
        "source_issued_asof_utc": None,
        "source_issued_asof_proven": False,
        "response_http_status": 200,
        "response_headers_selected": {
            "date": "Sun, 28 Jun 2026 22:15:45 GMT",
            "cache-control": "max-age=20, public, stale-while-revalidate=30, stale-if-error=86400",
            "age": "22",
            "x-cache": "HIT, MISS",
        },
        "raw_payload_sha256": raw_payload_sha256,
        "raw_payload_path": raw_payload_path,
        "score_blind_filter_required": True,
        "leakage_risk": "HIGH",
        "acceptance_status": "UNPROVEN",
    }


def test_required_manifest_fields_match_contract() -> None:
    assert REQUIRED_MANIFEST_FIELDS == (
        "manifest_version",
        "source_name",
        "source_url",
        "request_method",
        "requested_at_utc",
        "response_received_at_utc",
        "collector_observed_asof_utc",
        "source_issued_asof_utc",
        "source_issued_asof_proven",
        "response_http_status",
        "response_headers_selected",
        "raw_payload_sha256",
        "raw_payload_path",
        "score_blind_filter_required",
        "leakage_risk",
        "acceptance_status",
    )


def test_valid_manifest_passes_validation(tmp_path: Path) -> None:
    validate_asof_snapshot_manifest(valid_manifest(tmp_path), raw_payload_root=tmp_path)


def test_missing_required_manifest_field_fails(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    del manifest["source_url"]
    with pytest.raises(
        AsofSnapshotManifestValidationError, match="missing required manifest fields"
    ):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_source_issued_asof_proven_true_requires_source_issued_asof(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["source_issued_asof_proven"] = True
    with pytest.raises(AsofSnapshotManifestValidationError, match="cannot be true"):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_unproven_source_issued_asof_must_stay_null(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["source_issued_asof_utc"] = "2026-06-28T22:15:45Z"
    with pytest.raises(AsofSnapshotManifestValidationError, match="must be null"):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_source_issued_asof_cannot_copy_collector_timestamp(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["source_issued_asof_proven"] = True
    manifest["source_issued_asof_utc"] = manifest["collector_observed_asof_utc"]
    with pytest.raises(AsofSnapshotManifestValidationError, match="collector field"):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_source_issued_asof_cannot_copy_generic_http_header(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["source_issued_asof_proven"] = True
    manifest["source_issued_asof_utc"] = "Sun, 28 Jun 2026 22:15:45 GMT"
    with pytest.raises(AsofSnapshotManifestValidationError, match="generic HTTP header date"):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_raw_payload_sha256_mismatch_fails(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["raw_payload_sha256"] = "0" * 64
    with pytest.raises(AsofSnapshotManifestValidationError, match="raw_payload_sha256 mismatch"):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)


def test_acceptance_status_must_remain_unproven_in_draft_validation(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["acceptance_status"] = "PROVEN_SAFE"
    with pytest.raises(AsofSnapshotManifestValidationError, match="UNPROVEN"):
        validate_asof_snapshot_manifest(manifest, raw_payload_root=tmp_path)
