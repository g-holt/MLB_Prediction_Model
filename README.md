# MLB Prediction Model

This repository is for building a reproducible, score-blind MLB data collection, prediction, backtesting, and evaluation project.

The project uses verification-first, dependency-ordered development. A source or component is not accepted for downstream use until its interfaces, source behavior, leakage boundaries, and acceptance gates are proven from actual artifacts.

## Project goal

Build a system where the user can run a script for one date, multiple dates, or today's games, and the system will gather relevant MLB game context into a clean, auditable packet.

The packet should eventually support:

- historical data gathering;
- configurable as-of timing for pregame data;
- score-blind prediction runs;
- repeatable backtests;
- live, staging, and working model lanes;
- model comparison;
- wallet and betting evaluation after the data and prediction layers are stable.

## Current project order

1. Governance, packaging, Git workflow, and repository structure.
2. Data architecture, time semantics, score-blind storage, and reproducibility.
3. Date handling, schedule, and canonical game identity.
4. Source-specific audits and raw collection.
5. Pregame-safe feature and packet building.
6. Prediction model development.
7. Backtesting and model comparison.
8. Operationalization.
9. Betting and wallet strategy.

Each phase ends with an acceptance gate and roadmap review. If a new prerequisite appears, it must be inserted at the earliest correct position before downstream work continues.

Betting and wallet logic must come last. Prediction quality and data integrity must be proven first.

## Model lanes

The project will eventually maintain three separate model lanes.

### Live model

The live model is the stable model used for actual current-day prediction runs once the system is ready.

### Staging model

The staging model is where accepted candidate changes are tested before being promoted to live.

### Working model

The working model is where experimental changes are tested. Failed experiments are expected here and should not affect staging or live.

## Score-blind rule

Prediction packets must not include final scores, grading results, postgame win/loss labels, or any data that would not have been available under the configured pregame cutoff.

Final truth must be isolated from prediction inputs and introduced only during the grading phase.

## Configurable as-of timing

The preferred default as-of cutoff may be approximately one hour before scheduled first pitch, but this is not a hard rule.

The cutoff should be configurable so that different odds and pregame-data timing assumptions can be tested.

Examples of future cutoff settings may include:

- morning of game day;
- three hours before game time;
- one hour before game time;
- thirty minutes before game time;
- closest available pregame snapshot;
- closing-line-adjacent snapshot.

These are planning examples only. Final CLI arguments and config schema are not locked yet.

## Source-proof-first approach

The project should not be FanGraphs-first, Baseball Savant-first, or any other source-first system.

For each data category, the selected source should be the one that is most:

1. historically reproducible;
2. timestamp-safe or derivable only from prior games;
3. stable enough to script;
4. auditable from raw files;
5. free from final-score leakage;
6. easy to rerun for the same dates.

FanGraphs is allowed as a candidate source because the user has membership access, but it is not automatically canonical.

Baseball Savant, MLB data, Retrosheet-derived data, odds APIs, weather APIs, or other sources may be preferred if they are more reliable and auditable for a specific data category.

## Repository strategy

The repository should avoid copied script iterations such as:

```text
collector_v1.py
collector_v2.py
collector_final.py
collector_final_fixed.py
```

Instead, code history should live in Git commits and pull requests.

Run outputs should live in organized run folders and manifests, not in copied script folders.

## Current status

Phase 0 foundation work is active.

The MLB Stats API schedule endpoint and canonical game IDs are accepted only as a limited-use `FALLBACK` for forward-captured pre-cutoff snapshots or deterministic replay of those snapshots. This accepted vertical slice includes score-blind filtering, snapshot manifests, payload hashing, canonical identity reconstruction, fallback validation, and tests.

The schedule endpoint is not `PROVEN_SAFE`. Its accepted scope excludes probable pitchers, lineups, scores, packet schema, and every other unaudited model input.

Packaging, Git workflow, repository structure, and the broader data architecture remain open and must be completed before another production source collector is implemented.

No feature packet, prediction model, backtest promotion workflow, operational runner, or wallet contract is accepted yet.

See:

- `docs/verification_contract.md`
- `docs/assistant_operating_contract.md`
- `docs/project_list.md`
- `docs/source_capability_matrix.md`
