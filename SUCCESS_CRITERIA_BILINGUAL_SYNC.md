# SUCCESS_CRITERIA: Permanent Bilingual Synchronization

## 1. Core Logic Integration (Technical)
- [ ] **Bilingual Description Builder**: Create a helper in `Orchestrator` or `CloudIngestor` that takes raw Japanese content and returns a formatted bilingual string.
- [ ] **Field Mapping**: Ensure the `description` field is explicitly updated during both `CREATE` and `UPDATE` operations.

## 2. Translation Execution (Functional)
- [ ] **Retroactive Fix**: Re-apply English translations to `MD_SD-1249` through `MD_SD-1256`.
- [ ] **Future-Proofing**: The system must automatically prompt for or generate translations for any new rows detected in the future.

## 3. Audit (Style)
- [ ] Sentry must verify that `description` is never sent as an empty string or a raw Japanese-only string.
