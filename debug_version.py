import xml.etree.ElementTree as ET

files = ["audit_center_v19.7.8.xml", "pattern_engine_v19.7.8.xml"]

for filepath in files:
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Try different ways to find current_version
        v1 = root.find('./current_version')
        v2 = root.find('.//current_version')
        v3 = root.find('current_version')
        
        print(f"\n{filepath}:")
        print(f"  Direct child: {v1.text if v1 is not None else 'NOT FOUND'}")
        print(f"  Any level: {v2.text if v2 is not None else 'NOT FOUND'}")
        print(f"  Root level: {v3.text if v3 is not None else 'NOT FOUND'}")
        
        # Show what's actually at root level
        print(f"  Root tag: {root.tag}")
        print(f"  Root children: {[child.tag for child in root][:5]}")
        
    except Exception as e:
        print(f"{filepath}: ERROR - {e}")
