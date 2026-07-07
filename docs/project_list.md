# MLB Prediction / Backtesting Project List

This list is the active project roadmap.

When the user asks for the `List`, print the current phases and tasks in a clean layout.

Completed items should be shown with strikethrough instead of being deleted, so the list preserves project history.

## Linear sequencing rule

- Work proceeds in phase order.
- Do not begin a later phase until the preceding phase acceptance gate and roadmap review are complete.
- Existing work completed ahead of an unfinished prerequisite remains preserved, but it does not waive the missing foundation gate.
- When a new dependency, risk, contract, or missing task is discovered, stop downstream work and insert it at the earliest prerequisite position in this list.
- At the end of every phase, review the actual code, contracts, artifacts, logs, source status, and unresolved risks; then add, split, remove, or reorder future tasks before beginning the next phase.
- Preserve completed items with strikethrough when tasks move.
- A source-specific audit must complete before implementing or using that source beyond a read-only probe.
- Betting and wallet work remains last.

## Current sequencing state

The accepted MLB Stats API schedule work is preserved as a completed vertical slice for limited-use schedule and canonical identity fallback. It does not waive the open packaging, Git workflow, repository-structure, and data-architecture gates.

The current stop point is Phase 0. Complete Phase 0 and Phase 1 before implementing another production source collector.

## Phase 0 — Governance, repository foundation, and source-audit rules

### 0A — Lock project principles

- ~~Define the core project goal: build a reproducible, score-blind MLB data and prediction system.~~
- ~~Define three model lanes: live, staging, and working.~~
- ~~Define project order: data collection first, prediction models second, betting/wallets last.~~
- ~~Clarify that “one hour before game” is preferred but not strict.~~
- ~~Clarify that odds cutoff timing should be configurable for testing.~~
- ~~Clarify that FanGraphs is allowed because the user has membership access, but it is not automatically the canonical source.~~
- ~~Clarify that Baseball Savant or another source may be preferred if more reliable.~~
- ~~Clarify that the running project list should retain completed items using strikethrough instead of deleting them.~~

### 0B — Verification and workflow-control contract

- ~~No guessed schemas, function signatures, CLI arguments, columns, validators, or workflow contracts.~~
- ~~Before executable code, prove the interface from source code, help output, logs, file headers, summary JSON, or accepted artifacts.~~
- ~~Separate responses into Proven facts, Unknowns / not yet verified, and Safe next action.~~
- ~~Unknowns must stay unknown until a read-only audit proves them.~~
- ~~If a command fails, inspect the full relevant code path and downstream contracts before patching.~~
- ~~Avoid large wrapper scripts before contracts are proven.~~
- ~~Do not claim pass unless all acceptance gates pass.~~
- ~~Include confidence ratings and uncertainty.~~
- ~~Always check online for existing algorithms, methods, libraries, public workflows, research, or best practices before choosing or building a data-gathering, feature-engineering, prediction, validation, analysis, or optimization approach.~~
- ~~Always review code for correctness, maintainability, simplicity, practical optimization, and downstream compatibility before delivery.~~
- ~~Prioritize finding the right information, fact-checking, interface verification, and optimization over response speed.~~
- ~~Require repository PowerShell blocks to use the exact repository-entry lines and command-delivery constraints.~~
- ~~Require a phase-end roadmap review before work begins on the next phase.~~
- ~~Require newly discovered prerequisites to be inserted at the earliest correct point before downstream work continues.~~

### 0C — Environment and toolchain

- ~~Decide primary programming language: Python.~~
- ~~Decide Python version after dependency compatibility audit: Python 3.14.6 is accepted for the starter stack.~~
- ~~Decide package/dependency manager: uv.~~
- ~~Decide local run shell: Windows PowerShell.~~
- ~~Decide testing framework: pytest.~~
- ~~Decide formatter/linter: ruff.~~
- ~~Verify local Python version.~~
- ~~Verify local Git version.~~
- ~~Verify local uv availability.~~
- ~~Verify PowerShell version.~~
- ~~Verify PowerShell execution policy.~~
- ~~Verify local repository clone path.~~
- ~~Verify local repository working tree is clean.~~
- ~~Verify accidental local `doc` folder is absent.~~
- ~~Verify Python 3.14 starter dependency install compatibility.~~
- ~~Verify Python 3.14 starter dependency import compatibility.~~
- ~~Verify `uv pip check` compatibility.~~

