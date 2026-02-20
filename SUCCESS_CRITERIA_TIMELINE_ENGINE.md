# SUCCESS_CRITERIA: Holiday-Aware Resource Leveling

## 1. Holiday Integration (Technical)
- [ ] **Library Deployment**: Install and utilize the `holidays` Python library.
- [ ] **Locale Configuration**: Explicitly set the country to Japan (`JP`) to capture public holidays like Vernal Equinox, Golden Week, etc.

## 2. Scheduling Logic (Functional)
- [ ] **Triple-Exclusion**: The engine must skip:
    1. Saturdays
    2. Sundays
    3. Japanese Public Holidays
- [ ] **Bucket Integrity**: Ensure no "Daily Bucket" is created for a holiday.

## 3. Verification (Style)
- [ ] Log if a task's finish date was pushed further due to a holiday (e.g., "Skipping Holiday: Emperor's Birthday").
