# SUCCESS_CRITERIA: Retroactive Task Translation

## 1. Data Retrieval (Technical)
- [ ] **Accurate Matching**: Correctly match Backlog IDs (MD_SD-1249 to MD_SD-1255) to their corresponding rows in the Google Sheet.
- [ ] **Content Extraction**: Retrieve the full Japanese `報告/相談内容` for each of the 7 tasks.

## 2. Translation & Formatting (Functional)
- [ ] **Professional English**: Generate a clear, technically accurate English translation.
- [ ] **Bilingual Structure**: Format the Backlog description with `## English Description` and `## 原文 (Japanese)` sections.
- [ ] **Preservation**: Ensure URLs and specific technical values (dates, IDs) are unchanged.

## 3. Execution & Verification (Ops)
- [ ] **API Patching**: Use the `update_backlog_issue` method to push the updates to Backlog.
- [ ] **Logging**: Log each successful update with the Issue Key.
