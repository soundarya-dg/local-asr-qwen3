# Local ASR with Qwen3

A local speech-to-text application using **Qwen3-ASR 0.6B** and **Ollama** on macOS.

The application records audio from your microphone, transcribes speech locally, and displays the recognized text and detected language.

## Features

- Offline speech-to-text using Qwen3-ASR 0.6B
- Supports multiple languages
- Automatic language detection when provided by the model
- Microphone recording using Python
- No API key required

## Project Structure

```text
local-asr-qwen3/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── audio.py
│   └── transcriber.py
├── tests/
│   └── test_transcriber.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Setup

### 1. Install Ollama

Download and install [Ollama](https://ollama.com).

### 2. Download the model

```bash
ollama pull frozenlab/qwen3-asr:0.6b
```

### 3. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/local-asr-qwen3.git
cd local-asr-qwen3
```

### 4. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -e ".[dev]"
```

### 6. Configure environment variables

Create a `.env` file in the project root with:

```env
OLLAMA_URL=http://127.0.0.1:11434/api/chat
MODEL_NAME=frozenlab/qwen3-asr:0.6b
```

## Usage

Make sure Ollama is running.

```bash
python -m src.main
```

Press Enter to start recording, speak into your microphone, and press Enter again to stop.

## Output

![Terminal output screenshot](image-1.png)

## Notes

- Recording automatically stops after 5 minutes.
- The current version sends the entire recording to the ASR model in one request.
- Audio is processed locally and is not permanently saved.
- Currently, the model supports 30 languages (including English, German, Spanish, French, and Italian). For the full list of supported languages, check the official [Qwen3-ASR repository](https://github.com/QwenLM/Qwen3-ASR).