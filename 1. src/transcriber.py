import os
import base64
from dataclasses import dataclass
import requests
from dotenv import load_dotenv


load_dotenv()

# Load environment variables for Ollama API URL and model name
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not OLLAMA_URL or not MODEL_NAME:
    raise ValueError(
        "Ollama API URL or model name is missing in the environment variables."
    )


@dataclass
class TranscriptionResult:
    text: str # The transcribed text from the audio
    language: str | None = None # Detects the language of the transcribed text


# Parses the response content from the Ollama API and returns a TranscriptionResult object.
def parse_response(content: str) -> TranscriptionResult:
    if "<asr_text>" not in content:
        raise ValueError(
            f"Unexpected model response: {content}"
        )

    metadata, text = content.split("<asr_text>", 1)

    language = None
    metadata = metadata.strip()

    if metadata.lower().startswith("language "):
        language = metadata[9:].strip() or None

    text = text.replace("<|im_end|>", "").strip()

    return TranscriptionResult(
        text=text,
        language=language,
    )


# Sends the audio bytes to the Ollama API for transcription and returns the result as a TranscriptionResult object.
def transcribe_audio(audio_bytes: bytes) -> TranscriptionResult:
    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": "",
                "images": [encoded_audio],
            }
        ],
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180,
    )
    response.raise_for_status()

    content = response.json()["message"]["content"]

    return parse_response(content)
