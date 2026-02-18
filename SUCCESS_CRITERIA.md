# SUCCESS_CRITERIA: Autonomous Verification System

## 1. Workflow Integrity
- [ ] Every user request triggers the Architect -> Specialist -> Sentry pipeline.
- [ ] No result is returned to the user without a "GREEN LIGHT" from Sentry.
- [ ] Sentry successfully provides actionable feedback on "RED LIGHT" status.

## 2. Agent Consistency
- [ ] `master-agent.md` correctly identifies the protocol as the mandatory default.
- [ ] `architect.md` is optimized to generate checklists for the Sentry.
- [ ] `sentry.md` is configured for ruthless verification and rejection loops.

## 3. Autonomous Feedback Loop
- [ ] The system can demonstrate at least one loop (Specialist -> Sentry -> Specialist) if criteria aren't met on the first try.
- [ ] The final output is verified to meet all user requirements without user intervention during the cycle.

## 4. Documentation & Handover
- [ ] `GEMINI.md` in the `personal-agents` folder reflects this new architecture.
- [ ] The system is self-documenting for fresh sessions.
