#!/bin/bash
# XEREX System Health Check v19.7.9
# Run this to verify everything is working

echo "=================================================="
echo "🤖 XEREX SYSTEM HEALTH CHECK v19.7.9"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: Validator
echo "1. VALIDATOR CHECK:"
if python3 validate_xerex.py standalone/*.xml project_knowledge/*.xml > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ All files passing validation${NC}"
else
    echo -e "   ${RED}❌ Validation failures detected${NC}"
    python3 validate_xerex.py standalone/*.xml project_knowledge/*.xml
fi
echo ""

# Check 2: Git Status
echo "2. GIT STATUS:"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "   ${GREEN}✅ Repository clean${NC}"
else
    echo -e "   ${YELLOW}⚠️  Uncommitted changes:${NC}"
    git status --short
fi
echo ""

# Check 3: Pre-commit Hooks
echo "3. PRE-COMMIT HOOKS:"
if [ -f .git/hooks/pre-commit ]; then
    echo -e "   ${GREEN}✅ Hooks installed${NC}"
else
    echo -e "   ${RED}❌ Hooks not installed${NC}"
    echo "   Run: pre-commit install"
fi
echo ""

# Check 4: Version Consistency
echo "4. VERSION CONSISTENCY:"
VERSION_COUNT=$(grep -h "<current_version>" */*.xml | sort -u | wc -l)
if [ "$VERSION_COUNT" -eq 1 ]; then
    VERSION=$(grep -h "<current_version>" */*.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/')
    echo -e "   ${GREEN}✅ All files at version $VERSION${NC}"
else
    echo -e "   ${RED}❌ Multiple versions detected${NC}"
    grep -h "<current_version>" */*.xml | sort -u
fi
echo ""

# Check 5: File Structure
echo "5. FILE STRUCTURE:"
EXPECTED_FILES=(
    "standalone/personal_preferences_v19.7.9.xml"
    "standalone/project_instructions_v19.7.9.xml"
    "standalone/style_guide_v19.7.9.xml"
    "project_knowledge/safety_core_v19.7.9.xml"
    "project_knowledge/pattern_engine_v19.7.9.xml"
    "project_knowledge/system_intelligence_v19.7.9.xml"
    "project_knowledge/audit_center_v19.7.9.xml"
    "project_knowledge/testing_suite_v19.7.9.xml"
)

MISSING=0
for file in "${EXPECTED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "   ${RED}❌ Missing: $file${NC}"
        MISSING=$((MISSING+1))
    fi
done

if [ $MISSING -eq 0 ]; then
    echo -e "   ${GREEN}✅ All required files present${NC}"
fi
echo ""

# Check 6: GitHub Remote
echo "6. GITHUB CONNECTION:"
if git remote -v | grep -q "github.com"; then
    echo -e "   ${GREEN}✅ GitHub remote configured${NC}"
    LAST_PUSH=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
    if [ "$LAST_PUSH" -eq 0 ]; then
        echo -e "   ${GREEN}✅ All changes pushed${NC}"
    else
        echo -e "   ${YELLOW}⚠️  $LAST_PUSH commits not pushed${NC}"
    fi
else
    echo -e "   ${RED}❌ No GitHub remote found${NC}"
fi
echo ""

# Check 7: Python Dependencies
echo "7. PYTHON ENVIRONMENT:"
if python3 -c "import xml.etree.ElementTree" 2>/dev/null; then
    echo -e "   ${GREEN}✅ XML parsing available${NC}"
else
    echo -e "   ${RED}❌ XML module missing${NC}"
fi

if which pre-commit > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ pre-commit installed${NC}"
else
    echo -e "   ${YELLOW}⚠️  pre-commit not found${NC}"
fi
echo ""

# Summary
echo "=================================================="
echo "SUMMARY:"
echo "Run this check regularly to ensure system health"
echo "All green = Ready for production use!"
echo "=================================================="
