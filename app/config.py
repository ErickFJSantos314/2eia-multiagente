from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "dev"
    port: int = 8080
    log_level: str = "INFO"

    gcp_project_id: str = ""
    gcp_region: str = "us-central1"
    vertex_model: str = "gemini-1.5-pro"

    google_application_credentials: str = ""
    google_api_key: str = ""

    brand_profile_path: str = "data/brand/brand_profile.example.yaml"
    content_history_path: str = "data/brand/content_history.example.md"

    use_firestore: bool = False
    use_gcs: bool = False
    firestore_collection: str = "sessions"
    gcs_bucket: str = ""


settings = Settings()
