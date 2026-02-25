# SUCCESS_CRITERIA: REPOSITORY BLUEPRINTING & L1 INDEXING

## 🎯 GOAL
Create a high-density, machine-readable "Map" of a repository that allows a Lead Agent to understand the entire architecture, data flow, and dependencies within a 4,000-token context window.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **L1 Structure Map**: A complete directory tree (excluding noise like `node_modules`, `.git`, `venv`) with 1-sentence descriptions of folder purposes.
- **Tech Stack Manifest**: Identification of core frameworks (Django, Go, React), versions, and entry points.
- **Data Model Schema**: A summary of database tables, relationships, and core entities (e.g., `User`, `Application`).
- **API Surface Area**: List of primary endpoints (REST/GraphQL) and their corresponding controller files.
- **Cross-Repo Dependencies**: Identification of links to other repositories (e.g., `member` calling `bohr-individual` APIs).

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **Token Efficiency**: The final L1 Blueprint must NOT exceed 4,000 tokens.
- **Privacy/Security**: Must include an automated `secret-scrub` phase to prevent indexing `.env`, `.pem`, or hardcoded API keys.
- **Automation**: The blueprint should be regeneratable via a single command (e.g., `./index_repo.sh`) to keep up with code changes.
- **Format**: Output must be Markdown with clear headers and backticked file paths for easy "Search & Read" by agents.

## 🔍 SCOUT RESEARCH OBJECTIVES
The Scout must evaluate and recommend the most efficient toolset for this task, comparing:
1. **Static Analysis**: (e.g., `tree`, `grep`, `cloc`, `ctags`).
2. **LLM-Summarization**: Using a cheap, high-context model to "digest" READMEs and config files.
3. **Custom Hybrid**: A Python/Bash script that orchestrates the above.

## ✅ VERIFICATION (Sentry)
- The Blueprint is considered successful ONLY if the Master Agent can correctly identify the file responsible for a specific logic (e.g., "Where is the login validation logic?") using ONLY the Blueprint.
