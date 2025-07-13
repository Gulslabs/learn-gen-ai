# youtube_summarizer.py
import os
import subprocess
import whisper
from transformers import pipeline
import warnings
import requests
import json
# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore", category=UserWarning)
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def ensure_output_folder(folder):
    os.makedirs(folder, exist_ok=True)

def get_tittle_from_url(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        info = json.loads(result.stdout)
        return info.get("title", "YouTube Video")
    except Exception as e:
        print(f"Error getting video title from yt-dlp: {e}")
        return "YouTube Video"

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

def summarize_with_ollama(transcript):
    print("Generating structured markdown summary with LLaMA 3 via Ollama...")
    prompt = (
        "Create a clean, structured Markdown summary of the following transcript.\n"
        "Include a title, overview, key sections as headings with bullet points, specific details worth highlighting,\n"
        "and a timeline breakdown if you detect one.\n\n"
        f"Transcript:\n{transcript}"
    )

    response = requests.post(OLLAMA_ENDPOINT, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["response"]


def save_markdown_summary(title, url, markdown_summary, output_folder="outputs"):
    markdown_path = os.path.join(output_folder, "summary.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(f"# 📽️ Video Summary: {title}\n\n")
        f.write(f"**🔗 YouTube Link:** {url}\n\n")
        f.write("---\n\n")
        f.write(markdown_summary.strip() + "\n")
    return markdown_path


def process_youtube_video(url, model_size="base", output_folder="outputs"):
    print("\n🔽 Step 1: Downloading audio from YouTube")
    audio_path = download_audio(url, output_folder=output_folder)

    print("\n🧠 Step 2: Transcribing with Whisper")
    transcript = transcribe_audio(audio_path, model_size)

    transcript_path = os.path.join(output_folder, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

   # print("\n✂️ Step 3: Summarizing transcript")
    # summary = summarize_text(transcript)
    
    print("\n✂️ Step 3: Generating markdown summary")
    markdown_summary = summarize_with_ollama(transcript)
    
    markdown_path = save_markdown_summary(get_tittle_from_url(url), url, markdown_summary, output_folder)

    print("\n✅ Done! Markdown summary saved to:")
    print("📁", markdown_path)
    return transcript, markdown_summary

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    process_youtube_video(url, output_folder="outputs")
    #print(get_tittle_from_url(url))
