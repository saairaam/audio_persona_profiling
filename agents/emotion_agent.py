from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def predict_emotion(transcript):
    scores = emotion_classifier(transcript[:512])[0]
    score_dict = {item['label'].lower(): item['score'] for item in scores if item['label'].lower() in ['joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise']}
    valence = score_dict.get("joy", 0.0) - score_dict.get("sadness", 0.0)
    arousal = score_dict.get("anger", 0.0) + score_dict.get("surprise", 0.0)
    dominance = score_dict.get("joy", 0.0) + score_dict.get("anger", 0.0)
    label = max(score_dict, key=score_dict.get) if score_dict else "neutral"
    return {
        "valence": round(valence, 3),
        "arousal": round(arousal, 3),
        "dominance": round(dominance, 3),
        "label": label
    }