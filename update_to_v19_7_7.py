#!/usr/bin/env python3
"""
Updates all XEREX XML files to v19.7.7
Mac-compatible, handles special characters properly
"""

import os
import glob

def update_file(filepath):
    """Update a single XML file to v19.7.7"""
    print(f"Updating {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace version numbers
    content = content.replace('19.7.6', '19.7.7')
    
    # Fix context formula (handle various formats)
    old_formulas = [
        '(Characters ÷ 800,000) × 100 - 25%',
        'Characters ÷ 800,000',
        'Characters / 800,000'
    ]
    new_formula = '(input_tokens + output_tokens) / 200,000 × 100'
    
    for old in old_formulas:
        content = content.replace(old, new_formula)
    
    # Fix Rule #6
    content = content.replace("Catch Scott's mistakes", "Catch mistakes proactively")
    
    # Fix Personal Preferences rule count (add 8th rule if needed)
    if 'personal_preferences' in filepath and '<rule_7>' in content and '<rule_8>' not in content:
        # Add the missing 8th rule before </behavioral_rules>
        content = content.replace('</behavioral_rules>', 
            '<rule_8>-2% trust if ANY rule not displayed</rule_8>\n</behavioral_rules>')
    
    # Write updated content
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Updated to v19.7.7")
    return True

def main():
    """Update all XML files"""
    files = glob.glob('*_v19.7.6.xml')
    
    if not files:
        print("No v19.7.6 XML files found!")
        return
    
    print(f"Found {len(files)} files to update\n")
    
    for filepath in files:
        update_file(filepath)
    
    print("\n✅ All files updated to v19.7.7!")
    print("\nNow run: python3 validate_xerex.py *.xml")

if __name__ == "__main__":
    main()#!/usr/bin/env python3
"""
Updates all XEREX XML files to v19.7.7
Mac-compatible, handles special characters properly
"""

import os
import glob

def update_file(filepath):
    """Update a single XML file to v19.7.7"""
    print(f"Updating {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace version numbers
    content = content.replace('19.7.6', '19.7.7')
    
    # Fix context formula (handle various formats)
    old_formulas = [
        '(Characters ÷ 800,000) × 100 - 25%',
        'Characters ÷ 800,000',
        'Characters / 800,000'
    ]
    new_formula = '(input_tokens + output_tokens) / 200,000 × 100'
    
    for old in old_formulas:
        content = content.replace(old, new_formula)
    
    # Fix Rule #6
    content = content.replace("Catch Scott's mistakes", "Catch mistakes proactively")
    
    # Fix Personal Preferences rule count (add 8th rule if needed)
    if 'personal_preferences' in filepath and '<rule_7>' in content and '<rule_8>' not in content:
        # Add the missing 8th rule before </behavioral_rules>
        content = content.replace('</behavioral_rules>', 
            '<rule_8>-2% trust if ANY rule not displayed</rule_8>\n</behavioral_rules>')
    
    # Write updated content
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Updated to v19.7.7")
    return True

def main():
    """Update all XML files"""
    files = glob.glob('*_v19.7.6.xml')
    
    if not files:
        print("No v19.7.6 XML files found!")
        return
    
    print(f"Found {len(files)} files to update\n")
    
    for filepath in files:
        update_file(filepath)
    
    print("\n✅ All files updated to v19.7.7!")
    print("\nNow run: python3 validate_xerex.py *.xml")

if __name__ == "__main__":
    main()
