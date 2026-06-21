from dotenv import load_dotenv

from evaluation.retrieval_test_cases import (
    RETRIEVAL_TEST_CASES
)

from evaluation.response_evaluator import (
    ResponseEvaluator
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

from generation.prompt_builder import (
    PromptBuilder
)

from generation.openai_llm_client import (
    OpenAILLMClient
)

from generation.answer_generator import (
    AnswerGenerator
)


def main():

    load_dotenv()

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

    prompt_builder = PromptBuilder()

    llm_client = OpenAILLMClient()

    answer_generator = AnswerGenerator(
        prompt_builder,
        llm_client
    )

    evaluator = (
        ResponseEvaluator()
    )

    passed_count = 0

    print(
        "\nRESPONSE EVALUATION"
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

        answer = (
            answer_generator.generate_answer(
                query=query,
                retrieval_result=
                    reranked_result
            )
        )

        evaluation_result = (
            evaluator.evaluate(
                answer=answer,
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

            if (query == "How much family care and medical leave is available?"):
                print("\nRERANKED CHUNKS")
                print("=" * 80)

                for i, chunk in enumerate(
                    reranked_result.chunks, start=1):
                    print(f"\nChunk {i}")

                    print(chunk["text"])

                    print("-" * 80)
                    print("Generated Answer:")

                    print(answer)
                    print("\nPROMPT SENT TO LLM")
                    print("=" * 80)

                    prompt = prompt_builder.build_prompt(query, reranked_result)

                    print("\nSYSTEM PROMPT:\n")
                    print(prompt.system_prompt)

                    print("\nUSER PROMPT:\n")
                    print(prompt.user_prompt)

                    print("=" * 80)

        print()

    print("=" * 80)

    print(
        f"Passed: "
        f"{passed_count}/"
        f"{len(RETRIEVAL_TEST_CASES)}"
    )


if __name__ == "__main__":
    main()
