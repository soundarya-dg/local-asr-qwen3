import pytest

from src.voice_commands import process_voice_command


@pytest.mark.parametrize(
    "text, expected_text, should_stop",
    [
        (
            "Could you review my pull request before the deployment?",
            "Could you review my pull request before the deployment?",
            False,
        ),
        (
            "Explain the difference between RAG and fine-tuning. That's all.",
            "Explain the difference between RAG and fine-tuning.",
            True,
        ),
        (
            "Please schedule the deployment for tomorrow morning. End.",
            "Please schedule the deployment for tomorrow morning.",
            True,
        ),
        (
            "Summarize the API documentation.",
            "Summarize the API documentation.",
            True,
        ),
        (
            "  Can you explain how embeddings work? THAT'S ALL!  ",
            "Can you explain how embeddings work?",
            False,
        ),
        (
            "That's all.",
            "",
            True,
        ),
        (
            "",
            "",
            False,
        ),
    ],
)
def test_voice_commands(text, expected_text, should_stop):
    result = process_voice_command(text)

    assert result.text == expected_text
    assert result.should_stop == should_stop
