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

### Tag-worthy milestones (recommended)
- `milestone-kokoro-local-validation` — Kokoro works locally with baseline measurements
- `milestone-fastapi-local` — FastAPI `/tts` works locally and returns audio
- `milestone-react-mvp-local` — React MVP works locally end-to-end
- `milestone-vps-deploy-web` — frontend+express deployed on VPS behind reverse proxy
- `milestone-domain-https` — domain + HTTPS on VPS
- `milestone-ec2-inference` — FastAPI inference running on EC2 via Docker
- `milestone-mvp-online` — full MVP usable online (anonymous quota + download)
- `milestone-auth` — user accounts live
- `milestone-stripe` — payments live
- `milestone-voice-cloning` — voice cloning integrated (later)

> Rule: tag only when the milestone is **working, documented, and reproducible**.

---

## Phase 1 — Foundation ✅

### Goals
- clear architecture and scope
- clean repo structure and documentation
- dev environment ready

### Checklist
- [x] repository initialized
- [x] docs structure created (`docs/architecture`, `docs/product`)
- [x] README links to docs
- [x] initial architecture diagrams written (Mermaid)
- [x] tooling configured (VS Code, formatting, Python version pinned)


---

## Phase 2 — Local model validation ✅ (Kokoro)

### Goals
- confirm the model works locally
- test multiple voices and at least 2 languages
- record baseline latency and quality notes

### Checklist
- [x] install dependencies (`kokoro`, `soundfile`, `misaki[en]`, `espeak-ng`)
- [x] run smoke test and generate WAV output
- [x] test multiple voices (`af_*`, `bf_*`, `ff_siwis`)
- [x] record baseline timing + notes
- [x] write local testing docs and README in `services/tts_local`

### Deliverables
- `services/tts_local/run_kokoro_smoketest.py`
- `services/tts_local/README.md`
- `docs/development/01-kokoro-local-validation.md`

### Tag
- `milestone-kokoro-local-validation`

---

## Phase 3 — Expose Kokoro via FastAPI (local)

### Goals
- provide a stable HTTP API to generate audio
- enable manual testing via curl/Postman
- set foundation for production deployment later

### Checklist
- [ ] create service skeleton: `services/tts_api/`
- [ ] implement `/health`
- [ ] implement `POST /tts`
  - [ ] input validation (max chars, empty text)
  - [ ] parameters: `voice`, `lang`, `speed`
  - [ ] output: `audio/wav` response (bytes) OR signed URL later
- [ ] logging (request id, latency, chars)
- [ ] error handling and consistent response errors
- [ ] basic rate-limit placeholder (later enforced by Express)

### Manual testing
- [ ] Postman / curl request succeeds
- [ ] audio plays and downloads correctly
- [ ] verify boundary cases (empty text, too long, unsupported voice/lang)

### Tag
- `milestone-fastapi-local`

---

## Phase 4 — Minimal React MVP (local first)

### Goals
- minimal UI that proves the product loop:
  text → generate → play → download

### Checklist
- [ ] create React app with Vite
- [ ] UI elements:
  - [ ] text input
  - [ ] voice select (curated list)
  - [ ] generate button
  - [ ] audio player
  - [ ] download button
- [ ] connect React → FastAPI
  - [ ] POST request to `/tts`
  - [ ] handle `audio/wav` response
  - [ ] show loading/error state
- [ ] enforce max chars client-side (matches server)

### Tag
- `milestone-react-mvp-local`

---

## Phase 5 — Web deployment on VPS (frontend + Express)

### Goals
- put a real web app online on your own infrastructure
- introduce reverse proxy + process manager
- keep ML service separate (still local or staging at first)

### Checklist
- [ ] create Express API skeleton (`services/web_api` or similar)
- [ ] VPS setup:
  - [ ] SSH access + basic hardening
  - [ ] install Node.js
  - [ ] install Nginx or Caddy
  - [ ] install PM2
- [ ] deploy React build and serve with Nginx
- [ ] run Express with PM2
- [ ] configure reverse proxy:
  - [ ] `/` → React static
  - [ ] `/api/*` → Express

### Tag
- `milestone-vps-deploy-web`

---

## Phase 6 — Domain + HTTPS

### Goals
- professional URL and TLS everywhere

### Checklist
- [ ] buy domain
- [ ] DNS records:
  - [ ] A record → VPS IP
- [ ] configure Nginx/Caddy server_name
- [ ] Let’s Encrypt cert
- [ ] redirect HTTP → HTTPS

### Tag
- `milestone-domain-https`

---

## Phase 7 — Production-grade inference deployment (EC2 + Docker)

### Goals
- run FastAPI + Kokoro on a dedicated inference server
- containerized and reproducible
- restricted access (only VPS can call it)

### Checklist
- [ ] create Dockerfile for `tts_api`
- [ ] build and run locally with Docker
- [ ] provision EC2 instance (GPU optional)
- [ ] install Docker + Docker Compose
- [ ] deploy container
- [ ] open only necessary ports in security group
- [ ] restrict inbound access to the VPS IP
- [ ] optionally add reverse proxy on EC2 (TLS termination or internal only)
- [ ] connect:
  - [ ] Express (VPS) → FastAPI (EC2)

### Tag
- `milestone-ec2-inference`

---

## Phase 8 — MVP online (anonymous quota + S3)

### Goals
- “real product loop” online
- anonymous usage allowed with quota enforcement
- audio stored and served securely

### Checklist
- [ ] quota system (characters) for anonymous users
- [ ] persist generated audio in S3
- [ ] return signed URLs for download
- [ ] basic abuse protection (rate limits, max chars)
- [ ] minimal UI polish (errors, loading, empty state)

### Tag
- `milestone-mvp-online`

---

## Phase 9 — Product expansion (accounts + payments + premium)

### Goals
- user system and monetization
- prepare for voice cloning later

### Checklist
- [ ] landing page + product messaging
- [ ] user accounts (email/pass or OAuth)
- [ ] user quota tiers
- [ ] Stripe checkout + webhooks
- [ ] usage dashboard (quota, history, billing)

### Tags
- `milestone-auth`
- `milestone-stripe`

---

## Phase 10 — Voice cloning (later)

### Candidates
- XTTS v2
- OpenVoice

### Checklist
- [ ] licensing review before monetized deployment
- [ ] add voice upload + consent UX
- [ ] new inference service or model abstraction extension
- [ ] storage for reference audio (secure)
- [ ] “my voices” management UI

### Tag
- `milestone-voice-cloning`

---

## Upcoming features list (explicit)

### Near-term (after MVP is online)
- landing page + messaging
- better quota enforcement (anonymous + logged-in)
- basic admin controls (limits, abuse handling)
- S3 storage + signed URLs
- error reporting + basic monitoring

### Monetization features
- Stripe subscriptions/credits
- premium tier: higher limits + more voices
- usage dashboard (quota/history/billing)

### Advanced / later
- voice cloning
- streaming generation (optional)
- public API keys + developer portal
- CI/CD
- monitoring and observability
- model optimization (ONNX, batching, caching, cost tuning)

---

## Optional bonus extensions (kept separate)
- CI/CD pipelines
- automated tests
- observability stack (metrics, traces)
- product analytics
- security hardening and scalability
