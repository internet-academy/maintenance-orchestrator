# SUCCESS_CRITERIA: GitHub Workflow Path Correction

## 1. Path Alignment (Technical)
- [ ] **Dependency Fix**: Update the `pip install` command to use `requirements.txt` instead of `personal-agents/requirements.txt`.
- [ ] **Execution Fix**: Ensure the `python orchestrator.py` command is executed from the root where the script resides.

## 2. Environment Verification (Ops)
- [ ] **Workflow Validation**: The GitHub Action must successfully complete the "Install Dependencies" step on the next run.
