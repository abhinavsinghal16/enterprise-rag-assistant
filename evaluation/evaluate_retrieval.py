from evaluation.retrieval_test_cases import (
    RETRIEVAL_TEST_CASES
)
from evaluation.retrieval_evaluator import (
    RetrievalEvaluator
)

from embeddings.sentence_transformer_embedding_generator import (
    SentenceTransformerEmbeddingGenerator
)
from storage.json_storage import JsonStorage
from vector_store.faiss_vector_store import (
    FaissVectorStore
)
from retrieval.semantic_retriever import (
    SemanticRetriever
)


def main():

    generator = (
        SentenceTransformerEmbeddingGenerator()
    )

    storage = JsonStorage()

    vector_store = FaissVectorStore()

    retriever = SemanticRetriever(
        generator,
        vector_store,
        storage
    )

    evaluator = RetrievalEvaluator()

    passed_count = 0

    print("\nRETRIEVAL EVALUATION")
    print("=" * 80)

    for test_case in RETRIEVAL_TEST_CASES:

        query = test_case["query"]

        retrieval_result = retriever.search(
            query=query,
            top_k=10
        )

        evaluation_result = evaluator.evaluate(
            retrieval_result=retrieval_result,
            expected_facts=test_case[
                "expected_facts"
            ]
        )

        if evaluation_result["passed"]:
            passed_count += 1

            print(
                f"PASS  {query}"
            )

        else:

            print(
                f"FAIL  {query}"
            )

            print("Missing facts:")

            for fact in (
                evaluation_result[
                    "missing_facts"
                ]
            ):
                print(f"  - {fact}")

        print()

    print("=" * 80)

    print(
        f"Passed: "
        f"{passed_count}/"
        f"{len(RETRIEVAL_TEST_CASES)}"
    )

if __name__ == "__main__":
    main()
