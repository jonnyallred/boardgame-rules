import pytest
from scripts.extract_pdf import clean_text

# Note: We can't test PDF extraction without actual PDFs.
# These tests cover the text cleaning logic.

def test_clean_text_removes_page_numbers():
    text = "Some rules text\n\n42\n\nMore rules text"
    cleaned = clean_text(text)
    assert "\n42\n" not in cleaned
    assert "Some rules text" in cleaned
    assert "More rules text" in cleaned


def test_clean_text_removes_headers_footers():
    text = "© 2024 KOSMOS\nSome rules\n© 2024 KOSMOS\nMore rules\n© 2024 KOSMOS"
    cleaned = clean_text(text)
    assert cleaned.count("© 2024 KOSMOS") <= 1


def test_clean_text_normalizes_whitespace():
    text = "Rules   text   here\n\n\n\n\nMore text"
    cleaned = clean_text(text)
    assert "Rules text here" in cleaned
    assert "\n\n\n" not in cleaned


def test_clean_text_preserves_content():
    text = "Players: 3-4\nTime: 60 minutes\n\nSetup: Place the board in the center."
    cleaned = clean_text(text)
    assert "Players: 3-4" in cleaned
    assert "Time: 60 minutes" in cleaned
    assert "Setup: Place the board in the center." in cleaned
