# SUCCESS_CRITERIA: Calibrating Agent Autonomy

## 1. Safety Controls (Technical)
- [ ] **Risk Tiering**: Categorize tasks into "Safe" (Read-only, documentation) and "Critical" (Filesystem writes, API mutations).
- [ ] **Breakpoint Enforcement**: Mandatory pauses before high-risk commands (e.g., `rm`, `npm install`, `git push`).

## 2. Loop Autonomy (Functional)
- [ ] **Permission to Loop**: Allow the Specialist and Sentry to cycle up to 3 times autonomously to resolve "RED LIGHTS" before reporting to the user.
- [ ] **Feedback Transparency**: Ensure the logs show the internal "battle" between the Specialist and Sentry so the user can audit the reasoning later.

## 3. Human-in-the-loop (Social)
- [ ] **Consent for Closure**: The final "GREEN LIGHT" result must still be accepted by the user before the task is marked "Closed" in memory.
