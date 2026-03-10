# SUCCESS_CRITERIA: Weekly Standup Reporting Automation

## 1. Temporal Logic
- [ ] **Friday 9 AM Trigger**: The `Orchestrator` must automatically invoke `ReportManager` if the current run occurs on Friday between 9:00 AM and 10:00 AM JST.
- [ ] **Thursday Boundary**: "Last Week" results must strictly include tasks with deadlines on or before the immediately preceding Thursday.
- [ ] **Next Week Lookahead**: "Next Week" plan must include tasks with deadlines between the preceding Thursday and the upcoming Thursday.

## 2. Data Integrity & Sync
- [ ] **Rollover Enforcement**: Any task from the previous plan not marked "Done" on GitHub must automatically roll over to the "Next Week" plan with a "Rollover" remark.
- [ ] **Dynamic Requester**: The `依頼者` (Requester) column must pull from the GitHub `Requester` field, defaulting to "Sakamoto" for Bohr Ind and "Choo" otherwise.
- [ ] **Strict Deadlines**: Tasks without a GitHub `End date` must be excluded from the Weekly Report but marked as `[TBD - No Deadline]` in the Daily Operations report.

## 3. Visual Formatting
- [ ] **Bracket-Free Nesting**: Parent tasks with children must follow the format `Parent Title:\n 1. Child Title` (no square brackets).
- [ ] **Intelligent Grouping**: Related tasks (same product/prefix) must be consolidated into a single row if the PIC has more than 4 tasks in a block.
- [ ] **Status Marking**: "Last Week" results must be marked `〇` (Done) or `×` (Not Done) based on live GitHub state.

## 4. System Operationality
- [ ] **Target Reversion**: The code must be pointed back to the live `Weekly Report` and `Tables for Weekly Report` tabs.
- [ ] **Repository Parity**: All changes must be synchronized to both the personal and organization repositories.
