import json
import os

BASELINE_DIR = "baseline_profiles"
os.makedirs(BASELINE_DIR, exist_ok=True)

def save_baseline(speaker_id, profile):
    with open(f"{BASELINE_DIR}/{speaker_id}.json", "w") as f:
        json.dump(profile, f)

def load_baseline(speaker_id):
    try:
        with open(f"{BASELINE_DIR}/{speaker_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def detect_deviation(speaker_id, current_profile):
    baseline = load_baseline(speaker_id)
    if not baseline:
        save_baseline(speaker_id, current_profile)
        return {"status": "baseline saved", "deviation": {}}

    deviation = {}
    for key in current_profile:
        if isinstance(current_profile[key], (int, float)):
            diff = abs(current_profile[key] - baseline.get(key, 0))
            deviation[key] = diff
        elif isinstance(current_profile[key], dict):
            sub_deviation = {k: abs(current_profile[key][k] - baseline.get(key, {}).get(k, 0)) for k in current_profile[key]}
            deviation[key] = sub_deviation

    return {"status": "deviation detected", "deviation": deviation}
