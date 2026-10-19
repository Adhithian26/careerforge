import os
from typing import List, Dict, Optional, Any
from backend.app.ai.provider_base import ModelProvider
from backend.app.config import settings

class GeminiProvider(ModelProvider):
    """
    Official Google Gemini API implementation using the google-genai SDK.
    Supports gemini-2.5-flash, gemini-1.5-flash, etc.
    """
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.model_name = model_name or settings.GEMINI_MODEL or "gemini-2.5-flash"
        self._client = None
        
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self._client = None

    def is_configured(self) -> bool:
        return bool(self.api_key and self._client)

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, **kwargs) -> str:
        if not self.is_configured():
            raise ValueError("GEMINI_API_KEY is not configured or client failed to initialize.")
        
        try:
            from google.genai import types
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "quota" in err_msg.lower() or "rate" in err_msg.lower():
                raise RuntimeError(f"Gemini API rate limit or quota exceeded: {err_msg}")
            raise RuntimeError(f"Gemini API Error: {err_msg}")

    def generate_chat_reply(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        **kwargs
    ) -> str:
        if not self.is_configured():
            raise ValueError("GEMINI_API_KEY is not configured or client failed to initialize.")

        try:
            from google.genai import types
            # Format history for Gemini API
            formatted_contents = []
            for m in messages:
                role = "user" if m.get("role") in ["user", "student"] else "model"
                formatted_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=m.get("content", ""))]
                    )
                )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4
            )
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=formatted_contents,
                config=config
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "quota" in err_msg.lower() or "rate" in err_msg.lower():
                raise RuntimeError(f"Gemini API rate limit or quota exceeded: {err_msg}")
            raise RuntimeError(f"Gemini API Error: {err_msg}")
