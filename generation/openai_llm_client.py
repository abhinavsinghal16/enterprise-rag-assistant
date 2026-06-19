from openai import OpenAI
import os

from generation.llm_client import LLMClient
from models.prompt import Prompt

class OpenAILLMClient(LLMClient):

    def __init__(self, model: str = "gpt-4.1-mini"):
        
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: Prompt) -> str:
        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": prompt.system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt.user_prompt
                    }
                ]
            )
        )

        return response.choices[0].message.content
