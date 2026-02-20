# SUCCESS_CRITERIA: Time-Gated Daily Reporting

## 1. Scheduling (Technical)
- [ ] **State-Based Suppression**: Store the `last_report_date` in `sync_state.json`.
- [ ] **Hour Gating**: Only allow the report to trigger during a specific hour (Default: 9 AM).
- [ ] **Timezone Awareness**: Provide an environment variable `REPORT_HOUR` to allow the user to align with their local time (JST vs UTC).

## 2. Robustness (Functional)
- [ ] **Exactly Once**: Ensure that even with 20-minute runs, the report is only sent **once** during the 9 AM hour.
- [ ] **Continuous Sync**: Confirm that task creation and status updates still occur every 20 minutes regardless of the report status.

## 3. Verification (Ops)
- [ ] **Logic Test**: Verify that the report is skipped if the current hour does not match the target.
- [ ] **State Check**: Confirm that `sync_state.json` correctly records the date after a successful report.
