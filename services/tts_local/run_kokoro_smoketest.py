from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline


def resolve_device(preferred: str) -> str:
    if preferred != "auto":
        return preferred
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local Kokoro smoke test (wav generation)."
    )
    parser.add_argument(
        "--lang", default="a", help="Language code (e.g., a=en-US, b=en-GB, f=fr)."
    )
    parser.add_argument(
        "--voice",
        default="af_bella",
        help="Voice id (e.g., af_bella, af_heart, bf_emma).",
    )
    parser.add_argument(
        "--speed", type=float, default=1.0, help="Speech speed (e.g., 0.9, 1.0, 1.1)."
    )
    parser.add_argument("--device", default="auto", help="auto|mps|cpu")
    parser.add_argument(
        "--text",
        default="Hello! This is a local Kokoro smoke test. If you can hear this clearly, the pipeline works.",
        help="Text to synthesize.",
    )
    args = parser.parse_args()

    device = resolve_device(args.device)
    print(f"Device: {device}")

    pipeline = KPipeline(lang_code=args.lang)

    out_dir = Path("services/tts_local/out")
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    generator = pipeline(args.text, voice=args.voice, speed=args.speed)

    audios = []
    for _, (_, _, audio) in enumerate(generator):
        audios.append(audio)

    dt = time.perf_counter() - t0

    audio_all = np.concatenate(audios) if len(audios) > 1 else audios[0]
    out_wav = out_dir / f"kokoro_{args.voice}_speed{args.speed}.wav"
    sf.write(out_wav, audio_all, 24000)

    print(f"Saved: {out_wav}")
    print(f"Generation time: {dt:.2f}s")
    print(f"Chars: {len(args.text)}")


if __name__ == "__main__":
    main()
