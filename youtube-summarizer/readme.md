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

- Python 3.8+ and Pipe. Refer below for details. 
- Download [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip). Extract it somewhere and add `<YOUR_PATH>/ffmpeg/bin` folder to your system PATH variable
- Internet access (for downloading YouTube videos and model weights)
- Ollama Running locally. Follow https://www.kdnuggets.com/ollama-tutorial-running-llms-locally-made-super-simple. 
    - Pull `ollama pull llama3.2`. 
    - Run `ollama run llama3.2`
---

## 🚀 Quick Start

### 1.  Install Pyton and Pip on Windows. 
#### Install Python
- Download and install Python from: https://www.python.org/downloads/
- During installation, make sure to check **"Add Python to PATH"** option.


####  Install pip 
- Check if pip is already installed:
  ```bash
  pip --version
  ```
- If not installed run 
```bash 
python -m ensurepip --upgrade
```
---

### 2. Setup

```bash
git clone https://github.com/Gulslabs/learn-gen-ai.git
cd youtube-summarizer
rm -r outputs
python -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
```

### 3. Run
```bash
python.exe .\youtube_summarizer.py
Enter YouTube video URL: https://www.youtube.com/watch?v=LPZh9BOjkQs
```


