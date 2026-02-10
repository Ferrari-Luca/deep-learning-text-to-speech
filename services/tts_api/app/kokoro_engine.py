from __future__ import annotations

import io
import time
from dataclasses import dataclass
from typing import Dict

import numpy as np
import soundfile as sf
from kokoro import KPipeline


@dataclass(frozen=True)
class TTSResult:
    wav_bytes: bytes
    sample_rate: int
    latency_ms: int


class KokoroEngine:
    """
    Loads Kokoro pipelines once and reuses them across requests.

    Note:
      - We output PCM_16 WAV for maximum browser compatibility.
      - Kokoro returns float audio; we clip to [-1, 1] before encoding.
    """

    def __init__(self, repo_id: str = "hexgrad/Kokoro-82M", sample_rate: int = 24000):
        self._repo_id = repo_id
        self._sr = sample_rate
        self._pipelines: Dict[str, KPipeline] = {}

    def _get_pipeline(self, lang: str) -> KPipeline:
        if lang not in self._pipelines:
            self._pipelines[lang] = KPipeline(lang_code=lang, repo_id=self._repo_id)
        return self._pipelines[lang]

    def synthesize(
        self, text: str, *, lang: str, voice: str, speed: float
    ) -> TTSResult:
        t0 = time.perf_counter()

        pipeline = self._get_pipeline(lang)
        generator = pipeline(text, voice=voice, speed=speed)

        chunks: list[np.ndarray] = []
        for _, (_, _, audio) in enumerate(generator):
            chunks.append(audio)

        if not chunks:
            raise RuntimeError("Kokoro returned no audio chunks.")

        audio_all = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]

        # Ensure float32 and clip before PCM16 conversion
        audio_all = np.asarray(audio_all, dtype=np.float32)
        audio_all = np.clip(audio_all, -1.0, 1.0)

        buf = io.BytesIO()
        sf.write(buf, audio_all, self._sr, format="WAV", subtype="PCM_16")
        wav_bytes = buf.getvalue()

        latency_ms = int((time.perf_counter() - t0) * 1000)
        return TTSResult(
            wav_bytes=wav_bytes, sample_rate=self._sr, latency_ms=latency_ms
        )
