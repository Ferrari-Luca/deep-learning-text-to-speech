---

## 📄 `docs/architecture/02-network-and-security.md` (fixed formatting)

```markdown
# Network and Security Boundaries

This document describes the **trust zones** of the system and the enforced
security boundaries.

```mermaid
flowchart TB
  subgraph Public[Public Internet]
    U[User Browser]
  end

  subgraph VPS[VPS – Public Zone]
    N[Nginx / Caddy]
    FE[React]
    BE[Express API]
  end

  subgraph Cloud[Cloud / AWS]
    ML[EC2 – FastAPI + Kokoro]
    S3[(Amazon S3)]
  end

  subgraph Atlas[MongoDB Atlas]
    DB[(MongoDB)]
  end

  U -->|HTTPS| N
  N --> FE
  N --> BE

  BE -->|Restricted access| ML
  BE --> DB
  BE --> S3
