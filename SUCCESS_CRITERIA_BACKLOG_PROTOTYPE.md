# SUCCESS_CRITERIA: Backlog API Connector (Prototype)

## 1. Connectivity (Functional)
- [ ] Successfully fetch a list of issues from the Backlog API using the environment variables (`BACKLOG_API_KEY`, `BACKLOG_SPACE_ID`).
- [ ] Implement a basic `LoadBalancer` class that can query "In Progress" and "To Do" issues for a specific project.

## 2. Load Calculation (Technical)
- [ ] Sum the `estimatedHours` from all fetched issues.
- [ ] Correctly handle `None` values for estimated hours (treat as 0 or a small default).

## 3. Implementation (Style)
- [ ] Create a standalone test script `test_backlog_connection.py` to verify the logic.
- [ ] Follow existing Python patterns in the `personal-agents` directory.
