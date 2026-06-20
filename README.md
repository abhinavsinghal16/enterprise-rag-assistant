# Enterprise RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) system built from scratch to explore the architectural decisions, tradeoffs, and implementation details behind production AI assistants and enterprise knowledge systems.

The objective is not simply to use existing frameworks, but to gain a deep understanding of how enterprise-grade AI applications are built, from document ingestion and retrieval to orchestration and answer generation.

## Planned Architecture

The project covers the complete RAG pipeline:

* Document ingestion
* PDF processing
* Chunking and metadata extraction
* Embedding generation
* Vector search with FAISS
* Reranking
* Prompt construction
* LLM integration
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
* [x] FAISS vector storage
* [x] Semantic retrieval
* [x] Retrieval result model
* [x] Reranking

### Generation

* [x] Prompt construction
* [x] LLM integration
* [x] Answer generation

### Evaluation

* [x] Retrieval evaluation
* [ ] Reranking evaluation
* [ ] End-to-end response evaluation
* [ ] Source attribution


---

## Current Focus

Evaluating ranking and answer quality:

1. Reranking evaluation
2. End-to-end response evaluation
3. Source attribution

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

Technology Choices:

* all-MiniLM-L6-v2 for embedding generation

### Milestone 5: Retrieval

Completed

Implemented:

* FAISS vector storage
* Semantic retrieval
* Query embedding generation
* RetrievalResult abstraction
* Cross-encoder reranking

Validation:

* Verified retrieval against a 40-page employee handbook corpus
* Confirmed semantic retrieval returns contextually relevant chunks for natural-language queries
* Compared reranked results against baseline FAISS retrieval during validation
* Measured retrieval latency and end-to-end retrieval performance

Technology Choices:

* FAISS for vector similarity search
* ms-marco-MiniLM-L-6-v2 cross-encoder for reranking

Design Decisions:

* FAISS selected for local vector search due to simplicity and performance.
* Semantic retrieval and reranking were implemented as independent components to maintain separation of concerns.
* Retrieval returns candidate chunks while reranking is responsible only for relevance ordering.
* RetrievalResult provides a stable contract between retrieval and downstream generation components.

Observations:

* Retrieval quality is highly dependent on query specificity.
* Reranking improves ordering for some queries but does not universally improve results.
* Evaluation demonstrated the importance of measuring retrieval quality rather than assuming reranking improves relevance.

### Milestone 6: Generation

Completed

Implemented:

* Prompt model
* PromptBuilder
* LLMClient abstraction
* OpenAILLMClient implementation
* AnswerGenerator
* End-to-end answer generation

Validation:

* Verified OpenAI API integration
* Generated answers using retrieved and reranked document context
* Confirmed responses were grounded in retrieved content
* Verified end-to-end RAG flow from document ingestion to answer generation

Technology Choices:

* GPT-4.1 Mini for answer generation
* OpenAI Python SDK
* python-dotenv for environment configuration

Design Decisions:

* Prompt construction was separated from LLM integration to maintain provider independence.
* LLMClient abstraction enables future support for alternative model providers without impacting the rest of the application.
* AnswerGenerator acts as the orchestration layer between retrieval and generation.
* System and user prompts are modeled explicitly to separate behavioral instructions from user queries.

Observations:

* Answer quality is highly dependent on retrieval quality.
* Natural-language questions generally produced better retrieval and answer quality than keyword-only queries.
* Prompt structure significantly influences response accuracy and grounding.
* The generation layer can only reason over the context provided by retrieval.
* End-to-end testing demonstrated the importance of treating retrieval and generation as separate concerns.

### Milestone 7: Retrieval Evaluation

Completed

Implemented:

* Retrieval test case framework
* RetrievalEvaluator
* Automated retrieval evaluation runner
* Ground-truth validation workflow
* Retrieval quality reporting

Validation:

* Created 10 retrieval evaluation test cases covering vacation policies, holidays, sick leave, overtime, jury duty, health insurance, and family leave.
* Verified retrieval results against handbook ground truth.
* Identified and corrected evaluation issues caused by whitespace normalization and document template artifacts.
* Achieved 10/10 retrieval evaluation pass rate.

Design Decisions:

* Retrieval evaluation was separated from reranking and answer evaluation to isolate retrieval quality.
* Ground truth is defined using expected facts rather than page numbers to focus evaluation on information retrieval rather than document structure.
* Evaluation failures are investigated before modifying retrieval logic to distinguish retrieval issues from evaluation dataset issues.

Observations:

* Evaluation framework exposed several issues in test data and normalization logic before any retrieval deficiencies were identified.
* Accurate ground truth definition is critical for meaningful retrieval metrics.
* Retrieval quality should be measured independently from generation quality.
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

### Future Exploration

Future iterations of the project will explore agentic workflows, enabling the system to perform iterative retrieval, multi-step reasoning, and dynamic information gathering before generating a final response.

