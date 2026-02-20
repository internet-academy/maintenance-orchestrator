# SUCCESS_CRITERIA: Reverse Status Synchronization

## 1. Status Mapping (Technical)
- [ ] **Backlog to Sheet Mapping**: Map Backlog status names to spreadsheet-friendly terms:
    - `Open` -> `Open`
    - `In Progress` -> `In Progress`
    - `Resolved` -> `Resolved`
    - `Closed` -> `Complete!` (or equivalent)
- [ ] **Location Discovery**: Implement logic to find the "Status" value cell within each task block (currently observed at `offset 9`, `Column K`).

## 2. Bidirectional Awareness (Functional)
- [ ] **Selective Updates**: Only update the spreadsheet if the Backlog status has changed to minimize API calls and avoid "flapping."
- [ ] **Existing Task Logic**: During the `UPDATE` flow in `Orchestrator`, fetch the latest status from the Backlog issue object.

## 3. Execution (Ops)
- [ ] **Test Run**: Perform a dry run where status changes are detected and "would be" written to the sheet.
- [ ] **Live Run**: Successfully update the "System Development" section status for at least one task.
