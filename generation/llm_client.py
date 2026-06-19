from abc import ABC, abstractmethod
from models.prompt import Prompt

class LLMClient(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: Prompt
    ) -> str:
        pass
