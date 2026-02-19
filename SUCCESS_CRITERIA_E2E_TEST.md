# SUCCESS_CRITERIA: E2E Flow Test & Update Detection

## 1. End-to-End Connectivity (Functional)
- [ ] **Ingestion**: Successfully read a test row from the "Task List" Google Sheet.
- [ ] **Processing**: The Orchestrator correctly identifies the test row as "New".
- [ ] **Execution**: A new issue is created in Backlog project `MD_SD`.
- [ ] **Feedback**: The Backlog Issue Key is written back to the Google Sheet in a dedicated "Backlog ID" column.

## 2. Update Detection Logic (Technical)
- [ ] **Change Identification**: The system must detect if a row with an existing "Backlog ID" has modified data (e.g., changed `estimated_hours`).
- [ ] **API Patching**: Use the Backlog `PATCH /api/v2/issues/{issueIdOrKey}` endpoint to update the existing issue instead of creating a new one.
- [ ] **Integrity**: Ensure that updating a row does not accidentally clear other fields in Backlog.

## 3. Verification & Safety (Style/Audit)
- [ ] **Dry Run Mode**: Implement a flag to simulate the sync without making actual API calls.
- [ ] **Logging**: Detailed logs showing "CREATED Issue X" vs "UPDATED Issue Y".
