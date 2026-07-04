"""Static validation for repository PowerShell command blocks."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FIRST_LINE = '$RepoPath=Resolve-Path (Join-Path $HOME "Desktop\\MLB_Prediction_Model")'
REQUIRED_SECOND_LINE = "Set-Location $RepoPath"

_NATIVE_COMMAND_PATTERN = re.compile(
    r"(?:^|[=;(])\s*(?:git|gh|uv|python|python3|py|pwsh|powershell|cmd|dotnet)\b",
    re.IGNORECASE,
)
_PLAIN_GIT_PULL_PATTERN = re.compile(
    r"(?:^|[;{])\s*git\s+pull(?!\s+--ff-only(?:\s|;|$))",
    re.IGNORECASE,
)
_CD_PATTERN = re.compile(r"(?:^|[;{])\s*cd(?:\s|;|$)", re.IGNORECASE)
_EXIT_PATTERN = re.compile(r"(?:^|[;{])\s*exit(?:\s|;|$)", re.IGNORECASE)


def _previous_nonempty_line(lines: list[str], index: int) -> str:
    for previous_index in range(index - 1, -1, -1):
        if lines[previous_index].strip():
            return lines[previous_index]
    return ""


def _has_native_invocation_before_check(line: str) -> bool:
    before_check = line.split("$LASTEXITCODE", maxsplit=1)[0]
    return _NATIVE_COMMAND_PATTERN.search(before_check) is not None


def validate_powershell_command_block(command_text: str) -> tuple[str, ...]:
    """Return contract violations found in a repository PowerShell command block."""

    errors: list[str] = []
    lines = command_text.splitlines()

    if len(lines) < 2:
        errors.append("command block must contain at least the two mandatory repository-entry lines")
    else:
        if lines[0] != REQUIRED_FIRST_LINE:
            errors.append("first line does not exactly match the mandatory RepoPath assignment")
        if lines[1] != REQUIRED_SECOND_LINE:
            errors.append("second line does not exactly match the mandatory Set-Location command")

    if "`" in command_text:
        errors.append("PowerShell backtick characters are prohibited anywhere in delivered blocks")
    if "$RepoRoot" in command_text:
        errors.append("RepoRoot is prohibited; use the mandatory RepoPath variable")
    if any(token in command_text for token in ('@"', "@'", '"@', "'@")):
        errors.append("PowerShell here-string tokens are prohibited")
    if _CD_PATTERN.search(command_text):
        errors.append("cd is prohibited; use the mandatory Set-Location command")
    if _EXIT_PATTERN.search(command_text):
        errors.append("exit commands are prohibited unless the user explicitly requests one")
    if _PLAIN_GIT_PULL_PATTERN.search(command_text):
        errors.append("git pull must include --ff-only")
    if "$HadFailure=$false" not in command_text:
        errors.append("command block must initialize $HadFailure=$false")

    prohibited_multiline_endings = ("@(", "@{", "{", "(", "|", ",")
    for line_number, line in enumerate(lines, start=1):
        stripped = line.rstrip()
        if stripped.endswith(prohibited_multiline_endings):
            errors.append(
                f"line {line_number} ends with a token that opens a PowerShell multiline construct"
            )

    for index, line in enumerate(lines):
        if "$LASTEXITCODE" not in line:
            continue
        if _has_native_invocation_before_check(line):
            continue
        previous_line = _previous_nonempty_line(lines, index)
        if _NATIVE_COMMAND_PATTERN.search(previous_line) is None:
            errors.append(
                f"line {index + 1} checks $LASTEXITCODE without an immediately preceding "
                "native executable invocation"
            )

    return tuple(errors)


def assert_valid_powershell_command_block(command_text: str) -> None:
    """Raise ValueError when a command block violates the repository contract."""

    errors = validate_powershell_command_block(command_text)
    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"PowerShell command contract violations:\n{joined}")


def main(argv: list[str] | None = None) -> int:
    """Validate a UTF-8 command-block file or standard input."""

    parser = argparse.ArgumentParser(
        description="Validate a repository PowerShell command block before delivery."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="UTF-8 file containing the command block; omit to read standard input.",
    )
    args = parser.parse_args(argv)

    command_text = args.path.read_text(encoding="utf-8") if args.path else sys.stdin.read()
    errors = validate_powershell_command_block(command_text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_POWERSHELL_COMMAND_CONTRACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
