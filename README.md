# FORANDROID: AI-Augmented Android Privacy Audit & Leak Attribution Engine

## 🔍 Overview

**FORANDROID** is a modular, AI-powered forensic toolkit that empowers investigators, security analysts, and researchers to perform comprehensive privacy audits and data leak attribution on Android devices. The system is designed for both simulated and real-world environments and enables structured, explainable, and reproducible digital forensics workflows.

This repository covers **Module 1** of the project, which includes:

- 📱 AndroidManifest Permission Analyzer
- 🕵️ Leak Similarity Auditor (OCR + TF-IDF)
- 💬 Chat Log Intelligence Engine (NLP-powered)
- 🖥️ Streamlit-based Interactive Forensic Dashboard

---
### 📺 Live Demo

![App Demo]([https://raw.githubusercontent.com/yourusername/yourrepo/main/demo.gif](https://github.com/palak-khanna/Android-Forensics-and-OSINT-analysis-ISEA-III/blob/EDA-AIML/implementation_rec.gif))

---
## 📂 Project Structure

```bash
FORANDROID-Module1/
│
├── app.py # Streamlit main UI
├── requirements.txt # Python dependencies
├── utils/
│ ├── permission_analyzer.py # Manifest parsing & AI risk flagging
│ ├── leak_detector.py # OCR + similarity matching
│ ├── chat_parser.py # NLP-based Telegram/WhatsApp parser
│ └── file_utils.py # File loaders, format handlers
│
├── sample_data/
│ ├── manifests/ # Sample APK/manifest files
│ ├── leaks/ # Screenshots or leaked files
│ ├── internal_docs/ # Known device-side documents
│ ├── chat_exports/ # WhatsApp/Telegram exported chat logs
│
├── models/
│ ├── tfidf_vectorizer.pkl # TF-IDF trained model for document matching
│ └── bert_model/ # Pretrained NLP model
│
├── reports/
│ └── sample_output.pdf # Auto-generated audit report
└── README.md
```


---

## 🚀 Features

### 📱 AndroidManifest Permission Analyzer
- Parses `AndroidManifest.xml` from apps or Google Play scraping
- Detects risky permission combinations (e.g., `CAMERA + LOCATION + INTERNET`)
- Rule-based AI engine flags over-privileged or stalkerware-like apps
- Supports both local APKs and ADB-pulled manifests

### 📸 Leak Similarity Auditor
- Uses **EasyOCR** to extract text from suspected leaked images or PDFs
- Uses **TF-IDF + cosine similarity** to match against internal documents
- Ranks possible leak origins with confidence scores
- Supports multiple languages and noisy text

### 💬 Chat Log Intelligence Engine
- Parses exported **WhatsApp `.txt`** and **Telegram `.json`/.html** chats
- Applies **BERT/NLP-based context reconstruction** to detect:
  - Suspicious messages, transfers, attachments
  - Temporal anomalies
- Allows filtering by date, keyword, sender, file type

### 🖥️ Unified Streamlit Dashboard
- Upload and analyze artefacts from one place
- Switch between modules with ease
- View results, flags, and reports interactively
- Export PDF/CSV logs for legal and audit records

---

## ⚙️ Installation

### 🔧 Prerequisites

- Python 3.8+
- pip
- Git
- FFmpeg (for chat/audio/video if needed)

### 📦 Setup Steps

```bash
git clone https://github.com/yourusername/FORANDROID-Module1.git
cd FORANDROID-Module1

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### ▶️ Running the App
```bash
streamlit run app.py
```
Once launched, the Streamlit UI will open in your default browser. From there, you can upload manifest files, leaked images, chat logs, and documents.

### 📡 Real-Device Compatibility
If you wish to pull artefacts from a real Android phone:

1) Enable USB Debugging on the device.
2) Connect via USB and run:
```bash
adb devices                # Verify connection
adb pull /sdcard/WhatsApp/Databases/
adb pull /sdcard/Telegram/
adb shell pm list packages -f  # To list installed APKs
```
3) Place pulled artefacts into appropriate folders (e.g., sample_data/) and use the app.

### 🧠 Architecture Overview
1) Backend: Python + Scikit-learn + EasyOCR + HuggingFace Transformers
2) Frontend: Streamlit
3) Storage: Local SQLite/CSV/PDF export
4) Deployment: Desktop or VM-ready, supports integration with forensic pipelines

### 📚 Use Cases
1) Corporate device audits
2) Insider leak investigations
3) Stalkerware/spyware detection
4) Mobile app permission risk assessments
5) Journalistic & whistleblower protection forensics

### 🧩 Future Enhancements (Roadmap)
DNS Traffic Logger via VPNService

Network reputation scoring

Auto-identification of hidden apps

App metadata scraper from Play Store

WhatsApp decryption support (with key)
