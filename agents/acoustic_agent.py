# acoustic_agent.py
import librosa

def extract_acoustic_features(file_path):
    y, sr = librosa.load(file_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr).mean(axis=1).tolist()
    pitch = librosa.yin(y, fmin=50, fmax=300).mean()
    energy = float(sum(y**2) / len(y))
    return {"mfcc": mfcc, "pitch": pitch, "energy": energy}