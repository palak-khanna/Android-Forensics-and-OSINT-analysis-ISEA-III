import easyocr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

reader = easyocr.Reader(['en'])

def extract_text_easyocr(image_path):
    result = reader.readtext(image_path, detail=0, paragraph=True)
    return " ".join(result).strip()

# Paths to leaked and phone image
leaked_img = "leaked_samples/leaked.png"
phone_img = "phone_images/phone_1_page_1.png"  # <- update this to phone_2.png if needed

# Extract text
leaked_text = extract_text_easyocr(leaked_img)
phone_text = extract_text_easyocr(phone_img)

# Compute similarity
vectorizer = TfidfVectorizer().fit_transform([leaked_text, phone_text])
similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]

print(f"🔍 Similarity between leaked and phone image: {similarity * 100:.2f}%")
