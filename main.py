import argparse
import uuid

from ingestion.pdf_processor import extract_pages
from chunking.chunker import create_chunks
from embeddings.sentence_transformer_embedding_generator import SentenceTransformerEmbeddingGenerator


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "pdf_file",
        help="Path to PDF file"
    )

    args = parser.parse_args()

    # Extract document pages
    pages = extract_pages(
        args.pdf_file
    )

    document_id = str(
        uuid.uuid4()
    )

    # Create retrieval chunks from the extracted pages
    chunks = create_chunks(
        pages=pages,
        document_id=document_id,
        document_name=args.pdf_file
    )

    # Extract chunk text for embedding generation
    chunk_texts = [
        chunk.text
        for chunk in chunks
    ]

    generator = SentenceTransformerEmbeddingGenerator()

    # Generate embeddings for all chunks
    embeddings = generator.generate_embeddings(
        chunk_texts
    )

    print(
        f"Pages extracted: {len(pages)}"
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

if __name__ == "__main__":
    main()
