# SUCCESS_CRITERIA: Date-Filtered Live Sync

## 1. Filter Implementation (Technical)
- [ ] **Date Parsing**: Correctly parse the `date` string from the Google Sheet (e.g., "2026/03/02").
- [ ] **Boundary Enforcement**: Exclude any task with a report date earlier than 2026-03-02.
- [ ] **Tab Discovery**: Check if tasks for March are in the current `2602` tab or a new `2603` tab.

## 2. Live Execution (Functional)
- [ ] **No Mutations Before Filter**: Ensure the filter is applied *before* any Backlog API calls are made.
- [ ] **Sequential Sync**: Process all valid tasks from March 2nd onwards in order.

## 3. Reporting (Style)
- [ ] Log the specific count of tasks skipped due to the date filter.
