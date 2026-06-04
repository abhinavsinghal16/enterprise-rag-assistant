import argparse
import uuid

from ingestion.pdf_processor import extract_pages
from chunking.chunker import create_chunks


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "pdf_file",
        help="Path to PDF file"
    )

    args = parser.parse_args()

    pages = extract_pages(
        args.pdf_file
    )

    document_id = str(
        uuid.uuid4()
    )

    chunks = create_chunks(
        pages=pages,
        document_id=document_id,
        document_name=args.pdf_file
    )
    
    print(
        f"Pages extracted: {len(pages)}"
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

if __name__ == "__main__":
    main()
