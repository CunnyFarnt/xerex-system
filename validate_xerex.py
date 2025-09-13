#!/usr/bin/env python3
"""
validate_xerex.py - XEREX Robot Inspector v19.7.9
Fixed version that actually works
"""

import xml.etree.ElementTree as ET
import sys
from pathlib import Path

def validate_behavioral_rules(root):
    """Check if behavioral rules exist and are self-referential"""
    rules = root.find('.//behavioral_rules')
    if not rules:
        return False, "❌ No behavioral_rules found"
    
    rule_count = len(rules)
    if rule_count < 8:
        return False, f"❌ Only {rule_count} rules (need 8+)"
    
    # Check for self-referential rules
    has_self_ref = False
    has_self_check = False
    
    for rule in rules:
        if rule.text and 'self-referential' in rule.text:
            has_self_ref = True
        if rule.text and 'self-check' in rule.text:
            has_self_check = True
    
    if not (has_self_ref and has_self_check):
        return False, "❌ Missing self-referential rules"
    
    return True, f"✓ {rule_count} behavioral rules with self-reference"

def validate_character_count(root):
    """Check character optimization"""
    metadata = root.find('.//character_count')
    if not metadata:
        return True, "⚠️ No character count metadata"
    
    current = metadata.find('current')
    limit = metadata.find('limit')
    target = metadata.find('target')
    
    if limit and target:
        limit_val = int(limit.text)
        target_val = int(target.text)
        if target_val > limit_val * 0.8:
            return False, f"❌ Target too high ({target_val}/{limit_val})"
    
    return True, "✓ Character count optimized"

def validate_xml_structure(filepath):
    """Main validation function"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        results = []
        all_valid = True
        
        # Check behavioral rules
        valid, msg = validate_behavioral_rules(root)
        results.append(msg)
        all_valid = all_valid and valid
        
        # Check character optimization  
        valid, msg = validate_character_count(root)
        results.append(msg)
        all_valid = all_valid and valid
        
        # Check version - look in root level or anywhere
        version = root.find('current_version')
        if not version:
            version = root.find('.//current_version')
        
        if version is not None:
            v_text = version.text.strip() if version.text else ""
            if v_text == "19.7.9":
                results.append("✓ Version 19.7.9 confirmed")
            else:
                results.append(f"❌ Wrong version (found: '{v_text}')")
                all_valid = False
        else:
            results.append("❌ No version found")
            all_valid = False
        
        return all_valid, results
        
    except ET.ParseError as e:
        return False, [f"❌ XML Parse Error: {e}"]

def main():
    """Validate all XEREX documents"""
    print("=" * 50)
    print("🤖 XEREX ROBOT INSPECTOR v19.7.9")
    print("=" * 50)
    
    files = sys.argv[1:] if len(sys.argv) > 1 else list(Path('.').glob('*.xml'))
    
    if not files:
        print("No files to validate!")
        return 1
    
    all_valid = True
    for filepath in files:
        print(f"\nChecking: {filepath}")
        valid, results = validate_xml_structure(filepath)
        for result in results:
            print(f"  {result}")
        all_valid = all_valid and valid
    
    print("\n" + "=" * 50)
    if all_valid:
        print("✅ ALL CHECKS PASSED - Ready for upload!")
        return 0
    else:
        print("❌ PROBLEMS FOUND - Fix before uploading")
        return 1

if __name__ == "__main__":
    sys.exit(main())
