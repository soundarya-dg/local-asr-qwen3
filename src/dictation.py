import io
import threading
import time
import wave
import sounddevice as sd

from .transcriber import transcribe_audio
from .voice_commands import process_voice_command


SAMPLE_RATE = 16000
CHUNK_DURATION = 5
MAX_DURATION = 5 * 60


def create_wav(audio_data: bytes) -> bytes:
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(audio_data)

    return buffer.getvalue()


def run_dictation(stop_event: threading.Event) -> str:
    audio_buffer = bytearray()
    buffer_lock = threading.Lock()
    transcriptions = []
    started = time.monotonic()
    last_chunk = started
    voice_stop = False

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Audio warning: {status}")

        with buffer_lock:
            audio_buffer.extend(bytes(indata))

    def take_audio():
        with buffer_lock:
            data = bytes(audio_buffer)
            audio_buffer.clear()
        return data

    def transcribe_chunk(data: bytes) -> bool:
        if not data:
            return False

        result = transcribe_audio(create_wav(data))
        command = process_voice_command(result.text)

        if command.text:
            transcriptions.append(command.text)

        return command.should_stop

    print("Listening. Press the shortcut again to stop.")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=audio_callback,
    ):
        while not stop_event.is_set():
            now = time.monotonic()

            if now - started >= MAX_DURATION:
                print("Recording limit reached.")
                break

            if now - last_chunk >= CHUNK_DURATION:
                audio_data = take_audio()
                last_chunk = now

                if transcribe_chunk(audio_data):
                    voice_stop = True
                    break

            time.sleep(0.1)

    if not voice_stop:
        remaining_audio = take_audio()

        if remaining_audio:
            transcribe_chunk(remaining_audio)

    return " ".join(transcriptions).strip()
