from models.retrieval_result import RetrievalResult
from models.prompt import Prompt

class PromptBuilder:
    def build_prompt(
        self,
        query: str,
        retrieval_result: RetrievalResult
    ) -> Prompt:

        system_prompt = """
You are a helpful assistant.

Answer questions using only the provided context.

If the answer cannot be found in the context, say that the information is not available in the provided documents.

Do not make up information.
"""

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieval_result.chunks
        )

        user_prompt = f"""
Use the following context to answer the question.

Context:

{context}

Question:

{query}
"""

        return Prompt(
            system_prompt=system_prompt.strip(),
            user_prompt=user_prompt.strip()
        )
