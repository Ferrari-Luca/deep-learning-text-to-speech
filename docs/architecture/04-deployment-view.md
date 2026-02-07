# Deployment View

This document shows **where each component runs physically**.

```mermaid
flowchart LR
  subgraph VPS
    N[Nginx]
    FE[React Build]
    BE[Express API<br/>Process manager: PM2]
  end

  subgraph EC2
    D[Docker Engine]
    ML[FastAPI + Kokoro]
  end

  subgraph Managed
    DB[(MongoDB Atlas)]
    S3[(Amazon S3)]
    ST[Stripe]
  end

  BE --> ML
  BE --> DB
  BE --> S3
  BE -.-> ST
