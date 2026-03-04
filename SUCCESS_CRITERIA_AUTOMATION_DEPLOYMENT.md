# SUCCESS_CRITERIA: Full Autonomy Deployment

## 1. Automation Host (Technical)
- [x] **Continuous Execution**: Choose a host for the background process:
    - **GitHub Actions**: Preferred for lightweight scheduling.
    - **Local systemd**: Currently available on this Linux machine.
- [ ] **Systemd Configuration**: Create `/etc/systemd/system/gemini-orchestrator.service` to run `python3 orchestrator.py` every 10 minutes.

## 2. Bidirectional Sync (Functional)
- [x] **GitHub -> Sheet**: `GitSync` must pull Status, Assignee, and Dates from GitHub ProjectV2 and write them back to the Sheet.
- [x] **Sub-issue Requirement**: Automatically create a 20-minute "Understand the request" sub-issue for every new report.
- [x] **State Trigger**: Sheet status must remain "Open" until the GitHub status is explicitly moved to "In Progress".

## 3. Monitoring & Resilience (Ops)
- [ ] **Logging**: Pipe output to `logs/automation.log` with timestamps.
- [ ] **Error Handling**: Implement 3-strike retry logic for Sheet/GitHub API timeouts.
- [ ] **Credential Protection**: Ensure `.env` is securely managed in the production host.
