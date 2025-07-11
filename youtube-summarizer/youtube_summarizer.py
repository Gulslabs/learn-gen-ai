# youtube_summarizer.py

import os
import subprocess
import whisper
from transformers import pipeline
import warnings

# Suppress FP16 warning
warnings.filterwarnings("ignore", category=UserWarning)

def download_audio(youtube_url, output_filename="audio.mp3", ffmpeg_path=None):
    print("Using yt-dlp to download audio...")
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_filename,
        youtube_url
    ]
    if ffmpeg_path:
        command.insert(-2, "--ffmpeg-location")
        command.insert(-2, ffmpeg_path)

    subprocess.run(command, check=True)
    return output_filename

def transcribe_audio(file_path, model_size="base"):
    print(f"Loading Whisper model ({model_size})...")
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result['text']

def summarize_text(text, max_chunk=1000):
    print("Initializing summarization pipeline...")
    summarizer = pipeline("summarization")
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

def process_youtube_video(url, model_size="base", ffmpeg_path=None):
    print("\n🔽 Step 1: Downloading audio from YouTube")
    audio_path = download_audio(url, ffmpeg_path=ffmpeg_path)

    print("\n🧠 Step 2: Transcribing with Whisper")
    transcript = transcribe_audio(audio_path, model_size)
    
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print("\n✂️ Step 3: Summarizing transcript")
    summary = summarize_text(transcript)  

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("\n✅ Done! Transcript and summary saved as transcript.txt and summary.txt")
    return transcript, summary

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    ffmpeg_dir = "./outputs"  # Optionally set to "C:/ffmpeg/bin" if not in PATH
    process_youtube_video(url, ffmpeg_path=ffmpeg_dir)
