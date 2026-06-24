# MLB Prediction / Backtesting Project List

This list is the active project roadmap.

When the user asks for the `List`, print the current phases and tasks in a clean layout.

Completed items should be shown with strikethrough instead of being deleted, so the list preserves project history.

## Phase 0 — Project rules, source audit, and proof standards

### 0A — Lock project principles

- ~~Define the core project goal: build a reproducible, score-blind MLB data and prediction system.~~
- ~~Define three model lanes: live, staging, and working.~~
- ~~Define project order: data collection first, prediction models second, betting/wallets last.~~
- ~~Clarify that “one hour before game” is preferred but not strict.~~
- ~~Clarify that odds cutoff timing should be configurable for testing.~~
- ~~Clarify that FanGraphs is allowed because the user has membership access, but it is not automatically the canonical source.~~
- ~~Clarify that Baseball Savant or another source may be preferred if more reliable.~~
- ~~Clarify that the running project list should retain completed items using strikethrough instead of deleting them.~~

### 0B — Strict verification contract

- ~~No guessed schemas, function signatures, CLI arguments, columns, validators, or workflow contracts.~~
- ~~Before executable code, prove the interface from source code, help output, logs, file headers, summary JSON, or accepted artifacts.~~
- ~~Separate responses into Proven facts, Unknowns / not yet verified, and Safe next action.~~
- ~~Unknowns must stay unknown until a read-only audit proves them.~~
- ~~If a command fails, inspect the full relevant code path and downstream contracts before patching.~~
- ~~Avoid large wrapper scripts before contracts are proven.~~
- ~~Do not claim pass unless all acceptance gates pass.~~
- ~~Include confidence ratings and uncertainty.~~
- ~~Always check online for existing algorithms, methods, libraries, public workflows, research, or best practices that may help with data gathering, feature engineering, data analysis, model evaluation, or optimization before choosing or building an approach.~~
- ~~Always make sure code is reviewed for correctness, maintainability, and practical optimization before giving it to the user.~~
- ~~Prioritize finding the right information, fact-checking, interface verification, and optimization over response speed.~~

### 0C — Source capability matrix

- ~~Create source capability matrix.~~
- ~~List candidate sources for each data category.~~
- Prove whether each source supports historical data.
- Prove whether each source supports as-of or timestamped data.
- Prove whether data can be derived from prior games only.
- Prove login/API requirements.
- Prove raw export format.
- Identify leakage risk.
- ~~Define required proof artifact for each source.~~
- ~~Mark initial source status as unproven, proven-safe, proven-unsafe, fallback, final-truth-only, or excluded.~~

### 0D — Candidate source categories

- ~~Game schedule and canonical game IDs.~~
- ~~Odds snapshots.~~
- ~~Starting pitchers.~~
- ~~Confirmed/probable lineups.~~
- ~~Team batting stats.~~
- ~~Player batting stats.~~
- ~~Starting pitcher stats.~~
- ~~Bullpen usage.~~
- ~~Team defense.~~
- ~~Park factors.~~
- ~~Weather.~~
- ~~Injuries/roster status.~~
- ~~Final scores for grading only.~~

### 0E — Programming language, environment, and repository strategy

- ~~Decide primary programming language: Python.~~
- ~~Decide Python version after dependency compatibility audit: Python 3.14.6 is accepted for the starter stack.~~
- ~~Decide package/dependency manager: uv.~~
- ~~Decide local run shell: Windows PowerShell.~~
- Decide project packaging format.
- ~~Decide testing framework: pytest.~~
- ~~Decide formatter/linter: ruff.~~
- Decide Git/GitHub workflow.
- Design clean project structure to avoid script/folder sprawl.
- ~~Define rule: code history lives in Git, not copied script versions.~~
- ~~Define rule: run outputs live in run folders/manifests, not script iteration folders.~~
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

### 0F — GitHub repository setup

