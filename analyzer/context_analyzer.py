# analyzer/context_analyzer.py

import json
import joblib

def load_local_model(model_path="models/chat_context_model.pkl"):
    return joblib.load(model_path)

def analyze_chat(chat_path, model):
    with open(chat_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    flagged = []
    for msg in data:
        try:
            prediction = model(msg["message"])[0]  # already returns label, score
            if prediction["label"] in ["anger", "fear", "surprise"] and prediction["score"] > 0.7:
                flagged.append({
                    **msg,
                    "emotion": prediction["label"],
                    "confidence": round(prediction["score"], 2)
                })
        except Exception as e:
            print("Prediction error:", e)
            continue
    return flagged
