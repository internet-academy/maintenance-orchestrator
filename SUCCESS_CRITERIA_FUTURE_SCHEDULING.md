# SUCCESS_CRITERIA: Future-Started Scheduling

## 1. Timeline Flexibility (Technical)
- [ ] **Custom Start Date**: The `DeveloperTimeline` must accept an optional `start_date` parameter.
- [ ] **Shifted Buckets**: If a future start date is provided (e.g., 2026-03-02), the 14-day window must begin on that date, effectively treating today through Feb 28th as "Blocked/Ignore".

## 2. Load Integration (Functional)
- [ ] **Pre-fill Buffer**: Existing Backlog load should still be fetched, but the user has indicated the team is "packed" until March. We should decide if we pre-fill the *future* buckets with *current* load or start them clean.
    - [ ] *Decision*: Since the user says they are working on other things until then, we will start the March 2nd buckets as **Clean (0h usage)** to represent the new allocation period.

## 3. Reporting (Style)
- [ ] Log clearly: "Timeline initialized starting from 2026-03-02".
