from datetime import datetime
import re

def filter_messages(messages, keyword=None, contact=None, date=None, filetype=None):
    results = []
    logs = []

    for msg in messages:
        matched = False
        reasons = []

        # Keyword check
        if keyword and keyword.lower() in msg["message"].lower():
            matched = True
            reasons.append(f"🟨 Keyword matched: '{keyword}'")

        # Contact check
        if contact and contact.lower() == msg["sender"].lower():
            matched = True
            reasons.append(f"📞 Sender matched: '{contact}'")

        # Date check
        if date:
            msg_date = datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S").date()
            if msg_date == datetime.strptime(date, "%Y-%m-%d").date():
                matched = True
                reasons.append(f"📅 Date matched: {date}")

        # Filetype check
        if filetype:
            pattern = rf"\b\w+\.{filetype}\b"
            if re.search(pattern, msg["message"], re.IGNORECASE):
                matched = True
                reasons.append(f"📁 Filetype matched: .{filetype}")

        if matched:
            results.append(msg)
            logs.append({
                "timestamp": msg["timestamp"],
                "sender": msg["sender"],
                "reason": ", ".join(reasons),
                "message": msg["message"]
            })

    return results, logs
