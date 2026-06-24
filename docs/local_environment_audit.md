# Local Environment Audit

Date: 2026-06-24
Host OS context: Windows PowerShell
Repository path proven from terminal output: `C:\Users\gholt\Desktop\MLB_Prediction_Model`

## Proven local repository state

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Repository directory contents proven from terminal output:

```text
.git
docs
.gitignore
README.md
```

The accidental local `doc` folder was checked from the repository folder and was not found.

## Proven tool versions

```text
Python: 3.14.6
py launcher: Python 3.14.6, 64-bit
Git: 2.40.1.windows.1
uv: 0.11.23 (3cdf50e09 2026-06-19 x86_64-pc-windows-msvc)
PowerShell: 5.1.26100.8655
WinGet: v1.28.240
```

## Proven execution policy output

```text
MachinePolicy: Undefined
UserPolicy: Undefined
Process: Undefined
CurrentUser: Undefined
LocalMachine: Undefined
```

## Python 3.14 dependency compatibility audit

Audit folder proven from terminal output:

```text
C:\Users\gholt\Desktop\mlb_pred_env_audit_20260624
```

Virtual environment creation command proved successful:

```text
uv venv --python 3.14 .venv
```

The venv used CPython 3.14.6:

```text
Using CPython 3.14.6 interpreter at: C:\Users\gholt\AppData\Local\Python\pythoncore-3.14-64\python.exe
Creating virtual environment at: .venv
```

The starter dependency set installed successfully through `uv pip install`:

```text
pytest
ruff
requests
httpx
pydantic
pandas
polars
duckdb
pyarrow
beautifulsoup4
lxml
rich
typer
```

Installed versions proven from terminal output:

```text
beautifulsoup4==4.15.0
duckdb==1.5.4
httpx==0.28.1
lxml==6.1.1
pandas==3.0.3
polars==1.42.0
pyarrow==24.0.0
pydantic==2.13.4
pytest==9.1.1
requests==2.34.2
rich==15.0.0
ruff==0.15.19
typer==0.26.7
```

The import smoke test passed for every requested package:

```text
OK pytest: 9.1.1
OK ruff: VERSION_NOT_EXPOSED
OK requests: 2.34.2
OK httpx: 0.28.1
OK pydantic: 2.13.4
OK pandas: 3.0.3
OK polars: 1.42.0
OK duckdb: 1.5.4
OK pyarrow: 24.0.0
OK beautifulsoup4: 4.15.0
OK lxml: 6.1.1
OK rich: VERSION_NOT_EXPOSED
OK typer: 0.26.7

ALL_IMPORTS_OK
```

Dependency consistency check passed:

```text
Checked 39 packages in 2ms
All installed packages are compatible
```

## Notes

- Python is installed and callable.
- Git is installed and callable.
- uv was initially not recognized, then installed through WinGet and verified after restarting PowerShell.
- The local clone is clean and tracking `origin/main`.
- Python 3.14.6 passed a starter dependency compatibility audit for the current proposed stack.
- This audit proves installation/import compatibility only. It does not yet prove runtime performance, API-source behavior, file schemas, CLI contracts, or data-source correctness.

## Current status

Phase 0E local environment audit is complete for basic tool availability and starter dependency compatibility.

Completed:

- Verify local Python version.
- Verify local Git version.
- Verify local uv availability.
- Verify PowerShell version.
- Verify PowerShell execution policy.
- Verify local repository clone path.
- Verify working tree is clean.
- Verify accidental local `doc` folder is absent.
- Verify Python 3.14 starter dependency install compatibility.
- Verify starter dependency import compatibility.
- Verify `uv pip check` compatibility.

Not yet locked:

- Exact dependency pinning policy.
- Project package/module layout.
- Branch/PR workflow rules.
- Source-specific data contracts.
