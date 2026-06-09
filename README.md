# Enterprise RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) system being built from scratch to understand the architecture, design tradeoffs, and implementation details behind production AI assistants.

The objective is not simply to use existing frameworks, but to gain a deep understanding of how enterprise-grade AI applications are built, from document ingestion and retrieval to orchestration and answer generation.

## Planned Architecture

The project covers the complete retrieval pipeline:

* Document ingestion
* PDF processing
* Chunking and metadata extraction
* Embedding generation
* Vector search with FAISS
* Reranking
* Prompt construction
* LLM orchestration
* Answer generation

---

## Current Status

### Foundation

* [x] Repository setup
* [x] Core domain models
* [x] Project structure
* [x] GitHub integration

### Ingestion

* [x] PDF page extraction
* [x] Text normalization
* [x] Section-aware chunking
* [x] Metadata generation
* [x] Page number tracking
* [x] Hierarchical heading preservation

### Retrieval

* [x] Embedding generation
* [x] Embedding persistence
* [ ] FAISS vector storage
* [ ] Semantic retrieval
* [ ] Retrieval result model
* [ ] Reranking

### Generation

* [ ] Prompt construction
* [ ] LLM integration
* [ ] Answer generation

### Evaluation

* [ ] Retrieval evaluation
* [ ] Reranking evaluation
* [ ] End-to-end response evaluation


---

## Current Focus

Building the retrieval layer:

1. Generate embeddings for document chunks
2. Persist embeddings and chunk metadata
3. Implement FAISS vector storage
4. Implement semantic retrieval
5. Add reranking

---

## Milestones

### Milestone 1: Project Foundation

Completed

Implemented:

* Core domain models

  * Document
  * Chunk
  * ChunkMetadata
  * RetrievalResult
* Repository structure
* Development environment setup

### Milestone 2: PDF Extraction

Completed

Implemented:

* PDF extraction using pypdf
* Command-line PDF input
* Validation against a real-world employee handbook

Observations:

* Successfully extracted 40 pages from a sample employee handbook.
* PDF extraction quality is generally good.
* PDF-specific formatting artifacts were identified during testing.
* Semantic cleanup was intentionally deferred pending additional analysis.

### Milestone 3: Document Chunking

Completed

Implemented:

* Text normalization
* Paragraph extraction
* Section heading detection
* Hierarchical heading preservation
* Metadata generation
* Page number tracking
* Word-boundary chunk splitting

Design Decisions:

* Section headings are propagated into every chunk to improve retrieval quality.
* Nested headings are preserved using hierarchical paths.
* Chunks retain source metadata for attribution and debugging.
* Chunk boundaries respect word boundaries to avoid truncating content.

Validation:

* Tested against a 40-page employee handbook.
* Verified section-aware chunk generation.
* Verified page metadata tracking.
* Identified PDF extraction artifacts and deferred advanced cleanup to a future iteration.

### Milestone 4: Embedding Generation

Completed

Implemented:

* EmbeddingGenerator abstraction
* SentenceTransformerEmbeddingGenerator implementation
* Sentence Transformers integration
* Embedding normalization
* Batch embedding generation

Validation:

* Generated embeddings for 156 chunks
* Verified 384-dimensional embeddings
* Verified one embedding per chunk

---

## Design Decisions

### Document Processing

Document processors are responsible for extracting and normalizing format-specific artifacts while preserving document meaning.

Examples:

* Collapse excessive whitespace
* Normalize line endings
* Handle file-format-specific extraction quirks

Document processors should not remove semantic information such as headers, footers, section titles, or page numbers.

PDF extraction artifacts were identified during testing. Advanced cleanup was intentionally deferred because retrieval quality is expected to be driven primarily by embeddings, retrieval, and reranking rather than document-specific text cleanup.

### Chunking

Chunking is intentionally separated from document processing.

Document processors convert source files into a common text representation, while chunkers determine retrieval boundaries and generate chunk metadata.

This separation allows retrieval behavior to remain independent of the original document format.

Chunks are generated using section-aware chunking. Detected section headings are propagated into every chunk to preserve context and improve retrieval quality.

When multiple nested headings are encountered, they are combined into a hierarchical path:

```
Benefits > Health Insurance
```

This preserves document structure while avoiding standalone heading chunks.

Chunk boundaries are created on word boundaries to avoid truncating words and to maintain chunk readability.

### Metadata

Document-level metadata and chunk-level metadata are stored separately to avoid duplication and improve maintainability.

Document metadata describes the source document.

Chunk metadata describes a specific chunk extracted from that document.

Chunk metadata currently includes:

* Document name
* Source page number
* Section heading path

Preserving metadata enables source attribution, debugging, evaluation, and future filtering capabilities.

### Chunk Identifiers

Chunks use UUIDs instead of sequential identifiers to support parallel processing and distributed ingestion workflows.

UUIDs also allow chunks to remain uniquely identifiable regardless of ingestion order.

### Simplicity First

When multiple implementations are possible, the system favors simple deterministic approaches before introducing additional complexity.

Examples include:

* Heuristic heading detection instead of LLM-based structure extraction
* Non-overlapping chunks in the initial implementation
* Deferred cleanup of PDF-specific artifacts
* Retrieval-first optimization before introducing reranking and advanced evaluation

Additional complexity is introduced only when it produces measurable improvements in retrieval quality.

