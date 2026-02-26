# SUCCESS_CRITERIA: SEMANTIC MEANING INDEXING (L4)

## 🎯 GOAL
Add a "Semantic Layer" to the blueprints that describes the *purpose* and *intent* of code, enabling agents to find logic based on business goals rather than just file names.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **Component Summarization**: Generate 1-sentence summaries for every Django app, Go service, and Vue view.
- **Logic Mapping**: Identify "Business Logic Hubs" (e.g., "This file handles the payment gateway integration").
- **Intent-Based Search**: Allow the Master Agent to search the blueprint for keywords like "authentication," "file upload," or "billing" and find the relevant files regardless of their naming convention.

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **LLM-Assisted Indexing**: Use a single, fast LLM call per file during the indexing phase to generate the summary.
- **Caching**: Store summaries in a `semantics.json` so we don't re-run the LLM on every scan.
- **Token Efficiency**: Summaries must be strictly limited to 15-20 words to keep the blueprint compact.

## ✅ VERIFICATION (Sentry)
- The upgrade is successful if `member_blueprint.md` contains a "Purpose" section for the `bohr_api` app that accurately describes its role in the system.
