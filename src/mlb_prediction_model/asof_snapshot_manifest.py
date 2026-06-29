"""As-of snapshot manifest validation helpers."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

REQUIRED_MANIFEST_FIELDS: tuple[str, ...] = (
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

GENERIC_HTTP_TIMESTAMP_HEADERS = {"date", "expires", "last-modified"}
COLLECTOR_TIMESTAMP_FIELDS = (
    "requested_at_utc",
    "response_received_at_utc",
    "collector_observed_asof_utc",
)


class AsofSnapshotManifestValidationError(ValueError):
    """Raised when an as-of snapshot manifest violates the accepted contract."""


def _resolve_payload_path(raw_payload_path: object, raw_payload_root: Path | None) -> Path:
    if not isinstance(raw_payload_path, str) or not raw_payload_path:
        raise AsofSnapshotManifestValidationError("raw_payload_path must be a non-empty string")
    payload_path = Path(raw_payload_path)
    if not payload_path.is_absolute() and raw_payload_root is not None:
        payload_path = raw_payload_root / payload_path
    return payload_path


def _sha256_file(path: Path) -> str:
    if not path.is_file():
        raise AsofSnapshotManifestValidationError(f"raw payload does not exist: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_required_fields(manifest: Mapping[str, Any]) -> None:
    missing = [field for field in REQUIRED_MANIFEST_FIELDS if field not in manifest]
    if missing:
        raise AsofSnapshotManifestValidationError(f"missing required manifest fields: {missing}")


def _validate_source_issued_asof(manifest: Mapping[str, Any]) -> None:
    source_issued_asof = manifest["source_issued_asof_utc"]
    source_issued_proven = manifest["source_issued_asof_proven"]
    if not isinstance(source_issued_proven, bool):
        raise AsofSnapshotManifestValidationError("source_issued_asof_proven must be a boolean")
    if source_issued_proven and source_issued_asof is None:
        raise AsofSnapshotManifestValidationError(
            "source_issued_asof_proven cannot be true when source_issued_asof_utc is null"
        )
    if not source_issued_proven and source_issued_asof is not None:
        raise AsofSnapshotManifestValidationError(
            "source_issued_asof_utc must be null when source_issued_asof_proven is false"
        )
    if source_issued_asof is None:
        return
    for field in COLLECTOR_TIMESTAMP_FIELDS:
        if manifest.get(field) == source_issued_asof:
            raise AsofSnapshotManifestValidationError(
                f"source_issued_asof_utc must not be copied from collector field {field}"
            )
    headers = manifest["response_headers_selected"]
    if not isinstance(headers, Mapping):
        raise AsofSnapshotManifestValidationError("response_headers_selected must be a mapping")
    for header_name, header_value in headers.items():
        if (
            str(header_name).lower() in GENERIC_HTTP_TIMESTAMP_HEADERS
            and header_value == source_issued_asof
        ):
            raise AsofSnapshotManifestValidationError(
                f"source_issued_asof_utc must not be copied from generic HTTP header {header_name}"
            )


def validate_asof_snapshot_manifest(
    manifest: Mapping[str, Any], raw_payload_root: Path | None = None
) -> None:
    """Validate one as-of snapshot manifest against the accepted draft contract."""
    _validate_required_fields(manifest)
    if manifest["acceptance_status"] != "UNPROVEN":
        raise AsofSnapshotManifestValidationError(
            "draft manifest validation only accepts acceptance_status UNPROVEN"
        )
    if not isinstance(manifest["raw_payload_sha256"], str) or not manifest["raw_payload_sha256"]:
        raise AsofSnapshotManifestValidationError("raw_payload_sha256 must be a non-empty string")
    _validate_source_issued_asof(manifest)
    payload_path = _resolve_payload_path(manifest["raw_payload_path"], raw_payload_root)
    actual_sha256 = _sha256_file(payload_path)
    if actual_sha256 != manifest["raw_payload_sha256"]:
        raise AsofSnapshotManifestValidationError(
            f"raw_payload_sha256 mismatch: expected {manifest['raw_payload_sha256']}, got {actual_sha256}"
        )
