from models.retrieval_result import RetrievalResult

class AnswerGenerator:

    def __init__(
        self,
        prompt_builder,
        llm_client
    ):
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def generate_answer(
        self,
        query: str,
        retrieval_result: RetrievalResult
    ) -> str:

        prompt = self.prompt_builder.build_prompt(query, retrieval_result)
        answer = self.llm_client.generate(prompt)

        return answer
