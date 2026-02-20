# SUCCESS_CRITERIA: Robust Ownership Verification

## 1. Flexibility (Technical)
- [ ] **ID-Based Verification**: Instead of relying on the complex URL string (which can change if the spreadsheet tab changes), verify ownership by searching for the "Task ID" (e.g., `ID: 1`) at the start of the description.
- [ ] **URL Fallback**: If the ID is not found, use a fuzzy match for the row range rather than an exact string match.

## 2. Integrity (Functional)
- [ ] **False Positive Reduction**: Ensure that a legitimate task update is not rejected as a "collision."

## 3. Audit (Ops)
- [ ] **Sentry Pass**: Run a dry run where existing tasks are correctly identified as "Verified Updates."
