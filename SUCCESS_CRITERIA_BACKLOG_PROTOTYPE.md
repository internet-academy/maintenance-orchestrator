# SUCCESS_CRITERIA: Backlog API Connector (Live Test)

## 1. Project Identification (Functional)
- [ ] Successfully identify the numeric Project ID for the project key `MD_SD`.
- [ ] Verify that the `BACKLOG_SPACE_ID` is present and correct in the environment.

## 2. Live Execution (Technical)
- [ ] Run `test_backlog_connection.py` and retrieve at least one issue from the `MD_SD` project.
- [ ] Sum the `estimatedHours` and confirm the calculation logic works on real data.

## 3. Output Quality (Style)
- [ ] Log the results clearly in the session output.
- [ ] Sentry must verify that no sensitive data (like the API Key) is accidentally printed in the test output.
