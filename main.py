import argparse

from ingestion.pdf_processor import extract_pages


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "pdf_file",
        help="Path to PDF file"
    )

    args = parser.parse_args()

    pages = extract_pages(args.pdf_file)

    for page in pages[:3]:
        print("-" * 50)
        print(f"Page {page['page']}")

        preview = page["text"][:500]
        print(preview)

    print(f"Pages extracted: {len(pages)}")


if __name__ == "__main__":
    main()
