"""Tests for scripts/extract-pdf.py — PDF text extraction."""
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the module under test by path
SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "extract-pdf.py"

# We also import the functions directly for unit-level tests
sys.path.insert(0, str(SCRIPT.parent))
import importlib.util

_spec = importlib.util.spec_from_file_location("extract_pdf", SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
extract_pdf = _mod.extract_pdf


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_script(*args: str) -> subprocess.CompletedProcess:
    """Run extract-pdf.py as a subprocess and return the result."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

class TestHappyPath:
    def test_extract_single_pdf_json_structure(self, sample_pdf_paths, output_dir):
        """Extract one sample DDQ PDF and verify JSON output structure."""
        pdf = sample_pdf_paths[0]
        result = _run_script(str(pdf), "--output", str(output_dir))

        assert result.returncode == 0
        json_out = output_dir / f"{pdf.stem}.json"
        assert json_out.exists()

        data = json.loads(json_out.read_text())
        assert "file" in data
        assert data["file"] == pdf.name
        assert "pages" in data
        assert isinstance(data["pages"], list)
        assert len(data["pages"]) > 0

        # Each page must have a page number and text
        for page in data["pages"]:
            assert "page" in page
            assert isinstance(page["page"], int)
            assert page["page"] >= 1
            assert "text" in page
            assert len(page["text"].strip()) > 0

    def test_extract_single_pdf_page_numbers_are_sequential(self, sample_pdf_paths, output_dir):
        """Page numbers should be monotonically increasing."""
        pdf = sample_pdf_paths[0]
        _run_script(str(pdf), "--output", str(output_dir))

        data = json.loads((output_dir / f"{pdf.stem}.json").read_text())
        page_nums = [p["page"] for p in data["pages"]]
        assert page_nums == sorted(page_nums)
        # First page starts at 1
        assert page_nums[0] == 1

    def test_extract_multiple_pdfs(self, sample_pdf_paths, output_dir):
        """Extract all 3 sample DDQs in a single invocation."""
        args = [str(p) for p in sample_pdf_paths] + ["--output", str(output_dir)]
        result = _run_script(*args)

        assert result.returncode == 0
        for pdf in sample_pdf_paths:
            json_out = output_dir / f"{pdf.stem}.json"
            assert json_out.exists(), f"Missing output for {pdf.name}"
            data = json.loads(json_out.read_text())
            assert data["file"] == pdf.name
            assert len(data["pages"]) > 0


# ---------------------------------------------------------------------------
# Error-handling tests
# ---------------------------------------------------------------------------

class TestErrors:
    def test_nonexistent_file_skipped(self, output_dir):
        """A non-existent file should be skipped with an error message."""
        fake = "/tmp/does-not-exist-allocator-test.pdf"
        result = _run_script(fake, "--output", str(output_dir))

        # Script should still exit 0 (skips, doesn't crash)
        assert result.returncode == 0
        assert "Skipping" in result.stderr
        assert "not found" in result.stderr.lower() or "file not found" in result.stderr.lower()
        # No output JSON should be created for a skipped file
        assert not (output_dir / "does-not-exist-allocator-test.json").exists()

    def test_non_pdf_file_skipped(self, output_dir, tmp_path):
        """A non-PDF file should be skipped with an appropriate message."""
        txt = tmp_path / "readme.txt"
        txt.write_text("Not a PDF")
        result = _run_script(str(txt), "--output", str(output_dir))

        assert result.returncode == 0
        assert "Skipping" in result.stderr
        assert "not a PDF" in result.stderr
        assert not (output_dir / "readme.json").exists()

    def test_password_protected_pdf(self, output_dir):
        """Password-protected PDF should produce an error result with correct type."""
        fake_path = Path("/tmp/fake-encrypted.pdf")
        # We mock fitz.open to raise an encrypted error
        with patch.object(_mod, "fitz") as mock_fitz:
            mock_fitz.open.side_effect = Exception("cannot open encrypted PDF without password")
            result = extract_pdf(fake_path)

        assert result["error"] == "password_protected"
        assert "password" in result["message"].lower()
        assert result["pages"] == []
        assert result["file"] == "fake-encrypted.pdf"

    def test_scanned_image_pdf_detection(self, output_dir):
        """A PDF with pages but no extractable text triggers the scanned-image warning."""
        fake_path = Path("/tmp/scanned-doc.pdf")

        # Mock a PDF that has pages but get_text() returns empty strings
        mock_page = MagicMock()
        mock_page.get_text.return_value = "   \n  "  # whitespace only

        mock_doc = MagicMock()
        mock_doc.__len__ = lambda self: 3
        mock_doc.__getitem__ = lambda self, i: mock_page

        with patch.object(_mod, "fitz") as mock_fitz:
            mock_fitz.open.return_value = mock_doc
            result = extract_pdf(fake_path)

        assert result.get("warning") == "scanned_image_pdf"
        assert "scanned" in result["message"].lower() or "OCR" in result["message"]
        assert result["pages"] == []
        assert result["file"] == "scanned-doc.pdf"


# ---------------------------------------------------------------------------
# Unit test: extract_pdf function directly
# ---------------------------------------------------------------------------

class TestExtractPdfFunction:
    def test_returns_dict_with_required_keys(self, sample_pdf_paths):
        """extract_pdf() returns a dict with 'file' and 'pages' keys."""
        result = extract_pdf(sample_pdf_paths[0])
        assert set(result.keys()) >= {"file", "pages"}

    def test_each_sample_has_content(self, sample_pdf_paths):
        """Every sample DDQ should produce at least one page of text."""
        for pdf in sample_pdf_paths:
            result = extract_pdf(pdf)
            assert len(result["pages"]) > 0, f"{pdf.name} produced no pages"
