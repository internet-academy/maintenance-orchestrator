# SUCCESS_CRITERIA: Continuous Learning Protocol (Direct Injection)

## 1. Protocol Expansion (Master Agent)
- [ ] **The Retrospective Phase**: Update `master-agent.md` to include a mandatory final step after a successful Sentry "Green Light" on complex tasks.
- [ ] **Trigger Condition**: Define exactly when a lesson is recorded (e.g., "If a bug took more than 2 attempts to fix" or "If the Sentry caught a critical structural error").
- [ ] **Action**: The Master Agent must formulate a concise, generalized rule based on the failure.

## 2. Structural Memory Injection (Sub-Agents)
- [ ] **The `LESSONS LEARNED` Section**: Ensure that every sub-agent file in `gemini-active/` (e.g., `logic.md`, `pixel.md`, `sentry.md`) has a dedicated `## LESSONS LEARNED (ANTI-PATTERNS)` section.
- [ ] **Direct Update Mechanism**: The Master Agent must use a tool (like `replace` or `write_file`) to append the generalized rule directly into the specific sub-agent's `.md` file, permanently altering their system prompt for all future sessions.

## 3. Formatting & Granularity (The Rules)
- [ ] **Actionable Format**: Lessons must be written as strict negative constraints or absolute mandates (e.g., "NEVER use 0-based indexing for gspread cell updates; ALWAYS convert to 1-based.").
- [ ] **Contextual Tagging**: Include a brief tag indicating *why* the rule exists so the agent understands the context (e.g., "[Google Sheets API] ...").

## 4. Verification
- [ ] **Testing the Loop**: Simulate a failure, trigger the Retrospective phase, and verify that the target sub-agent's `.md` file is physically updated with the new rule.