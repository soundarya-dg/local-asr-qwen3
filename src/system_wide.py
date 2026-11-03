import threading
from pynput import keyboard

from .dictation import run_dictation
from .text_inserter import insert_text


HOTKEY = "<ctrl>+<alt>+<space>"

worker = None
stop_event = threading.Event()
state_lock = threading.Lock()


def dictation_worker():
    global worker

    try:
        text = run_dictation(stop_event)

        if text:
            insert_text(text)
            print("Text inserted into the active application.")
        else:
            print("No speech recognized.")

    except Exception as error:
        print(f"Dictation error: {error}")

    finally:
        with state_lock:
            worker = None


def toggle_dictation():
    global worker

    with state_lock:
        if worker is not None:
            stop_event.set()
            return

        stop_event.clear()

        worker = threading.Thread(
            target=dictation_worker,
            daemon=True,
        )
        worker.start()


def main():
    print("Voice typing is active.")
    print("Press Ctrl + Option + Space to start or stop dictation.")
    print("Press Ctrl + C here to exit.")

    with keyboard.GlobalHotKeys({
        HOTKEY: toggle_dictation,
    }) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            stop_event.set()
            listener.stop()


if __name__ == "__main__":
    main()
