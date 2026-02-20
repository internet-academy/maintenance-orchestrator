# SUCCESS_CRITERIA: Proper Markdown & Newline Rendering

## 1. String Integrity (Technical)
- [ ] **Actual Newlines**: Utilize Python's triple-quoted strings (`"""`) or proper `
` characters to ensure the API receives true line breaks.
- [ ] **Markdown Compliance**: Ensure a blank line exists between headers (`##`) and body text to trigger correct rendering in Backlog.

## 2. Formatting (Functional)
- [ ] **No Escaped Characters**: The final text in Backlog must not contain visible `
` or `
` strings.
- [ ] **Standard Headers**:
    - `## English Description`
    - `## 原文 (Japanese)`

## 3. Verification (Ops)
- [ ] Verify the fix on a single task (MD_SD-1249) before applying to all.