### 0D — Packaging, configuration, and repository structure

- ~~Formally decide whether the project is an installable application package, a reusable library package, or both.~~
- ~~Formally accept or revise the current `pyproject.toml`, `uv_build`, and `src` layout.~~
- ~~Define package boundaries for source adapters, domain models, validation, storage, feature engineering, packet building, prediction, grading, and wallet logic.~~
- ~~Define which files are package code, repository tooling, tests, documentation, configuration, and runtime artifacts.~~
- ~~Design the clean repository directory structure before adding another collector.~~
- ~~Define the runtime artifact root outside importable package code.~~
- ~~Define configuration precedence for defaults, checked-in configuration, environment variables, and command-line overrides.~~
- ~~Define secrets handling and explicitly exclude API keys, tokens, browser states, and credentials from Git.~~
- ~~Define naming and versioning rules for schemas, manifests, raw snapshots, derived datasets, packets, predictions, truth, and grading outputs.~~
- ~~Decide whether a packaged CLI entry point is created now or deferred until stable interfaces exist.~~
- ~~Record the existing schedule modules and tests as temporary compatibility placement, preserve the limited-use FALLBACK scope, and defer architectural reconciliation to the Phase 1 acceptance gate.~~
- ~~Update the README so its status matches the accepted schedule fallback and current roadmap.~~

### 0E — Git and GitHub workflow

- ~~Confirm GitHub connector availability.~~
- ~~Confirm authenticated GitHub user.~~
- ~~Confirm access to `g-holt/MLB_Prediction_Model`.~~
- ~~Confirm repository default branch is `main`.~~
- ~~Confirm repository permissions include admin, maintain, pull, push, and triage.~~
- ~~Create the initial documentation commit manually when connector writes were unavailable.~~
- ~~Repair the scaffold through the connector after write access became available.~~
- ~~Verify committed documentation files from repository contents.~~
- ~~Clone the repository locally.~~
- ~~Verify the local clone tracks `origin/main`.~~
- ~~Decide and document the branch strategy.~~
- ~~Decide whether direct commits to `main` are prohibited.~~
- ~~Decide whether every code, contract, roadmap, and documentation change requires a pull request.~~
- ~~Decide the merge method: squash, merge commit, or rebase.~~
- ~~Define branch naming and branch cleanup rules.~~
- ~~Define required pre-merge gates for tests, lint, formatting, diff checks, and contract-specific validation.~~
- ~~Define whether documentation-only changes may use reduced gates.~~
- ~~Decide whether branch protection and required status checks will be enabled.~~
- ~~Implement and prove a GitHub Actions pull-request job named `quality-gate`.~~
- Configure repository merge settings to allow squash merge only and automatically delete merged head branches.
- Create an active `main` ruleset requiring pull requests, strict `quality-gate`, conversation resolution, and linear history while blocking force pushes and deletion.
- Verify the enforced workflow with blocked direct-update and passing pull-request controls, then record the accepted settings.
- ~~Define one isolated change set per branch and pull request.~~
- ~~Define post-merge verification and local cleanup requirements.~~

### 0F — Source capability audit framework

- ~~Create the source capability matrix.~~
- ~~List candidate sources for each data category.~~
- ~~List Game schedule and canonical game IDs.~~
- ~~List Odds snapshots.~~
- ~~List Starting pitchers.~~
- ~~List Confirmed/probable lineups.~~
- ~~List Team batting stats.~~
- ~~List Player batting stats.~~
- ~~List Starting pitcher stats.~~
- ~~List Bullpen usage.~~
- ~~List Team defense.~~
- ~~List Park factors.~~
- ~~List Weather.~~
- ~~List Injuries/roster status.~~
- ~~List Final scores for grading only.~~
- ~~Define the required proof artifact checklist.~~
- ~~Define source status values: `UNPROVEN`, `PROVEN_SAFE`, `PROVEN_UNSAFE`, `FALLBACK`, `FINAL_TRUTH_ONLY`, and `EXCLUDED`.~~
- ~~Define the per-source proof dimensions: historical access, as-of/timestamp behavior, prior-game-only derivation, login/API requirements, raw format, and leakage risk.~~
- ~~Define the source decision rule requiring raw proof, schema proof, leakage review, reproducibility review, and explicit acceptance.~~
- ~~Set the initial source-audit priority order.~~
- Require every source-specific phase below to complete all proof dimensions before implementation acceptance.
- Require a source-specific acceptance review before any matrix row changes from `UNPROVEN`.
- Require matrix evidence text to reference the exact accepted artifacts and merge commits.
- Require source limitations and fallback scopes to be enforced in code and tests, not only documented.

