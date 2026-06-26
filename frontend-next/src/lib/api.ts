export type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue };
export type JsonObject = { [key: string]: JsonValue };

export interface Source {
  id?: string;
  title?: string;
  source?: string;
  url?: string;
  chunk_id?: string;
  [key: string]: JsonValue | undefined;
}

export interface MessageMetadata {
  warnings?: string[];
  suggestions?: string[];
  sources?: Source[];
  agentType?: string;
  confidence?: number;
  rawLog?: JsonObject;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: MessageMetadata;
  streaming?: boolean;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  agent_type: string;
  confidence: number;
  sources: Source[];
  warnings: string[];
  suggestions: string[];
  metadata: JsonObject;
}

export interface FeedbackPayload {
  query: string;
  response: string;
  rating: number;
  feedback_type?: string;
  metadata?: JsonObject;
  text_feedback?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface StreamCallbacks {
  onToken: (token: string) => void;
  onDone: (meta: Omit<MessageMetadata, 'rawLog'> & { metadata?: JsonObject }) => void;
  onError: (err: string) => void;
}

export async function sendMessageStream(
  message: string,
  sessionId: string,
  context: JsonObject | undefined,
  callbacks: StreamCallbacks,
  signal?: AbortSignal
): Promise<void> {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId, context }),
    signal,
  });

  if (!response.ok || !response.body) {
    throw new Error(`HTTP ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split('\n\n');
    buffer = lines.pop() ?? '';

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      try {
        const parsed = JSON.parse(line.slice(6));
        if (parsed.type === 'token') {
          callbacks.onToken(parsed.data);
        } else if (parsed.type === 'done') {
          const d = parsed.data || parsed;
          callbacks.onDone({
            sources: d.sources,
            warnings: d.warnings,
            suggestions: d.suggestions,
            agentType: d.agent_type,
            confidence: d.confidence,
            metadata: d.metadata,
          });
        } else if (parsed.type === 'error') {
          callbacks.onError(parsed.data || parsed.content || 'Unknown error');
        }
      } catch { /* ignore parse errors */ }
    }
  }
}

export async function submitFeedback(payload: FeedbackPayload) {
  const response = await fetch(`${API_URL}/feedback/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error('Failed to submit feedback');
  return response.json();
}

export async function getHistory(sessionId: string): Promise<Message[]> {
  const response = await fetch(`${API_URL}/chat/history/${sessionId}`);
  if (!response.ok) return [];
  const data = await response.json();
  return data.data || [];
}
