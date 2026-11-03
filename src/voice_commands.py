import re
from dataclasses import dataclass


STOP_PATTERN = re.compile(
    r"(?:that's all|that is all|end|stop dictation)"
    r"[.!?]*\s*$",
    re.IGNORECASE,
)


@dataclass
class CommandResult:
    text: str
    should_stop: bool = False


def process_voice_command(text: str) -> CommandResult:
    text = text.strip()

    match = STOP_PATTERN.search(text)

    if match:
        cleaned_text = text[:match.start()].strip()

        return CommandResult(
            text=cleaned_text,
            should_stop=True,
        )

    return CommandResult(text=text)
