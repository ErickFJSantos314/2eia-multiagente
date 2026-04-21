from __future__ import annotations

from pathlib import Path

from app.agents import AgentSpec, BaseAgent, simple_critic_gate
from app.brain_store import BrandBrain
from app.schemas import AgentArtifact, OrchestrateRequest, OrchestrateResponse
from app.vertex_client import VertexClient


class Orchestrator:
    def __init__(self, vertex: VertexClient, brain: BrandBrain) -> None:
        self.vertex = vertex
        self.brain = brain

    def _load_prompt(self, prompt_name: str) -> str:
        path = Path("prompts/system") / f"{prompt_name}.md"
        if not path.exists():
            return f"System prompt missing: {prompt_name}"
        return path.read_text(encoding="utf-8")

    def _build_agents(self) -> list[BaseAgent]:
        specs = [
            AgentSpec("CTO", "L3", self._load_prompt("cto")),
            AgentSpec("CMO", "L3", self._load_prompt("cmo")),
            AgentSpec("CFO", "L3", self._load_prompt("cfo")),
            AgentSpec("Backend Specialist", "L4", self._load_prompt("backend_specialist")),
            AgentSpec("Frontend Specialist", "L4", self._load_prompt("frontend_specialist")),
            AgentSpec("Designer Specialist", "L4", self._load_prompt("designer_specialist")),
            AgentSpec("Treasurer Specialist", "L4", self._load_prompt("treasurer")),
            AgentSpec("Financial Planning Specialist", "L4", self._load_prompt("financial_planning")),
            AgentSpec("FP&A Specialist", "L4", self._load_prompt("fpa")),
        ]
        return [BaseAgent(spec=s, vertex=self.vertex) for s in specs]

    def run(self, req: OrchestrateRequest) -> OrchestrateResponse:
        brand_context = self.brain.build_context_block()
        base_input = (
            f"session_id={req.session_id}\n"
            f"client={req.client}\n"
            f"user_input={req.input}\n"
            f"{brand_context}\n"
        )

        artifacts: list[AgentArtifact] = []
        for agent in self._build_agents():
            artifact = agent.run(base_input)
            approved, reason = simple_critic_gate(artifact)

            if not approved:
                refine_input = f"{base_input}\nCritic feedback: {reason}"
                artifact = agent.run(refine_input)
                artifact.metadata["critic_feedback"] = reason
                artifact.metadata["mode"] = "refined"

            artifacts.append(artifact)

        reducer_prompt = self._load_prompt("orchestrator")
        combined = "\n\n".join([f"[{a.agent}]\n{a.content}" for a in artifacts])
        summary = self.vertex.generate(reducer_prompt, combined)

        return OrchestrateResponse(
            session_id=req.session_id,
            summary=summary,
            artifacts=artifacts,
            next_actions=[
                "HITL review output package",
                "Approve or reject deployment",
                "Send final package to client channel",
            ],
        )
