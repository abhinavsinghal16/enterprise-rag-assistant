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
* [x] Reranking evaluation
* [x] Deterministic End-to-end response evaluation
* [x] LLM-as-a-Judge End-to-end response evaluation
* [ ] Source attribution

---

## Current Focus

1. Source attribution

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
* Initial validation suggested reranking improved ordering for some queries.
* Formal evaluation was deferred to a dedicated reranking evaluation milestone.
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

### Milestone 8: Reranking Evaluation

Completed

Implemented:

* RerankingEvaluator
* Automated reranking evaluation runner
* Fact coverage validation across reranked chunks
* End-to-end reranking quality reporting

Validation:

* Evaluated reranked results using the retrieval evaluation dataset.
* Verified that all expected facts remained present after reranking.
* Confirmed that reducing context from 10 retrieved chunks to 3 reranked chunks preserved answerability across all evaluation queries.
* Achieved 10/10 reranking evaluation pass rate.

Design Decisions:

* Reranking quality is measured using fact coverage rather than individual chunk ranking.
* Evaluation focuses on preserving answerability within the chunk set passed to generation.
* Reranking is evaluated independently from answer generation to isolate retrieval pipeline quality.

Observations:

* The reranker successfully preserved all required information across the evaluation dataset.
* Context reduction from 10 retrieved chunks to 3 reranked chunks did not result in information loss for tested queries.
* Fact coverage proved to be an effective proxy for measuring answerability after context reduction.

### Milestone 9: Deterministic End-to-End Response Evaluation

Completed

Implemented:

* ResponseEvaluator
* Automated end-to-end response evaluation runner
* Generated answer validation against expected facts
* End-to-end RAG quality reporting

Validation:

* Evaluated generated answers using the retrieval evaluation dataset.
* Verified that generated responses were grounded in retrieved and reranked context.
* Identified cases where deterministic evaluation failed despite semantically correct answers.
* Identified cases where the language model omitted relevant information that was present in the provided context.
* Achieved 8/10 pass rate using deterministic fact matching, exposing both semantic matching limitations and generation completeness issues.

Design Decisions:

* End-to-end evaluation is performed independently from retrieval and reranking evaluation.
* Generated answers are validated against expected facts rather than source locations.
* Deterministic fact matching is intentionally strict and requires expected facts to appear in the generated answer.
* Strict evaluation was chosen to establish a baseline before introducing semantic evaluation using an LLM judge.

Observations:

* Strong retrieval and reranking performance does not guarantee complete answers.
* End-to-end evaluation revealed that answer quality depends on retrieval quality, prompt design, and generation behavior.
* The language model may omit relevant facts even when those facts are present in the provided context.
* Deterministic evaluation can incorrectly fail semantically equivalent answers because it relies on exact text matching.
* Prompt instructions currently emphasize groundedness and non-hallucination, but do not explicitly optimize for completeness.
* Prompts that emphasize groundedness alone may still produce incomplete answers.
* Production RAG systems often require explicit instructions to include all relevant facts, exceptions, and qualifying conditions from the retrieved context.
* Retrieval evaluation and reranking evaluation both achieved perfect scores, yet end-to-end evaluation still identified answer quality issues.
* Evaluation demonstrated that retrieval quality, reranking quality, and answer quality are distinct dimensions that must be measured independently.
* End-to-end evaluation exposed failure modes that were not visible through retrieval-only or reranking-only metrics.
* Evaluation serves not only as a measurement tool but also as a feedback mechanism for identifying opportunities to improve prompts, answer quality, and overall system behavior.

### Evaluation Findings

#### Finding 1: Deterministic Evaluation Limitation

Query:

How much paid jury duty leave is provided?

Expected Fact:

[10] working days

Generated Answer:

10 working days

Result:

FAIL

Analysis:

* The generated answer was semantically correct but failed deterministic evaluation because the expected fact included document-specific bracket formatting.
* The model preserved the meaning of the source material while using slightly different wording.
* This demonstrates a limitation of exact fact matching and motivates the introduction of semantic evaluation using an LLM judge.

Expected LLM Judge Outcome:

PASS

Reason:
The answer preserves the meaning of the source material even though the wording differs.


#### Finding 2: Generation Completeness Limitation

Query:

How much family care and medical leave is available?

Expected Facts:

12 weeks
26 weeks

Generated Answer:

Included 12 weeks
Omitted 26 weeks

Result:

FAIL

Analysis:

* The reranked context contained multiple references to 26 weeks of leave, including military caregiver leave.
* Retrieval evaluation and reranking evaluation both confirmed that the information was available to the model.
* The generated answer included the 12-week leave entitlement but omitted the 26-week leave entitlement.
* Inspection of the generated prompt confirmed that the 26-week leave entitlement was present in the context supplied to the language model.
* This demonstrates a true generation failure rather than a retrieval or reranking failure.
* The finding highlights the importance of evaluating generation independently from retrieval and reranking. Retrieval evaluation and reranking evaluation both achieved perfect scores, yet end-to-end evaluation still exposed answer quality issues.
* The result demonstrates that retrieval quality, reranking quality, and answer quality are distinct dimensions of a RAG system and must be evaluated separately.
* The omission also highlights the importance of prompt design. The system prompt instructed the model to answer using only the provided context and avoid hallucinations, but did not explicitly instruct the model to provide a complete or exhaustive answer.

Current System Prompt:

```text
You are a helpful assistant.
Answer questions using only the provided context.
If the answer cannot be found in the context, say that the information is not available in the provided documents.
Do not make up information.
```

Prompt Limitation:

