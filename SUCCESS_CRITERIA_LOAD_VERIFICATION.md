# SUCCESS_CRITERIA: Multi-Task Load Verification

## 1. Load Calculation (Technical)
- [ ] **State Tracking**: The Orchestrator must maintain a "Projected Load" in memory during a single run to account for tasks *just* assigned but not yet reflected in the API.
- [ ] **Real-time API Check**: Query the current Backlog load for each developer *before* each assignment decision.

## 2. Capacity Enforcement (Functional)
- [ ] **Hard Limit**: No developer should be assigned more than 6.0 total hours (Current + New) in a single cycle.
- [ ] **Redistribution**: If Saurabh reaches 6h, the system must automatically pivot to the next available developer (e.g., Raman, Choo, or Ewan).
- [ ] **Overload Handling**: If no developers have capacity, the tasks must be logged as "PENDING" or "SKIPPED" without being created in Backlog.

## 3. Transparency (Style)
- [ ] Log the running load for each developer as tasks are assigned during the batch process.
