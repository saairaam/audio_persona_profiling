from sklearn.linear_model import LogisticRegression
import numpy as np

# Dummy model initialization (for testing purposes)
model = LogisticRegression()
model.classes_ = np.array(["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"])
model.coef_ = np.random.rand(5, 10)
model.intercept_ = np.random.rand(5)
model.n_features_in_ = 10

def classify_personality(features, lexical, fluency):
    vector = features.get("mfcc", [])[:5] + [
        features.get("pitch", 0), features.get("energy", 0),
        fluency.get("speech_rate", 0), fluency.get("fillers", 0), fluency.get("pause_ratio", 0),
        lexical.get("type_token_ratio", 0)
    ]
    vector = (vector + [0] * 10)[:10]
    X = np.array(vector).reshape(1, -1)
    probs = model.predict_proba(X)[0].tolist()
    return {str(k): v for k, v in zip(model.classes_, probs)}
