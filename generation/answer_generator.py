from models.retrieval_result import RetrievalResult
from models.generated_answer import GeneratedAnswer

class AnswerGenerator:

    def __init__(
        self,
        prompt_builder,
        llm_client,
        source_extractor
    ):
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        self.source_extractor = source_extractor

    def generate_answer(
        self,
        query: str,
        retrieval_result: RetrievalResult
    ) -> str:

        prompt = self.prompt_builder.build_prompt(query, retrieval_result)
        answer = self.llm_client.generate(prompt)
        sources = self.source_extractor.extract_sources(retrieval_result)

        return GeneratedAnswer(answer=answer, sources=sources)
