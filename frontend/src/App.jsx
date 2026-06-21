import React, { useEffect, useMemo, useRef, useState } from "react";
import { useGSAP } from "@gsap/react";
import { gsap } from "gsap";
import {
  ArrowClockwise,
  ChatsCircle,
  CheckCircle,
  FirstAidKit,
  Heartbeat,
  MagnifyingGlass,
  PaperPlaneTilt,
  ShieldCheck,
  Siren,
  Sparkle,
  WarningCircle,
} from "@phosphor-icons/react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

const examples = [
  {
    label: "Cảm khi bị tiểu đường",
    text: "Tui bị tiểu đường, giờ muốn mua thuốc cảm thì nên tránh loại nào?",
    tone: "caution",
  },
  {
    label: "Tương tác thuốc",
    text: "Aspirin uống chung với ibuprofen có sao không?",
    tone: "danger",
  },
  {
    label: "Bệnh thận",
    text: "Tôi bị suy thận, đau đầu thì nên tránh thuốc giảm đau nào?",
    tone: "caution",
  },
  {
    label: "Dấu hiệu khẩn cấp",
    text: "Tôi uống thuốc xong bị khó thở và sưng môi thì làm sao?",
    tone: "danger",
  },
];

const openingMessages = [
  {
    id: "hello",
    role: "assistant",
    message:
      "Chào bạn. Mình sẽ kiểm tra câu hỏi qua safety router, bệnh nền, tương tác thuốc và bằng chứng RAG trước khi trả lời. Nếu thiếu tuổi, bệnh nền, thuốc đang dùng hoặc dị ứng, mình sẽ hỏi lại trước.",
    metadata: {
      rag_action: "ready",
      intent: "drug_info",
      selected_agents: ["Safety Router", "Patient Context Collector", "Graph Safety", "Hybrid RAG"],
      patient_context: {},
    },
  },
];