### 0G — Phase 0 acceptance and roadmap review gate

- Verify the packaging decision is documented and matches `pyproject.toml`.
- Verify the repository structure is documented before additional collector work.
- Verify the Git/GitHub workflow is documented and enforceable.
- Verify the source-audit framework is complete and unambiguous.
- Verify README, project list, operating contract, verification contract, and source matrix do not contradict one another.
- Review all completed schedule work and identify any reconciliation required after Phase 1 architecture.
- Re-evaluate every later phase for missing prerequisites and reorder or add tasks where needed.
- Record the Phase 0 review in the repository.
- Do not begin Phase 1 until this gate passes.

## Phase 1 — Data architecture, time semantics, and score-blind storage

### 1A — Time and as-of semantics

- Define the canonical timezone policy and require timezone-aware timestamps.
- Define scheduled game time, configured cutoff, request time, response-received time, collector-observed time, source-issued time, selected snapshot time, prediction-lock time, and grading time.
- Define inclusive and exclusive cutoff comparisons for each artifact type.
- Define current collection, forward capture, deterministic replay, and historical reconstruction modes.
- Define how postponed, suspended, resumed, and doubleheader timing changes affect cutoff eligibility.
- Define clock-skew and missing-timestamp failure behavior.
- Define the date and cutoff configuration contract before implementing general date input handling.

### 1B — Folder and artifact separation

- Design the raw source data folder.
- Design the as-of snapshot folder.
- Design the derived pregame feature folder.
- Design the canonical game-index folder.
- Design the model packet folder.
- Design the prediction output folder.
- Design the wallet folder.
- Design the postgame truth folder.
- Design the grading folder.
- Design the audit folder.
- Design the manifest folder.
- Define run-ID and date-partition layout.
- Define temporary and cache locations that must never be treated as accepted artifacts.

### 1C — Data contracts, schemas, and versioning

- Define a common raw snapshot envelope.
- Define the manifest schema and required provenance fields.
- Define schema-version fields and compatibility rules.
- Define canonical serialization and hashing rules.
- Define file naming, partitioning, and overwrite policy.
- Define atomic-write behavior and partial-run cleanup.
- Define source adapter interfaces only after real source artifacts prove the required inputs and outputs.
- Define validation error categories and blocked-record representation.
- Define configuration snapshot and code-version provenance for every run.

### 1D — Score-blind and leakage boundaries

- Ensure prediction input builders cannot read postgame truth.
- Ensure final scores are stored only in grading/final-truth areas.
- Ensure raw historical responses containing scores are filtered before any pregame-derived output.
- Ensure wallets are generated only after predictions are locked.
- Ensure repeated backtests do not rely on remembered outcomes.
- Define an automated leakage audit requirement.
- Define denylisted fields and denylisted paths for packet construction.
- Define a fail-closed rule when as-of eligibility cannot be proven.

### 1E — Reproducibility and integrity rules

- Store raw source files unchanged.
- Store derived files separately from raw files.
- Store manifests with source paths, timestamps, hashes, cutoff settings, schema versions, and code versions.
- Require deterministic packet rebuilds when accepted raw files and configuration are unchanged.
- Add rerun comparison using file hashes.
- Add raw-payload hash validation before derivation.
- Add duplicate-artifact and duplicate-key detection.
- Require accepted runs to be immutable and new runs to receive new run IDs.

### 1F — Phase 1 acceptance and roadmap review gate

- Prove one sample run can place raw, manifest, derived, truth, and audit artifacts only in their allowed locations.
- Prove the packet path cannot access truth or grading paths.
- Prove a deterministic rebuild produces identical accepted outputs.
- Prove hash mismatch, missing provenance, and ambiguous cutoff fail closed.
- Reconcile the existing schedule vertical slice with the accepted architecture.
- Re-evaluate every later phase for missing prerequisites and reorder or add tasks where needed.
- Record the Phase 1 review in the repository.
- Do not begin Phase 2 extension work until this gate passes.

