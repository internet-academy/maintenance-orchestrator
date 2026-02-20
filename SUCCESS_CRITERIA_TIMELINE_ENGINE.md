# SUCCESS_CRITERIA: Timeline-Based Resource Leveling

## 1. Timeline Engine (Technical)
- [ ] **Capacity Model**: Each developer has a `Timeline` representing 14 consecutive days.
- [ ] **Weekend Exclusion**: The engine must identify and skip Saturdays and Sundays when calculating dates.
- [ ] **Pre-fill Logic**: Existing Backlog tasks (Open/In Progress) must be consumed first, filling buckets from Day 1 onwards.

## 2. Assignment Algorithm (Functional)
- [ ] **Sequential Pouriing**: New task hours must flow into the first available space in the timeline.
- [ ] **DueDate Calculation**: The system must return the specific date of the day the task is completed.
- [ ] **Manager Trigger**: "Manager Overflow" should only trigger if the Core Team's **Day 1** (Today) is entirely full.

## 3. Transparency & Logging (Style)
- [ ] **Timeline Visualization**: Print a simple text-based "capacity map" at the start of the run.
- [ ] **Assignment Details**: Log which days a task was split across (e.g., "Task 4: Day 1 (2h), Day 2 (1h)").
