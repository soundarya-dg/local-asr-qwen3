import subprocess
import time
import Quartz


V_KEYCODE = 9 # Keycode for the 'V' key in macOS Quartz framework

def copy_text(text: str) -> None:
    subprocess.run(
        ["pbcopy"],
        input=text,
        text=True,
        check=True,
    )


def press_command_v() -> None:
    key_down = Quartz.CGEventCreateKeyboardEvent(
        None, V_KEYCODE, True
    )
    key_up = Quartz.CGEventCreateKeyboardEvent(
        None, V_KEYCODE, False
    )

    for event in (key_down, key_up):
        Quartz.CGEventSetFlags(
            event,
            Quartz.kCGEventFlagMaskCommand,
        )
        Quartz.CGEventPost(
            Quartz.kCGHIDEventTap,
            event,
        )


def insert_text(text: str) -> None:
    if not text:
        return

    copy_text(text)

    # Allow the global shortcut keys to be released.
    time.sleep(0.3)

    press_command_v()
