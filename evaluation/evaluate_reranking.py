from evaluation.retrieval_test_cases import (
    RETRIEVAL_TEST_CASES
)

from evaluation.reranking_evaluator import (
    RerankingEvaluator
)

from embeddings.sentence_transformer_embedding_generator import (
    SentenceTransformerEmbeddingGenerator
)

from storage.json_storage import (
    JsonStorage
)

from vector_store.faiss_vector_store import (
    FaissVectorStore
)

from retrieval.semantic_retriever import (
    SemanticRetriever
)

from retrieval.reranker import (
    Reranker
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

    reranker = Reranker()

    evaluator = (
        RerankingEvaluator()
    )

    passed_count = 0

    print(
        "\nRERANKING EVALUATION"
    )

    print("=" * 80)

    for test_case in (
        RETRIEVAL_TEST_CASES
    ):

        query = test_case["query"]

        retrieval_result = (
            retriever.search(
                query=query,
                top_k=10
            )
        )

        reranked_result = (
            reranker.rerank(
                query=query,
                retrieval_result=retrieval_result,
                top_k=3
            )
        )

        evaluation_result = (
            evaluator.evaluate(
                reranked_result=
                    reranked_result,

                expected_facts=
                    test_case[
                        "expected_facts"
                    ]
            )
        )

        if (
            evaluation_result[
                "passed"
            ]
        ):

            passed_count += 1

            print(
                f"PASS  {query}"
            )

        else:

            print(
                f"FAIL  {query}"
            )

            print(
                "Missing facts:"
            )

            for fact in (
                evaluation_result[
                    "missing_facts"
                ]
            ):
                print(
                    f"  - {fact}"
                )

        print()

    print("=" * 80)

    print(
        f"Passed: "
        f"{passed_count}/"
        f"{len(RETRIEVAL_TEST_CASES)}"
    )


if __name__ == "__main__":
    main()
