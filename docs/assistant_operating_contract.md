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
- no line-continuation backticks;
- no here-strings;
- no exit commands unless explicitly requested;
- banner only inside the code block;
- prove facts from repo, docs, logs, or artifacts;
- keep statuses UNPROVEN until acceptance gates pass.
