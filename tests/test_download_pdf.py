import pytest
from unittest.mock import patch, MagicMock
from scripts.download_pdf import download_pdf, verify_pdf


def test_verify_pdf_valid(tmp_path):
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.4 some content here padding" + b"\0" * 10000)
    assert verify_pdf(str(pdf)) is True


def test_verify_pdf_too_small(tmp_path):
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.4 tiny")
    assert verify_pdf(str(pdf)) is False


def test_verify_pdf_wrong_magic(tmp_path):
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"<html>not a pdf</html>" + b"\0" * 10000)
    assert verify_pdf(str(pdf)) is False


def test_verify_pdf_missing_file():
    assert verify_pdf("/nonexistent/path.pdf") is False


@patch("scripts.download_pdf.requests.get")
def test_download_pdf_success(mock_get, tmp_path):
    pdf_content = b"%PDF-1.4 " + b"\0" * 20000
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.iter_content = MagicMock(return_value=[pdf_content])
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp
    dest = str(tmp_path / "test.pdf")
    result = download_pdf("https://example.com/test.pdf", dest)
    assert result is True
    assert (tmp_path / "test.pdf").exists()


@patch("scripts.download_pdf.requests.get")
def test_download_pdf_failure(mock_get, tmp_path):
    import requests as req
    mock_get.side_effect = req.RequestException("Connection failed")
    dest = str(tmp_path / "test.pdf")
    result = download_pdf("https://example.com/test.pdf", dest)
    assert result is False
