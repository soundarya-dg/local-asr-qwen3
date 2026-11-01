import requests

from .audio import record_audio
from .transcriber import transcribe_audio


def main():
    print("\nTranscribing speech using Qwen3-ASR 0.6B")

    try:
        audio = record_audio()
        result = transcribe_audio(audio)

        print()

        if result.language:
            print(f"Language: {result.language}")

        if result.text:
            print(f"Transcription: {result.text}")
        else:
            print("No speech recognized.")

    except KeyboardInterrupt:
        print("\nRecording cancelled.")

    except requests.RequestException as error:
        print(f"\nOllama connection error: {error}")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
