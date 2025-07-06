import whisper


model_whisper = whisper.load_model("base")

def analyze_lexical(file_path):
    result = model_whisper.transcribe(file_path)
    transcript = result["text"]
    ttr = len(set(transcript.split())) / len(transcript.split())
    return {"transcript": transcript, "type_token_ratio": ttr}
