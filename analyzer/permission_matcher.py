# analyzer/permission_matcher.py

import re

def match_permissions_to_description(perms, desc):
    desc = desc.lower()
    flagged = []

    keywords = {
        "CAMERA": ["camera", "photo", "scan"],
        "RECORD_AUDIO": ["voice", "record", "audio", "mic"],
        "LOCATION": ["map", "gps", "location", "nearby"],
        "CONTACTS": ["contact", "sync", "invite"],
        "READ_SMS": ["otp", "sms"],
        "STORAGE": ["save", "download", "upload", "file"],
    }

    for perm in perms:
        base = perm.upper().split(".")[-1]
        if base in keywords:
            if not any(word in desc for word in keywords[base]):
                flagged.append(base)

    return flagged