- ~~Confirm GitHub connector availability.~~
- ~~Confirm authenticated GitHub user.~~
- ~~Confirm access to `g-holt/MLB_Prediction_Model`.~~
- ~~Confirm repository default branch is `main`.~~
- ~~Confirm repository permissions include admin, maintain, pull, push, and triage.~~
- ~~Create initial documentation commit manually if connector write actions remain blocked.~~
- ~~Repair scaffold through connector once write path became available.~~
- ~~Verify committed documentation files from repository contents.~~
- ~~Clone repository locally.~~
- ~~Verify local clone tracks `origin/main`.~~
- ~~Verify no accidental local `doc` folder exists.~~
- Decide branch strategy.
- Decide whether direct commits to `main` are allowed after initial scaffold.
- Decide whether all future changes require pull requests.

## Phase 1 — Data architecture and score-blind storage

### 1A — Folder and file separation

- Design raw source data folder.
- Design as-of snapshot folder.
- Design derived pregame feature folder.
- Design model packet folder.
- Design prediction output folder.
- Design wallet folder.
- Design postgame truth folder.
- Design grading folder.
- Design audit folder.
- Design manifest folder.

### 1B — Score-blind boundaries

- Ensure prediction packet builder cannot read postgame truth.
- Ensure final scores are stored only in grading/final-truth area.
- Ensure wallets are generated from predictions plus final truth only after predictions are locked.
- Ensure repeated backtests do not rely on remembered outcomes.
- Add leakage audit requirement.

### 1C — Reproducibility rules

- Store raw source files unchanged.
- Store derived files separately from raw files.
- Store manifest with source paths, timestamps, hashes, and cutoff settings.
- Require deterministic packet rebuilds when raw files are unchanged.
- Add rerun comparison using file hashes.

## Phase 2 — Date and game identity system

### 2A — Date input handling

- Support specific dates.
- Support multiple dates.
- Support today’s games.
- Support future live slate collection.
- Support historical backtest dates.
- Support configurable as-of cutoff timing.

### 2B — Canonical game index

- Build one canonical game list per date.
- Prove schedule source.
- Prove source-specific game IDs.
- Map MLB game ID.
- Map FanGraphs game/team identifiers if available.
- Map Baseball Savant/Statcast identifiers if available.
- Map Odds API event identifiers.
- Map Retrosheet identifiers if used.
- Handle doubleheaders.
- Handle postponed games.
- Handle suspended games.
- Handle neutral-site games.

### 2C — Acceptance gate

- For one test date, every game has a canonical ID or a documented missing-source reason.
- No downstream collector runs until game identity is proven for the test date.

## Phase 3 — Odds collection

### 3A — Odds source audit

- Prove The Odds API account access.
- Prove MLB sport key from API output.
- Prove historical endpoint access.
- Prove current odds endpoint access.
- Prove markets available.
- Prove bookmakers available.
- Prove timestamp format.
- Prove rate limit/quota behavior.
- Prove raw JSON response format.

### 3B — Configurable odds cutoff

- Define default cutoff setting.
- Allow alternate cutoff settings.
- Select snapshot closest to cutoff.
- Preserve actual odds timestamp.
- Store requested cutoff and selected snapshot time separately.
- Flag if selected snapshot is after cutoff.
- Flag if selected snapshot is too far from cutoff.

### 3C — Odds normalization

- Normalize moneyline.
- Normalize total.
- Normalize spread.
- Normalize book name.
- Normalize home/away team names.
- Calculate implied probability.
- Calculate vig.
- Create consensus price later only after raw odds are proven.

### 3D — Acceptance gate

- For one historical date, raw odds are collected.
- Selected odds snapshot timestamp is proven.
- Prediction input contains no final score leakage.
- Missing odds are documented by game/book/market.

## Phase 4 — Player, team, and rolling-stat data

### 4A — Source audit

- Audit FanGraphs exports.
- Audit Baseball Savant/Statcast exports.
- Audit MLB data if used.
- Audit Retrosheet-derived data if used.
- Prove raw file headers.
- Prove date filters.
- Prove whether exports are true historical as-of data or current reconstructed data.

