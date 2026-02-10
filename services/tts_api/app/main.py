from __future__ import annotations

import logging
import uuid

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .kokoro_engine import KokoroEngine
from .schemas import MAX_CHARS, LangCode, TTSRequest
from .validation import expected_lang_for_voice

logger = logging.getLogger("tts_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="TTS Inference API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = KokoroEngine(repo_id=settings.repo_id, sample_rate=settings.sample_rate)


def _wav_response(
    *, wav_bytes: bytes, request_id: str, latency_ms: int, chars: int, voice: str
) -> Response:
    filename = f"tts_{voice}_{request_id}.wav"
    return Response(
        content=wav_bytes,
        media_type="audio/wav",
        headers={
            "X-Request-Id": request_id,
            "X-Latency-Ms": str(latency_ms),
            "X-Chars": str(chars),
            "Content-Disposition": f'inline; filename="{filename}"',
        },
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "tts_api", "model_repo": settings.repo_id}


@app.post(
    "/tts",
    responses={
        200: {
            "content": {"audio/wav": {"schema": {"type": "string", "format": "binary"}}}
        },
        422: {"description": "Validation error"},
        500: {"description": "TTS failure"},
    },
)
def tts(req: TTSRequest) -> Response:
    request_id = str(uuid.uuid4())[:8]

    # Validate lang/voice coherence (MVP safety)
    expected = expected_lang_for_voice(req.voice)
    if expected is not None and expected != req.lang:
        raise HTTPException(
            status_code=422,
            detail=f"Voice '{req.voice}' implies lang '{expected}', but got lang '{req.lang}'.",
        )

    try:
        result = engine.synthesize(
            req.text, lang=req.lang, voice=req.voice, speed=req.speed
        )
    except Exception as e:
        # 500 here is fine: request validated, but synthesis failed
        raise HTTPException(
            status_code=500, detail=f"TTS failed ({request_id}): {e}"
        ) from e

    logger.info(
        "[%s] lang=%s voice=%s chars=%s speed=%s latency_ms=%s bytes=%s",
        request_id,
        req.lang,
        req.voice,
        len(req.text),
        req.speed,
        result.latency_ms,
        len(result.wav_bytes),
    )

    return _wav_response(
        wav_bytes=result.wav_bytes,
        request_id=request_id,
        latency_ms=result.latency_ms,
        chars=len(req.text),
        voice=req.voice,
    )


@app.get(
    "/tts/preview",
    responses={
        200: {
            "content": {"audio/wav": {"schema": {"type": "string", "format": "binary"}}}
        },
        422: {"description": "Validation error"},
        500: {"description": "TTS failure"},
    },
)
def tts_preview(
    text: str = Query(..., min_length=1, max_length=MAX_CHARS),
    lang: LangCode = Query(default=settings.default_lang),  # type: ignore[assignment]
    voice: str = Query(default=settings.default_voice, min_length=1),
    speed: float = Query(default=1.0, ge=settings.min_speed, le=settings.max_speed),
) -> Response:
    """
    Convenience endpoint for Swagger UI: easier than POSTing JSON.
    """
    request_id = str(uuid.uuid4())[:8]

    expected = expected_lang_for_voice(voice)
    if expected is not None and expected != lang:
        raise HTTPException(
            status_code=422,
            detail=f"Voice '{voice}' implies lang '{expected}', but got lang '{lang}'.",
        )

    try:
        result = engine.synthesize(text, lang=lang, voice=voice, speed=speed)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"TTS failed ({request_id}): {e}"
        ) from e

    logger.info(
        "[%s] lang=%s voice=%s chars=%s speed=%s latency_ms=%s bytes=%s (preview)",
        request_id,
        lang,
        voice,
        len(text),
        speed,
        result.latency_ms,
        len(result.wav_bytes),
    )

    return _wav_response(
        wav_bytes=result.wav_bytes,
        request_id=request_id,
        latency_ms=result.latency_ms,
        chars=len(text),
        voice=voice,
    )
