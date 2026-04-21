from __future__ import annotations

from typing import Optional


class VertexClient:
    def __init__(self, project_id: str, region: str, model_name: str, api_key: Optional[str] = None) -> None:
        self.project_id = project_id
        self.region = region
        self.model_name = model_name
        self.api_key = api_key

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Stub para facilitar inicio rapido.
        Substitua por chamada real ao Vertex AI Gemini.
        """
        return (
            "[SIMULATED_VERTEX_RESPONSE]\n"
            f"system={system_prompt[:300]}\n"
            f"user={user_prompt[:500]}\n"
        )
