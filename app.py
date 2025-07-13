# app.py
from chat_analysis.filters import filter_messages
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from analyzer.file_matcher import FileAuditMatcher
from analyzer.file_reporter import generate_pdf_report
from analyzer.manifest_parser import extract_all_manifests
from analyzer.metadata_loader import load_metadata
from analyzer.permission_audit import rule_based_flag  # placeholder for now

# Directories
leaked_dir = "leaked_samples"
device_dir = "device_files"
data_dir = "data"
os.makedirs(leaked_dir, exist_ok=True)
os.makedirs(device_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

# Streamlit Page
st.set_page_config(page_title="LeakTrace-AI++", layout="wide")
st.title("🔍 LeakTrace-AI++ Forensics Dashboard")

# Sidebar
feature = st.sidebar.radio("📌 Select Analysis Module", [
    "📱 Permission Audit",
    "📂 File Audit System",
    "💬 Chat Leak Analysis"
])

# ------------------------------------------------------------------------------
# 📱 PERMISSION AUDIT
# ------------------------------------------------------------------------------
if feature == "📱 Permission Audit":
    st.subheader("📱 Android Permission Auditing")

    # Load manifest and metadata
    metadata = load_metadata("scraper/simulated_metadata.json")
    results = extract_all_manifests("manifests")
    report = []
    safe_count, flagged_count = 0, 0
    flagged_perm_hist = []

    for app in results:
        pkg = app.get("package_name")
        perms = app.get("permissions", [])
        desc = metadata.get(pkg, "⚠️ Description not found.")
        flagged = rule_based_flag(perms, desc)

        st.markdown(f"### 📦 {pkg or 'Unknown Package'}")
        st.markdown(f"**Permissions Declared:** `{', '.join(perms) if perms else 'None'}`")
        st.markdown(f"**Play Store Description:** {desc}")

        if flagged:
            st.error(f"🚨 Suspicious Permissions: `{', '.join(flagged)}`")
            flagged_count += 1
            flagged_perm_hist.extend(flagged)
        else:
            st.success("✅ No suspicious permissions flagged.")
            safe_count += 1

        report.append({
            "file": app.get("file"),
            "package_name": pkg,
            "permissions": perms,
            "description": desc,
            "flagged": flagged
        })

    # Visual Insights
    st.markdown("---")
    st.header("📊 Visual Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Summary")
        fig1, ax1 = plt.subplots()
        ax1.pie([flagged_count, safe_count], labels=['Flagged', 'Safe'], autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        st.subheader("Common Dangerous Permissions")
        if flagged_perm_hist:
            perm_counts = pd.Series(flagged_perm_hist).value_counts()
            fig2, ax2 = plt.subplots()
            perm_counts.plot(kind='bar', color='tomato', ax=ax2)
            ax2.set_title("Most Frequently Flagged Permissions")
            ax2.set_xlabel("Permission")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)
        else:
            st.info("No flagged permissions found.")

    # Text Report
    report_txt = os.path.join(data_dir, "flagged_report.txt")
    with open(report_txt, "w", encoding="utf-8") as f:
        for r in report:
            f.write(f"App: {r['file']}\n")
            f.write(f"Package: {r['package_name']}\n")
            f.write(f"Permissions: {', '.join(r['permissions'])}\n")
            f.write(f"Description: {r['description']}\n")
            f.write(f"Flagged: {', '.join(r['flagged']) if r['flagged'] else 'None'}\n")
            f.write("-" * 40 + "\n")

    with open(report_txt, "r", encoding="utf-8") as f:
        st.download_button("📥 Download Text Report", f.read(), file_name="flagged_report.txt")

# ------------------------------------------------------------------------------
# 📂 FILE AUDIT SYSTEM
# ------------------------------------------------------------------------------
elif feature == "📂 File Audit System":
    st.subheader("📂 File-Based Leak Detection")

    # Upload files
    leaked_files = st.file_uploader("Upload Leaked Images (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    device_files = st.file_uploader("Upload Device Files (PDF/TXT)", type=["pdf", "txt"], accept_multiple_files=True)

    # Save files
    if leaked_files and device_files:
        if len(leaked_files) != len(device_files):
            st.warning("⚠️ Please upload the same number of leaked and device files for 1-to-1 matching.")
        else:
            for f in leaked_files:
                with open(os.path.join(leaked_dir, f.name), "wb") as out:
                    out.write(f.read())
            for f in device_files:
                with open(os.path.join(device_dir, f.name), "wb") as out:
                    out.write(f.read())

            if st.button("🔍 Run Leak Similarity Audit"):
                matcher = FileAuditMatcher()
                matches = []

                for i in range(len(leaked_files)):
                    leaked = leaked_files[i]
                    device = device_files[i]

                    leaked_path = os.path.join(leaked_dir, leaked.name)
                    device_path = os.path.join(device_dir, device.name)

                    leaked_text = matcher.extract_text(leaked_path)
                    device_text = matcher.extract_text(device_path)

                    if "ERROR" in leaked_text or "ERROR" in device_text:
                        matches.append({
                            "file": leaked.name,
                            "matched_with": device.name,
                            "similarity": 0.0,
                            "text": "",
                            "error": "❌ Failed to extract text from one or both files."
                        })
                        continue

                    score, snippet = matcher.match(leaked_text, device_text)
                    matches.append({
                        "file": leaked.name,
                        "matched_with": device.name,
                        "similarity": round(score * 100, 2),
                        "text": snippet
                    })

                # Show results
                st.markdown("### ✅ Match Results")
                for match in matches:
                    st.markdown(f"#### 📌 Leaked File: `{match['file']}`")
                    st.markdown(f"**Matched With:** `{match['matched_with']}`")
                    st.markdown(f"**Similarity Score:** `{match['similarity']}%`")
                    st.markdown(f"**Matched Snippet:** `{match['text']}`")
                    if match.get("error"):
                        st.error(match["error"])
                    st.markdown("---")

                # Generate PDF Report
                pdf_path = generate_pdf_report(matches, output_path="data/match_report.pdf")
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download PDF Report", f.read(), file_name="match_report.pdf")
    else:
        st.info("📂 Please upload both leaked and device files to start.")

# ------------------------------------------------------------------------------
# 💬 CHAT LEAK ANALYSIS
# ------------------------------------------------------------------------------
elif feature == "💬 Chat Leak Analysis":
    st.header("💬 Chat Log Analyzer")
    st.write("Upload one or more `chat.json` files exported from WhatsApp/Telegram.")

    # File uploader supports multiple chat files
    chat_files = st.file_uploader("📁 Upload Chat File(s) (JSON format)", type=["json"], accept_multiple_files=True)

    # Pre-analyzed emotion detection results from Colab (optional)
    uploaded_chat = "C:/Users/palak/PycharmProjects/Android and OSINT analysis/chat_analysis/example_logs/flagged_chats.json"

    all_messages = []

    if chat_files:
        for uploaded_file in chat_files:
            try:
                messages = json.load(uploaded_file)
                all_messages.extend(messages)
                st.success(f"✅ Successfully loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ Failed to load {uploaded_file.name}: {e}")

        # Load optional emotion-flagged results (from Colab or simulation)
        emotion_data_path = uploaded_chat
        if os.path.exists(emotion_data_path):
            with open(emotion_data_path, "r") as f:
                emotion_results = json.load(f)
            st.success("✅ Pre-analyzed emotion model result loaded.")
        else:
            st.warning("⚠️ Emotion model output not found. Please ensure Colab export exists.")

        # Show flagged emotion messages (if available)
        if emotion_results:
            st.subheader("🚨 Emotion-Flagged Messages")
            for msg in emotion_results:
                st.markdown(f"🧠 **{msg['sender']}** at `{msg['timestamp']}`")
                st.markdown(f"> {msg['message']}")
                st.markdown(f"⚠️ **Emotion Detected:** `{msg['emotion'].upper()}` (Confidence: `{msg['confidence']*100:.1f}%`)")
                st.markdown("---")

        # Add Filters for Search
        st.subheader("🔍 Chat Filters")
        keyword = st.text_input("🔑 Keyword Search")
        contact = st.text_input("📞 Sender/Contact")
        date = st.date_input("📅 Filter by Date", format="YYYY-MM-DD")
        filetype = st.text_input("📁 File Type (e.g., pdf, docx, xlsx)")

        # Filter Logic Execution
        if st.button("Apply Filters"):
            # Call your filter function here
            filtered_msgs, logs = filter_messages(all_messages,
                                                  keyword=keyword,
                                                  contact=contact,
                                                  date=str(date) if date else None,
                                                  filetype=filetype)
            if filtered_msgs:
                st.success(f"✅ {len(filtered_msgs)} messages matched your filters.")

                for log in logs:
                    st.markdown(f"🕒 `{log['timestamp']}` | 👤 **{log['sender']}**")
                    st.markdown(f"> {log['message']}")
                    st.markdown(f"📌 Match Reasons: {log['reason']}")
                    st.markdown("---")
            else:
                st.warning("⚠️ No messages matched the applied filters.")
    else:
        st.info("📂 Please upload at least one chat JSON file to begin analysis.")
