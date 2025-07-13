from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import easyocr
import PyPDF2
import os

class FileAuditMatcher:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.vectorizer = TfidfVectorizer()  # ✅ Make sure this is here!

    def extract_text(self, filepath):
        ext = os.path.splitext(filepath)[-1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            result = self.reader.readtext(filepath, detail=0)
            return " ".join(result)
        elif ext == ".pdf":
            try:
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    return " ".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                return f"ERROR: {str(e)}"
        elif ext == ".txt":
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"ERROR: {str(e)}"
        else:
            return ""

    def match(self, text1, text2):
        if not text1 or not text2:
            return 0.0, ""
        vectors = self.vectorizer.fit_transform([text1, text2])  # ✅ Now it works!
        score = cosine_similarity(vectors[0], vectors[1])[0][0]
        words1 = text1.split()
        words2 = text2.split()
        snippet = " ".join(words1[:20] + ["..."] + words2[:20])
        return score, snippet
