from __future__ import annotations

from dataclasses import dataclass

from app.schemas import AgentArtifact
from app.vertex_client import VertexClient


@dataclass
class AgentSpec:
    name: str
    layer: str
    system_prompt: str


class BaseAgent:
    def __init__(self, spec: AgentSpec, vertex: VertexClient) -> None:
        self.spec = spec
        self.vertex = vertex

    def run(self, task_input: str) -> AgentArtifact:
        content = self.vertex.generate(self.spec.system_prompt, task_input)
        return AgentArtifact(
            agent=self.spec.name,
            layer=self.spec.layer,
            content=content,
            quality_score=0.7,
            metadata={"mode": "draft"},
        )


def simple_critic_gate(artifact: AgentArtifact) -> tuple[bool, str]:
    # Placeholder heuristic for initial loop.
    if len(artifact.content) < 80:
        return False, "Artifact too short, request refinement"
    return True, "Accepted"
