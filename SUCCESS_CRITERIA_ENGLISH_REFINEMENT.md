# SUCCESS_CRITERIA: High-Fidelity English Titling & Translation

## 1. Title Language (Functional)
- [ ] **Strict English**: The text between `[ERROR]` and the brackets `(Requester - #ID)` must be a concise English summary.
- [ ] **Descriptive**: It must describe the *action* or *defect* (e.g., "Correct enrollment date" instead of "Mao task").

## 2. Description Translation (Technical)
- [ ] **True Translation**: The `## English Summary` section must contain an English translation of the Japanese text, not a snippet of the original.
- [ ] **Bilingual Separation**: Maintain the clear distinction between the English translation and the `## 原文 (Japanese)` section.

## 3. Implementation Accuracy (Ops)
- [ ] **Retroactive Correction**: Successfully update MD_SD-1249 through MD_SD-1256 with the corrected English titles and summaries.
- [ ] **Orchestrator Hardening**: Ensure the code logic no longer defaults to Japanese snippets for English fields.
