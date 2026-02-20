# SUCCESS_CRITERIA: Auto-Translated Backlog Descriptions

## 1. Translation Quality (Technical)
- [ ] **Context-Aware Translation**: Use an LLM-based translation (not just Google Translate) to ensure technical terms (e.g., "LMS", "Auth", "DB") are translated correctly.
- [ ] **Bilingual Integrity**: Keep the original Japanese text at the bottom of the description for reference by the original requester.

## 2. Information Mapping (Functional)
- [ ] **Clear Sectioning**: Use Markdown headers in the Backlog description:
    - `## English Description`
    - `## 原文 (Japanese)`
- [ ] **Technical Extraction**: Ensure that specific URLs, error codes, or IDs within the text are preserved exactly as they are.

## 3. Automation Sync (Ops)
- [ ] Update the `Orchestrator` to automatically perform this translation *before* creating the Backlog issue.
