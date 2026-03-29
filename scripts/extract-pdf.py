#!/usr/bin/env python3
"""Extract text from PDF files with page numbers.

Usage:
    python scripts/extract-pdf.py input1.pdf input2.pdf --output workspace/extracted/

Output: One JSON file per PDF in the output directory:
    {"file": "manager-name.pdf", "pages": [{"page": 1, "text": "..."}, ...]}
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF required: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


def extract_pdf(pdf_path: Path) -> dict:
    """Extract text from a PDF, returning page-level content."""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        if "encrypted" in str(e).lower() or "password" in str(e).lower():
            return {
                "file": pdf_path.name,
                "error": "password_protected",
                "message": "PDF is password-protected — provide the password or an unlocked version.",
                "pages": [],
            }
        raise

    pages = []
    total_pages = len(doc)
    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            pages.append({"page": page_num + 1, "text": text})
    doc.close()

    if total_pages > 0 and len(pages) == 0:
        return {
            "file": pdf_path.name,
            "warning": "scanned_image_pdf",
            "message": "No selectable text found — this appears to be a scanned document. OCR may be required.",
            "pages": [],
        }

    return {"file": pdf_path.name, "pages": pages}


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDFs with page numbers")
    parser.add_argument("pdfs", nargs="+", type=Path, help="PDF files to extract")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output directory")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    for pdf_path in args.pdfs:
        if not pdf_path.exists():
            print(f"Skipping {pdf_path}: file not found", file=sys.stderr)
            continue
        if not pdf_path.suffix.lower() == ".pdf":
            print(f"Skipping {pdf_path}: not a PDF", file=sys.stderr)
            continue

        try:
            result = extract_pdf(pdf_path)
            output_file = args.output / f"{pdf_path.stem}.json"
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
            print(f"Extracted {len(result['pages'])} pages from {pdf_path.name}")
        except Exception as e:
            error_result = {"file": pdf_path.name, "error": str(e), "pages": []}
            output_file = args.output / f"{pdf_path.stem}.json"
            with open(output_file, "w") as f:
                json.dump(error_result, f, indent=2)
            print(f"Error extracting {pdf_path.name}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
