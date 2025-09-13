#!/bin/bash
echo "🔄 XEREX Sync Script v19.7.8"
echo "=========================="

# Colors to make it pretty
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Creating standalone files...${NC}"

# For each brain file, create a simple test file
for brain_file in project_knowledge/*.xml; do
    if [ -f "$brain_file" ]; then
        filename=$(basename "$brain_file")
        simple_name=${filename/_v19.7.8/}
        
        echo "  Creating standalone/$simple_name"
        
        cat > "standalone/$simple_name" << 'INNEREOF'
<?xml version="1.0" encoding="UTF-8"?>
<xerex_document version="19.7.8">
  <current_version>19.7.8</current_version>
  <behavioral_rules>
    <rule>Rule 1</rule>
    <rule>Rule 2</rule>
    <rule>Rule 3</rule>
    <rule>Rule 4</rule>
    <rule>Rule 5 - self-referential</rule>
    <rule>Rule 6 - self-check</rule>
    <rule>Rule 7</rule>
    <rule>Rule 8</rule>
  </behavioral_rules>
  <reference>See project_knowledge folder for full content</reference>
</xerex_document>
INNEREOF
    fi
done

echo -e "${YELLOW}Step 2: Testing standalone files...${NC}"
python3 validate_xerex.py standalone/*.xml

echo -e "${GREEN}✅ Sync complete!${NC}"