## Phase 2 — Date handling, schedule, and canonical game identity

### 2A — Date input contract

- Support one specific date.
- Support multiple dates.
- Support today’s games.
- Support future live-slate collection.
- Support historical backtest dates.
- Support configurable as-of cutoff timing.
- Define date ordering, duplicate-date handling, and invalid-date behavior.
- Define timezone conversion from local operator input to canonical UTC.
- Define the interface only after the Phase 1 configuration contract is accepted.

### 2B — Schedule source audit

- ~~Audit the MLB Stats API schedule endpoint with a historical response sample.~~
- ~~Audit a future-date schedule range.~~
- ~~Prove the observed access method does not require login or an API key.~~
- ~~Prove the raw response format is JSON.~~
- ~~Identify historical score and winner fields as a high leakage risk.~~
- ~~Audit HTTP retrieval and cache timestamp behavior.~~
- ~~Probe GET and HEAD variants for durable source-issued timestamps.~~
- ~~Record that no durable source-issued representation timestamp was proven.~~
- ~~Define the score-blind schedule filter contract.~~
- ~~Define the limited-use forward-capture or deterministic-replay fallback contract.~~

### 2C — Schedule collection and limited-use fallback implementation

- ~~Implement score-blind schedule filtering.~~
- ~~Implement canonical MLB game identity construction.~~
- ~~Implement duplicate canonical-ID validation.~~
- ~~Implement the as-of snapshot manifest validator used by the schedule vertical slice.~~
- ~~Implement the MLB schedule snapshot collector with payload hashing.~~
- ~~Implement the limited-use fallback validator.~~
- ~~Add positive, negative, cutoff, timestamp, status, hash, allowlist, and deterministic-replay tests.~~
- ~~Accept Game schedule as limited-use `FALLBACK`.~~
- ~~Accept Canonical game IDs as limited-use `FALLBACK`.~~
- ~~Record that the fallback is not `PROVEN_SAFE` and excludes scores, probable pitchers, lineups, packet schema, and all other unaudited model inputs.~~

### 2D — Canonical game index and crosswalks

- Define the canonical game-index schema under the Phase 1 schema rules.
- Build one canonical game list per date.
- ~~Map MLB `gamePk` and `gameGuid` into the accepted canonical identity output.~~
- Define stable team identity and alias normalization.
- Map FanGraphs game and team identifiers if available.
- Map Baseball Savant or Statcast identifiers if available.
- Map Odds API event identifiers.
- Map Retrosheet identifiers if used.
- Record a documented missing-source reason when a crosswalk cannot be proven.
- Prevent downstream joins on unproven fuzzy matching.
- Reconcile the existing canonical identity helper with the accepted canonical index schema.

### 2E — Game lifecycle edge cases

- Handle doubleheaders.
- Handle postponed games.
- Handle canceled games.
- Handle suspended games.
- Handle resumed games.
- Handle neutral-site games.
- Handle venue changes.
- Handle schedule-time changes after an earlier snapshot.
- Define canonical identity stability when lifecycle status changes.

### 2F — Phase 2 acceptance and roadmap review gate

- For one test date, prove every game has a canonical ID or a documented missing-source reason.
- Prove the schedule snapshot is eligible under the configured cutoff.
- Prove duplicate IDs and ambiguous crosswalks fail closed.
- Prove each lifecycle edge case has passing behavior or an explicit blocker.
- Prove no downstream collector runs for a game whose identity is unproven.
- Re-evaluate every later phase for missing prerequisites and reorder or add tasks where needed.
- Record the Phase 2 review in the repository.
- Do not begin Odds implementation until this gate passes.

## Phase 3 — Odds source audit, snapshots, and normalization

### 3A — Odds source audit

- Prove The Odds API account access.
- Prove the MLB sport key from actual API output.
- Prove historical endpoint access under the actual account plan.
- Prove current odds endpoint access.
- Prove available markets.
- Prove available bookmakers.
- Prove timestamp and timezone format.
- Prove rate-limit and quota behavior.
- Prove raw JSON response format and keys.
- Prove whether historical responses are immutable snapshots or reconstructed responses.
- Identify final-score, settlement, or postgame leakage fields.
- Complete a source-specific acceptance review before implementing production use.

