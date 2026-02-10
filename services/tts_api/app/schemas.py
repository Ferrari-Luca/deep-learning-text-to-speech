from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .config import settings

LangCode = Literal["a", "b", "f"]  # MVP: en-US, en-GB, fr

MAX_CHARS = settings.max_chars


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_CHARS)
    lang: LangCode = Field(default=settings.default_lang)  # type: ignore[arg-type]
    voice: str = Field(default=settings.default_voice, min_length=1)
    speed: float = Field(default=1.0, ge=settings.min_speed, le=settings.max_speed)


class TTSError(BaseModel):
    detail: str
