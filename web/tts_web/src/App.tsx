import { useEffect, useMemo, useState } from 'react';
import { postTTS, type LangCode } from './api/tts';

const MAX_CHARS = 500;

type VoiceOption = { label: string; voice: string; lang: LangCode };

const VOICES: VoiceOption[] = [
  { label: 'EN (US) — Bella', voice: 'af_bella', lang: 'a' },
  { label: 'EN (GB) — Emma', voice: 'bf_emma', lang: 'b' },
  { label: 'FR — Siwis', voice: 'ff_siwis', lang: 'f' },
];

export default function App() {
  const [text, setText] = useState('Hello from the React MVP!');
  const [voice, setVoice] = useState(VOICES[0].voice);
  const [speed, setSpeed] = useState(1.0);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [meta, setMeta] = useState<{ requestId?: string; latencyMs?: number } | null>(null);

  const selected = useMemo(() => VOICES.find((v) => v.voice === voice)!, [voice]);
  const remaining = MAX_CHARS - text.length;

  useEffect(() => {
    return () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  async function onGenerate() {
    setError(null);
    setMeta(null);

    const trimmed = text.trim();
    if (!trimmed) return setError('Text cannot be empty.');
    if (trimmed.length > MAX_CHARS)
      return setError(`Text is too long (max ${MAX_CHARS} characters).`);

    setLoading(true);
    try {
      const res = await postTTS({
        text: trimmed,
        lang: selected.lang,
        voice: selected.voice,
        speed,
      });

      if (audioUrl) URL.revokeObjectURL(audioUrl);
      const url = URL.createObjectURL(res.blob);
      setAudioUrl(url);
      setMeta({ requestId: res.requestId, latencyMs: res.latencyMs });
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  function onDownload() {
    if (!audioUrl) return;
    const a = document.createElement('a');
    a.href = audioUrl;
    a.download = `tts_${voice}_${meta?.requestId ?? 'local'}.wav`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  return (
    <div style={{ maxWidth: 720, margin: '40px auto', padding: 16, fontFamily: 'system-ui' }}>
      <h1>TTS MVP (Local)</h1>

      <label>
        Text ({text.length}/{MAX_CHARS})
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          style={{ width: '100%', marginTop: 8 }}
        />
      </label>
      <div style={{ marginTop: 6, opacity: 0.8 }}>Remaining: {remaining}</div>

      <div style={{ display: 'flex', gap: 12, marginTop: 16, alignItems: 'center' }}>
        <label>
          Voice
          <select
            value={voice}
            onChange={(e) => setVoice(e.target.value)}
            style={{ marginLeft: 8 }}
            disabled={loading}
          >
            {VOICES.map((v) => (
              <option key={v.voice} value={v.voice}>
                {v.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Speed
          <input
            type="number"
            step={0.1}
            min={0.8}
            max={1.2}
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            style={{ marginLeft: 8, width: 80 }}
            disabled={loading}
          />
        </label>

        <button onClick={onGenerate} disabled={loading} style={{ padding: '8px 12px' }}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </div>

      {error && (
        <div style={{ marginTop: 16, padding: 12, border: '1px solid #ccc' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {audioUrl && (
        <div style={{ marginTop: 24 }}>
          <audio controls src={audioUrl} style={{ width: '100%' }} />
          <div style={{ marginTop: 12, display: 'flex', gap: 12, alignItems: 'center' }}>
            <button onClick={onDownload}>Download WAV</button>
            {meta?.requestId && <span style={{ opacity: 0.8 }}>request_id: {meta.requestId}</span>}
            {typeof meta?.latencyMs === 'number' && (
              <span style={{ opacity: 0.8 }}>latency: {meta.latencyMs} ms</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
