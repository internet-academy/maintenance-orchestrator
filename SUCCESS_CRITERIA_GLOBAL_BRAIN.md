# SUCCESS_CRITERIA: GLOBAL BRAIN (CROSS-PROJECT WISDOM)

## 🎯 GOAL
Create a global search mechanism that allows agents to query past session logs and retrospectives across all project directories.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **Multi-Project Grep**: Tool must search across `~/ia/` and `~/personal-projects/` for any `active_logs.md` or `GEMINI.md` files.
- **Semantic Filtering**: Ability to search for specific problem keywords (e.g., "Nginx 413", "SSL mismatch", "CORS").
- **Lesson Extraction**: Prioritize results found in `## LESSONS LEARNED` sections.

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **Speed**: Use `grep` or `ripgrep` for high-speed indexing.
- **Context Limit**: Return the match plus 5 lines of context above/below to capture the "Why" and "How."
- **Blacklist**: Exclude `node_modules`, `.git`, and binary files.

## ✅ VERIFICATION (Sentry)
- The upgrade is successful if the agent can answer "How did we solve the email issue in Bohr?" by finding the "Postfix SSL/OpenSSL mismatch" entry in the global logs.
