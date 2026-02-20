# SUCCESS_CRITERIA: Forward-Scheduled Load Balancing (Bucket Filling)

## 1. Scheduling Logic (Technical)
- [ ] **Capacity Buckets**: Each developer has an array of "Daily Buckets" (e.g., Day 1 = 6h, Day 2 = 6h, etc.).
- [ ] **Serial Assignment**: New tasks must "fill" the first available bucket.
    - [ ] 10h task -> Fills Bucket 1 (6h) and Bucket 2 (4h).
    - [ ] 3h task -> Fills remaining Bucket 2 (2h) and starts Bucket 3 (1h).
- [ ] **Due Date Calculation**: The `dueDate` pushed to Backlog must match the date of the *last bucket* touched by that specific task.

## 2. Temporal Awareness (Functional)
- [ ] **Working Days Only**: The system must skip Saturdays and Sundays when projecting into future buckets.
- [ ] **Current Load Integration**: Before adding new tasks, the buckets must be pre-filled with the developer's *existing* active workload from Backlog.

## 3. Managerial Oversight (Style)
- [ ] The Orchestrator output must show the "Projected Finish Date" for each task assigned.
