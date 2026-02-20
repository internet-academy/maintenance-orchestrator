# SUCCESS_CRITERIA: Copy-Paste Resilient Deduplication

## 1. Ownership Verification (Technical)
- [ ] **Remote-Link Validation**: When an existing Backlog ID is found in a row, the system must fetch that issue from the Backlog API.
- [ ] **Cross-Check**: The "Sheet Link" stored in the Backlog description must be extracted and compared against the *current* row's deep-link.
- [ ] **Collision Detection**: If the links do not match (i.e., the ID was copied from another row), the system must flag it as a "Collision."

## 2. Automatic Rectification (Functional)
- [ ] **Reset & Re-create**: If a collision is detected, the system must ignore the copied ID, treat the row as a NEW task, and overwrite the copied ID in the Sheet with a fresh Backlog Issue Key.
- [ ] **Safety Notification**: Log a warning: "Detected copied ID {ID} in Row {Row}. Creating a fresh issue to prevent overwriting."

## 3. Performance (Ops)
- [ ] **Targeted Checks**: Only perform the remote fetch if a `backlog_id` is present in the sheet (optimizing API calls).