### 3B — Raw odds snapshot collection

- Define the odds raw-snapshot contract from actual responses.
- Implement authenticated configuration without committing secrets.
- Implement current and historical raw snapshot collectors only for proven endpoints.
- Preserve raw responses unchanged.
- Write manifests, hashes, request parameters, quota headers, and timestamps.
- Fail closed on authentication, quota, timestamp, schema, or partial-response errors.
- Add deterministic replay from stored raw odds.

### 3C — Odds event identity mapping

- Map Odds API event IDs to canonical game IDs.
- Normalize team aliases only through accepted team crosswalks.
- Handle doubleheaders and same-day repeated matchups.
- Document unmatched and ambiguous events.
- Block unmatched or ambiguous odds from packet construction.

### 3D — Configurable odds cutoff selection

- Define the default cutoff setting.
- Allow alternate cutoff settings.
- Select the snapshot closest to the requested cutoff without crossing prohibited boundaries.
- Preserve the source odds timestamp.
- Store requested cutoff and selected snapshot time separately.
- Flag any selected snapshot after cutoff.
- Flag any selected snapshot too far from cutoff.
- Define deterministic tie-breaking when snapshots are equally close.

### 3E — Odds normalization

- Normalize moneyline.
- Normalize total.
- Normalize spread.
- Normalize book name.
- Normalize home and away teams through accepted IDs.
- Preserve raw price and source fields beside normalized output.
- Calculate implied probability.
- Calculate vig.
- Delay consensus pricing until raw odds and book-level normalization are accepted.

### 3F — Phase 3 acceptance and roadmap review gate

- For one historical date, collect and hash raw odds.
- Prove the selected snapshot timestamp and cutoff decision.
- Prove canonical game mapping for every accepted odds record.
- Prove prediction input contains no final-score or settlement leakage.
- Document missing odds by game, book, and market.
- Prove deterministic replay from stored raw odds.
- Re-evaluate every later phase for missing prerequisites and reorder or add tasks where needed.
- Record the Phase 3 review in the repository.
- Do not begin roster or player source implementation until this gate passes.

## Phase 4 — Team, player, roster, lineup, and starter identity

### 4A — Identity and availability source audits

- Audit candidate team and player identifier sources.
- Audit historical roster and transaction sources.
- Audit injury and availability sources.
- Audit probable starting-pitcher sources.
- Audit confirmed and probable lineup sources.
- Prove historical access, as-of behavior, authentication, raw format, and leakage risk for each source.
- Prove the distinction between announced, probable, projected, and confirmed status.
- Complete source-specific acceptance reviews before implementation use.

### 4B — Canonical team and player identity

- Define canonical team IDs and alias rules.
- Define canonical player IDs.
- Map MLB player IDs.
- Map FanGraphs player IDs if used.
- Map Baseball Savant or Statcast player IDs if used.
- Map Retrosheet player IDs if used.
- Define name-change, suffix, accent, and duplicate-name handling.
- Block fuzzy or ambiguous player matches from accepted packets.

### 4C — Roster and transaction timeline

- Build as-of roster membership by game cutoff.
- Preserve transaction effective times and source timestamps.
- Handle call-ups, options, injured-list moves, releases, trades, and substitutions.
- Distinguish current reconstructed roster data from true historical as-of records.
- Define missing and conflicting roster-status behavior.

### 4D — Lineup and starting-pitcher states

- Represent projected, probable, announced, and confirmed lineups separately.
- Represent probable and confirmed starters separately.
- Require confirmed starters from accepted lineup evidence when the model policy requires confirmation.
- Block TBD or unconfirmed starters when required.
- Identify opener and bulk-pitcher roles.
- Define lineup revision and late-scratch behavior.
- Preserve the exact as-of evidence used for each status.

### 4E — Phase 4 acceptance and roadmap review gate

- For one test date, map all accepted teams and players to canonical IDs or documented missing reasons.
- Prove roster, lineup, injury, and starter status is cutoff-safe.
- Prove ambiguous identities and unsupported status states block.
- Prove opener and bulk roles are represented without silently treating both as traditional starters.
- Re-evaluate every later phase for missing prerequisites and reorder or add tasks where needed.
- Record the Phase 4 review in the repository.
- Do not begin statistical feature-source implementation until this gate passes.

