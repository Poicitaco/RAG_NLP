'use client';

import { useEffect, useRef, useState } from 'react';
import { X } from 'lucide-react';

interface AskUserInputProps {
  question: string;
  options: string[];
  onSubmit: (answer: string) => void;
  onSkip: () => void;
  disabled?: boolean;
}

export default function AskUserInput({ question, options, onSubmit, onSkip, disabled }: AskUserInputProps) {
  const [focused, setFocused] = useState(0); // 0..n-1 = options, n = free text
  const [freeText, setFreeText] = useState('');
  const freeInputRef = useRef<HTMLInputElement>(null);
  const freeIndex = options.length;

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (disabled) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setFocused(f => Math.min(f + 1, freeIndex)); }
      if (e.key === 'ArrowUp')   { e.preventDefault(); setFocused(f => Math.max(f - 1, 0)); }
      if (e.key === 'Escape')    { onSkip(); }
      if (e.key === 'Enter') {
        e.preventDefault();
        if (focused < freeIndex) onSubmit(options[focused]);
        else if (freeText.trim()) onSubmit(freeText.trim());
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [focused, freeText, options, freeIndex, onSubmit, onSkip, disabled]);

  useEffect(() => {
    if (focused === freeIndex) freeInputRef.current?.focus();
  }, [focused, freeIndex]);

  return (
    <div className="w-full max-w-2xl mx-auto mt-2 mb-4">
      <div className="bg-[#2a2a2a] border border-white/10 rounded-2xl overflow-hidden shadow-xl">
        {/* Header */}
        <div className="flex items-start justify-between px-5 pt-5 pb-3">
          <p className="text-white text-sm font-medium leading-snug pr-4">{question}</p>
          <button onClick={onSkip} className="text-white/30 hover:text-white/60 transition-colors flex-shrink-0 mt-0.5">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Options */}
        <div className="px-3 pb-3 space-y-1">
          {options.map((opt, i) => (
            <button
              key={i}
              disabled={disabled}
              onClick={() => onSubmit(opt)}
              onMouseEnter={() => setFocused(i)}
              className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl text-left transition-colors group ${
                focused === i ? 'bg-white/10' : 'hover:bg-white/5'
              }`}
            >
              <span className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-colors ${
                focused === i ? 'bg-white text-black' : 'bg-white/15 text-white/70'
              }`}>
                {i + 1}
              </span>
              <span className="text-sm text-white/80 group-hover:text-white transition-colors">{opt}</span>
            </button>
          ))}

          {/* Free text option */}
          <div
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-colors ${
              focused === freeIndex ? 'bg-white/10' : 'hover:bg-white/5'
            }`}
            onMouseEnter={() => setFocused(freeIndex)}
          >
            <span className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors ${
              focused === freeIndex ? 'bg-white/20' : 'bg-white/10'
            }`}>
              <svg className="w-3 h-3 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </span>
            <input
              ref={freeInputRef}
              value={freeText}
              onChange={e => setFreeText(e.target.value)}
              onFocus={() => setFocused(freeIndex)}
              onKeyDown={e => { if (e.key === 'Enter' && freeText.trim()) { e.stopPropagation(); onSubmit(freeText.trim()); } }}
              placeholder="Câu trả lời khác..."
              className="flex-1 bg-transparent text-sm text-white/70 placeholder-white/25 outline-none"
              disabled={disabled}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-5 py-3 border-t border-white/5">
          <span className="text-white/25 text-xs">↑↓ điều hướng · Enter chọn · Esc bỏ qua</span>
          <button
            onClick={onSkip}
            className="text-xs text-white/40 hover:text-white/70 border border-white/15 hover:border-white/30 px-3 py-1.5 rounded-lg transition-colors"
          >
            Bỏ qua
          </button>
        </div>
      </div>
    </div>
  );
}
