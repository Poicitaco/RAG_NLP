'use client';

export const dynamic = 'force-dynamic';

import { useEffect, useState, useCallback } from 'react';
import { ShieldCheck, RefreshCw, Save, Wifi, WifiOff, CheckCircle, XCircle, AlertCircle, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const GROQ_MODELS = [
  'llama-3.3-70b-versatile', 'llama-3.1-8b-instant',
  'llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it',
];

type Config = Record<string, string | boolean | number>;
type HealthCheck = { status: string; code?: number; error?: string; size_mb?: number };
type Health = { overall: string; checks: Record<string, HealthCheck> };

function StatusBadge({ status }: { status: string }) {
  if (status === 'ok') return <span className="flex items-center gap-1 text-emerald-400 text-xs"><CheckCircle className="w-3.5 h-3.5" />OK</span>;
  if (status === 'missing') return <span className="flex items-center gap-1 text-red-400 text-xs"><XCircle className="w-3.5 h-3.5" />Missing</span>;
  return <span className="flex items-center gap-1 text-amber-400 text-xs"><AlertCircle className="w-3.5 h-3.5" />{status}</span>;
}

export default function AdminPage() {
  const [config, setConfig] = useState<Config>({});
  const [health, setHealth] = useState<Health | null>(null);
  const [kaggle, setKaggle] = useState<{ status: string; latency_ms?: number; error?: string } | null>(null);
  const [saving, setSaving] = useState<string | null>(null);
  const [pingLoading, setPingLoading] = useState(false);
  const [healthLoading, setHealthLoading] = useState(false);
  const [toast, setToast] = useState('');

  const showToast = (msg: string) => { setToast(msg); setTimeout(() => setToast(''), 3000); };

  const loadConfig = useCallback(async () => {
    const res = await fetch(`${API}/admin/config`);
    const data = await res.json();
    setConfig(data.config || {});
  }, []);

  const loadHealth = useCallback(async () => {
    setHealthLoading(true);
    const res = await fetch(`${API}/admin/health`);
    setHealth(await res.json());
    setHealthLoading(false);
  }, []);

  useEffect(() => { loadConfig(); loadHealth(); }, [loadConfig, loadHealth]);

  const save = async (key: string, value: string | boolean | number) => {
    setSaving(key);
    await fetch(`${API}/admin/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key, value }),
    });
    setSaving(null);
    showToast(`✓ Đã lưu ${key}`);
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  const pingKaggle = async () => {
    setPingLoading(true);
    const res = await fetch(`${API}/admin/ping-kaggle`);
    setKaggle(await res.json());
    setPingLoading(false);
  };

  const row = 'flex items-center justify-between py-3 border-b border-white/5';
  const label = 'text-sm text-white/70 w-48 shrink-0';
  const input = 'bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-white/30 w-64';

  return (
    <div className="min-h-screen bg-[#212121] text-white p-6">
      {toast && (
        <div className="fixed top-4 right-4 bg-emerald-500 text-white px-4 py-2 rounded-lg text-sm z-50">{toast}</div>
      )}
      <div className="max-w-3xl mx-auto space-y-8">

        {/* Header */}
        <div className="flex items-center gap-4">
          <Link href="/" className="text-white/40 hover:text-white/70 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-blue-400" />
            <h1 className="text-xl font-bold">Admin Panel</h1>
          </div>
        </div>

        {/* Health */}
        <section className="bg-white/5 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-white/80">System Health</h2>
            <div className="flex items-center gap-2">
              {health && (
                <span className={`text-xs px-2 py-0.5 rounded-full ${health.overall === 'ok' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                  {health.overall.toUpperCase()}
                </span>
              )}
              <button onClick={loadHealth} disabled={healthLoading} className="text-white/40 hover:text-white/70 transition-colors">
                <RefreshCw className={`w-4 h-4 ${healthLoading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>
          {health && Object.entries(health.checks).map(([name, check]) => (
            <div key={name} className="flex items-center justify-between text-sm">
              <span className="text-white/50 capitalize">{name.replace('_', ' ')}</span>
              <div className="flex items-center gap-2">
                {check.size_mb && <span className="text-white/30 text-xs">{check.size_mb} MB</span>}
                <StatusBadge status={check.status} />
              </div>
            </div>
          ))}
        </section>

        {/* LLM Config */}
        <section className="bg-white/5 rounded-2xl p-5 space-y-1">
          <h2 className="font-semibold text-white/80 mb-4">LLM Configuration</h2>

          <div className={row}>
            <span className={label}>Provider</span>
            <div className="flex gap-2">
              {['groq', 'gemini'].map(p => (
                <button key={p} onClick={() => save('LLM_PROVIDER', p)}
                  className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${config.LLM_PROVIDER === p ? 'bg-blue-500 text-white' : 'bg-white/5 text-white/50 hover:text-white'}`}>
                  {p}
                </button>
              ))}
            </div>
          </div>

          <div className={row}>
            <span className={label}>Model</span>
            <select value={String(config.LLM_MODEL || '')} onChange={e => save('LLM_MODEL', e.target.value)}
              className={input}>
              {GROQ_MODELS.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>

          <div className={row}>
            <span className={label}>Planner Model</span>
            <select value={String(config.LLM_PLANNER_MODEL || '')} onChange={e => save('LLM_PLANNER_MODEL', e.target.value)}
              className={input}>
              {GROQ_MODELS.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>

          <div className={row}>
            <span className={label}>Max Output Tokens</span>
            <EditableNumber configKey="LLM_MAX_OUTPUT_TOKENS" value={config.LLM_MAX_OUTPUT_TOKENS} onSave={save} saving={saving} />
          </div>

          <div className={row}>
            <span className={label}>Temperature</span>
            <EditableNumber configKey="LLM_TEMPERATURE" value={config.LLM_TEMPERATURE} onSave={save} saving={saving} />
          </div>
        </section>

        {/* Feature Flags */}
        <section className="bg-white/5 rounded-2xl p-5 space-y-1">
          <h2 className="font-semibold text-white/80 mb-4">Feature Flags</h2>
          {(['USE_LLM_ANSWER', 'USE_LLM_PLANNER', 'USE_TIERED_CLARIFICATION'] as const).map(key => (
            <div key={key} className={row}>
              <span className={label}>{key}</span>
              <button onClick={() => save(key, !config[key])}
                className={`relative w-10 h-5 rounded-full transition-colors ${config[key] ? 'bg-blue-500' : 'bg-white/10'}`}>
                <span className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${config[key] ? 'left-5' : 'left-0.5'}`} />
              </button>
            </div>
          ))}
        </section>

        {/* Retrieval Tuning */}
        <section className="bg-white/5 rounded-2xl p-5 space-y-1">
          <h2 className="font-semibold text-white/80 mb-4">Retrieval Tuning</h2>
          <div className={row}>
            <span className={label}>Min Hybrid Score</span>
            <EditableNumber configKey="MIN_HYBRID_SCORE" value={config.MIN_HYBRID_SCORE} onSave={save} saving={saving} />
          </div>
          <div className={row}>
            <span className={label}>Rule Match Threshold</span>
            <EditableNumber configKey="RULE_MATCH_THRESHOLD" value={config.RULE_MATCH_THRESHOLD} onSave={save} saving={saving} />
          </div>
        </section>

        {/* Kaggle API */}
        <section className="bg-white/5 rounded-2xl p-5 space-y-4">
          <h2 className="font-semibold text-white/80">Kaggle Embedding API</h2>
          <EditableText configKey="KAGGLE_API_URL" value={String(config.KAGGLE_API_URL || '')} onSave={save} saving={saving} placeholder="https://xxx.trycloudflare.com" />
          <div className="flex items-center gap-3">
            <button onClick={pingKaggle} disabled={pingLoading}
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/15 rounded-lg text-sm transition-colors disabled:opacity-50">
              {pingLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Wifi className="w-4 h-4" />}
              Ping API
            </button>
            {kaggle && (
              <span className={`flex items-center gap-1.5 text-sm ${kaggle.status === 'ok' ? 'text-emerald-400' : 'text-red-400'}`}>
                {kaggle.status === 'ok' ? <CheckCircle className="w-4 h-4" /> : <WifiOff className="w-4 h-4" />}
                {kaggle.status === 'ok' ? `OK — ${kaggle.latency_ms}ms` : kaggle.error || kaggle.status}
              </span>
            )}
          </div>
        </section>

        <p className="text-center text-xs text-white/25 pb-4">
          Thay đổi được ghi vào .env — restart backend để áp dụng đầy đủ
        </p>
      </div>
    </div>
  );
}

function EditableNumber({ configKey, value, onSave, saving }: {
  configKey: string; value: unknown; onSave: (k: string, v: number) => void; saving: string | null;
}) {
  const [v, setV] = useState(String(value ?? ''));
  useEffect(() => setV(String(value ?? '')), [value]);
  return (
    <div className="flex gap-2">
      <input type="number" value={v} onChange={e => setV(e.target.value)} step="any"
        className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-white/30 w-32" />
      <button onClick={() => onSave(configKey, Number(v))} disabled={saving === configKey}
        className="p-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-white/70 transition-colors disabled:opacity-50">
        {saving === configKey ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
      </button>
    </div>
  );
}

function EditableText({ configKey, value, onSave, saving, placeholder }: {
  configKey: string; value: string; onSave: (k: string, v: string) => void; saving: string | null; placeholder?: string;
}) {
  const [v, setV] = useState(value);
  useEffect(() => setV(value), [value]);
  return (
    <div className="flex gap-2">
      <input type="text" value={v} onChange={e => setV(e.target.value)} placeholder={placeholder}
        className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-white/30 flex-1" />
      <button onClick={() => onSave(configKey, v)} disabled={saving === configKey}
        className="p-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-white/70 transition-colors disabled:opacity-50">
        {saving === configKey ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
      </button>
    </div>
  );
}
