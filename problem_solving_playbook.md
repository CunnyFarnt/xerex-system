# XEREX Problem-Solving Playbook v19.7.9
## How to Fix Things When They Break

---

## 🎯 DIAGNOSTIC DECISION TREE

### STEP 1: IDENTIFY THE PROBLEM TYPE

```
Is it a VALIDATION error?
├─ YES → Go to VALIDATION FIXES
└─ NO → Continue
    │
    Is it a VERSION SYNC issue?
    ├─ YES → Go to VERSION FIXES
    └─ NO → Continue
        │
        Is it a GITHUB/GIT issue?
        ├─ YES → Go to GIT FIXES
        └─ NO → Continue
            │
            Is it a CLAUDE.AI retrieval issue?
            ├─ YES → Go to RETRIEVAL FIXES
            └─ NO → Go to GENERAL DEBUGGING
```

---

## 🔧 VALIDATION FIXES

### Problem: "Wrong version" error
```bash
# 1. Check what validator expects
grep -n "current_version" validate_xerex.py

# 2. Check what files have
head -5 standalone/*.xml | grep current_version

# 3. Debug with simple script
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('standalone/safety_core_v19.7.9.xml')
root = tree.getroot()
v = root.find('.//current_version')
print(f'Version found: {v.text if v else None}')
"
```

### Problem: Validator file corrupted
```bash
# Symptoms: Duplicate code, syntax errors
# Fix: Replace with clean version
cp validate_xerex.py validate_xerex_broken.py
curl -O https://raw.githubusercontent.com/YOUR_REPO/main/validate_xerex.py
# Or recreate from this playbook's template
```

### Problem: BOM characters
```bash
# Check for BOM
hexdump -C *.xml | head -2 | grep "ef bb bf"

# Remove BOM from all files
for file in *.xml; do
    sed -i '' '1s/^\xEF\xBB\xBF//' "$file"
done
```

---

## 🔄 VERSION SYNC FIXES

### Problem: Multiple versions across files
```bash
# Find all versions
grep -h "<current_version>" */*.xml | sort -u

# Update all to same version (e.g., 19.7.9)
find . -name "*.xml" -exec sed -i '' 's/<current_version>.*<\/current_version>/<current_version>19.7.9<\/current_version>/g' {} \;

# Verify
grep -h "<current_version>" */*.xml | sort -u
```

### Problem: Filename vs content mismatch
```bash
# Rename files to match content
for file in *.xml; do
    VERSION=$(grep "<current_version>" "$file" | sed 's/.*>\(.*\)<.*/\1/')
    NEW_NAME=$(echo "$file" | sed "s/v[0-9.]*\.xml/v${VERSION}.xml/")
    if [ "$file" != "$NEW_NAME" ]; then
        mv "$file" "$NEW_NAME"
        echo "Renamed $file to $NEW_NAME"
    fi
done
```

---

## 🐙 GIT/GITHUB FIXES

### Problem: Can't push to GitHub
```bash
# Check remote
git remote -v

# If no remote, add it
git remote add origin https://github.com/USERNAME/xerex-system.git

# If authentication fails, use token
# 1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
# 2. Generate token with 'repo' scope
# 3. Use token as password when pushing
```

### Problem: GitHub Actions not running
```bash
# Check workflow file exists
ls -la .github/workflows/

# Create if missing
mkdir -p .github/workflows
# Copy workflow from this playbook

# Push to trigger
git add .github/
git commit -m "Fix GitHub Actions"
git push
```

### Problem: Pre-commit hooks not working
```bash
# Reinstall
pre-commit uninstall
pre-commit install

# Test manually
pre-commit run --all-files

# If still broken, check config
cat .pre-commit-config.yaml
```

---

## 🤖 CLAUDE.AI RETRIEVAL FIXES

### Problem: Claude can't find documents
**Symptoms:** "I don't have access to..." or wrong version info

