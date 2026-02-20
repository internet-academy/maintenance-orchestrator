# SUCCESS_CRITERIA: Enhanced Task Context & Deep-Linking

## 1. Informative Summaries (Functional)
- [ ] **AI-Generated Titles**: The task summary must be an English one-sentence summary of the actual problem (e.g., "[BUG] Login Redirect Failure"), not just the requester's name.
- [ ] **Bracketed Metadata**: Include the original Sheet ID and Requester in brackets at the end of the title for reference.

## 2. Cross-Platform Linking (Technical)
- [ ] **Deep-Link Construction**: Generate a direct URL to the specific row in the Google Sheet.
    - Format: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid={GID}&range=A{ROW_INDEX+1}`
- [ ] **Description Integration**: Add a `## Reference Links` section to the Backlog description containing the deep link.

## 3. Implementation Logic (Technical)
- [ ] **Worksheet GID Retrieval**: Update `CloudIngestor` to capture the `gid` of the active worksheet.
- [ ] **Title Generation**: Implement a method to extract a concise "Subject" from the translated English text.
