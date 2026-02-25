# SUCCESS_CRITERIA: SENTRY CI VALIDATOR

## 🎯 GOAL
Create a universal validation script (`sentry_check.sh`) that allows the Sentry agent to programmatically verify the health of any repository (Django, Go, or Vue) before issuing an audit report.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **Stack Detection**: Automatically identify the repository type (Django, Go/Vue) based on local files.
- **Linting Phase**: Run the project's preferred linter (e.g., `ruff` or `flake8` for Python, `eslint` for Vue/TS).
- **Testing Phase**: Run the project's test suite (e.g., `pytest`, `go test`, or `vitest`).
- **Binary Signal**: Output a clear `VALIDATION PASSED` or `VALIDATION FAILED` message at the end of the run.
- **Surgical Reporting**: If a failure occurs, output only the relevant error lines (tracebacks/lint errors) to avoid context bloat.

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **Non-Interactive**: Must run with flags that prevent hanging (e.g., no "watch" modes).
- **Environment Aware**: Use `venv/bin/python` if it exists for Python projects to ensure correct dependency usage.
- **Performance**: Should timeout if a test suite hangs for more than 5 minutes.
- **Exit Codes**: Must return non-zero exit codes on any failure.

## ✅ VERIFICATION (Sentry)
- The tool is successful if the Sentry can call `./sentry_check.sh` in the `member` repository and receive a report on whether the current state passes the local test suite.