**Fix:**
1. Check Project Knowledge in Claude.ai settings
2. Re-upload all files from `project_knowledge/` folder
3. Ensure filenames match exactly
4. Test retrieval with specific queries

### Problem: Format mismatch
**Symptoms:** Claude expects different XML structure

**Fix:**
```bash
# Project Knowledge files need <project_knowledge> root
# Standalone files need simpler structure
# Never mix formats!

# Verify format
head -3 project_knowledge/*.xml | grep -A2 "==>"
head -3 standalone/*.xml | grep -A2 "==>"
```

---

## 🔍 GENERAL DEBUGGING

### Create debug script
```bash
cat > debug_xerex.py << 'EOF'
#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys
import os

def debug_file(filepath):
    print(f"\n{'='*50}")
    print(f"DEBUGGING: {filepath}")
    print('='*50)
    
    # Check file exists
    if not os.path.exists(filepath):
        print(f"❌ File not found")
        return
    
    # Check file size
    size = os.path.getsize(filepath)
    print(f"📦 Size: {size} bytes")
    
    # Check for BOM
    with open(filepath, 'rb') as f:
        first_bytes = f.read(3)
        if first_bytes == b'\xef\xbb\xbf':
            print("⚠️  BOM detected!")
    
    # Parse XML
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        print(f"✅ Valid XML")
        print(f"📌 Root tag: {root.tag}")
        
        # Find version
        v1 = root.find('current_version')
        v2 = root.find('.//current_version')
        
        if v1:
            print(f"✅ Version (direct): {v1.text}")
        if v2 and v2 != v1:
            print(f"✅ Version (nested): {v2.text}")
        if not v1 and not v2:
            print(f"❌ No version found")
        
        # Check behavioral rules
        rules = root.find('.//behavioral_rules')
        if rules:
            print(f"✅ Behavioral rules: {len(rules)} found")
        else:
            print(f"❌ No behavioral rules")
            
    except Exception as e:
        print(f"❌ Parse error: {e}")

if __name__ == "__main__":
    for pattern in sys.argv[1:] if sys.argv[1:] else ['*.xml']:
        import glob
        for file in glob.glob(pattern):
            debug_file(file)
EOF

chmod +x debug_xerex.py
python3 debug_xerex.py standalone/*.xml
```

---

## 🚀 PROACTIVE PREVENTION

### Daily Health Check
```bash
# Run this every day before starting work
./health_check.sh

# If any issues, fix before proceeding
```

### Before Each Claude Session
1. Run validator: `python3 validate_xerex.py */*.xml`
2. Check git status: `git status`
3. Verify version: `grep -h "<current_version>" */*.xml | sort -u`

### After Making Changes
1. Test locally first
2. Run pre-commit: `pre-commit run --all-files`
3. Push to GitHub
4. Check GitHub Actions

### Weekly Maintenance
```bash
# Update all tools
pip3 install --upgrade pre-commit

# Clean up old files
find . -name "*.backup" -mtime +7 -delete

# Check for updates
git pull
```

---

## 📞 EMERGENCY CONTACTS

### When You're Stuck
1. Check this playbook first
2. Review Sessions 12-15 conversations
3. Run debug_xerex.py for detailed diagnostics
4. Use health_check.sh for system status

### Common Patterns to Remember
- **Pattern #75:** Lazy verification (always verify first)
- **Pattern #79:** Documentation without implementation (do first, document after)
- **Pattern #89:** Version sync (all files same version)
- **Pattern #92:** Context explosion (watch percentage)

---

## ✅ SUCCESS INDICATORS

You know the system is healthy when:
- ✅ All files pass validation
- ✅ GitHub Actions shows green
- ✅ Pre-commit hooks block bad commits
- ✅ Browser monitor shows 6/6
- ✅ Claude retrieves correct versions
- ✅ No uncommitted changes
- ✅ Version consistency across all files

---

*Generated from Session 15 after fixing the validator corruption issue*
*Last updated: September 13, 2025*