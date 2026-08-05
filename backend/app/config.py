"""
EduPilot AI – Application Configuration
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    app_name: str = "EduPilot AI"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # ── Security ─────────────────────────────────────────────────────────────
    secret_key: str = "change-me-in-production-use-a-long-random-string"

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://edupilot:edupilot_pass@localhost:5432/edupilot_db"
    database_sync_url: str = "postgresql://edupilot:edupilot_pass@localhost:5432/edupilot_db"

    # ── LLM Provider ─────────────────────────────────────────────────────────
    llm_provider: str = "gemini"        # "gemini" | "ollama"

    # ── Gemini ───────────────────────────────────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"

    # ── Ollama (fallback) ─────────────────────────────────────────────────────
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5"
    ollama_temperature: float = 0.7
    ollama_max_tokens: int = 4096

    # ── MCP Servers ──────────────────────────────────────────────────────────
    mcp_gmail_server_port: int = 8001
    mcp_filesystem_server_port: int = 8002
    mcp_postgres_server_port: int = 8003

    # ── Gmail OAuth ──────────────────────────────────────────────────────────
    gmail_client_id: str = ""
    gmail_client_secret: str = ""

    # ── File Storage ─────────────────────────────────────────────────────────
    upload_dir: str = "./uploads"
    reports_dir: str = "./reports/generated"
    max_file_size_mb: int = 10

    # ── CORS ─────────────────────────────────────────────────────────────────
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"

    # ── Logging ──────────────────────────────────────────────────────────────
    log_level: str = "INFO"
    log_format: str = "json"

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
