# SUCCESS_CRITERIA: Requester Parent Automation (◆リクエラ)

## 1. Parent Task Lifecycle (Technical)
- [ ] **End-of-Month Calculation**: Implement logic to determine the last day of the month for any given `dueDate`.
- [ ] **Naming Standard**: Parent tasks must follow the format `◆リクエラ(YYYY/MM/DD)` (e.g., `◆リクエラ(2026/02/28)`).
- [ ] **Memoized Lookup**: Use `find_issue_by_summary` in `LoadBalancer` to locate existing parents.
- [ ] **Auto-Provisioning**: If the monthly parent does not exist, the system must create it as a top-level task before assigning sub-tasks.

## 2. Hierarchical Integration (Functional)
- [ ] **Sub-Task Linking**: Every error report sub-task created must include the `parentIssueId` of its corresponding monthly parent.
- [ ] **Spillover Handling**: Tasks assigned to March must automatically land under the March parent, even if the run happens in February.

## 3. Verification (Ops)
- [ ] **Dry Run Trace**: Log: "HIERARCHY: Task X linked to parent '◆リクエラ(YYYY/MM/DD)' (ID: Y)".
- [ ] **Sentry Check**: Ensure parent tasks are created with appropriate priority and category (if any).
