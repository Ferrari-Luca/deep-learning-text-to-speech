from __future__ import annotations

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables when available.

    Example:
      export TTS_REPO_ID="hexgrad/Kokoro-82M"
      export TTS_MAX_CHARS="800"
    """

    model_config = SettingsConfigDict(
        env_prefix="TTS_",
        case_sensitive=False,
    )

    # Kokoro / HF
    repo_id: str = Field(default="hexgrad/Kokoro-82M")
    sample_rate: int = Field(default=24000, ge=8000, le=48000)

    # API behavior
    max_chars: int = Field(default=500, ge=1, le=5000)
    default_lang: str = Field(default="a")  # a=en-US, b=en-GB, f=fr
    default_voice: str = Field(default="af_bella")
    min_speed: float = Field(default=0.8, ge=0.5, le=2.0)
    max_speed: float = Field(default=1.2, ge=0.5, le=2.0)

    # CORS for local dev
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )

    def speed_clamped(self, speed: float) -> float:
        return max(self.min_speed, min(self.max_speed, speed))


settings = Settings()
