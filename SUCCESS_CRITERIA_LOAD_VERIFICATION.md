# SUCCESS_CRITERIA: Multi-Task Load Verification (Manager Overflow)

## 1. Prioritization Logic (Functional)
- [ ] **Tiered Assignment**: Divide developers into "Core Team" (Saurabh, Raman, Ewan) and "Manager" (Choo).
- [ ] **Overflow Rule**: Choo must only be considered for assignment if ALL Core Team members have reached their 6.0h limit for the session.
- [ ] **Fairness within Tier**: Within the Core Team, the lowest-load assignment logic must still apply.

## 2. Capacity Enforcement (Technical)
- [ ] **Hard Limit**: Choo still maintains a 6.0h limit; if he is also full, the task must be marked as "OVERLOAD".
- [ ] **Session Integrity**: The `session_load` must correctly track Choo's load if he is finally utilized.

## 3. Reporting (Style)
- [ ] Log messages should clearly indicate if a task was assigned via "Manager Overflow".
