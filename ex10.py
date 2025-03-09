import pytest


def test_phrase_length():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"Phrase is too long: {len(phrase)} characters"
