import argparse
import uuid
from pathlib import Path

from ingestion.pdf_processor import extract_pages
from models.document import Document
from chunking.chunker import create_chunks
from embeddings.sentence_transformer_embedding_generator import SentenceTransformerEmbeddingGenerator
from storage.json_storage import JsonStorage
from vector_store.faiss_vector_store import FaissVectorStore
from retrieval.semantic_retriever import SemanticRetriever
from retrieval.reranker import Reranker
from dotenv import load_dotenv

from generation.openai_llm_client import OpenAILLMClient
from generation.prompt_builder import PromptBuilder
from generation.answer_generator import AnswerGenerator
from generation.source_extractor import SourceExtractor

def main():

    load_dotenv()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "pdf_file",
        help="Path to PDF file"
    )

    args = parser.parse_args()

    # Create document metadata
    document = Document(
        id=str(uuid.uuid4()),
        name=args.pdf_file,
        document_type=Path(args.pdf_file).suffix.lstrip(".")
    )

    # Extract pages from the input document
    pages = extract_pages(document.name)
   
    # Create retrieval chunks from the extracted pages
    chunks = create_chunks(
        pages=pages,
        document_id=document.id,
        document_name=document.name
    )

    # Extract text from chunks for embedding generation
    chunk_texts = [
        chunk.text
        for chunk in chunks
    ]

    generator = SentenceTransformerEmbeddingGenerator()

    # Generate vector embeddings for each chunk
    embeddings = generator.generate_embeddings(
        chunk_texts
    )

    storage = JsonStorage()
    document_records = [
        {
            "id": document.id,
            "name": document.name,
            "type": document.document_type
        }
    ]

    # Persist document metadata
    storage.save_documents(document_records)

    chunk_records = [
        {
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "text": chunk.text,
            "metadata": {
                "document_name": chunk.metadata.document_name,
                "page_number": chunk.metadata.page_number,
                "section": chunk.metadata.section
            }
        }
        for chunk in chunks
    ]

    # Persist chunk data and metadata
    storage.save_chunks(chunk_records)

    embedding_records = [
        {
            "chunk_id": chunk.id,
            "embedding": embedding
        }
        for chunk, embedding in zip(
            chunks,
            embeddings
        )
    ]

    # Persist chunk-to-embedding mappings
    storage.save_embeddings(embedding_records)

    # Build a searchable vector index from persisted embeddings
    vector_store = FaissVectorStore()

    # Load embeddings and create a FAISS index
    index = vector_store.build_index_from_file("data/embeddings.json")

    # Persist the FAISS index for future retrieval operations
    vector_store.save_index(
        index,
        "data/faiss.index"
    )

    retriever = SemanticRetriever(
        generator,
        vector_store,
        storage
    )
    query='how many vacation days do employees receive'
    retrieval_result = retriever.search(query, top_k=10)

    reranker = Reranker()

    reranked_result = reranker.rerank(
        query=query,
        retrieval_result=retrieval_result,
        top_k=3
    )

    prompt_builder = PromptBuilder()

    llm_client = OpenAILLMClient()

    source_extractor = SourceExtractor()

    answer_generator = AnswerGenerator(
        prompt_builder,
        llm_client,
        source_extractor)

    generated_answer = answer_generator.generate_answer(
        query=query,
        retrieval_result=reranked_result)
    
    print("\nANSWER")
    print("=" * 80)
    print(generated_answer.answer)

    print("\nSOURCES")
    print("=" * 80)

    for source_index, source in enumerate(generated_answer.sources, start=1):
        print(f"\n[{source_index}] {source.document_name}")

        print(
            f"    {source.section} "
            f"(Page {source.page_number})"
        )

    print(f"Pages extracted: {len(pages)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Embeddings generated: {len(embeddings)}")
    print(f"Embeddings indexed: {index.ntotal}")
    print(f"Embedding dimension: {index.d}")

    print(
        f"Retrieval time: "
        f"{retrieval_result.retrieval_time_ms:.2f} ms"
    )

if __name__ == "__main__":
    main()
