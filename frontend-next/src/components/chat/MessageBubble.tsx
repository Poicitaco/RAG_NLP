'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { AlertTriangle, BookOpen, Info, ShieldAlert, ThumbsDown, ThumbsUp } from 'lucide-react';
import { Source } from '@/lib/api';

interface Props {
  role: 'user' | 'assistant';
  content: string;
  streaming?: boolean;
  warnings?: string[];
  suggestions?: string[];
  sources?: Source[];
  agentType?: string;
  confidence?: number;
  rawLog?: Record<string, unknown>;
  onSuggestionClick?: (s: string) => void;
  feedbackRating?: number;
  onFeedback?: (r: number) => void;
}

export default function MessageBubble({
  role, content, streaming,
  warnings = [], suggestions = [], sources = [],
  agentType, confidence, rawLog,
  onSuggestionClick, feedbackRating, onFeedback,
}: Props) {
  const isUser = role === 'user';

  // Process citations: replace [S1] with inline badge (handled inside markdown as text)
  const processedContent = content; // We'll render citations after markdown

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div className="max-w-[80%] bg-[#2f2f2f] rounded-2xl rounded-tr-sm px-4 py-3 text-sm text-white leading-relaxed">
          {content}
        </div>
      </div>
    );
  }

  const confidenceLabel =
    typeof confidence === 'number'
      ? confidence >= 0.75 ? { text: 'Độ tin cậy cao', cls: 'text-emerald-400' }
        : confidence >= 0.45 ? { text: 'Độ tin cậy trung bình', cls: 'text-amber-400' }
        : { text: 'Độ tin cậy thấp', cls: 'text-red-400' }
      : null;

  return (
    <div className="flex justify-start mb-4 group">
      <div className="max-w-[85%] md:max-w-[80%] w-full space-y-3">
        
        {/* Main content */}
        <div className={`text-sm text-white/90 leading-relaxed prose-chat ${streaming ? 'typing-cursor' : ''}`}>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              // Inline code
              code: ({ children, className, ...props }) => {
                const isBlock = className?.includes('language-');
                if (isBlock) {
                  return <code className={className} {...props}>{children}</code>;
                }
                return <code className="bg-white/10 px-1.5 py-0.5 rounded text-[0.85em] font-mono" {...props}>{children}</code>;
              },
              // Render citation badges [S1], [S2]
              text: ({ children }) => {
                const str = String(children);
                if (!/\[S\d+\]/.test(str)) return <>{children}</>;
                const parts = str.split(/(\[S\d+\])/g);
                return (
                  <>
                    {parts.map((part, i) => {
                      const match = part.match(/^\[S(\d+)\]$/);
                      if (!match) return <React.Fragment key={i}>{part}</React.Fragment>;
                      const idx = Number(match[1]) - 1;
                      const src = sources[idx];
                      return (
                        <span key={i} className="citation-badge mx-0.5 group/cite relative">
                          {part}
                          {src && (
                            <span className="pointer-events-none absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-10 hidden group-hover/cite:block w-64 bg-[#1a1a1a] border border-white/20 rounded-xl p-3 text-xs text-white/80 shadow-xl">
                              <strong className="block text-white mb-1">{src.title || part}</strong>
                              <span className="text-white/50">{src.source}</span>
                            </span>
                          )}
                        </span>
                      );
                    })}
                  </>
                );
              },
            }}
          >
            {processedContent}
          </ReactMarkdown>
        </div>

        {/* Confidence & agent badge */}
        {(agentType || confidenceLabel) && !streaming && (
          <div className="flex items-center gap-2 flex-wrap">
            {agentType && (
              <span className="text-xs text-white/40 bg-white/5 px-2 py-0.5 rounded-full">
                {agentType}
              </span>
            )}
            {confidenceLabel && (
              <span className={`text-xs ${confidenceLabel.cls}`}>
                {confidenceLabel.text}
              </span>
            )}
          </div>
        )}

        {/* Warnings */}
        {!streaming && warnings.length > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-red-300">
            <div className="flex items-center gap-2 font-semibold text-sm mb-2">
              <ShieldAlert className="w-4 h-4" />
              Cảnh báo an toàn
            </div>
            <ul className="list-disc pl-4 space-y-1 text-xs leading-relaxed">
              {warnings.map((w, i) => <li key={i}>{w}</li>)}
            </ul>
          </div>
        )}

        {/* Suggestions */}
        {!streaming && suggestions.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center gap-1.5 text-xs text-white/40">
              <AlertTriangle className="w-3.5 h-3.5" />
              Câu hỏi gợi ý
            </div>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => onSuggestionClick?.(s)}
                  className="text-xs px-3 py-1.5 rounded-full border border-white/20 text-white/70 hover:text-white hover:border-white/40 hover:bg-white/5 transition-colors text-left max-w-[280px] truncate"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Sources */}
        {!streaming && sources.length > 0 && (
          <div className="space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs text-white/40 uppercase tracking-wider">
              <BookOpen className="w-3.5 h-3.5" />
              Nguồn tham khảo
            </div>
            <div className="space-y-1">
              {sources.map((src, i) => (
                <a
                  key={i}
                  href={src.url || '#'}
                  target="_blank"
                  rel="noreferrer"
                  className="block text-xs text-blue-400/80 hover:text-blue-400 truncate py-0.5"
                >
                  [{i + 1}] {src.title} <span className="text-white/30">— {src.source}</span>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Feedback + Audit Log */}
        {!streaming && onFeedback && (
          <div className="flex items-center gap-3 pt-1 border-t border-white/5">
            <button
              onClick={() => onFeedback(1)}
              className={`p-1.5 rounded-lg transition-colors ${feedbackRating === 1 ? 'text-emerald-400 bg-emerald-400/10' : 'text-white/30 hover:text-white/60'}`}
              aria-label="Hữu ích"
            >
              <ThumbsUp className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onFeedback(-1)}
              className={`p-1.5 rounded-lg transition-colors ${feedbackRating === -1 ? 'text-red-400 bg-red-400/10' : 'text-white/30 hover:text-white/60'}`}
              aria-label="Không hữu ích"
            >
              <ThumbsDown className="w-3.5 h-3.5" />
            </button>
            {rawLog && (
              <details className="ml-auto">
                <summary className="flex items-center gap-1 text-xs text-white/20 hover:text-white/40 cursor-pointer list-none">
                  <Info className="w-3 h-3" />
                  Audit log
                </summary>
                <div className="mt-2 bg-black/40 rounded-lg p-3 text-[11px] font-mono text-green-400 overflow-x-auto max-h-48">
                  <pre className="whitespace-pre-wrap break-all">{JSON.stringify(rawLog, null, 2)}</pre>
                </div>
              </details>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
