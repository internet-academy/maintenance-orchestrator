# SUCCESS_CRITERIA: Section-Based Time Estimation

## 1. Data Extraction (Technical)
- [ ] **Section Identification**: Locate the "System Development" row within each task block.
- [ ] **Precise Mapping**: Extract the hours value specifically from the "Work Hours" cell associated with the "System Development" role.
- [ ] **Multi-Role Handling**: If multiple roles (e.g., Design, Marketing) have hours, ensure the system only counts "System Development" for the developers' load.

## 2. Logic Resilience (Functional)
- [ ] **Dynamic Row Offset**: The system must not rely on a fixed offset (e.g., "+2 rows") if the "System Development" section can move.
- [ ] **Numeric Conversion**: Robustly handle cases where the cell is empty or contains non-numeric strings (default to 0.0 if empty, but log a warning).

## 3. Auditability (Style)
- [ ] Log the exact value found in the "System Development" section for each task.
