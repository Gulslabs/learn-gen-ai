# youtube_summarizer.py

import os
import subprocess
import whisper
from transformers import pipeline
import warnings

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore", category=UserWarning)

def ensure_output_folder(folder):
    os.makedirs(folder, exist_ok=True)

def download_audio(youtube_url, output_folder="outputs", output_filename="audio.mp3"):
    print("Using yt-dlp to download audio...")
    ensure_output_folder(output_folder)
    output_path = os.path.join(output_folder, output_filename)

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_path,
        youtube_url
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("\n❌ yt-dlp failed!")
        print("Command:", ' '.join(command))
        print("Error Output:\n", e.stderr)
        raise

    return output_path

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

def process_youtube_video(url, model_size="base", output_folder="outputs"):
    print("\n🔽 Step 1: Downloading audio from YouTube")
    audio_path = download_audio(url, output_folder=output_folder)

    print("\n🧠 Step 2: Transcribing with Whisper")
    transcript = transcribe_audio(audio_path, model_size)

    transcript_path = os.path.join(output_folder, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print("\n✂️ Step 3: Summarizing transcript")
    summary = summarize_text(transcript)

    summary_path = os.path.join(output_folder, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print("\n✅ Done! Files saved in:")
    print("Transcript:", transcript_path)
    print("Summary:", summary_path)
    return transcript, summary

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    process_youtube_video(url, output_folder="outputs")
