# SUCCESS_CRITERIA: Stateful Ingestor Implementation

## 1. Block Recognition & Extraction
- [ ] **ID-Driven Identification**: Correcty identify a task block starting with a numeric Task ID in the first column.
- [ ] **Stateful Boundary Detection**: Dynamically determine the end of a block by searching for the start of the next ID or a significant blank space/end of data.
- [ ] **Label-Based Parsing**: Locate values (PIC, Estimated Hours, Status, Content) by searching for their respective header labels within the block, rather than relying on hardcoded row offsets.

## 2. Robustness & Validation
- [ ] **Header/Example Resilience**: Successfully skip non-task blocks like headers and the "記入例" (Example) block.
- [ ] **Data Sanitization**: Handle missing values or malformed data within a block gracefully (e.g., default 1.0 hour for missing estimates).
- [ ] **Multi-Row Content**: Capture "Content" and "Translation" across multiple rows if they span across the block structure.

## 3. Integration & Performance
- [ ] **Standardized Output**: Produce a `StandardizedTaskObject` consistent with the existing Orchestrator expectations.
- [ ] **Efficiency**: Minimize Google Sheets API calls by fetching the entire range and parsing locally in memory.

## 4. Reverse Sync Support
- [ ] **Write-Back Capability**: Ensure `write_backlog_id` and `write_status` can still accurately target the correct cells within the dynamic block structure.
