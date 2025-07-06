# audio_persona_dashboard.py
import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import librosa
import whisper
import re
from transformers import pipeline
from sklearn.linear_model import LogisticRegression
from dashboard.dashboard import plot_dashboard

# --- Gradio UI ---
with gr.Blocks(title="Audio Persona Profiler", css=".gr-button { background-color: #ff6600; color: white; font-weight: bold; } .gr-textbox { font-family: monospace; }") as interface:
    gr.Markdown("## Upload an audio file to profile personality, emotion, and fluency metrics")
    with gr.Column():
        audio_input = gr.Audio(type="filepath", label="Input Audio")
        def enable_button_if_audio(file):
            return gr.update(interactive=bool(file))
        submit_button = gr.Button("Analyze", interactive=False)
        audio_input.change(fn=enable_button_if_audio, inputs=audio_input, outputs=submit_button)
    with gr.Tabs():
        with gr.Tab("Sentiment Timeline"):
            sentiment_plot = gr.Image(type="filepath", label="Sentiment Over Time")
        with gr.Tab("Persona Dashboard"):
            dashboard_img = gr.Image(type="filepath", label="Personality + Emotion + Fluency")
        with gr.Tab("MFCC Heatmap"):
            mfcc_img = gr.Image(type="filepath", label="MFCC Features")
        with gr.Tab("Summary Table"):
            summary_table = gr.Dataframe(headers=["Metric", "Value"], label="Metrics")
        with gr.Tab("Transcript"):
            transcript_box = gr.Textbox(label="Transcript", lines=10, max_lines=20, interactive=False)
        with gr.Tab("Expert Summary"):
            pdf_report = gr.File(label="Download Expert Summary PDF")
    submit_button.click(fn=plot_dashboard, inputs=audio_input, outputs=[sentiment_plot, dashboard_img, mfcc_img, summary_table, transcript_box, pdf_report], show_progress=True)

if __name__ == "__main__":
    interface.launch()