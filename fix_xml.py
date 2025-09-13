#!/usr/bin/env python3
"""
XEREX XML Fix Script - Repairs common XML formatting issues
Run this to fix "not well-formed" errors from validator
"""

import os
import re
import sys
from pathlib import Path

def fix_xml_file(filepath):
    """Fix common XML formatting issues"""
    print(f"Fixing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Ensure proper XML declaration
    if not content.startswith('<?xml'):
        content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
    
    # Fix 2: Fix unescaped ampersands (common issue)
    # But don't break already escaped ones
    content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', content)
    
    # Fix 3: Fix mismatched CDATA sections
    # Ensure CDATA sections are properly closed
    content = re.sub(r'<!\[CDATA\[(?!.*?\]\]>)', '<![CDATA[', content, flags=re.DOTALL)
    
    # Fix 4: Remove any null bytes (can break XML)
    content = content.replace('\x00', '')
    
    # Fix 5: Fix smart quotes that break XML
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")
    
    # Fix 6: Ensure file ends with proper closing tag
    if '</project_knowledge>' not in content:
        if '<project_knowledge>' in content:
            content = content.rstrip() + '\n</project_knowledge>'
    
    # Fix 7: Remove any content after closing tag
    if '</project_knowledge>' in content:
        idx = content.index('</project_knowledge>') + len('</project_knowledge>')
        content = content[:idx] + '\n'
    
    # Save if changes were made
    if content != original:
        # Backup original
        backup_path = filepath + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        print(f"  Backed up to: {backup_path}")
        
        # Write fixed version
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed and saved")
        return True
    else:
        print(f"  No issues found")
        return False

def main():
    """Fix all XML files in the xerex-system directory"""
    
    # Find xerex-system directory
    if os.path.exists('standalone'):
        base_dir = '.'
    elif os.path.exists(os.path.expanduser('~/xerex-system')):
        base_dir = os.path.expanduser('~/xerex-system')
    else:
        print("ERROR: Can't find xerex-system directory")
        sys.exit(1)
    
    os.chdir(base_dir)
    print(f"Working in: {os.getcwd()}\n")
    
    # Fix standalone files
    print("=== FIXING STANDALONE FILES ===")
    standalone_files = [
        'standalone/personal_preferences_v19.7.9.xml',
        'standalone/project_instructions_v19.7.9.xml',
        'standalone/style_guide_v19.7.9.xml'
    ]
    
    for filepath in standalone_files:
        if os.path.exists(filepath):
            fix_xml_file(filepath)
        else:
            print(f"Not found: {filepath}")
    
    print("\n=== FIXING PROJECT_KNOWLEDGE FILES ===")
    project_files = Path('project_knowledge').glob('*.xml')
    
    for filepath in project_files:
        fix_xml_file(str(filepath))
    
    print("\n=== RUNNING VALIDATION ===")
    os.system('python3 validate_xerex.py standalone/*.xml')
    print()
    os.system('python3 validate_xerex.py project_knowledge/*.xml')
    
    print("\n✅ Fix attempt complete! Check results above.")

if __name__ == '__main__':
    main()