# TTS API (FastAPI + Kokoro)

Local inference API that exposes **Kokoro** through HTTP and returns **browser-friendly WAV (PCM_16, 24kHz)**.

---

## Run (macOS Apple Silicon / MPS)

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 uvicorn services.tts_api.app.main:app --reload --port 8000
```

API will be available at:

- Health: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Endpoints

- **GET /health** → health check
- **POST /tts** → generate audio from JSON body (returns `audio/wav`)
- **GET /tts/preview** → same as `/tts` but via query params (useful for Swagger UI)

---

## Example (curl)

```bash
curl -X POST "http://127.0.0.1:8000/tts" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from FastAPI!", "lang":"a", "voice":"af_bella", "speed":1.0}' \
  --output out.wav
```

---

## Example (Swagger-friendly preview)

Open:
http://127.0.0.1:8000/docs

Then:
**GET /tts/preview → Try it out**

---

## Notes

- The API returns **raw WAV bytes** (`audio/wav`) suitable for browser playback.
- WAV is encoded as **PCM 16-bit** for compatibility (some browsers reject float WAV).
- Basic validation ensures the **voice prefix matches the language code**:
  - `af_*` → `lang="a"`
  - `bf_*` → `lang="b"`
  - `ff_*` → `lang="f"`
