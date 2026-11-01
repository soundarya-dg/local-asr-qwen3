
import pytest
from src.transcriber import parse_response


def test_english_transcription():
    text = (
        "The weather is beautiful today, so I am planning to visit the park with my friends."
        "After that, we might have lunch at a nearby restaurant."
    )

    result = parse_response(f"language English<asr_text>{text}")

    assert result.language == "English"
    assert result.text == text


def test_french_transcription():
    text = (
        "Bonjour tout le monde! Aujourd'hui, il fait très beau"
        "et je vais me promener dans le parc avec mes amis."
        "Ensuite, nous allons déjeuner dans un petit restaurant."
    )

    result = parse_response(f"language French<asr_text>{text}")

    assert result.language == "French"
    assert result.text == text


def test_german_transcription():
    text = (
        "Hallo zusammen! Heute ist das Wetter sehr schön. "
        "Ich plane, mit meinen Freunden im Park spazieren zu gehen. "
        "Danach möchten wir in einem Restaurant zu Mittag essen."
    )

    result = parse_response(f"language German<asr_text>{text}")

    assert result.language == "German"
    assert result.text == text


def test_missing_language():
    result = parse_response(
        "<asr_text>Today is a wonderful day to spend time with family and friends."
    )
    assert result.language is None
    assert result.text == "Today is a wonderful day to spend time with family and friends."


def test_invalid_response():
    with pytest.raises(ValueError):
        parse_response("Invalid response")
