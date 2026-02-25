# SUCCESS_CRITERIA: LOG-MINING SPECIALIST

## 🎯 GOAL
Equip agents with a tool to read and analyze system logs across local and production-like environments to automate root-cause analysis.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **Multi-Source Log Reading**: Tool must be able to read:
    1. Local log files (e.g., `logs/logfile.log`).
    2. Systemd journal (e.g., `journalctl`).
    3. Docker logs (if applicable).
- **Intelligent Filtering**: Ability to filter by "ERROR" or "CRITICAL" keywords.
- **Tail Functionality**: Ability to read the *last* N lines of a log.

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **Safe Execution**: Tool must use `tail` or `grep` to avoid loading multi-GB log files into memory.
- **Privacy**: Automated scrubbing of any passwords or auth tokens found in log tracebacks.
- **Context Management**: Limit log output to 100 lines per tool call to prevent context overflow.

## ✅ VERIFICATION (Sentry)
- The upgrade is successful if the **Scout** can run the tool and successfully identify the last 5 errors in the `member` log file.
