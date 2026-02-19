# SUCCESS_CRITERIA: Excel-to-Backlog Sync Process

## 1. Task Ingestion (Functional)
- [ ] **Data Capture**: Detect new rows in the "Task List" Google Sheet.
- [ ] **State Persistence**: Maintain a "Last Processed Row" or use a "Sync Status" column in the sheet to prevent duplicate issue creation in Backlog.

## 2. Update Logic (Technical)
- [ ] **Uni-directional Sync**: (Current) New Sheet Row -> New Backlog Issue.
- [ ] **Change Detection**: (Planned) Detect if an existing row's "Estimated Hours" or "Deadline" changes and update the corresponding Backlog issue.
- [ ] **ID Mapping**: Store the Backlog Issue ID back in the Google Sheet for future reference.

## 3. Automation Cadence (Ops)
- [ ] **Polling**: Implement a cron job or a background loop that checks the sheet every X minutes.
- [ ] **Manual Override**: Provide a script to trigger a manual "Full Sync".
