from typing import Any, Dict, List

from openai import OpenAI


class OpenAIService:
    def __init__(self):
        from gptool.config import get_config

        config = get_config()
        self.client = OpenAI(api_key=config.openai_key, base_url=config.openai_url)

    def create_embeddings(self, *args, **kwargs) -> List[float]:
        response = self.client.embeddings.create(*args, **kwargs)
        embeddings = response.data[0].embedding
        return embeddings

    def chat(self, *args, **kwargs) -> Dict[str, Any]:
        response = self.client.chat.completions.create(*args, **kwargs)
        response_message = response.choices[0].message
        return response_message

    @staticmethod
    def get_embeddings_size():
        return 1536
