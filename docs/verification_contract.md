# Verification Contract

This project follows a verification-first workflow.

Guessing, making up schemas, assuming unverified interfaces, skipping fact-checks, or giving executable code without checking contracts is not acceptable.

## Required response structure

Substantive project responses should separate information into:

1. Proven facts
2. Unknowns / not yet verified
3. Safe next action

## Strict rules

### 1. No inferred contracts

Do not infer a file schema, function signature, command-line argument, expected column list, validator rule, or workflow contract unless it has been verified from an actual source of truth.

Accepted sources of truth include source code, help output, logs, summary JSON, manifest JSON, file headers, raw API responses, accepted artifacts, and user-provided terminal output.

### 2. Prove interfaces before executable code

Before giving executable code, prove the interface being used from a real source of truth.

### 3. Unknowns must stay unknown

If something is unknown, say it is not proven yet and give a read-only audit or diagnostic step to determine it.

### 4. Read-only audits before patches

When a command fails, inspect the relevant code path and downstream contracts before patching.

### 5. Avoid large wrappers before contracts are proven

Do not provide large wrapper scripts until the relevant contracts are proven.

### 6. Do not claim pass unless every gate passes

A step may only be called PASS if every required acceptance gate passed.

### 7. Confidence ratings are mandatory

For main claims, include a confidence rating of High, Medium, or Low, and explain uncertainty when confidence is not High.

### 8. Correct violations immediately

If the verification contract is violated, acknowledge it and correct course with a verification-first step.

### 9. Online method research

Before choosing or building any data-gathering, feature-engineering, prediction, validation, analysis, or optimization approach, check online for existing methods, libraries, public workflows, research, or best practices that may help.

### 10. Code optimization before delivery

Before giving executable code, review it for correctness, maintainability, simplicity, practical optimization, avoidable inefficiency, and downstream compatibility with proven contracts.

### 11. Quality over speed

Time to answer is less important than finding the right information, fact-checking it, proving interfaces, avoiding hallucinations, and optimizing the solution.

## Project-specific isolation rules

Prediction input builders must not read from final-result, grading, or later-evaluation folders.

Final truth may only be introduced during the grading/evaluation phase.

The same date should be testable multiple times using stored raw files, manifests, hashes, and deterministic derived files.

Pregame data should be gathered or derived according to a configurable as-of cutoff.

No source is automatically canonical. Each source must pass a source capability audit before it is trusted.

## Repository cleanliness

Avoid copied script iterations. Use Git history, branches, and pull requests instead.

Run outputs should be stored by run ID, manifest, and configured date set.

Do not commit secrets, API keys, tokens, browser sessions, local credentials, or large private data outputs.

## Current implementation status

Some Phase 0C implementation helpers are accepted on `main` only after passing tests, ruff, pull request review, and merge verification.

Accepted helper code does not by itself prove production source status, packet schema, command-line arguments, model features, or betting/wallet behavior.

Schemas, command-line arguments, package layout, model features, and source production status remain unaccepted unless an active contract or source matrix row says otherwise.

## Assistant operating contract

Before answering project-control requests, the assistant must check docs/assistant_operating_contract.md and the relevant project document instead of relying on memory.

Project-control requests include List, next step, current phase, status, command blocks, PRs, source status, acceptance gates, workflow order, and project constraints.

If the assistant cannot check the required file, it must say so and must not proceed as if it verified the answer.
