# Architecture Decisions

## Why a VPS instead of fully managed platforms?
To maximize learning around deployment, networking, process management, and
system administration, which are essential skills for real-world AI products.

## Why separate Express and FastAPI?
- Clear separation of concerns
- Independent scaling of web logic and ML inference
- Ability to swap or upgrade models without impacting the frontend

## Why self-host the model?
- Deeper understanding of inference constraints
- Full control over customization, latency, and costs
