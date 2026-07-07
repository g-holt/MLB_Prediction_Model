# Phase 0E Quality Gate Acceptance

Status: accepted baseline continuous-integration workflow.

## Accepted implementation

The accepted workflow is:

- repository path: `.github/workflows/quality-gate.yml`;
- workflow name: `Quality Gate`;
- required job name: `quality-gate`;
- workflow ID: `308421209`;
- pull-request trigger for changes targeting `main`;
- push trigger for changes merged or pushed to `main`;
- read-only repository contents permission;
- pinned checkout, Python setup, and uv setup actions;
- Python selected from `.python-version`;
- uv pinned to `0.11.23`;
- locked environment synchronization;
- pytest;
- Ruff lint;
- Ruff formatting validation; and
- Git diff whitespace validation.

## Pull-request proof

Pull request #29 added the workflow.

- feature commit: `b2be43347cb30411ed338a79e64c04346d4c7107`;
- merge commit: `dd0ea7007c75f4afb29c8a721b579012fcdcf77a`;
- pull-request workflow run: `28838750178`;
- run number: `1`;
- event: `pull_request`;
- job ID: `85528034193`;
- job name: `quality-gate`;
- run conclusion: `success`; and
- job conclusion: `success`.

The following required steps each completed successfully:

- Check out repository;
- Set up Python;
- Install uv;
- Synchronize locked environment;
- Run tests;
- Run Ruff lint;
- Check Ruff formatting; and
- Check Git diff formatting.

## Push-to-main proof

The squash merge triggered the workflow on `main`.

- push workflow run: `28839337636`;
- run number: `2`;
- event: `push`;
- head branch: `main`;
- head commit: `dd0ea7007c75f4afb29c8a721b579012fcdcf77a`;
- job ID: `85529851964`;
- job name: `quality-gate`;
- run conclusion: `success`; and
- job conclusion: `success`.

The same required steps each completed successfully.

## Local post-merge proof

After the push workflow passed:

- `uv sync --locked` passed;
- 67 pytest tests passed;
- Ruff lint passed;
- Ruff formatting validation passed;
- Git diff validation passed;
- the feature branch was removed locally and remotely; and
- the final `main` working tree was clean.

## Accepted scope

This acceptance proves that the uniquely named `quality-gate` workflow runs and passes
for both required event types.

The workflow is now eligible to be selected as a required status check.

## Open enforcement work

This acceptance does not claim that GitHub enforcement is active.

The following Phase 0E work remains open:

1. configure repository merge settings for squash-only merges and automatic head-branch deletion;
2. create the active `main` ruleset requiring strict `quality-gate`;
3. prove a blocked direct update and a passing compliant pull request; and
4. read back and record the accepted repository settings.