function uid(prefix = "msg") {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function actionMeta(action) {
  const normalized = action || "ready";
  const map = {
    emergency: { label: "Khẩn cấp", tone: "danger", icon: Siren },
    contraindicated: { label: "Không nên dùng", tone: "danger", icon: WarningCircle },
    needs_clarification: { label: "Cần hỏi thêm", tone: "question", icon: MagnifyingGlass },
    allow_with_caution: { label: "Dùng thận trọng", tone: "caution", icon: WarningCircle },
    allowed: { label: "Có thể trả lời", tone: "safe", icon: CheckCircle },
    ready: { label: "Sẵn sàng", tone: "safe", icon: ShieldCheck },
  };
  return map[normalized] || { label: normalized, tone: "neutral", icon: Heartbeat };
}

function splitResponse(message) {
  if (!message) return [];
  const blocks = [];
  const lines = message.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  let current = null;

  for (const line of lines) {
    const heading = line.match(/^\*\*(.+?)\*\*:?\s*(.*)$/);
    const plainHeading = line.match(/^([A-ZÀ-ỴĐ0-9\s/,-]{4,60}):\s*(.*)$/);
    if (heading) {
      if (current) blocks.push(current);
      current = { title: heading[1], body: heading[2] ? [heading[2]] : [] };
    } else if (plainHeading && !line.startsWith("-")) {
      if (current) blocks.push(current);
      current = {
        title: plainHeading[1].trim(),
        body: plainHeading[2] ? [plainHeading[2]] : [],
      };
    } else if (current) {
      current.body.push(line);
    } else {
      blocks.push({ title: "Trả lời", body: [line] });
    }
  }
  if (current) blocks.push(current);
  return blocks.length ? blocks : [{ title: "Trả lời", body: [message] }];
}

function sourceLabel(source) {
  if (!source) return "Nguồn nội bộ";
  if (typeof source === "string") return source;
  return source.title || source.source || source.url || "Nguồn tham chiếu";
}

function formatPercent(value) {
  if (typeof value !== "number") return null;
  return `${Math.round(value * 100)}%`;
}

function normalizeAgentName(agent) {
  if (!agent) return null;
  if (typeof agent === "string") return agent.replaceAll("_", " ");
  return agent.name || agent.agent || JSON.stringify(agent);
}

function extractPatientContext(messages) {
  const latest = [...messages]
    .reverse()
    .find((msg) => msg.role === "assistant" && msg.metadata?.patient_context);
  return latest?.metadata?.patient_context || {};
}

function App() {
  const root = useRef(null);
  const listRef = useRef(null);
  const inputRef = useRef(null);
  const [sessionId, setSessionId] = useState(() => `demo-${Date.now()}`);
  const [messages, setMessages] = useState(openingMessages);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const patientContext = useMemo(() => extractPatientContext(messages), [messages]);
  const latestAssistant = useMemo(
    () => [...messages].reverse().find((msg) => msg.role === "assistant"),
    [messages]
  );
  const latestAction = latestAssistant?.metadata?.rag_action || latestAssistant?.metadata?.action || "ready";
  const action = actionMeta(latestAction);

  useGSAP(
    () => {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      gsap.from(".shell-panel", {
        y: 18,
        opacity: 0,
        duration: 0.7,
        ease: "power3.out",
        stagger: 0.08,
      });
      gsap.from(".quick-card", {
        y: 16,
        opacity: 0,
        duration: 0.5,
        delay: 0.25,
        ease: "power2.out",
        stagger: 0.06,
      });
    },
    { scope: root }
  );

  useEffect(() => {
    listRef.current?.lastElementChild?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const item = listRef.current?.lastElementChild;
    if (!item) return;
    gsap.fromTo(item, { y: 12, opacity: 0 }, { y: 0, opacity: 1, duration: 0.28, ease: "power2.out" });
  }, [messages.length]);

  async function sendMessage(text = input) {
    const clean = text.trim();
    if (!clean || loading) return;

    const userMessage = { id: uid("user"), role: "user", message: clean };
    setMessages((current) => [...current, userMessage]);
    setInput("");
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: clean,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || `HTTP ${response.status}`);
      }

      const data = await response.json();
      setMessages((current) => [
        ...current,
        {
          id: uid("assistant"),
          role: "assistant",
          message: data.message,
          metadata: data.metadata || {},
          sources: data.sources || [],
          warnings: data.warnings || [],
          confidence: data.confidence,
          agentType: data.agent_type,
        },
      ]);
    } catch (err) {
      setError(
        "Chưa gọi được backend. Hãy chạy API ở port 8001 rồi thử lại. Chi tiết: " +
          (err?.message || "unknown error")
      );
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function resetSession() {
    setSessionId(`demo-${Date.now()}`);
    setMessages(openingMessages);
    setInput("");
    setError("");
    inputRef.current?.focus();
  }

  const ActionIcon = action.icon;

  return (
    <main className="app-shell" ref={root}>
      <section className="topbar shell-panel">
        <div>
          <p className="eyebrow">Vietnamese Medication Safety Agent</p>
          <h1>An tâm dùng thuốc</h1>
        </div>
        <div className={`status-pill ${action.tone}`}>
          <ActionIcon size={18} weight="bold" />
          <span>{action.label}</span>
        </div>
      </section>

      <section className="workspace">
        <aside className="left-rail shell-panel">
          <div className="rail-card primary">
            <div className="card-heading">
              <ShieldCheck size={22} weight="fill" />
              <span>Lưới an toàn</span>
            </div>
            <p>
              Bot chỉ dùng LLM để viết lại câu trả lời đã được kiểm tra. Cảnh báo từ Graph Safety được ưu tiên
              hơn câu trả lời RAG.
            </p>
          </div>

          <div className="rail-card">
            <div className="card-heading">
              <FirstAidKit size={22} weight="fill" />
              <span>Hồ sơ đang biết</span>
            </div>
            <PatientContext context={patientContext} />
          </div>

          <div className="rail-card">
            <div className="card-heading">
              <Heartbeat size={22} weight="fill" />
              <span>Agent trace</span>
            </div>
            <AgentTrace metadata={latestAssistant?.metadata || {}} />
          </div>
        </aside>

        <section className="chat-shell shell-panel">
          <div className="chat-header">
            <div>
              <p className="eyebrow">Demo hội thoại</p>
              <h2>Hỏi như người dân thật</h2>
            </div>
            <button className="ghost-button" onClick={resetSession} type="button">
              <ArrowClockwise size={18} />
              Làm mới
            </button>
          </div>

          <div className="quick-grid" aria-label="Câu hỏi thử nhanh">
            {examples.map((example) => (
              <button
                className={`quick-card ${example.tone}`}
                key={example.label}
                onClick={() => sendMessage(example.text)}
                type="button"
                disabled={loading}
              >
                <span>{example.label}</span>
                <small>{example.text}</small>
              </button>
            ))}
          </div>

          <div className="message-list" ref={listRef} aria-live="polite">
            {messages.map((message) => (
              <MessageBubble key={message.id} item={message} />
            ))}
            {loading && <TypingBubble />}
          </div>

          {error && (
            <div className="error-box" role="alert">
              <WarningCircle size={20} weight="fill" />
              <span>{error}</span>
            </div>
          )}

          <form
            className="composer"
            onSubmit={(event) => {
              event.preventDefault();
              sendMessage();
            }}
          >
            <label className="sr-only" htmlFor="message-input">
              Nhập câu hỏi thuốc
            </label>
            <ChatsCircle size={22} weight="fill" />
            <textarea
              id="message-input"
              ref={inputRef}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  sendMessage();
                }
              }}
              placeholder="Ví dụ: Tôi 45 tuổi bị tăng huyết áp, đang muốn mua thuốc cảm..."
              rows={2}
            />
            <button className="send-button" type="submit" disabled={loading || !input.trim()}>
              <PaperPlaneTilt size={20} weight="fill" />
              Gửi
            </button>
          </form>
        </section>

        <aside className="right-rail shell-panel">
          <div className="rail-card">
            <div className="card-heading">
              <Sparkle size={22} weight="fill" />
              <span>Đọc kết quả</span>
            </div>
            <ul className="check-list">
              <li>Khối cảnh báo luôn nằm đầu nếu có vi phạm an toàn.</li>
              <li>Nếu thiếu thông tin bệnh nền hoặc thuốc đang dùng, bot hỏi lại.</li>
              <li>Citation và agent trace giúp giải thích vì sao bot trả lời như vậy.</li>
            </ul>
          </div>
          <div className="rail-card soft">
            <p className="metric-label">Backend</p>
            <strong>{API_BASE_URL}</strong>
            <p className="muted">Đổi bằng biến `VITE_API_BASE_URL` khi deploy hoặc demo port khác.</p>
          </div>
        </aside>
      </section>
    </main>
  );
}

