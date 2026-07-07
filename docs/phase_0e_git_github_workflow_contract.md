# Phase 0E Git and GitHub Workflow Contract

Status: required project policy after merge to `main`.

Date: 2026-07-06

## Audit baseline

A read-only audit at commit
`90eec3af53885015985d985508b7cfd4bcf86717` proved:

- the default branch is `main`;
- local `main` tracks `origin/main`;
- the local and remote working states were clean and synchronized;
- squash, merge-commit, and rebase merge methods were all enabled;
- automatic deletion of merged head branches was disabled;
- `main` had no classic branch-protection rule;
- the repository had no rulesets;
- the repository had no GitHub Actions workflows;
- there were no open pull requests; and
- recent accepted work used isolated feature branches and pull requests.

This contract chooses the required workflow. Separate implementation tasks remain open
for continuous integration, repository merge settings, and an enforced `main` ruleset.

## Protected integration branch

`main` is the protected integration branch.

Routine direct commits and direct pushes to `main` are prohibited. Every code, test,
contract, roadmap, documentation, configuration, workflow, and repository-policy change
must enter `main` through a pull request.

An emergency ruleset or repository-setting change is allowed only to recover repository
access or repair a broken enforcement configuration. The reason, before-state,
after-state, and restoration must be recorded and reviewed through the next pull request.

## Branch creation and naming

Each change begins from a clean, current local `main` after:

1. fetching `origin/main`;
2. verifying local `main` equals `origin/main`;
3. using `git pull --ff-only` when an update is required; and
4. verifying the working tree is clean.

Branches use lowercase kebab-case and one of these descriptive forms:

- `phase-<phase>-<purpose>` for phase implementation or acceptance work;
- `contract-<purpose>` for cross-phase contract work;
- `audit-<purpose>` for evidence-only audits;
- `fix-<purpose>` for focused corrections;
- `docs-<purpose>` for isolated documentation work; or
- `roadmap-<purpose>` for dependency-order and project-list changes.

A branch contains one isolated logical change set. A merged or abandoned branch is not
reused for unrelated work.

## Pull-request requirements

Every pull request must:

- target `main`;
- identify the exact purpose and scope;
- list the important files or interfaces changed;
- distinguish accepted behavior from open work and non-goals;
- report the validation commands and results;
- contain no unrelated changes;
- be marked ready for review only after local gates pass; and
- resolve or explicitly acknowledge every review conversation before merge.

The pull-request title should be an imperative, stable description suitable for the
single squash commit recorded on `main`.

The repository is currently maintained by one owner. The enforced pull-request rule
will therefore require zero approving reviews. Review is still encouraged when an
independent reviewer is available, but the project must not create an impossible
self-approval requirement.

## Merge strategy

Squash merge is the only accepted merge method.

The repository settings must disable merge commits and rebase merges. Squashing keeps
one accepted commit per isolated pull request and preserves a linear `main` history.

Automatic merge and merge queue are deferred. The repository currently has low
concurrency and does not need either mechanism.

Merged remote head branches must be deleted automatically. The matching local branch
must be deleted after post-merge verification.

## Required pre-merge gates

Documentation-only changes do not receive a reduced baseline gate during Phase 0.
The test suite is small, and one uniform gate is simpler and less error-prone than a
path-dependent exemption.

Every pull request must pass:

- exact branch, base commit, and changed-file scope checks;
- `uv sync`;
- `uv run pytest`;
- `uv run ruff check .`;
- `uv run ruff format --check .`;
- `git diff --check`;
- the PowerShell command validator for every delivered repository command block; and
- every contract-specific validation required by the affected component.

Additional gates apply when relevant:

- packaging changes must build and audit the wheel and source distribution;
- source-status changes must prove the required raw artifacts, contracts, tests, and
  source-matrix updates;
- schema or artifact changes must run their accepted compatibility and determinism
  checks;
- repository-setting changes must read back and compare the resulting GitHub settings;
  and
- roadmap or contract changes must verify that active project documents do not
  contradict one another.

A local pass is required before push. The later GitHub Actions implementation must run
the same baseline quality gate on every pull request and on pushes to `main`.

## Continuous-integration contract

The repository will add one uniquely named required GitHub Actions job:

`quality-gate`

The workflow must run for pull requests targeting `main` and for pushes to `main`.
The job must use the accepted Python and `uv` toolchain and execute the baseline gates
defined above.

Required status checks will use strict mode: the pull-request branch must be current
with `main` before merge. Required job names must remain unique across workflows so
GitHub cannot report an ambiguous required check.

The exact workflow implementation remains open until it is added, observed on a real
pull request, and verified from GitHub Actions output.

## GitHub enforcement contract

After the `quality-gate` check has run successfully and can be selected as a required
check, the repository will create one active branch ruleset targeting `main`.

The ruleset must:

- require all changes to be associated with a pull request;
- require zero approving reviews;
- require all review conversations to be resolved;
- allow only squash merge for pull requests;
- require the strict `quality-gate` status check;
- require linear history;
- block force pushes;
- block deletion of `main`; and
- provide no routine bypass actor.

Classic branch protection will not be layered on top of this ruleset unless a later
contract documents a separate requirement. Avoiding overlapping systems keeps the
effective policy auditable.

Repository-level merge settings must:

- allow squash merge;
- disable merge commits;
- disable rebase merges;
- automatically delete merged head branches;
- keep automatic merge disabled; and
- keep merge queue deferred.

These enforcement settings remain unaccepted until they are implemented, read back,
and tested with both a blocked negative control and a passing pull-request control.

## Post-merge verification and cleanup

After every merge:

1. verify the pull request is merged and record its merge commit;
2. switch to `main`;
3. run `git pull --ff-only origin main`;
4. verify local `main` and `origin/main` equal the merge commit;
5. rerun the relevant accepted validation gates on merged `main`;
6. verify the working tree is clean;
7. verify the remote head branch is deleted;
8. delete the local head branch; and
9. record the merge commit in any acceptance document or source-matrix evidence that
   depends on that change.

A merge is not accepted merely because GitHub reports it as merged. The post-merge
verification and cleanup must pass.

## Enforcement implementation order

The remaining Phase 0E work must occur in this order:

1. merge this workflow-policy contract;
2. add and prove the `quality-gate` GitHub Actions workflow;
3. configure squash-only merging and automatic branch deletion;
4. create the active `main` ruleset with the observed status-check name;
5. prove direct `main` updates fail while a compliant pull request succeeds;
6. read back and record all repository settings; and
7. complete the Phase 0E roadmap items only after enforcement is proven.

## Non-goals

This contract does not:

- require an external approving reviewer while the repository has one maintainer;
- require signed commits;
- enable automatic merge;
- enable a merge queue;
- define release or deployment workflows;
- define package, source, schema, model, grading, or wallet interfaces; or
- claim that GitHub enforcement already exists.
