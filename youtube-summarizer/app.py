# app.py
import gradio as gr
from youtube_summarizer import process_youtube_video

def handle_input(url):
    try:
        transcript, summary = process_youtube_video(url)
        return transcript, summary
    except Exception as e:
        return f"Error: {str(e)}", ""

iface = gr.Interface(
    fn=handle_input,
    inputs=gr.Textbox(label="YouTube Video URL", placeholder="Paste a YouTube video link here..."),
    outputs=[
        gr.Textbox(label="Full Transcript", lines=20),
        gr.Textbox(label="Summarized Text", lines=10)
    ],
    title="🎙️ YouTube Video Summarizer",
    description="This tool downloads audio from a YouTube video, transcribes it with Whisper, and summarizes it using HuggingFace Transformers. 100% local & free. Make sure ffmpeg and yt-dlp are installed.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()
