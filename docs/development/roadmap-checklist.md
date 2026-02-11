# Development Roadmap & Checklist

This document is the **execution plan** for building the Deep Learning Text-to-Speech web application.

It complements:

- `docs/product/roadmap.md` (feature direction / product evolution)
- `docs/architecture/*` (system design and decisions)

Here we focus on **what to build, in what order, and how to validate each stage**.

---

## Guiding principles

### Pedagogical objective (primary)

We intentionally choose solutions that maximize learning:

- infrastructure fundamentals (VPS, reverse proxy, TLS),
- API design and service boundaries,
- model serving constraints (latency, caching, quotas),
- production concerns (logging, monitoring, costs).

### Portfolio objective

We build a repository that looks like a real production project:

- clean commits,
- documented milestones,
- reproducible setup,
- clear architecture and decision records.

### Product objective (optional)

We keep the architecture extensible:

- model abstraction,
- S3 storage pipeline,
- user + billing layer,
- voice cloning integration later.

---

## Milestones & Git tags

We use Git tags to mark “stable milestones” (immutable checkpoints).

Recommended format:

- `milestone-<short-name>`
- or semantic releases later: `v0.1.0`, `v0.2.0`, …

### Tag-worthy milestones

- `milestone-kokoro-local-validation`
- `milestone-fastapi-local`
- `milestone-react-mvp-local`
- `milestone-frontend-refactor-config`
- `milestone-vps-deploy-web`
- `milestone-domain-https`
- `milestone-ec2-inference`
- `milestone-mvp-online`
- `milestone-auth`
- `milestone-stripe`
- `milestone-voice-cloning`

> Rule: tag only when the milestone is **working, documented, and reproducible**.

---

# Phase 1 — Foundation ✅

## Goals

- clear architecture and scope
- clean repo structure and documentation
- dev environment ready

## Checklist

- [x] repository initialized
- [x] docs structure created
- [x] README links to docs
- [x] architecture diagrams written (Mermaid)
- [x] tooling configured

---

# Phase 2 — Local Model Validation (Kokoro) ✅

## Goals

- confirm the model works locally
- test multiple voices and languages
- record baseline latency and quality

## Deliverables

- `services/tts_local/run_kokoro_smoketest.py`
- `services/tts_local/README.md`
- `docs/development/01-kokoro-local-validation.md`

## Tag

- `milestone-kokoro-local-validation`

---

# Phase 3 — FastAPI Local Inference Service ✅

## Goals

- expose Kokoro through a clean HTTP API
- validate inputs
- return browser-compatible WAV

## Completed Features

- `/health`
- `POST /tts`
- `GET /tts/preview`
- server-side validation
- structured logging
- OpenAPI docs
- consistent error handling
- PCM 16-bit WAV output
- latency + request id headers

## Deliverables

- `services/tts_api/app/main.py`
- `services/tts_api/app/kokoro_engine.py`
- `services/tts_api/app/schemas.py`
- `services/tts_api/app/config.py`
- `services/tts_api/app/validation.py`
- `services/tts_api/README.md`

## Tag

- `milestone-fastapi-local`

---

# Phase 4 — Minimal React MVP (Local) ✅

## Goals

Prove the full product loop locally:

```
Text → Generate → Play → Download
```

## Completed Features

- Vite + React + TypeScript setup
- Text input with character counter
- Curated voice selector
- Speed control
- Generate button
- Loading + error states
- Proper binary `audio/wav` handling (Blob + object URL)
- `<audio>` playback
- Download button
- Header extraction (`X-Request-Id`, latency)
- Client-side validation aligned with backend

## Deliverables

- `web/tts_web/`
- `src/api/tts.ts`
- functional React UI
- local end-to-end validation

## Tag

- `milestone-react-mvp-local`

---

# Phase 4.5 — Frontend Architecture Refactor + Authoritative Config 🔄

## Goals

Prepare frontend and backend for production separation and long-term scalability.

## Backend Tasks

- [ ] Add `GET /config` endpoint
  - expose:
    - max_chars
    - min_speed
    - max_speed
    - default values
    - curated voice list
- [ ] Keep backend authoritative for all constraints

## Frontend Tasks

- [ ] Split components:
  - `TtsForm`
  - `VoiceSelect`
  - `AudioPlayer`
- [ ] Extract runtime configuration handling
- [ ] Fetch limits from `/config`
- [ ] Remove hardcoded MAX_CHARS / speed bounds
- [ ] Move API base URL to environment variable
- [ ] Add `.env.local`
- [ ] Prepare support for `/api` proxy
- [ ] Optional: add Vite dev proxy

## Deliverables

- `GET /config` endpoint
- `src/components/`
- `src/types/`
- `src/config/appConfig.ts`
- `.env.local`
- env-based API base handling
- future-ready `/api` abstraction

## Tag

- `milestone-frontend-refactor-config`

---

# Phase 5 — VPS Deployment (Frontend + Express)

## Goals

- deploy real web app on own infrastructure
- introduce public API layer (Express)
- keep ML inference private

## Checklist

- [ ] Create Express API skeleton
- [ ] VPS setup
- [ ] Install Node.js
- [ ] Install Nginx or Caddy
- [ ] Install PM2
- [ ] Deploy React build
- [ ] Reverse proxy:
  - `/` → React
  - `/api/*` → Express

## Tag

- `milestone-vps-deploy-web`

---

# Phase 6 — Domain + HTTPS

## Goals

- production-ready domain
- full HTTPS

## Checklist

- [ ] Buy domain
- [ ] Configure DNS
- [ ] Configure reverse proxy
- [ ] Install Let’s Encrypt
- [ ] Force HTTPS redirect

## Tag

- `milestone-domain-https`

---

# Phase 7 — Production Inference Deployment (EC2 + Docker)

## Goals

- dedicated inference server
- containerized FastAPI
- restricted network access

## Checklist

- [ ] Dockerize `tts_api`
- [ ] Provision EC2
- [ ] Install Docker
- [ ] Restrict inbound traffic to VPS IP
- [ ] Connect Express → FastAPI

## Tag

- `milestone-ec2-inference`

---

# Phase 8 — MVP Online (Anonymous Quota + S3)

## Goals

- anonymous quota system
- secure audio storage
- basic abuse protection

## Checklist

- [ ] Anonymous cookie + IP identification
- [ ] Daily quota enforcement
- [ ] Rate limiting
- [ ] Store audio in S3
- [ ] Signed download URLs

## Tag

- `milestone-mvp-online`

---

# Phase 9 — Accounts + Payments

- [ ] User accounts
- [ ] Quota tiers
- [ ] Stripe integration
- [ ] Usage dashboard

## Tags

- `milestone-auth`
- `milestone-stripe`

---

# Phase 10 — Voice Cloning

- [ ] Licensing review
- [ ] Voice upload system
- [ ] Secure reference storage
- [ ] New inference integration

## Tag

- `milestone-voice-cloning`
