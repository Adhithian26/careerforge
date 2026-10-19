from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class ModelProvider(ABC):
    """Abstract Base Class for LLM Provider Abstraction."""
    
    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, **kwargs) -> str:
        """Generates text from a single prompt with optional system instruction."""
        pass

    @abstractmethod
    def generate_chat_reply(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        **kwargs
    ) -> str:
        """Generates a reply from a multi-turn conversation history."""
        pass
