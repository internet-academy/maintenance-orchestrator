# SUCCESS_CRITERIA: High-Frequency Sync & Daily Reporting

## 1. Frequency (Ops)
- [ ] **20-Minute Intervals**: Update the GitHub Actions cron schedule to `*/20 * * * *`.
- [ ] **Locking Mechanism**: Ensure that if a run takes longer than 20 minutes (unlikely), a second run doesn't start and cause race conditions.

## 2. Google Chat Integration (Technical)
- [ ] **Target Space**: `AAAAXcdPfl0`.
- [ ] **Thread Management**: 
    - Logic to detect if a "Daily Report YYYYMMDD" thread exists.
    - If not, create it.
    - If yes, append/update messages within that thread.
- [ ] **@Mentions**: Map developer names to their Google Chat IDs for active notification.

## 3. Reporting Logic (Functional)
- [ ] **Daily Task Load**: For each developer, extract all tasks with a `dueDate` of Today (or Open tasks assigned to them).
- [ ] **Message Formatting**:
    - Header: `Daily Report 20260220`
    - Body: `@DeveloperName here are your tasks for today: [MD_SD-XXXX] Title...`

## 4. Verification (Ops)
- [ ] **Dry Run**: Print the exact payload that would be sent to Google Chat.
