#!/usr/bin/env python3
"""
validate_xerex.py - Your Robot Quality Inspector
This checks XEREX documents like a teacher checking homework
"""

import xml.etree.ElementTree as ET
import sys
import hashlib
from pathlib import Path

def validate_behavioral_rules(root):
    """Check if behavioral rules exist and are self-referential"""
    rules = root.find('.//behavioral_rules')
    if not rules:
        return False, "❌ No behavioral_rules found"
    
    rule_count = len(rules)
    if rule_count < 8:
        return False, f"❌ Only {rule_count} rules (need 8+)"
    
    # Check for self-referential rules (like a note that says "read this note")
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
    """Check if we're using space wisely"""
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
    """Main validation function - the robot's brain"""
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
        
        # Check version
        version = root.find('.//current_version')
        if version and version.text == "19.7.9":
            results.append("✓ Version 19.7.9 confirmed")
        else:
            results.append("❌ Wrong version")
            all_valid = False
        
        return all_valid, results
        
    except ET.ParseError as e:
        return False, [f"❌ XML Parse Error: {e}"]

def main():
    """Run the robot inspector on all files"""
    print("=" * 50)
    print("🤖 XEREX ROBOT INSPECTOR v19.7.9")
    print("=" * 50)
    
    # Find all XML files to check
    files = sys.argv[1:] if len(sys.argv) > 1 else Path('.').glob('*v19.7.9.xml')
    
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
    sys.exit(main())#!/usr/bin/env python3
"""
validate_xerex.py - Validates XEREX implementation
Run before each session to ensure compliance
"""

import xml.etree.ElementTree as ET
import sys
import hashlib
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
        
        # Check version
        version = root.find('.//current_version')
        if version and version.text == "19.7.9":
            results.append("✓ Version 19.7.9 confirmed")
        else:
            results.append("❌ Wrong version")
            all_valid = False
        
        return all_valid, results
        
    except ET.ParseError as e:
        return False, [f"❌ XML Parse Error: {e}"]

def main():
    """Validate all XEREX documents"""
    print("=" * 50)
    print("XEREX VALIDATION v19.7.9")
    print("=" * 50)
    
    files = sys.argv[1:] if len(sys.argv) > 1 else Path('.').glob('*v19.7.9.xml')
    
    all_valid = True
    for filepath in files:
        print(f"\nValidating: {filepath}")
        valid, results = validate_xml_structure(filepath)
        for result in results:
            print(f"  {result}")
        all_valid = all_valid and valid
    
    print("\n" + "=" * 50)
    if all_valid:
        sys.exit(main())

