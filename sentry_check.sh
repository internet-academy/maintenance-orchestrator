#!/bin/bash

# Sentry CI Validator: Automated Testing & Linting
# Target: Multi-stack (Django, Go, Vue)

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

REPO_PATH=${1:-$(pwd)}
echo "🔍 Sentry CI: Scanning $REPO_PATH..."
cd "$REPO_PATH" || exit 1

# 1. Stack Detection
if [ -f "manage.py" ]; then
    STACK="Django"
elif [ -f "backend/go.mod" ] || [ -f "go.mod" ]; then
    STACK="Bohr-Fullstack"
elif [ -f "requirements.txt" ]; then
    STACK="General-Python"
else
    echo -e "${RED}❌ Error: Unknown stack. No manage.py or go.mod found.${NC}"
    exit 1
fi

echo -e "📦 Detected Stack: ${GREEN}$STACK${NC}"

# 2. Execution Logic
case $STACK in
    "Django")
        echo "🧪 Running Django Tests..."
        # Use venv if available
        PYTHON_EXEC="python3"
        [ -f "venv/bin/python" ] && PYTHON_EXEC="venv/bin/python"
        
        $PYTHON_EXEC manage.py test --noinput
        EXIT_CODE=$?
        ;;

    "General-Python")
        echo "🧪 Running Python Syntax & Unit Checks..."
        PYTHON_EXEC="python3"
        [ -f "venv/bin/python" ] && PYTHON_EXEC="venv/bin/python"
        
        # 1. Syntax check ALL changed/new files (or just everything)
        $PYTHON_EXEC -m py_compile *.py agents/*.py 
        SYNTAX_EXIT=$?

        # 2. Run specific unit tests if they exist
        [ -f "test_stateful_parsing.py" ] && $PYTHON_EXEC test_stateful_parsing.py
        TEST_EXIT=$?

        if [ $SYNTAX_EXIT -eq 0 ] && [ $TEST_EXIT -eq 0 ]; then
            EXIT_CODE=0
        else
            EXIT_CODE=1
        fi
        ;;

    "Bohr-Fullstack")
        echo "🧪 Running Go Backend Tests..."
        if [ -d "backend" ]; then
            (cd backend && go test ./...)
        else
            go test ./...
        fi
        BACKEND_EXIT=$?

        echo "🧪 Running Frontend Lint Check..."
        if [ -d "frontend" ]; then
            (cd frontend && npm run lint:check || npm run lint)
        fi
        FRONTEND_EXIT=$?

        # Combine exit codes
        if [ $BACKEND_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ]; then
            EXIT_CODE=0
        else
            EXIT_CODE=1
        fi
        ;;
esac

# 3. Final Signal
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "
${GREEN}✅ VALIDATION PASSED${NC}"
    exit 0
else
    echo -e "
${RED}❌ VALIDATION FAILED${NC}"
    exit 1
fi
