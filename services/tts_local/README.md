# Local Kokoro TTS (Smoke Tests)

This folder contains **local validation tooling** for the Kokoro Text-to-Speech model.
It is used to:
- confirm Kokoro runs correctly on the development machine,
- benchmark basic latency (rough baseline),
- test multiple voices and languages,
- generate sample WAV files for subjective quality review.

> Scope: this is **not** the production inference service.
> The production service will be implemented later in `services/tts_api/` using FastAPI.

---

## Kokoro in this project

- Model family: **Kokoro-82M**
- Local inference API: **`pip install kokoro`** (recommended)
- Weights source: Hugging Face Hub (`hexgrad/Kokoro-82M`)
- Output: **24 kHz WAV**

### Versions (important)
Kokoro has multiple releases:
- **v1.0** (2025-01-27): multi-language, more voices, more training data
- **v0.19** (2024-12-25): legacy, different usage/layout

In this repo we currently validate Kokoro using the **modern `kokoro` Python package**
(`KPipeline`), which aligns with **v1.0** and the current Hugging Face assets.

---

## Quick start (macOS)

### 1) System dependency: `espeak-ng`
Kokoro relies on G2P/phonemization. Install `espeak-ng`:

```bash
brew install espeak-ng
espeak-ng --version
```

### 2) Python dependencies

From your project root (virtual environment activated):

```bash
python -m pip install -U pip
python -m pip install "kokoro>=0.9.4" soundfile "misaki[en]"
```

Note: additional language support may require extra misaki extras (see below).

### 3) Run the smoke test

On Apple Silicon, enable MPS fallback for better performance:

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python services/tts_local/run_kokoro_smoketest.py
```

Generated WAV files are written to:

```
services/tts_local/out/
```

---

## Using the smoke test script

### Basic usage

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python services/tts_local/run_kokoro_smoketest.py
```

### Choose voice / language / speed / text

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python services/tts_local/run_kokoro_smoketest.py --voice af_heart --lang a
PYTORCH_ENABLE_MPS_FALLBACK=1 python services/tts_local/run_kokoro_smoketest.py --voice bf_emma --lang b
PYTORCH_ENABLE_MPS_FALLBACK=1 python services/tts_local/run_kokoro_smoketest.py --voice ff_siwis --lang f --text "Le dromadaire resplendissant déambulait tranquillement."
PYTORCH_ENABLE_MPS_FALLBACK=1 python services/tts_local/run_kokoro_smoketest.py --speed 0.95
```

---

## Language codes (KPipeline)

Kokoro uses short language codes that must match the selected voice:
- a → American English (en-us)
- b → British English (en-gb)
- e → Spanish (es)
- f → French (fr-fr)
- h → Hindi (hi)
- i → Italian (it)
- j → Japanese (requires misaki[ja])
- p → Brazilian Portuguese (pt-br)
- z → Mandarin Chinese (requires misaki[zh])

Rule of thumb: the first letter of the voice id usually matches the language group.

---

## Voices

Examples:
- American English: af_bella, af_heart, af_nicole, am_michael
- British English: bf_emma, bm_lewis
- French: ff_siwis
- Mandarin Chinese: zf_xiaobei, zm_yunxi
- Japanese: jf_alpha, jm_kumo

For the full list and quality grades, see:
- third_party/Kokoro-82M/VOICES.md
- https://huggingface.co/hexgrad/Kokoro-82M

---

## Hugging Face downloads & caching

Even if the HF repository is cloned locally, the kokoro package may still
download assets from Hugging Face Hub (depending on cache state).

First runs may therefore be slower.

Recommended: use an HF token

```bash
export HF_TOKEN="your_huggingface_token"
```

Never commit tokens to the repository.

---

## Performance notes
- First run is slower due to downloads
- Voice used for the first time may trigger an extra fetch
- Longer text → longer inference time
- Very long text (>400 tokens) may sound rushed
- Consider chunking or adjusting speed
- Apple Silicon acceleration:

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python ...
```

---

## Troubleshooting

### “Defaulting repo_id …”
Harmless warning. You can silence it by passing:

```python
KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
```

### Hugging Face timeouts
Use an HF token and retry. This is a network/rate-limit issue, not a code bug.

### espeak-ng not found

```bash
which espeak-ng
espeak-ng --version
```

If missing:

```bash
brew install espeak-ng
```

### Japanese / Chinese not working

```bash
python -m pip install "misaki[ja]"
python -m pip install "misaki[zh]"
```

### Torch warnings (dropout / weight_norm)
These are internal model/library warnings and can be ignored for local validation.