### 4B — Team batting features

- Season-to-date offense before game.
- Last 7 days offense before game.
- Last 14 days offense before game.
- Last 30 days offense before game.
- Last 10 games offense before game.
- Last 15 games offense before game.
- Split by pitcher handedness if source supports it safely.

### 4C — Player batting features

- Projected/confirmed lineup player stats.
- Season-to-date batting before game.
- Recent batting windows before game.
- Handedness splits if source supports it safely.
- Missing-player handling rule.

### 4D — Starting pitcher features

- Season-to-date pitcher stats before game.
- Recent pitcher windows before game.
- Pitcher handedness.
- Starter workload.
- Starter rest days.
- Starter split data if source supports it safely.
- Opener/bulk pitcher handling rule.

### 4E — Bullpen features

- Recent bullpen usage.
- Last 1 day usage.
- Last 2 days usage.
- Last 3 days usage.
- Last 5 days usage.
- Bullpen availability estimate.
- Bullpen quality estimate.
- Missing bullpen data rule.

### 4F — Acceptance gate

- Every feature has provenance.
- Every feature is generated only from data available before the target game.
- Every missing value has a documented rule.
- No final score columns enter prediction packet.

## Phase 5 — Lineups, starters, roster, and injuries

### 5A — Starters

- Prove source for probable starters.
- Prove source for confirmed starters.
- Define confirmed starter rule.
- Define probable starter rule.
- Define TBD starter rule.
- Define opener rule.
- Define bulk pitcher rule.
- Define late scratch handling.

### 5B — Lineups

- Prove source for historical confirmed lineups.
- Prove source for current day confirmed lineups.
- Define what happens if lineup is not confirmed by cutoff.
- Define projected lineup fallback if allowed.
- Store lineup confidence status.

### 5C — Roster and injuries

- Prove source for historical roster status.
- Prove source for historical injuries.
- Decide whether injury data is required, optional, or excluded.
- Define missing injury data rule.

### 5D — Acceptance gate

- Each game is marked confirmed, probable, blocked, or degraded.
- Blocked/degraded reason is stored.
- No lineup/starters data is assumed without proof.

## Phase 6 — Weather and park context

### 6A — Weather source decision

- Identify candidate weather sources.
- Prove historical forecast availability if possible.
- Prove observed weather availability if used.
- Decide whether forecast, observed, or both will be stored.
- Label weather as forecast or observed.

### 6B — Weather fields

- Temperature.
- Wind speed.
- Wind direction.
- Precipitation.
- Humidity.
- Roof status if available.
- Start-time weather timestamp.
- Weather source timestamp.

### 6C — Park context

- Park name.
- Park factor source.
- Roof/dome status if available.
- Altitude if used.
- Run environment label if used.

### 6D — Acceptance gate

- Weather data is timestamped and source-labeled.
- Forecast and observed data are not mixed without labels.
- Park context is stored separately from weather.

## Phase 7 — Pregame prediction packet builder

### 7A — Packet structure

- Build one packet per date.
- Include one game card per game.
- Include raw source references.
- Include derived feature summaries.
- Include missing-data report.
- Include cutoff configuration.
- Include source manifest.
- Include leakage audit.

### 7B — Human-readable output

- Game summary.
- Starting pitchers.
- Lineups if available.
- Team form.
- Player form.
- Bullpen context.
- Odds context.
- Weather/park context.
- Data confidence flags.

### 7C — Model-readable output

- Normalized feature table.
- Game ID table.
- Odds table.
- Team/player summary tables.
- Missing-value table.
- Manifest JSON.

### 7D — Acceptance gate

- Packet can be regenerated.
- Packet hashes match when source files are unchanged.
- Packet contains no final scores.
- Packet is easy to read and use for predictions.

## Phase 8 — Model lanes

### 8A — Live model

- Define live model folder.
- Define live model version file.
- Define live prediction output.
- Define live promotion requirements.
- Prevent unapproved working/staging changes from affecting live.

