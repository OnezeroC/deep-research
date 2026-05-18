from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def analyze(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        """Send prompt to AI and return the text response."""
        ...