function PatientContext({ context }) {
  const fields = [
    ["Tuổi", context.age || context.age_months],
    ["Bệnh nền", Array.isArray(context.conditions) ? context.conditions.join(", ") : context.conditions],
    ["Đang dùng thuốc", Array.isArray(context.current_medications) ? context.current_medications.join(", ") : context.current_medications],
    ["Dị ứng", Array.isArray(context.allergies) ? context.allergies.join(", ") : context.allergies],
  ];
  const hasAny = fields.some(([, value]) => value);

  if (!hasAny) {
    return <p className="empty-note">Chưa có thông tin. Bot sẽ hỏi lại khi câu hỏi có rủi ro.</p>;
  }

  return (
    <div className="context-list">
      {fields.map(([label, value]) => (
        <div className="context-row" key={label}>
          <span>{label}</span>
          <strong>{value || "Chưa rõ"}</strong>
        </div>
      ))}
    </div>
  );
}

function AgentTrace({ metadata }) {
  const agents = metadata.selected_agents || metadata.agent_pipeline || [];
  const intent = metadata.intent || "chưa phân loại";
  const confidence = formatPercent(metadata.confidence);

  return (
    <div className="trace">
      <div className="context-row">
        <span>Intent</span>
        <strong>{intent}</strong>
      </div>
      {confidence && (
        <div className="context-row">
          <span>Tin cậy</span>
          <strong>{confidence}</strong>
        </div>
      )}
      <div className="agent-stack">
        {(agents.length ? agents : ["Safety Router", "Hybrid RAG"]).slice(0, 6).map((agent, index) => (
          <span key={`${normalizeAgentName(agent)}-${index}`}>{normalizeAgentName(agent)}</span>
        ))}
      </div>
    </div>
  );
}

function MessageBubble({ item }) {
  const isUser = item.role === "user";
  const action = actionMeta(item.metadata?.rag_action || item.metadata?.action);
  const ActionIcon = action.icon;
  const blocks = splitResponse(item.message);
  const sources = item.sources || [];

  return (
    <article className={`message ${isUser ? "user" : "assistant"}`}>
      {!isUser && (
        <div className={`message-badge ${action.tone}`}>
          <ActionIcon size={16} weight="bold" />
          {action.label}
        </div>
      )}
      <div className="bubble">
        {isUser ? (
          <p>{item.message}</p>
        ) : (
          <div className="response-blocks">
            {blocks.map((block) => (
              <section className={blockClass(block.title)} key={block.title + block.body.join("")}>
                <h3>{block.title}</h3>
                {block.body.map((line) => (
                  <p key={line}>{line}</p>
                ))}
              </section>
            ))}
          </div>
        )}
      </div>
      {!isUser && sources.length > 0 && (
        <div className="source-strip">
          {sources.slice(0, 4).map((source, index) => (
            <a
              key={`${sourceLabel(source)}-${index}`}
              href={typeof source === "object" && source.url ? source.url : undefined}
              target="_blank"
              rel="noreferrer"
            >
              [{index + 1}] {sourceLabel(source)}
            </a>
          ))}
        </div>
      )}
    </article>
  );
}

function blockClass(title) {
  const normalized = title.toLowerCase();
  if (normalized.includes("cảnh báo") || normalized.includes("an toàn")) return "answer-block alert";
  if (normalized.includes("nguồn") || normalized.includes("citation")) return "answer-block source";
  if (normalized.includes("cần hỏi")) return "answer-block question";
  return "answer-block";
}

function TypingBubble() {
  return (
    <article className="message assistant typing">
      <div className="message-badge question">
        <MagnifyingGlass size={16} weight="bold" />
        Đang kiểm tra
      </div>
      <div className="bubble">
        <div className="typing-row">
          <span />
          <span />
          <span />
        </div>
        <p>Đang chạy safety router, graph safety và RAG evidence...</p>
      </div>
    </article>
  );
}

export default App;
