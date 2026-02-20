# SUCCESS_CRITERIA: Multi-Day Workload Distribution

## 1. Daily Load Logic (Technical)
- [ ] **Duration-Based Division**: If a task has a Start Date and a Deadline, the system should calculate `Daily_Load = Total_Estimate / Working_Days`.
- [ ] **Default Behavior**: If no duration is provided, assume the `Estimated Hours` apply to the current day (preserving existing safety).
- [ ] **Backlog Integration**: Extract `startDate` and `dueDate` from the Backlog API response to calculate current task durations.

## 2. Capacity Accuracy (Functional)
- [ ] **Dynamic Load Calculation**: Ensure that a 20-hour task spanning 5 days only counts as 4 hours toward today's 6-hour limit.
- [ ] **Weekend Awareness**: (Optional/Preferred) Exclude non-working days from the duration divisor.

## 3. Transparency (Style)
- [ ] The Load Report must show both the "Total Remaining" and the "Today's Contribution" for multi-day tasks.
