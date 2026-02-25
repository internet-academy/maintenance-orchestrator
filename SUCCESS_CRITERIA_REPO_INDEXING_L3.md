# SUCCESS_CRITERIA: DEPENDENCY GRAPH INDEXING (L3)

## 🎯 GOAL
Enhance the indexing system to map relationships between symbols, allowing agents to perform "Impact Analysis" before making a change.

## 🟢 FUNCTIONAL REQUIREMENTS (The "What")
- **Django Model Relationships**: Map `ForeignKey`, `OneToOne`, and `ManyToMany` fields to their target models (e.g., `Profile` -> `User`).
- **Internal Call Mapping**: For core business logic files, identify which internal functions are called by other functions.
- **Cross-Stack Bridge**: Identify Vue.js API calls (`axios`, `fetch`) and match them to Go/Django backend routes.
- **Import Mapping**: Track which files import which other files to understand the "Ripple Effect" of a change.

## 🛠️ TECHNICAL CONSTRAINTS (The "How")
- **AST Parsing (Python)**: Use the `ast` module for Python files to accurately identify imports and function calls without running the code.
- **Regex Heuristics (Go/Vue)**: Use targeted regex to find API endpoint strings (e.g., `"/api/..."`) and Go route registrations.
- **Graph Representation**: Output a "Dependency Map" in the blueprint that shows `[Symbol] -> [Depends On]`.
- **Token Efficiency**: Use a highly compressed "Relationship Shorthand" to keep the blueprint under the 5,000-token limit.

## ✅ VERIFICATION (Sentry)
- The upgrade is successful if `bohr_blueprint.md` can show that `BenefitOtherApplication.vue` depends on the `/api/support/doc/enroll` endpoint, which is handled by `supportController.go`.
