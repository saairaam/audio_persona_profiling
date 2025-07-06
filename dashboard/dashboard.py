# dashboard.py
import librosa
import matplotlib.pyplot as plt
import numpy as np
from agents.acoustic_agent import extract_acoustic_features
from agents.lexical_agent import analyze_lexical
from agents.fluency_agent import analyze_fluency
from agents.emotion_agent import predict_emotion
from agents.personality_agent import classify_personality
import os
from dotenv import load_dotenv

load_dotenv()

def plot_dashboard(file_path):
    y, sr = librosa.load(file_path)
    duration = librosa.get_duration(y=y, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    features = extract_acoustic_features(file_path)
    lexical = analyze_lexical(file_path)
    transcript = lexical.get("transcript", "")
    fluency = analyze_fluency(transcript)
    emotion = predict_emotion(transcript)
    personality = classify_personality(features, lexical, fluency)

    fig, axs = plt.subplots(2, 3, figsize=(18, 10))

    labels = list(personality.keys())
    values = [max(0.001, float(v)) for v in personality.values()]
    log_values = [np.log10(v) for v in values]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    log_values += log_values[:1]
    angles += angles[:1]

    ax_radar = fig.add_subplot(131, polar=True)
    ax_radar.plot(angles, log_values, color="blue", linewidth=2)
    ax_radar.fill(angles, log_values, color="skyblue", alpha=0.4)
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(labels)
    ax_radar.set_title("Personality (Radar, log scale)")
    ax_radar.set_yticklabels([])

    axs[0, 1].bar(["valence", "arousal", "dominance"], [emotion["valence"], emotion["arousal"], emotion["dominance"]], color="salmon")
    axs[0, 1].set_ylim(0, 1)
    axs[0, 1].set_title(f"Emotion: {emotion['label'].capitalize()}")

    axs[0, 2].bar(fluency.keys(), fluency.values(), color="seagreen")
    axs[0, 2].set_ylim(0, max(fluency.values()) * 1.5)
    axs[0, 2].set_title("Fluency Metrics")

    axs[1, 0].plot(np.linspace(0, duration, len(y)), y)
    axs[1, 0].set_title("Waveform")

    img = axs[1, 1].imshow(D, aspect='auto', origin='lower', cmap='viridis')
    axs[1, 1].set_title("Spectrogram")
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Frequency")
    fig.colorbar(img, ax=axs[1, 1])

    axs[1, 2].axis('off')
    axs[1, 2].text(0, 0.5, f"Transcript:{transcript}", fontsize=10, wrap=True)

    plt.tight_layout()

    # Sentiment timeline graph (word-level valence approximation)
    words = transcript.split()
    chunks = [" ".join(words[i:i+20]) for i in range(0, len(words), 20)]
    valences = [predict_emotion(chunk)["valence"] for chunk in chunks]
    plt.figure(figsize=(10, 3))
    plt.plot(range(len(valences)), valences, marker='o', color='purple')
    plt.title("Sentiment (Valence) Over Time")
    plt.xlabel("Chunk Index")
    plt.ylabel("Valence")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sentiment_timeline.png")
    plt.close()
    plt.savefig("dashboard.png")
        # Export metrics as CSV
    import pandas as pd
    df = pd.DataFrame([
        {"Metric": "Pitch", "Value": features.get("pitch", 0)},
        {"Metric": "Energy", "Value": features.get("energy", 0)},
        {"Metric": "Speech Rate", "Value": fluency.get("speech_rate", 0)},
        {"Metric": "Fillers", "Value": fluency.get("fillers", 0)},
        {"Metric": "Pause Ratio", "Value": fluency.get("pause_ratio", 0)},
        {"Metric": "Type-Token Ratio", "Value": lexical.get("type_token_ratio", 0)}
    ] + [
        {"Metric": f"Personality - {k}", "Value": v} for k, v in personality.items()
    ] + [
        {"Metric": f"Emotion - {k}", "Value": v} for k, v in emotion.items() if k != "label"
    ])
    df.to_csv("audio_analysis_summary.csv", index=False)
    plt.close()
    # Save MFCC heatmap
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.feature.mfcc(y=y, sr=sr), x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.savefig("mfcc_heatmap.png")
    plt.close()
     # Optionally zip all outputs
    import zipfile
    with zipfile.ZipFile("analysis_outputs.zip", "w") as zipf:
        zipf.write("dashboard.png")
        zipf.write("audio_analysis_summary.csv")
        zipf.write("mfcc_heatmap.png")
        zipf.write("sentiment_timeline.png")

    df_data = df.values.tolist()
    from fpdf import FPDF
    from openai import OpenAI
    prompt = f"""
    You are a clinical psychologist. Provide a detailed psychological interpretation based on the following:
    
    Transcript: {transcript}
    
    Features:
    Pitch: {features['pitch']:.2f} Hz
    Energy: {features['energy']:.6f}
    Speech Rate: {fluency['speech_rate']:.2f} wps
    Fillers: {fluency['fillers']}
    Pause Ratio: {fluency['pause_ratio']*100:.1f}%
    Emotion: {emotion['label']} (Valence: {emotion['valence']}, Arousal: {emotion['arousal']}, Dominance: {emotion['dominance']})
    Personality: {personality}
    
    Respond as a professional psychologist with clinical insight.
    """
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    summary = response.choices[0].message.content

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    cleaned_summary = summary.encode("latin-1", "replace").decode("latin-1")
    for line in cleaned_summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output("expert_summary.pdf")

    return ["sentiment_timeline.png", "dashboard.png", "mfcc_heatmap.png", df_data, transcript, "expert_summary.pdf"]