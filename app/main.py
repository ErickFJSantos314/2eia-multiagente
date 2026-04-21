from fastapi import FastAPI

from app.brain_store import BrandBrain
from app.config import settings
from app.orchestrator import Orchestrator
from app.schemas import OrchestrateRequest, OrchestrateResponse
from app.vertex_client import VertexClient

app = FastAPI(title="2E.IA Orchestrator", version="0.1.0")

vertex = VertexClient(
    project_id=settings.gcp_project_id,
    region=settings.gcp_region,
    model_name=settings.vertex_model,
    api_key=settings.google_api_key or None,
)
brain = BrandBrain(
    brand_profile_path=settings.brand_profile_path,
    content_history_path=settings.content_history_path,
)
orchestrator = Orchestrator(vertex=vertex, brain=brain)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "2eia-orchestrator"}


@app.post("/v1/orchestrate", response_model=OrchestrateResponse)
def orchestrate(payload: OrchestrateRequest) -> OrchestrateResponse:
    return orchestrator.run(payload)
