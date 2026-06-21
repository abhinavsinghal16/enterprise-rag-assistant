from dotenv import load_dotenv
from generation.source_extractor import SourceExtractor

from evaluation.retrieval_test_cases import (
    RETRIEVAL_TEST_CASES
)

from evaluation.llm_judge import (
    LLMJudge
)

from evaluation.llm_judge_evaluator import (
    LLMJudgeEvaluator
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

    source_extractor = SourceExtractor()

    answer_generator = AnswerGenerator(
        prompt_builder,
        llm_client,
        source_extractor
    )

    llm_judge = LLMJudge(
        llm_client
    )

    llm_judge_evaluator = (
        LLMJudgeEvaluator()
    )

    passed_count = 0

    print(
        "\nLLM JUDGE EVALUATION"
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
                retrieval_result=
                    retrieval_result,
                top_k=3
            )
        )

        generated_answer = (
            answer_generator.generate_answer(
                query=query,
                retrieval_result=
                    reranked_result
            )
        )

        judge_response = (
            llm_judge.evaluate(
                query=query,
                expected_facts=
                    test_case[
                        "expected_facts"
                    ],
                generated_answer=
                    generated_answer.answer
            )
        )

        evaluation_result = (
            llm_judge_evaluator.evaluate(
                judge_response
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
            f"Reason: "
            f"{evaluation_result['reason']}"
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
