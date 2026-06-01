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
* [ ] Text normalization
* [ ] Chunking
* [ ] Metadata generation

### Retrieval

* [ ] Embedding generation
* [ ] FAISS vector storage
* [ ] Semantic retrieval
* [ ] Reranking

### Generation

* [ ] Prompt construction
* [ ] LLM integration
* [ ] Answer generation

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

---

## Design Decisions

### Document Processing

Document processors are responsible for extracting and normalizing format-specific artifacts while preserving document meaning.

Examples:

* Collapse excessive whitespace
* Normalize line endings
* Handle file-format-specific extraction quirks

Document processors should not remove semantic information such as headers, footers, section titles, or page numbers.

### Chunking

Chunking is intentionally separated from document processing.

Document processors convert source files into a common text representation, while chunkers determine retrieval boundaries and generate chunk metadata.

This allows retrieval behavior to remain independent of the original document format.

### Metadata

Document-level metadata and chunk-level metadata are stored separately to avoid duplication and improve maintainability.

Document metadata describes the source document.

Chunk metadata describes a specific chunk extracted from that document.

### Chunk Identifiers

Chunks use UUIDs instead of sequential identifiers to support parallel processing and distributed ingestion workflows.

