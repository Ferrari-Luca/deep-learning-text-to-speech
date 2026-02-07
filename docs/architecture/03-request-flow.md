# Request Flow – Text-to-Speech Generation

This diagram shows the **lifecycle of a TTS request** from user input to audio
delivery.

```mermaid
sequenceDiagram
  participant U as User
  participant FE as React
  participant BE as Express
  participant ML as FastAPI (EC2)
  participant S3 as S3
  participant DB as MongoDB

  U->>FE: Enter text and click Generate
  FE->>BE: POST /api/tts
  BE->>DB: Check quota
  BE->>ML: POST /tts
  ML-->>BE: Audio bytes
  BE->>S3: Upload audio
  BE->>DB: Store metadata
  BE-->>FE: Audio URL
  FE-->>U: Play / Download
