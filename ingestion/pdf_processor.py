from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
import re

def normalize_text(text: str) -> str:
    text = text.strip()

    text = text.replace("\u2009", " ")
    text = text.replace("\xa0", " ")
    text = re.sub(
            r"\n\s*\n",
            "\n\n",
            text
           )

    return text

def extract_pages(pdf_path: str) -> List[Dict]:
    """
    Returns:
    [
        {
            "page_number": 1,
            "text": "..."
        }
    ]
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = normalize_text(text)

        pages.append(
            {
                "page_number": page_number,
                "text": text
            }
        )

    return pages
