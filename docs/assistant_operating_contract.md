# Assistant Operating Contract

Status: required project-control behavior.

## Reserved command words

Reserved command words have fixed meanings and must not be reinterpreted.

When the user says "List", always print the current project phases and the tasks within each phase in a clean layout from the active project list. Do not summarize it as next steps. Do not replace it with recommendations. Preserve completed items with strikethrough.

## Project memory guardrail

Do not answer project-control requests from memory.

Before answering any request involving List, next step, current phase, status, command blocks, PRs, source status, acceptance gates, workflow order, or project constraints, first check the active repo documents or the latest verified artifact/log.

If the answer depends on the project roadmap, read docs/project_list.md.
If the answer depends on rules, command style, verification discipline, or reserved terms, read docs/verification_contract.md and this file.
If the answer depends on source status, read docs/source_capability_matrix.md.
If the answer depends on a merged contract, read the relevant file under docs/source_contracts/.

Do not substitute memory, summaries, or assumptions for those files.

If the required file cannot be checked, say so and do not proceed as if it was verified.

If this contract is violated, stop the workflow, acknowledge the exact violated rule, and patch the repo contract before continuing.

## Command block constraints

For code and workflow commands:

- no PowerShell multiline constructs;
- no PowerShell backtick characters anywhere in the delivered block;
- no here-strings;
- no exit commands unless explicitly requested;
- banner only inside the code block;
- prove facts from repo, docs, logs, or artifacts;
- keep statuses UNPROVEN until acceptance gates pass.

The backtick prohibition includes line continuation, escaping, and Markdown-style backticks copied into PowerShell string literals.

### Mandatory repository entry

Every PowerShell command block that operates on this repository must begin with exactly these two lines:

    $RepoPath=Resolve-Path (Join-Path $HOME "Desktop\MLB_Prediction_Model")
    Set-Location $RepoPath

Do not replace RepoPath with another variable name. Do not use cd. Do not prepend cls, prompt text, comments, or any other characters to the first line.

Every repository update must use git pull --ff-only. Plain git pull is not permitted.

LASTEXITCODE may only be checked immediately after a native executable invocation. PowerShell cmdlets and .NET operations must use try/catch or direct state checks instead of relying on LASTEXITCODE.

Before presenting a repository command block, verify literally that its first two lines match the mandatory repository entry above.

## Command delivery self-check

Before presenting a PowerShell command block, validate the exact final text with:

    uv run python -m mlb_prediction_model.powershell_command_contract PATH_TO_UTF8_COMMAND_FILE

Do not present the block unless the validator returns `PASS_POWERSHELL_COMMAND_CONTRACT` with exit code zero.

The validator must enforce the exact repository entry, the RepoPath variable, the absence of cd, all PowerShell backtick characters, here-strings, exit commands, plain git pull, PowerShell multiline openings, stale LASTEXITCODE checks, and the required HadFailure initialization.

If the validator is unavailable, failing, or does not cover a newly discovered command-delivery failure, do not present another workflow block. Patch the validator and its tests first.

When a generated script body is required, write it through a repository file, a compact Python command, or another contract-compliant method instead of embedding a PowerShell here-string.

If a proposed command violates these constraints, do not present it; rewrite and revalidate it first.
