import io
import threading
import wave
import sounddevice as sd


SAMPLE_RATE = 16000
MAX_DURATION = 5 * 60  # 5 minutes


def record_audio():
    chunks = [] # List to store audio chunks
    stop_event = threading.Event()

    print("\nPress the Enter key to start recording.")
    input()

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Audio warning: {status}")
        chunks.append(bytes(indata)) # Append the recorded audio chunk to the list

    def wait_for_stop():
        try:
            input()
        except EOFError:
            pass
        finally:
            stop_event.set()

    print("\nRecording audio...")
    print("Press the Enter key again to stop recording.")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=audio_callback,
    ):
        stop_thread = threading.Thread(
            target=wait_for_stop,
            daemon=True,
        )
        stop_thread.start()

        stopped = stop_event.wait(timeout=MAX_DURATION)

    if not stopped:
        print("\nTimeout reached. Stopping recording.")

    audio_data = b"".join(chunks) # Combine all audio chunks into a single byte string

    if not audio_data:
        raise ValueError("No audio was recorded.")

    # Create an in-memory buffer to store the WAV file
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data) # Write the combined audio data to the WAV file

    return buffer.getvalue()
