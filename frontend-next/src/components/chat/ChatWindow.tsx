'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import MessageBubble from './MessageBubble';
import QuickStartPanel from './QuickStartPanel';
import AskUserInput from './AskUserInput';
import { sendMessageStream, submitFeedback, Message, JsonObject } from '@/lib/api';
import { Send, Square } from 'lucide-react';

interface ChatWindowProps {
  sessionId: string;
  patientContext?: JsonObject | null;
}

const GREETING: Message = {
  role: 'assistant',
  content: 'Xin chào! Tôi là trợ lý tư vấn dược phẩm dựa trên **Dược thư Quốc gia Việt Nam**.\n\nBạn muốn hỏi về thuốc gì, hoặc đang có triệu chứng nào cần tư vấn?',
  timestamp: new Date().toISOString(),
};

export default function ChatWindow({ sessionId, patientContext }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([GREETING]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [feedbackRatings, setFeedbackRatings] = useState<Record<number, number>>({});
  const [accumulatedContext, setAccumulatedContext] = useState<JsonObject>({});
  const abortRef = useRef<AbortController | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
  }, [input]);

  const submitMessage = useCallback(async (content: string) => {
    const cleaned = content.trim();
    if (!cleaned || isStreaming) return;

    const userMsg: Message = { role: 'user', content: cleaned, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsStreaming(true);

    // Placeholder streaming message
    const streamingMsg: Message = {
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
      streaming: true,
    };
    setMessages(prev => [...prev, streamingMsg]);

    const context: JsonObject = { ...accumulatedContext, ...(patientContext || {}) };
    abortRef.current = new AbortController();

    try {
      await sendMessageStream(
        cleaned,
        sessionId,
        Object.keys(context).length ? context : undefined,
        {
          onToken: (token) => {
            setMessages(prev => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last?.role === 'assistant') {
                updated[updated.length - 1] = { ...last, content: last.content + token };
              }
              return updated;
            });
          },
          onDone: (meta) => {
            if (meta.metadata?.patient_context && typeof meta.metadata.patient_context === 'object') {
              setAccumulatedContext(prev => ({ ...prev, ...(meta.metadata!.patient_context as JsonObject) }));
            }
            setMessages(prev => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last?.role === 'assistant') {
                updated[updated.length - 1] = {
                  ...last,
                  streaming: false,
                  metadata: {
                    warnings: meta.warnings,
                    suggestions: meta.suggestions,
                    sources: meta.sources,
                    agentType: meta.agentType,
                    confidence: meta.confidence,
                    rawLog: meta.metadata as JsonObject,
                  },
                };
              }
              return updated;
            });
            setIsStreaming(false);
          },
          onError: (err) => {
            setMessages(prev => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                role: 'assistant',
                content: `Xin lỗi, đã xảy ra lỗi: ${err}`,
                timestamp: new Date().toISOString(),
                streaming: false,
              };
              return updated;
            });
            setIsStreaming(false);
          },
        },
        abortRef.current.signal
      );
    } catch (err: unknown) {
      if ((err as { name?: string }).name !== 'AbortError') {
        setMessages(prev => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: 'assistant',
            content: 'Xin lỗi, tôi đang gặp sự cố kết nối. Vui lòng thử lại.',
            timestamp: new Date().toISOString(),
            streaming: false,
          };
          return updated;
        });
      }
      setIsStreaming(false);
    }
  }, [isStreaming, sessionId, patientContext, accumulatedContext]);

  const handleStop = () => {
    abortRef.current?.abort();
    setIsStreaming(false);
    setMessages(prev => {
      const updated = [...prev];
      const last = updated[updated.length - 1];
      if (last?.streaming) {
        updated[updated.length - 1] = { ...last, streaming: false };
      }
      return updated;
    });
  };

  const handleSend = (e?: React.FormEvent) => {
    e?.preventDefault();
    submitMessage(input);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFeedback = async (messageIndex: number, rating: number) => {
    const msg = messages[messageIndex];
    if (!msg || msg.role !== 'assistant') return;
    const prev = messages.slice(0, messageIndex).reverse().find(m => m.role === 'user');
    try {
      await submitFeedback({ query: prev?.content || '', response: msg.content, rating, feedback_type: 'thumbs' });
      setFeedbackRatings(r => ({ ...r, [messageIndex]: rating }));
    } catch { /* ignore */ }
  };

  const hasUserMsg = messages.some(m => m.role === 'user');

  return (
    <div className="flex-1 flex flex-col min-h-0">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-6">
        <div className="max-w-3xl mx-auto px-4 space-y-1">
          {messages.map((msg, i) => (
            <MessageBubble
              key={i}
              role={msg.role}
              content={msg.content}
              streaming={msg.streaming}
              warnings={msg.metadata?.warnings}
              suggestions={msg.metadata?.suggestions}
              sources={msg.metadata?.sources}
              agentType={msg.metadata?.agentType}
              confidence={msg.metadata?.confidence}
              rawLog={msg.metadata?.rawLog}
              onSuggestionClick={submitMessage}
              feedbackRating={feedbackRatings[i]}
              onFeedback={msg.role === 'assistant' && !msg.streaming ? (r) => handleFeedback(i, r) : undefined}
            />
          ))}
          {/* AskUserInput — hiện sau tin nhắn cuối nếu needs_clarification và có triage_options */}
          {(() => {
            const last = [...messages].reverse().find(m => m.role === 'assistant');
            const rawLog = last?.metadata?.rawLog as Record<string, unknown> | undefined;
            if (!last || !rawLog || isStreaming) return null;
            if (rawLog.rag_action !== 'needs_clarification') return null;
            const question = (rawLog.clarification_questions as string[])?.[0] || '';
            const options = (rawLog.triage_options as string[]) || [];
            if (!question) return null;
            return (
              <AskUserInput
                key={messages.length}
                question={question}
                options={options}
                disabled={isStreaming}
                onSubmit={submitMessage}
                onSkip={() => submitMessage('Bỏ qua')}
              />
            );
          })()}
          {!hasUserMsg && !isStreaming && (
            <QuickStartPanel disabled={false} onSelect={submitMessage} />
          )}
          {/* Typing indicator — hiện khi đang xử lý, trước khi có token đầu tiên */}
          {isStreaming && messages[messages.length - 1]?.role !== 'assistant' && (
            <div className="flex justify-start mb-2">
              <div className="flex items-center gap-3 bg-[#2f2f2f] rounded-2xl rounded-bl-sm px-4 py-3 max-w-[120px]">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-white/60 animate-bounce [animation-delay:0ms]" />
                  <span className="w-2 h-2 rounded-full bg-white/60 animate-bounce [animation-delay:150ms]" />
                  <span className="w-2 h-2 rounded-full bg-white/60 animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-white/10 px-4 py-4">
        <form onSubmit={handleSend} className="max-w-3xl mx-auto relative">
          <div className="flex items-end gap-2 bg-[#2f2f2f] rounded-2xl border border-white/10 px-4 py-3 focus-within:border-white/30 transition-colors">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Hỏi về thuốc, liều dùng, tương tác... (Enter để gửi, Shift+Enter xuống dòng)"
              rows={1}
              disabled={isStreaming}
              className="flex-1 bg-transparent resize-none outline-none text-white placeholder-white/30 text-sm leading-relaxed max-h-48 overflow-y-auto"
            />
            {isStreaming ? (
              <button
                type="button"
                onClick={handleStop}
                className="flex-shrink-0 p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
                aria-label="Dừng"
              >
                <Square className="w-4 h-4 fill-current" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!input.trim()}
                className="flex-shrink-0 p-2 rounded-lg bg-white text-black hover:bg-white/90 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                aria-label="Gửi"
              >
                <Send className="w-4 h-4" />
              </button>
            )}
          </div>
          <p className="text-center text-xs text-white/25 mt-2">
            SafeRAG chỉ mang tính tham khảo — không thay thế chẩn đoán bác sĩ
          </p>
        </form>
      </div>
    </div>
  );
}
