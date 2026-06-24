
---

# `docs/verification_contract.md`

```markdown
# Verification Contract

This project must follow a strict verification-first workflow.

Guessing, making things up, hallucinating, assuming unverified schemas, skipping fact-checks, or giving code without double-checking is unacceptable.

## Core response structure

Every substantive project response should separate information into:

1. Proven facts
2. Unknowns / not yet verified
3. Safe next action

## Strict rules

### 1. No inferred contracts

Do not infer a file schema, function signature, CLI argument, expected column list, validator rule, or workflow contract unless it has been verified from an actual source of truth.

Accepted sources of truth include:

- source code;
- script help output;
- logs;
- summary JSON;
- manifest JSON;
- file headers;
- raw API response samples;
- accepted prior artifacts;
- user-provided terminal output.

### 2. Prove interfaces before executable code

Before giving executable code, prove the interface being used.

The proof must summarize or cite the exact source of truth, such as:

- script help output;
- source code;
- log output;
- file headers;
- summary JSON;
- accepted artifact.

### 3. Unknowns must stay unknown

If something is unknown, do not fill the gap with a guess.

Use direct language such as:

- `I don't know yet.`
- `Not proven yet.`
- `The interface is not verified yet.`
- `The schema is not locked yet.`

Then give a read-only audit or diagnostic step to determine the answer.

### 4. Read-only audits before patches

When a command fails, do not patch only the first visible error.

First inspect the relevant code path and downstream contracts, including:

- caller;
- callee;
- validators;
- output file names;
- required columns;
- expected artifacts;
- manifests;
- downstream readers;
- likely next blockers.

### 5. Avoid large wrappers before contracts are proven

Do not provide large wrapper scripts until the relevant contracts are proven.

Prefer small read-only audits first.

### 6. Do not claim pass unless every acceptance gate passes

A step may only be called `PASS` if every required acceptance gate passed.

If only part of a step passed, state exactly what passed and exactly what failed.

### 7. Confidence ratings are mandatory

For main claims, include a confidence rating:

- High
- Medium
- Low

If confidence is not High, explain exactly what remains uncertain.

### 8. Correct violations immediately

If the verification contract is violated, acknowledge it directly and correct course with a verification-first step.

### 9. Online research for algorithms and methods

Before choosing or building any data-gathering, feature-engineering, prediction, analysis, validation, or optimization approach, check online for existing algorithms, methods, libraries, public workflows, research, or best practices that may help.

Do not rely only on memory when current or niche methods may exist.

### 10. Code optimization before delivery

Before giving executable code, review it for:

- correctness;
- maintainability;
- simplicity;
- practical optimization;
- avoidable inefficiency;
- downstream compatibility with proven contracts.

Optimized does not mean overcomplicated. It means the code should be the best practical version for the proven contract and current phase.

### 11. Quality over speed

Time to answer does not matter.

The priority order is:

1. find the right information;
2. fact-check it;
3. prove the interfaces;
4. avoid hallucinations;
5. optimize the solution;
6. then present the result.

Fast but unverified work is not acceptable.

## Project-specific score-blind rules

### Prediction input isolation

Prediction packet builders must not read from final-score, grading, result, or wallet-output folders.

### Final truth isolation

Final scores and postgame outcomes may only be introduced during grading.

### Repeatable backtests

The same date should be testable multiple times without relying on remembered outcomes.

The system should use stored raw files, manifests, hashes, and deterministic derived files.

### As-of timing

Pregame data should be gathered or derived according to a configurable as-of cutoff.

The preferred default may be approximately one hour before scheduled first pitch, but the cutoff must be configurable.

### Source selection

No source is automatically canonical.

FanGraphs, Baseball Savant, MLB data, Retrosheet-derived data, odds APIs, weather APIs, and other sources must be evaluated by source capability audits before they are trusted.

## Implementation rules

### Repository cleanliness

Avoid script sprawl.

Do not create repeated files such as:

```text
collector_v1.py
collector_v2.py
collector_final.py
collector_fixed.py
