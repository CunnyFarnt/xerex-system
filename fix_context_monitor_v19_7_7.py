#!/usr/bin/env python3
"""
fix_context_monitor.py - Patches context formula in all v19.7.6 documents
Fixes the broken character-based formula to proper token-based calculation
Created for XEREX v19.7.7 upgrade
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import re
from datetime import datetime

def fix_context_formula(filepath):
    """Replace broken character-based formula with token-based"""
    
    print(f"\nProcessing: {filepath}")
    changes_made = []
    
    try:
        # Parse XML with UTF-8 encoding
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Pattern to find old formula
        old_formula_pattern = r'\(Characters ÷ 800,000\) × 100 - 25%'
        new_formula = '(input_tokens + output_tokens) / 200,000 × 100'
        
        # Also fix the encoded version (Ã· instead of ÷)
        old_formula_encoded = r'\(Characters Ã· 800,000\) Ã— 100 - 25%'
        
        # Search all text nodes
        for elem in root.iter():
            if elem.text:
                original_text = elem.text
                
                # Check for both versions of the formula
                if re.search(old_formula_pattern, elem.text) or re.search(old_formula_encoded, elem.text):
                    # Replace both patterns
                    elem.text = re.sub(old_formula_pattern, new_formula, elem.text)
                    elem.text = re.sub(old_formula_encoded, new_formula, elem.text)
                    
                    if elem.text != original_text:
                        changes_made.append(f"  ✓ Fixed formula in <{elem.tag}>")
                        print(f"  ✓ Fixed formula in <{elem.tag}>")
        
        # Update version to 19.7.7 if it's 19.7.6
        version_elem = root.find('.//current_version')
        if version_elem is not None and version_elem.text == "19.7.6":
            version_elem.text = "19.7.7"
            changes_made.append("  ✓ Updated version to 19.7.7")
            print("  ✓ Updated version to 19.7.7")
        
        # Update metadata version
        for elem in root.iter():
            if elem.tag == 'version' and elem.text == "19.7.6":
                elem.text = "19.7.7"
                changes_made.append(f"  ✓ Updated <{elem.tag}> to 19.7.7")
        
        # Update session number from 8 to 9
        session_elem = root.find('.//session_created')
        if session_elem is not None and session_elem.text == "8":
            session_elem.text = "9"
            changes_made.append("  ✓ Updated session to 9")
            print("  ✓ Updated session to 9")
        
        # Update canonical metrics to current values
        trust_elem = root.find('.//trust_level[@value]')
        if trust_elem is not None and trust_elem.get('value') == "64%":
            trust_elem.set('value', '94%')
            changes_made.append("  ✓ Updated trust to 94%")
            print("  ✓ Updated trust to 94%")
        
        # Add improvement note about context fix
        improvements = root.find('.//improvements')
        if improvements is not None:
            new_improvement = ET.SubElement(improvements, 'improvement')
            new_improvement.text = 'Fixed context formula to token-based calculation'
            changes_made.append("  ✓ Added context fix note")
        
        if changes_made:
            # Save with _fixed suffix first
            output = filepath.replace('.xml', '_fixed.xml')
            tree.write(output, encoding='utf-8', xml_declaration=True)
            print(f"  ✓ Saved as: {output}")
            print(f"  Total changes: {len(changes_made)}")
            return output, len(changes_made)
        else:
            print("  ⚠️ No changes needed (already fixed or different structure)")
            return None, 0
            
    except ET.ParseError as e:
        print(f"  ❌ XML Parse Error: {e}")
        return None, -1
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, -1

def main():
    """Fix all v19.7.6 documents and prepare for v19.7.7"""
    
    print("=" * 60)
    print("XEREX CONTEXT MONITOR FIX - v19.7.6 → v19.7.7")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Find all v19.7.6 XML files
    xml_files = list(Path('.').glob('*v19.7.6.xml'))
    
    if not xml_files:
        print("\n❌ No v19.7.6 XML files found in current directory!")
        print("Make sure you're in the ~/xerex-system directory")
        return 1
    
    print(f"\nFound {len(xml_files)} v19.7.6 files to process")
    
    total_changes = 0
    fixed_files = []
    failed_files = []
    
    for filepath in xml_files:
        output, changes = fix_context_formula(str(filepath))
        
        if changes > 0:
            fixed_files.append(str(filepath))
            total_changes += changes
        elif changes == -1:
            failed_files.append(str(filepath))
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    if fixed_files:
        print(f"✅ Successfully fixed {len(fixed_files)} files:")
        for f in fixed_files:
            print(f"   - {f}")
        print(f"\nTotal changes made: {total_changes}")
        
        print("\n📋 NEXT STEPS:")
        print("1. Review the _fixed.xml files to verify changes")
        print("2. If satisfied, rename them to replace originals:")
        print("   for file in *_fixed.xml; do")
        print('       mv "$file" "${file/_fixed/}"')
        print("   done")
        print("3. Run validation: python3.11 validate_xerex.py")
        print("4. Re-combine with files-to-claude-xml")
        print("5. Upload new _claude.txt to Project Knowledge")
        
    else:
        print("⚠️ No files needed fixing")
        print("Either already fixed or using different structure")
    
    if failed_files:
        print(f"\n❌ Failed to process {len(failed_files)} files:")
        for f in failed_files:
            print(f"   - {f}")
    
    print("\n" + "=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if not failed_files else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
