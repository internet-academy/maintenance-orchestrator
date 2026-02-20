# SUCCESS_CRITERIA: Precision Parent Naming (◆リクエラ)

## 1. String Formatting (Technical)
- [ ] **No Leading Zeros**: Format months and days without leading zeros (e.g., `2/28` instead of `02/28`).
- [ ] **Year Inclusion**: Keep the `YYYY/` prefix for long-term data integrity.
- [ ] **Exact Match**: The generated summary must be `◆リクエラ(YYYY/M/D)` where `D` is the last day of the month.

## 2. Verification (Ops)
- [ ] **Dry Run Trace**: Log: `HIERARCHY: Linking to Parent '◆リクエラ(2026/2/28)'`.
- [ ] **Transition Check**: Confirm that a task finishing in March is linked to `◆リクエラ(2026/3/31)`.
