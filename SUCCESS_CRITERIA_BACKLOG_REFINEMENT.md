# SUCCESS_CRITERIA: Backlog Logic Refinement & Stability

## 1. Rescheduling & Deadline Stability (Technical)
- [ ] **Preserve Existing Deadlines**: The `dueDate` of an existing Backlog ticket MUST NOT be changed during an update unless the `estimated_hours` in the sheet has changed.
- [ ] **Prevent Double Counting**: The `DeveloperTimeline` MUST NOT be filled with hours from existing tickets during the sync loop, as these are already accounted for in the initial workload fetch.
- [ ] **Surgical Updates**: Only update fields in Backlog that have actually changed (e.g., if only the status changed, do not push a new description).

## 2. Hash Integrity & Sync Granularity (Functional)
- [ ] **Stabilize Change Detection**: Improve `_get_task_hash` to be resilient to whitespace-only changes and non-content metadata.
- [ ] **Robuster Capture**: `CloudIngestor` must strictly distinguish between Japanese content and English fallback translation to prevent hash "flapping."
- [ ] **AI Non-Determinism Guard**: If a ticket description is being updated, prefer the existing English translation if it's already "AI-polished" to avoid minor wording fluctuations.

## 3. GitHub Integration (Logic)
- [ ] **Stateful PR Scanning**: Track the last scanned PR timestamp/ID to avoid re-processing old PRs on every run.
- [ ] **Commit Message Support**: Scan commit messages (not just PR titles) for issue keys (e.g., `fixes MD_SD-123`).

## 4. Verification (Ops)
- [ ] **Dry Run Validation**: Verify that running the orchestrator twice on an unchanged sheet results in 0 updates.
- [ ] **Load Consistency**: Confirm that `DeveloperTimeline` usage remains constant across multiple runs for existing tasks.
