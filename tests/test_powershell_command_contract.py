from mlb_prediction_model.powershell_command_contract import (
    assert_valid_powershell_command_block,
    validate_powershell_command_block,
)

VALID_BLOCK = """$RepoPath=Resolve-Path (Join-Path $HOME \"Desktop\\MLB_Prediction_Model\")
Set-Location $RepoPath
$HadFailure=$false
git status
if($LASTEXITCODE -ne 0){Write-Host \"GIT_STATUS_FAILED\"; $HadFailure=$true}
if($HadFailure){Write-Host \"STEP_STATUS=FAILED_BUT_POWERSHELL_LEFT_OPEN\"} else {Write-Host \"STEP_STATUS=PASS\"}
"""


def test_valid_block_passes() -> None:
    assert validate_powershell_command_block(VALID_BLOCK) == ()
    assert_valid_powershell_command_block(VALID_BLOCK)


def test_wrong_repository_variable_fails() -> None:
    command = VALID_BLOCK.replace("$RepoPath=Resolve-Path", "$RepoRoot=Resolve-Path", 1)
    errors = validate_powershell_command_block(command)
    assert any("mandatory RepoPath" in error for error in errors)
    assert any("RepoRoot is prohibited" in error for error in errors)


def test_leading_clear_command_fails() -> None:
    command = "cls\n" + VALID_BLOCK
    errors = validate_powershell_command_block(command)
    assert any("first line" in error for error in errors)
    assert any("second line" in error for error in errors)


def test_markdown_backticks_in_string_fail() -> None:
    command = VALID_BLOCK.replace(
        'git status',
        'Write-Host "limited-use `FALLBACK`"\ngit status',
    )
    errors = validate_powershell_command_block(command)
    assert any("backtick characters are prohibited" in error for error in errors)


def test_line_continuation_backtick_fails() -> None:
    command = VALID_BLOCK.replace("git status", "git status `")
    errors = validate_powershell_command_block(command)
    assert any("backtick characters are prohibited" in error for error in errors)


def test_here_string_fails() -> None:
    command = VALID_BLOCK.replace("git status", '$Text=@"\nvalue\n"@\ngit status')
    errors = validate_powershell_command_block(command)
    assert any("here-string tokens are prohibited" in error for error in errors)


def test_exit_fails() -> None:
    command = VALID_BLOCK.replace("git status", "exit 1\ngit status")
    errors = validate_powershell_command_block(command)
    assert any("exit commands are prohibited" in error for error in errors)


def test_cd_fails() -> None:
    command = VALID_BLOCK.replace("git status", "cd .\ngit status")
    errors = validate_powershell_command_block(command)
    assert any("cd is prohibited" in error for error in errors)


def test_plain_git_pull_fails() -> None:
    command = VALID_BLOCK.replace("git status", "git pull\ngit status")
    errors = validate_powershell_command_block(command)
    assert any("git pull must include --ff-only" in error for error in errors)


def test_fast_forward_only_pull_passes() -> None:
    command = VALID_BLOCK.replace("git status", "git pull --ff-only\ngit status")
    assert validate_powershell_command_block(command) == ()


def test_missing_failure_flag_fails() -> None:
    command = VALID_BLOCK.replace("$HadFailure=$false\n", "")
    errors = validate_powershell_command_block(command)
    assert any("initialize $HadFailure=$false" in error for error in errors)


def test_stale_last_exit_code_check_fails() -> None:
    command = VALID_BLOCK.replace(
        "git status\nif($LASTEXITCODE -ne 0)",
        'git status\nWrite-Host "status read"\nif($LASTEXITCODE -ne 0)',
    )
    errors = validate_powershell_command_block(command)
    assert any("immediately preceding native executable" in error for error in errors)


def test_native_assignment_before_last_exit_code_passes() -> None:
    command = VALID_BLOCK.replace(
        "git status\nif($LASTEXITCODE -ne 0)",
        "$CurrentBranch=git branch --show-current\nif($LASTEXITCODE -ne 0)",
    )
    assert validate_powershell_command_block(command) == ()


def test_guarded_native_command_with_same_line_check_passes() -> None:
    command = VALID_BLOCK.replace(
        'git status\nif($LASTEXITCODE -ne 0){Write-Host "GIT_STATUS_FAILED"; $HadFailure=$true}',
        'if(!$HadFailure){git status; if($LASTEXITCODE -ne 0){Write-Host "GIT_STATUS_FAILED"; $HadFailure=$true}}',
    )
    assert validate_powershell_command_block(command) == ()


def test_multiline_construct_opening_fails() -> None:
    command = VALID_BLOCK.replace("git status", "$Values=@(\ngit status")
    errors = validate_powershell_command_block(command)
    assert any("opens a PowerShell multiline construct" in error for error in errors)
