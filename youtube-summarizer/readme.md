# 🎙️ YouTube Video Summarizer

This project allows you to:
- Download audio from a YouTube video
- Transcribe the audio using OpenAI Whisper
- Summarize the content using Hugging Face Transformers
- All through a simple **web interface (Gradio)** or **CLI**

---



## 💡 Features

✅ Automatic download and conversion of YouTube audio  
✅ Accurate speech-to-text transcription (Whisper)  
✅ Concise summarization (Transformer-based models)  
✅ Easy-to-use Web UI (via Gradio)  
✅ 100% Free and local processing — no API keys required

---

---

## ⚙️ Requirements

- Python 3.8+ and Pipe
- Download [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip). Extract it somewhere and add `ffmpeg/bin` folder to your system PATH
- Internet access (for downloading YouTube videos and model weights)

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/youtube-summarizer.git
python -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
cd youtube-summarizer
python.exe .\youtube_summarizer.py
Enter YouTube video URL: https://www.youtube.com/watch?v=LPZh9BOjkQs&t=6s
```