The prompt emphasizes groundedness and non-hallucination but does not explicitly require the model to include all relevant facts, exceptions, limits, or qualifying conditions found in the supplied context.

* As a result, the model appears to have optimized for brevity and selected what it considered the primary leave entitlement while omitting an additional qualifying leave category.
* This finding demonstrates that prompt design influences not only factual grounding but also answer completeness.

Expected LLM Judge Outcome:

FAIL

Reason:
A required fact was omitted from the generated answer even though it was present in the supplied context.

### Prompt Engineering Learnings

* Prompt design influences answer completeness in addition to factual grounding.
* Instructions that focus on preventing hallucinations do not necessarily encourage comprehensive answers.
* The current prompt successfully constrained the model to use only retrieved context but did not explicitly require the inclusion of all relevant information.
* Language models may optimize for concise responses unless instructed otherwise.
* Production RAG systems often require prompts that explicitly emphasize completeness, exceptions, qualifying conditions, and multiple applicable categories.
* Retrieval and reranking determine what information is available to the model, while prompt design influences how much of that information appears in the final answer.
* Evaluation demonstrated that answer omissions can occur even when the necessary information is successfully retrieved and provided to the model.

### Milestone Takeaway

```text
Retrieval Quality
+
Reranking Quality
+
Prompt Quality
+
Generation Quality
=
Answer Quality
```

* Milestone 9 demonstrated that successful retrieval and reranking do not guarantee complete answers.
* The generated response is influenced not only by the quality of retrieved context but also by the instructions provided to the language model.
* Evaluation revealed that answer quality depends on retrieval quality, reranking quality, prompt design, and generation behavior, each of which must be validated independently.

### Future Work

* The next evaluation phase will introduce an LLM-as-a-Judge evaluator.
* Unlike deterministic fact matching, the LLM judge will evaluate semantic correctness rather than exact text matches.
* The LLM judge will distinguish between semantically correct paraphrases and genuine omissions of required information.
* Answers that preserve meaning through paraphrasing are expected to pass LLM evaluation even when deterministic evaluation fails.
* Answers that omit required facts are expected to fail both deterministic evaluation and LLM-based evaluation.

### Milestone 10: LLM-as-a-Judge End-to-End Response Evaluation

Completed

Implemented:

* LLMJudge
* LLMJudgeEvaluator
* Automated LLM-based response evaluation runner
* Semantic answer validation workflow
* End-to-end answer quality reporting

Validation:

* Evaluated generated answers using the retrieval evaluation dataset.
* Compared LLM-based evaluation results against deterministic evaluation results.
* Verified that the judge correctly identifies semantically equivalent answers.
* Verified that the judge continues to identify genuine answer omissions.
* Achieved 9/10 pass rate using semantic evaluation.

Design Decisions:

* LLM evaluation operates on the same inputs as deterministic evaluation:
  - User query
  - Expected facts
  - Generated answer
* Retrieved chunks and reranked context are intentionally excluded from evaluation.
* Retrieval and reranking quality are evaluated independently in earlier milestones.
* The judge focuses exclusively on answer correctness and completeness.

Observations:

* Semantic evaluation more closely matches human judgment than deterministic fact matching.
* Exact string matching can incorrectly fail answers that preserve meaning through paraphrasing.
* LLM-based evaluation successfully distinguishes between wording differences and genuine answer omissions.
* Evaluation quality improves when semantic understanding is incorporated into the assessment process.

### Evaluation Findings

#### Finding 1: Semantic Equivalence

Query:

How much paid jury duty leave is provided?

Expected Fact:

[10] working days

Generated Answer:

10 working days

Deterministic Evaluation:

FAIL

LLM Judge Evaluation:

PASS

Analysis:

* The generated answer preserved the meaning of the source material.
* Deterministic evaluation failed because it relied on exact string matching.
* The LLM judge correctly identified the answer as semantically equivalent.
* This demonstrates the primary advantage of semantic evaluation over deterministic evaluation.

#### Finding 2: Genuine Information Omission

Query:

How much family care and medical leave is available?

Expected Facts:

12 weeks
26 weeks

Generated Answer:

Included 12 weeks
Omitted 26 weeks

Deterministic Evaluation:

FAIL

LLM Judge Evaluation:

FAIL

Analysis:

* The generated answer omitted required information.
* Both evaluation methods correctly identified the failure.
* The result confirms that semantic evaluation does not simply increase pass rates.
* The judge continued to detect genuine answer quality issues despite allowing semantic flexibility.

### Deterministic vs Semantic Evaluation

Evaluation Method	        Result
Deterministic Evaluation	8/10
LLM-as-a-Judge Evaluation	9/10

Difference:

* Deterministic evaluation failed both identified test cases.
* LLM evaluation passed the semantically correct jury duty response.
* Both evaluation methods failed the family leave response because required information was omitted.
* The LLM judge produced results that more closely aligned with human evaluation.

### Milestone Takeaway

Deterministic Evaluation
↓
Measures exact fact matching

LLM-as-a-Judge Evaluation
↓
Measures semantic correctness and answer completeness

* Deterministic evaluation is effective for identifying literal fact coverage.
* LLM-based evaluation is more effective for assessing whether answers communicate the intended meaning.
* Semantic evaluation provides a more accurate assessment of answer quality by evaluating meaning rather than exact wording.
* Semantic evaluation reduces false failures caused by wording differences while continuing to identify genuine answer quality issues.

### Future Work

* Introduce source attribution for generated answers.
* Evaluate attribution accuracy alongside answer quality.
* Extend evaluation datasets with additional document types and question categories.

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
