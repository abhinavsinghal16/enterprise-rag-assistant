from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader


def extract_pages(pdf_path: str) -> List[Dict]:
    """
    Returns:
    [
        {
            "page": 1,
            "text": "..."
        }
    ]
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            {
                "page": page_number,
                "text": text
            }
        )

    return pages
