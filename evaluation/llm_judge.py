from models.prompt import Prompt

from generation.openai_llm_client import (
    OpenAILLMClient
)


class LLMJudge:

    def __init__(
        self,
        llm_client: OpenAILLMClient
    ):
        self.llm_client = llm_client

    def evaluate(
        self,
        query: str,
        expected_facts: list[str],
        generated_answer: str
    ) -> str:

        expected_facts_text = "\n".join(
            [
                f"- {fact}"
                for fact in expected_facts
            ]
        )

        prompt = f"""
Question:
{query}

Expected Facts:
{expected_facts_text}

Generated Answer:
{generated_answer}

Determine whether the generated answer
correctly and completely answers the question.

The answer does NOT need to use the exact
wording of the expected facts.

PASS if:
- All expected information is present.
- Information may be paraphrased.

FAIL if:
- Required information is missing.
- Information is incorrect.
- Information contradicts expected facts.

Respond ONLY in this format:

PASS
Reason: <reason>

or

FAIL
Reason: <reason>
"""
        judge_prompt = Prompt(system_prompt=("You are an evaluation judge."), user_prompt=prompt)
        return self.llm_client.generate(judge_prompt)
