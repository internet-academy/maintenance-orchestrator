# SUCCESS_CRITERIA: Daily Report Automation Fix

## 1. Reporting Destination
- [ ] Update the `GOOGLE_CHAT_REPORT_WEBHOOK` to point to the user's personal chat: `https://chat.google.com/u/0/app/chat/AAAA13Bwi2M` (Note: This needs to be the webhook URL, not the space URL).
- [ ] Provide a fallback mechanism or clear instruction for the user to update the GitHub Secret if the direct URL is not the webhook.

## 2. Execution Frequency Fix
- [ ] **Maintenance Sync Report**: Modify `orchestrator.py` to only send the sync report if `stats["new_tasks"] > 0`. Status updates and minor syncs should not trigger a chat message every 15 minutes.
- [ ] **Daily Operations Report**: Ensure the daily report is strictly sent once per calendar day.
- [ ] **Target Hour Check**: Refine the `target_hour` logic to handle cases where the automation might not run exactly at the top of the hour (e.g., check if the report for *today* has been sent yet).

## 3. System Integrity & Other Issues
- [ ] Audit `orchestrator.py` for potential race conditions or state-saving failures that could cause duplicate reports.
- [ ] Verify that the `state` (last_report_date) is correctly persisted between GitHub Action runs using the Gist-based state manager.
- [ ] Check for any hardcoded webhook URLs in other files (e.g., `test_live_chat.py`) and ensure they are neutralized or moved to environment variables.

## 4. Technical Constraints
- [ ] **Surgical Changes**: Only modify the minimum necessary code in `orchestrator.py`.
- [ ] **Environment Parity**: Ensure the fix works both in local dry-runs and in the GitHub Action environment.
