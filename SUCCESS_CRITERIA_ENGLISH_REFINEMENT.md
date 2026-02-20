# SUCCESS_CRITERIA: Multi-Source Translation & Verification

## 1. Sheet Discovery (Technical)
- [ ] **Column Identification**: Locate the exact column in the Google Sheet containing the Google-translated English description.
- [ ] **Ingestion Upgrade**: Update `CloudIngestor` to capture this `google_translation` field.

## 2. Fallback Logic (Functional)
- [ ] **Hierarchical Translation**:
    1. Primary: Gemini AI (for high-fidelity professional tone).
    2. Secondary: Google Translation from Sheet (if Gemini fails/quota hit).
    3. Tertiary: Hardcoded English Title + Original snippet (absolute fallback).

## 3. Title Refinement (Style)
- [ ] **Translation Audit**: Compare current Backlog titles against the "Google Translation" column to identify where the AI is drifting or failing.
- [ ] **Action-Oriented Titles**: Ensure titles describe the problem accurately.

## 4. Verification (Ops)
- [ ] **Content Check**: Fetch one task from Backlog and compare it side-by-side with the Sheet data to confirm "incorrectness" root cause.
