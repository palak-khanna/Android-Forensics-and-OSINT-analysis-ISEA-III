# permission_audit.py

dangerous_permissions = [
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG"
]

def rule_based_flag(permission_list, description):
    flagged = []
    description = description.lower()

    for perm in permission_list:
        if perm in dangerous_permissions:
            if (
                ("camera" not in description and "photo" not in description and "video" not in description and "record" not in description)
                and ("contact" not in description)
                and ("location" not in description and "map" not in description and "weather" not in description)
                and ("sms" not in description and "message" not in description)
                and ("call" not in description)
            ):
                flagged.append(perm)
    return flagged
