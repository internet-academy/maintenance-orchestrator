# SUCCESS_CRITERIA: GitHub Maintenance Project Integration

## 1. Backlog Decommissioning (Cleanup)
- [ ] **Code Removal**: Delete `LoadBalancer` and all Backlog API dependencies from `orchestrator.py` and `agents/`.
- [ ] **State Migration**: Update `sync_state.json` to use GitHub Issue URLs or numbers as the primary keys for task tracking.
- [ ] **Variable Deprecation**: Mark `BACKLOG_API_KEY` and `BACKLOG_SPACE_ID` as unused in `.env`.

## 2. GitHub Issue & Project Integration (Functional)
- [ ] **Automated Issue Creation**:
    - Repository: `internet-academy/member`.
    - Content: Bilingual (JP/EN) description, Sheet deep-link, and original Task ID.
    - Labels: Automatically apply the `staff-report` label.
- [ ] **Project V2 Assignment**:
    - Automatically add every created GitHub Issue to **Project 4 (Maintenance)** under the `internet-academy` organization.
    - **Technical**: Use GitHub GraphQL API (ProjectV2) to link the Issue to the Project immediately after creation.
- [ ] **Automatic PIC Assignment**:
    - Map the `pic` from the existing `developer_map` (now using GitHub usernames).
    - Assign the GitHub Issue to the calculated developer via the GitHub REST API.

## 3. Scheduling & Sheet Update (Technical)
- [ ] **6-Hour Bucket Calculation**:
    - Retain the capacity tracking logic for developers.
    - Use the PIC's workload (calculated from active GitHub issues in Project 4) to determine the `Start Date` and `End Date`.
- [ ] **Sheet Write-back**:
    - Write the GitHub Issue URL/Number back to the "Backlog ID" column.
    - Update the "PIC" name in the Sheet based on the automated assignment.
    - Write the calculated `Start Date` and `End Date` back to the Google Sheet.

## 4. Reverse Status Sync (GitHub -> Sheet)
- [ ] **Bidirectional Status Mapping**:
    - Issue Open -> "In Progress" (since we assign PIC automatically)
    - Issue Closed / Linked PR Merged -> "Complete!" (Sheet)
- [ ] **Direct Write**: `GitSync` must call `CloudIngestor.write_status` directly when a state change is detected.

## 5. Security & Style
- [ ] **GraphQL Implementation**: Use robust GraphQL queries for ProjectV2 (handling IDs, not just names).
- [ ] **Dry Run Integrity**: Ensure all GitHub mutations (Issue creation, Project adding, Assignments) respect the `DRY_RUN=True` flag.
