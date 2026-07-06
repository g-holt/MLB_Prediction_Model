# Phase 0D Packaging and Repository Structure Contract

Status: required project policy after merge to `main`.

Date: 2026-07-06

## Decision

The project is both:

- an installable Python application package; and
- a set of reusable internal library modules.

The project does not yet promise a stable public library API, publish a command-line
interface, or accept model, packet, grading, or wallet interfaces.

The existing packaging foundation is accepted:

- build backend: `uv_build`;
- distribution name: `mlb-prediction-model`;
- import package: `mlb_prediction_model`;
- source layout: `src/mlb_prediction_model`;
- package version source: `src/mlb_prediction_model/__init__.py`;
- lockfile: `uv.lock`;
- supported Python range: `>=3.14,<3.15`.

No `pyproject.toml` change is required for this decision.

## Build evidence

A read-only build audit at commit
`67874d4d4f466c10ddf9916ac342000ee2264906` proved that `uv build` produced exactly
one wheel and one source distribution.

The wheel contained only:

- the `mlb_prediction_model` import package;
- its six current Python modules; and
- standard distribution metadata.

The wheel did not contain repository documentation, tests, configuration, runtime
artifacts, source-audit evidence, or other repository-root files.

The source distribution contained:

- `README.md`;
- `pyproject.toml`;
- the import package under `src/`; and
- generated package metadata.

It did not contain `docs/`, `tests/`, `config/`, or `runs/`.

## Repository boundaries

### Importable package code

`src/mlb_prediction_model/` is the only importable project-code root.

As interfaces become accepted, package code should be organized by responsibility.
Expected responsibility boundaries include:

- source adapters;
- domain models and canonical identities;
- validation;
- storage and manifests;
- feature engineering;
- packet construction;
- prediction;
- grading;
- wallet logic; and
- a command-line layer, if later accepted.

These are responsibility boundaries, not permission to create speculative interfaces
or empty package trees before their contracts are proven.

### Tests

`tests/` contains automated tests. Tests may use tiny sanitized fixtures that are
explicitly accepted for version control. Tests must not depend on private runtime data,
credentials, browser state, or final-truth files outside an accepted grading test.

### Documentation and evidence

`docs/` contains project contracts, acceptance records, source capability decisions,
and small auditable source-proof artifacts.

Documentation is not importable package code and is not included in the wheel.

### Checked-in configuration

`config/` is reserved for non-secret checked-in configuration after a configuration
schema is accepted.

Local overrides and secrets must use ignored files or environment variables. No
credential, API key, browser state, token, cookie, or private account material may be
committed.

### Repository tooling

`tools/` is reserved for repository maintenance and audit utilities that are not part
of the importable application package.

A tool that becomes required application behavior must move behind an accepted package
interface rather than remaining an ad hoc script.

### Runtime artifacts

`runs/` is the single project runtime-artifact root.

Runtime outputs must not be written under `src/`, `tests/`, `docs/`, or `config/`.
The internal run-ID, date-partition, raw, derived, truth, grading, audit, and manifest
layout remains a Phase 1 decision.

Existing ignored `data/` paths are not accepted artifact locations. They remain ignored
to prevent accidental commits until Phase 1 either adopts, migrates, or removes them.

## Configuration precedence

When configuration interfaces are introduced, precedence is lowest to highest:

1. package defaults;
2. checked-in non-secret configuration;
3. environment variables;
4. explicit command-line overrides.

A higher-precedence value may override a lower-precedence value only through an
accepted, validated configuration field.

Secrets may be provided only through environment variables or ignored local
configuration. Checked-in configuration must never contain secrets.

## Naming and versioning

- Python packages, modules, and functions use `snake_case`.
- Contracts and documentation use stable descriptive names rather than copied
  `final`, `fixed`, or numbered script variants.
- Code history belongs in Git commits and pull requests.
- Schemas, manifests, packets, predictions, truth, and grading artifacts must carry
  explicit schema or contract versions when those formats are introduced.
- Runtime artifact names must be deterministic from accepted identifiers and
  configuration. Exact run-ID and date-partition rules remain a Phase 1 decision.
- Accepted artifacts are immutable. A changed run must receive a new run identity
  under the future Phase 1 contract.

## Command-line interface

A packaged command-line entry point is deferred.

No stable date, cutoff, collector, packet, prediction, grading, or wallet command
contract exists yet. A CLI may be added only after its configuration and application
interfaces are accepted.

## Existing schedule vertical slice

The existing schedule modules and tests remain in their current package locations:

- `asof_snapshot_manifest.py`;
- `mlb_statsapi_schedule.py`;
- `mlb_statsapi_schedule_fallback_asof.py`;
- `mlb_statsapi_schedule_snapshot.py`; and
- their tests.

This is a temporary compatibility decision, not final package architecture.

Reconciliation remains open until Phase 1 accepts the common raw snapshot, manifest,
storage, validation, and artifact-location contracts. That later work must preserve the
schedule source's limited-use `FALLBACK` scope and must not broaden its accepted fields.

The PowerShell command validator remains repository workflow support inside the package
until a later accepted tooling boundary provides an equally enforceable replacement.

## Acceptance requirements

This decision is accepted only after:

- exactly the intended contract, README, roadmap, and package metadata files change;
- `uv sync` passes;
- the full pytest suite passes;
- Ruff lint and format checks pass;
- `git diff --check` passes;
- one wheel and one source distribution build successfully;
- the wheel contains only importable package code and distribution metadata;
- the source distribution excludes `docs/`, `tests/`, `config/`, and `runs/`;
- the temporary build directory is removed; and
- the branch is committed and pushed for pull-request review.

## Non-goals

This contract does not accept:

- detailed Phase 1 storage or run-folder schemas;
- source adapter interfaces;
- a CLI;
- prediction packet schemas;
- model interfaces;
- grading truth interfaces;
- wallet behavior; or
- any source beyond its separately accepted capability status.
