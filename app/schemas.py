from typing import Any

from pydantic import BaseModel, Field


class OrchestrateRequest(BaseModel):
    session_id: str = Field(..., description="Session unique identifier")
    input: str = Field(..., description="Business request from HITL")
    client: str = Field(..., description="Client name")


class AgentArtifact(BaseModel):
    agent: str
    layer: str
    content: str
    quality_score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class OrchestrateResponse(BaseModel):
    session_id: str
    summary: str
    artifacts: list[AgentArtifact]
    next_actions: list[str]