## Phase 5 — Statistical source audits, raw collection, and pregame features

### 5A — Statistical and contextual source audits

- Audit FanGraphs exports.
- Audit Baseball Savant and Statcast exports.
- Audit MLB data used for statistics.
- Audit Retrosheet-derived data if used.
- Audit prior-game logs for bullpen usage.
- Audit team-defense sources.
- Audit park-factor sources.
- Audit historical weather-forecast sources.
- Prove raw file headers or JSON keys.
- Prove date filters.
- Prove timestamp and timezone behavior.
- Prove whether each export is true historical as-of data or current reconstructed data.
- Prove login, membership, API-key, and download requirements.
- Identify score, result, and future-information leakage fields.
- Complete a separate acceptance review for each source and data category.

### 5B — Source selection and raw collection

- Select accepted sources for team batting.
- Select accepted sources for player batting.
- Select accepted sources for starting-pitcher statistics.
- Select accepted sources for bullpen usage.
- Select accepted sources for team defense.
- Select accepted sources for park factors.
- Select an accepted historical forecast source for weather.
- Document fallback precedence without silently mixing incompatible definitions.
- Define each raw snapshot or export contract from accepted artifacts.
- Implement one isolated adapter per accepted source.
- Preserve raw files unchanged.
- Write common manifests, hashes, query parameters, timestamps, and source versions.
- Implement deterministic replay from stored raw files.
- Add source-specific schema and negative-control tests.

### 5C — Feature contract and rolling-window engine

- Define the feature-table key and schema-version contract.
- Require every feature to document source, definition, time window, units, null behavior, and cutoff rule.
- Require all rolling features to use only events available before the target game cutoff.
- Define missing-stat neutral handling and minimum sample-size rules.
- Build season-to-date windows excluding the target game.
- Build date windows for 7, 14, and 30 days.
- Build game-count windows for last 10 and last 15 games.
- Prove deterministic ordering for same-day and doubleheader events.
- Add boundary tests for first game, missing history, postponed games, and season transitions.

### 5D — Team batting features

- Season-to-date offense before game.
- Last 7 days offense before game.
- Last 14 days offense before game.
- Last 30 days offense before game.
- Last 10 games offense before game.
- Last 15 games offense before game.
- Split by opposing pitcher handedness only if an accepted source supports it safely.

### 5E — Player batting features

- Join only projected or confirmed lineup players supported by accepted as-of evidence.
- Season-to-date batting before game.
- Recent batting windows before game.
- Handedness splits only if supported safely.
- Define missing-player and limited-sample behavior.
- Prevent lineup changes after cutoff from rewriting locked historical inputs.

### 5F — Starting-pitcher features

- Season-to-date pitcher stats before game.
- Recent pitcher windows before game.
- Pitcher handedness.
- Starter workload.
- Starter rest days.
- Starter split data only if supported safely.
- Weight opener and bulk roles according to an accepted rule.
- Block unsupported or unconfirmed starter states.

### 5G — Bullpen features

- Recent bullpen usage.
- Last 1 day usage.
- Last 2 days usage.
- Last 3 days usage.
- Last 5 days usage.
- Bullpen availability estimate.
- Define pitcher-to-bullpen membership as of the target cutoff.
- Prevent target-game appearances from entering usage features.

### 5H — Defense, park, weather, and availability features

- Build accepted team-defense features.
- Build accepted park-factor features with version and season context.
- Build historical weather-forecast features using forecast issue time.
- Build injury and roster-availability features.
- Define neutral values for missing contextual inputs.
- Keep observed postgame weather out of pregame inputs.

### 5I — Phase 5 acceptance and roadmap review gate

- Prove one historical sample for every accepted statistical and contextual source.
- Prove each adapter writes only accepted raw and manifest artifacts.
- Prove every feature is cutoff-safe and prior-game-only where required.
- Prove target-game outcomes and postgame fields are absent.
- Prove missing and blocked inputs behave according to contract.
- Prove deterministic raw replay and deterministic feature hashes.
- Re-evaluate the project and add later packet, truth, model, backtest, operational, and wallet phases only after the Phase 5 evidence supports their exact contracts.
- Record the Phase 5 review in the repository.
