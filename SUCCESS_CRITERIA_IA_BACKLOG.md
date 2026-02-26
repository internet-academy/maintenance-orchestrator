# SUCCESS_CRITERIA: Requester Parent Automation (◆リクエラ)

## 1. Parent Task Lifecycle (Technical)
- [x] **End-of-Month Calculation**: Implement logic to determine the last day of the month for any given `dueDate`.
- [x] **Naming Standard**: Parent tasks must follow the format `◆リクエラ(YYYY/M/D)` (Note: Spreadsheet uses single-digit M/D).
- [x] **Memoized Lookup**: Use `find_issue_by_summary` in `LoadBalancer` to locate existing parents.
- [x] **Auto-Provisioning**: If the monthly parent does not exist, the system must create it as a top-level task before assigning sub-tasks.

## 2. Hierarchical Integration (Functional)
- [x] **Sub-Task Linking**: Every error report sub-task created must include the `parentIssueId` of its corresponding monthly parent.
- [x] **Spillover Handling**: Tasks assigned to March must automatically land under the March parent, even if the run happens in February.

## 3. Verification (Ops)
- [x] **Dry Run Trace**: Log: "HIERARCHY: Task X linked to parent '◆リクエラ(YYYY/M/D)' (ID: Y)".
- [x] **Sentry Check**: Ensure parent tasks are created with appropriate priority and category (MD_SD Project: Bug type, Normal Priority).
