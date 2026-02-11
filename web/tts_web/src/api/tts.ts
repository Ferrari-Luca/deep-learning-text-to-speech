export type LangCode = 'a' | 'b' | 'f';

export type TTSRequest = {
  text: string;
  lang: LangCode;
  voice: string;
  speed: number;
};

export type TTSResponse = {
  blob: Blob;
  requestId?: string;
  latencyMs?: number;
  chars?: number;
};

const API_BASE = 'http://127.0.0.1:8000';

export async function postTTS(payload: TTSRequest): Promise<TTSResponse> {
  const res = await fetch(`${API_BASE}/tts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      if (data?.detail) message = String(data.detail);
    } catch {
      try {
        message = await res.text();
      } catch {
        // ignore
      }
    }
    throw new Error(message);
  }

  const blob = await res.blob();

  const requestId = res.headers.get('x-request-id') ?? undefined;
  const latencyMsStr = res.headers.get('x-latency-ms');
  const charsStr = res.headers.get('x-chars');

  return {
    blob,
    requestId,
    latencyMs: latencyMsStr ? Number(latencyMsStr) : undefined,
    chars: charsStr ? Number(charsStr) : undefined,
  };
}
