# SUCCESS_CRITERIA: Dynamic Real-Time Scheduling

## 1. Timeline Initialization (Technical)
- [ ] **Default to Today**: The `DeveloperTimeline` must default to the current system date (`datetime.now()`) if no override is provided.
- [ ] **Environment Override**: Support an environment variable `SYNC_START_DATE` to allow manual shifting of the timeline without changing code.

## 2. Load Awareness (Functional)
- [ ] **Continuous Pre-fill**: For every run, the system must fetch current active load from Backlog to ensure new assignments don't conflict with work already in progress.
- [ ] **7-Day Window**: Maintain the "Freshness Filter" (last 7 days) to ignore zombie tasks.

## 3. Deployment Safety (Ops)
- [ ] Ensure the GitHub Actions workflow does not have a hard-coded date, allowing it to naturally progress with the calendar.
