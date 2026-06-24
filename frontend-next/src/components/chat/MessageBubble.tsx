import React from 'react';
import { ShieldAlert, Info, AlertTriangle, BookOpen, CheckCircle } from 'lucide-react';

interface Source {
  title: string;
  url: string | null;
  source: string;
}

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  warnings?: string[];
  suggestions?: string[];
  sources?: Source[];
  agentType?: string;
  rawLog?: any;
}

export default function MessageBubble({
  role,
  content,
  warnings = [],
  suggestions = [],
  sources = [],
  agentType,
  rawLog
}: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      <div className={`max-w-[85%] md:max-w-[75%] rounded-2xl p-5 shadow-sm ${isUser ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white border border-gray-100 text-gray-800 rounded-bl-none'}`}>
        
        {/* Helper badge cho AI */}
        {!isUser && agentType && (
          <div className="flex items-center gap-1.5 mb-3 text-xs font-medium text-blue-600 bg-blue-50 w-fit px-2.5 py-1 rounded-full">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Trợ lý Y tế (AI)</span>
          </div>
        )}

        {/* Nội dung chính */}
        <div 
          className="prose prose-sm md:prose-base max-w-none break-words" 
          dangerouslySetInnerHTML={{ 
            __html: content
              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
              .replace(/\*(.*?)\*/g, '<em>$1</em>')
              .replace(/\n/g, '<br/>')
              .replace(/(<br\/>)+\s*-\s/g, '<br/>• ')
          }} 
        />
        {/* Cảnh báo an toàn (Warnings) */}
        {!isUser && warnings.length > 0 && (
          <div className="mt-4 bg-red-50 border border-red-100 rounded-xl p-3 md:p-4 text-red-800">
            <div className="flex items-center gap-2 mb-2 font-bold">
              <ShieldAlert className="w-5 h-5 text-red-600" />
              <span>Cảnh báo An toàn quan trọng</span>
            </div>
            <ul className="list-disc pl-5 space-y-1 text-sm md:text-base">
              {warnings.map((w, idx) => (
                <li key={idx}>{w}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Lời khuyên (Suggestions) */}
        {!isUser && suggestions.length > 0 && (
          <div className="mt-3 bg-amber-50 border border-amber-100 rounded-xl p-3 md:p-4 text-amber-900">
            <div className="flex items-center gap-2 mb-2 font-semibold">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
              <span>Lời khuyên kèm theo</span>
            </div>
            <ul className="list-disc pl-5 space-y-1 text-sm md:text-base">
              {suggestions.map((s, idx) => (
                <li key={idx}>{s}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Trích dẫn (Sources) - Dành cho niềm tin */}
        {!isUser && sources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-gray-100">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider">
              <BookOpen className="w-3.5 h-3.5" />
              <span>Nguồn Tham Khảo Chính Thống</span>
            </div>
            <div className="space-y-2">
              {sources.map((s, idx) => (
                <a
                  key={idx}
                  href={s.url || '#'}
                  target="_blank"
                  rel="noreferrer"
                  className="block text-xs md:text-sm bg-gray-50 hover:bg-gray-100 p-2 rounded-lg border border-gray-100 transition-colors text-blue-700 font-medium truncate"
                >
                  {idx + 1}. {s.title} <span className="text-gray-400 font-normal">({s.source})</span>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Audit Log / Chứng minh thuật toán */}
        {!isUser && rawLog && (
          <div className="mt-4 pt-3 border-t border-gray-100">
            <details className="group">
              <summary className="flex items-center gap-1.5 text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider cursor-pointer hover:text-gray-700 list-none">
                <Info className="w-3.5 h-3.5" />
                <span>Bằng chứng kỹ thuật (Audit Log)</span>
                <span className="ml-auto text-[10px] bg-gray-100 px-2 py-0.5 rounded text-gray-500 group-open:hidden">Xem chi tiết</span>
                <span className="ml-auto text-[10px] bg-gray-100 px-2 py-0.5 rounded text-gray-500 hidden group-open:block">Thu gọn</span>
              </summary>
              <div className="mt-2 bg-gray-900 rounded-lg p-3 overflow-x-auto text-left">
                <pre className="text-[11px] text-green-400 font-mono whitespace-pre-wrap break-all">
                  {JSON.stringify(rawLog, null, 2)}
                </pre>
              </div>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
