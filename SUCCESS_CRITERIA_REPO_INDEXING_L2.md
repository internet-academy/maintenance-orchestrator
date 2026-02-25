# SUCCESS_CRITERIA: DEEP SYMBOL INDEX (L2)

## 🎯 GOAL
Enhance `scanner.py` to extract symbolic data (Classes, Functions, Models) to provide agents with "Micro-Context" without exhausting the token window.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **Symbolic Extraction**: Extract name, parameters, and line numbers for all functions/classes in `.py`, `.go`, and `.ts/.vue` files.
- **Model Deep-Scan**: For Django/Go models, extract all field names (e.g., `CharField`, `string`).
- **L2 Output**: Generate a `symbols.json` or append a "Symbol Map" to the existing blueprints.
- **Searchable Index**: Ensure the Master Agent can query "Which file contains the function `submit_application`?" and get an instant, accurate answer.

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **Regex/AST Efficiency**: Use robust regex or lightweight AST parsing to avoid execution overhead.
- **Noise Reduction**: Exclude internal/private symbols (e.g., those starting with `_` unless they are core Django methods).
- **Format**: Maintain the 4,000-token limit for the total blueprint size by using a "Compressed Symbol Map" format.

## ✅ VERIFICATION (Sentry)
- The upgrade is successful if `member_blueprint.md` now lists the fields for the `Profile` model and the functions within `bohr_api/views.py`.