### 8B — Staging model

- Define staging model folder.
- Define staging model version file.
- Define staging comparison output.
- Track candidate changes intended for live promotion.
- Require promotion report before live replacement.

### 8C — Working model

- Define working model folder.
- Define experiment naming.
- Allow failed experiments without affecting staging/live.
- Track experiment notes.
- Track removed/rejected ideas.

### 8D — Acceptance gate

- Same packet can be scored by live, staging, and working.
- Outputs remain separate.
- Model version and config are written into every prediction output.

## Phase 9 — Prediction model development

### 9A — Baseline model

- Define first simple baseline after data packets exist.
- Use only proven packet fields.
- Produce game winner probabilities.
- Produce confidence labels.
- Produce no decisions yet unless explicitly separated.

### 9B — Feature weighting

- Define feature groups.
- Define initial weights.
- Track weight changes by version.
- Compare model outputs to baseline.
- Avoid overfitting to single dates.

### 9C — Model evaluation

- Accuracy.
- Calibration.
- Brier score if used.
- Log loss if used.
- Edge versus odds if used.
- Performance by confidence tier.
- Performance by odds range.
- Performance by feature availability level.

### 9D — Acceptance gate

- Model can run score-blind on frozen packets.
- Model output is reproducible.
- Evaluation is separate from prediction generation.

## Phase 10 — Backtesting and promotion gates

### 10A — Backtest packet freezing

- Freeze data packet before prediction.
- Hash packet.
- Store model version.
- Store prediction output before grading.
- Prevent prediction rewrite after final truth is introduced.

### 10B — Grading

- Pull final scores only in grading phase.
- Grade winner predictions.
- Grade probability calibration.
- Grade model confidence tiers.
- Grade against odds only after odds normalization is proven.

### 10C — Promotion requirements

- Reproducibility pass.
- Leakage audit pass.
- Minimum sample size.
- Improvement over live baseline.
- No obvious single-date overfit.
- No unacceptable risk profile once wallets exist.
- Human-readable promotion report.

### 10D — Acceptance gate

- Staging can only replace live after all promotion requirements pass.
- Failed experiments remain documented instead of deleted.

## Phase 11 — Wallet and decision strategy

### 11A — Wallet separation

- Live wallet.
- Staging wallet.
- Working wallet.
- Backtest wallet.
- Actual-day prediction wallet.

### 11B — Decision layer

- Keep prediction confidence separate from decision logic.
- Start with flat-unit evaluation.
- Add staking rules only after prediction model is stable.
- Test moneyline first unless another market is explicitly added later.
- Track no-action decisions.

### 11C — Wallet metrics

- Stake.
- Odds.
- Result.
- Profit/loss.
- ROI.
- Hit rate.
- Closing line value if available.
- Drawdown.
- Decision type.
- Model version.
- Packet version.

### 11D — Acceptance gate

- Wallet can be rebuilt from prediction output, odds file, and final truth.
- Wallet does not require rerunning the model.
- Decision strategy is not promoted until prediction quality is proven.

## Phase 12 — One-command runner

### 12A — Final user workflow

- Run today’s games.
- Run specific date.
- Run multiple dates.
- Build data packet only.
- Predict only.
- Grade existing predictions.
- Run backtest.
- Compare live/staging/working.

### 12B — CLI/interface

- Do not define final CLI arguments until contracts are proven.
- Prove every script interface from help output or source code.
- Add PowerShell entry point after Python contracts are proven.
- Add clear run manifest after each execution.

### 12C — Acceptance gate

- User can run one command.
- Script gathers required data.
- Script builds readable packet.
- Script runs selected model lane.
- Script stores outputs in the correct folders.
- Script can rerun the same dates reproducibly.

## Unknowns / not yet verified

- No source interface has been proven yet for this new project.
- No final schema, CLI, folder contract, or model feature list is locked yet.
- No phase beyond planning/environment setup has passed implementation acceptance gates yet.
