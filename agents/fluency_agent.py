import re

def analyze_fluency(transcript):
    words = transcript.split()
    fillers = len(re.findall(r'\b(um|uh|like|you know)\b', transcript))
    speech_rate = len(words) / 30.0
    pause_ratio = 0.15
    return {"speech_rate": speech_rate, "fillers": fillers, "pause_ratio": pause_ratio}