import os
import xml.etree.ElementTree as ET

def extract_permissions_from_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        package_name = root.attrib.get("package", "unknown.package")
        permissions = [
            elem.attrib["{http://schemas.android.com/apk/res/android}name"]
            for elem in root.findall("uses-permission")
        ]
        return {
            "file": os.path.basename(xml_path),
            "package_name": package_name,
            "permissions": permissions
        }
    except Exception as e:
        return {
            "file": os.path.basename(xml_path),
            "package_name": None,
            "permissions": [],
            "error": str(e)
        }

def extract_all_manifests(manifest_dir="manifests"):
    results = []
    for file in os.listdir(manifest_dir):
        if file.endswith(".xml"):
            result = extract_permissions_from_xml(os.path.join(manifest_dir, file))
            results.append(result)
    return results
