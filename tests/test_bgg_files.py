import pytest
from scripts.bgg_files import parse_files_page, find_rulebook_files

# Minimal fixture mimicking BGG files page structure.
FILES_HTML = """
<html><body>
<div class="file-list">
  <div class="file-row">
    <a href="/filepage/12345/catan-rules-english" class="file-link">Catan Rules (English)</a>
    <span class="file-category">Rules</span>
    <a href="/file/download_redirect/abc123def/CatanRules.pdf" class="download-link">Download</a>
  </div>
  <div class="file-row">
    <a href="/filepage/12346/catan-faq" class="file-link">Catan FAQ</a>
    <span class="file-category">FAQ</span>
    <a href="/file/download_redirect/xyz789/CatanFAQ.pdf" class="download-link">Download</a>
  </div>
  <div class="file-row">
    <a href="/filepage/12347/catan-reference-card" class="file-link">Catan Player Reference</a>
    <span class="file-category">Player Aid</span>
    <a href="/file/download_redirect/ref456/CatanRef.pdf" class="download-link">Download</a>
  </div>
</div>
</body></html>
"""


def test_parse_files_page():
    files = parse_files_page(FILES_HTML)
    assert len(files) == 3
    assert files[0]["title"] == "Catan Rules (English)"
    assert files[0]["category"] == "Rules"
    assert "download_redirect" in files[0]["download_url"]


def test_find_rulebook_files():
    files = parse_files_page(FILES_HTML)
    rulebooks = find_rulebook_files(files)
    # Should prefer files with "Rules" category or "rule" in title
    assert len(rulebooks) >= 1
    assert rulebooks[0]["title"] == "Catan Rules (English)"
