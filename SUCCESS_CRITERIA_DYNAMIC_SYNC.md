# SUCCESS_CRITERIA: Full Change Detection (Stateful Sync)

## 1. Hashing (Technical)
- [ ] **Content Hashing**: Implement a method to generate a SHA-256 hash of the "Task Content" (Japanese + Hours).
- [ ] **Local State Persistence**: Save these hashes in a local `project_states.json` file, mapped by Backlog ID.

## 2. Selective Backlog Updates (Functional)
- [ ] **Change Detection**: Before calling `update_backlog_issue`, compare the current row's hash against the stored hash.
- [ ] **Skip Logic**: If the hashes match, skip the Backlog PATCH request.
- [ ] **Logging**: Log "SKIP: No changes detected for MD_SD-XXXX" to keep the logs clean.

## 3. Execution (Ops)
- [ ] **Clean Run**: Verify that on a second run with no changes, zero Backlog API mutations occur.
