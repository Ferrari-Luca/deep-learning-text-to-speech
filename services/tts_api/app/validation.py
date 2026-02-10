from __future__ import annotations

from .schemas import LangCode


def expected_lang_for_voice(voice: str) -> LangCode | None:
    """
    Infer expected lang_code from voice prefix.

    Examples:
      - "af_bella" -> "a"
      - "bf_emma"  -> "b"
      - "ff_siwis" -> "f"

    Returns None if unknown (we don't block unknown prefixes in MVP).
    """
    if not voice or "_" not in voice:
        return None

    prefix = voice.split("_", 1)[0]  # e.g. "af", "bf", "ff"
    first = prefix[:1].lower()

    if first in {"a", "b", "f"}:
        return first  # type: ignore[return-value]
    return None
