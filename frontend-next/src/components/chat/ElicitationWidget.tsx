'use client';

import React, { useMemo, useState } from 'react';
import { Check, ChevronRight, HelpCircle, X } from 'lucide-react';

interface ElicitationWidgetProps {
  missingContext?: string[];
  questions?: string[];
  disabled?: boolean;
  onSubmit: (message: string) => void;
}

interface Option { label: string; value: string; }
interface Step { key: string; type: 'single' | 'multi' | 'text'; title: string; helper: string; placeholder: string; options: Option[]; }

const STEPS: Record<string, Step> = {
  age_or_age_months: { key: 'age_or_age_months', type: 'single', title: 'Người dùng thuốc bao nhiêu tuổi?', helper: 'Tuổi ảnh hưởng đến liều dùng và lựa chọn thuốc an toàn.', placeholder: '', options: [{ label: 'Dưới 1 tuổi', value: 'dưới 1 tuổi' }, { label: '1–5 tuổi', value: '1–5 tuổi' }, { label: '6–12 tuổi', value: '6–12 tuổi' }, { label: 'Trên 12 tuổi', value: 'trên 12 tuổi' }] },
  age: { key: 'age', type: 'single', title: 'Người dùng thuốc bao nhiêu tuổi?', helper: 'Tuổi giúp phân biệt liều người lớn, trẻ em, người cao tuổi.', placeholder: '', options: [{ label: 'Dưới 12 tuổi', value: 'dưới 12 tuổi' }, { label: '12–60 tuổi', value: '12–60 tuổi' }, { label: 'Trên 60 tuổi', value: 'trên 60 tuổi' }] },
  conditions_confirmed: { key: 'conditions_confirmed', type: 'multi', title: 'Có bệnh nền nào không?', helper: 'Có thể chọn nhiều. Bệnh nền ảnh hưởng đến an toàn thuốc.', placeholder: '', options: [{ label: 'Không có', value: 'không có bệnh nền' }, { label: 'Tiểu đường', value: 'tiểu đường' }, { label: 'Huyết áp', value: 'huyết áp' }, { label: 'Bệnh tim', value: 'bệnh tim' }, { label: 'Gan/thận', value: 'bệnh gan hoặc thận' }, { label: 'Dạ dày', value: 'bệnh dạ dày' }, { label: 'Hen suyễn', value: 'hen suyễn' }] },
  allergies_confirmed: { key: 'allergies_confirmed', type: 'single', title: 'Có từng dị ứng thuốc không?', helper: 'Dị ứng là dữ kiện bắt buộc trước khi gợi ý thuốc.', placeholder: '', options: [{ label: 'Không có dị ứng', value: 'không có dị ứng thuốc' }, { label: 'Có dị ứng thuốc', value: 'có dị ứng thuốc' }] },
  current_medications_confirmed: { key: 'current_medications_confirmed', type: 'single', title: 'Đang dùng thuốc nào khác không?', helper: 'Cần kiểm tra tương tác thuốc.', placeholder: '', options: [{ label: 'Không dùng thuốc khác', value: 'không đang dùng thuốc khác' }, { label: 'Có đang dùng thuốc', value: 'có đang dùng thuốc khác' }] },
  pregnancy_breastfeeding_confirmed: { key: 'pregnancy_breastfeeding_confirmed', type: 'single', title: 'Có mang thai hoặc cho con bú không?', helper: 'Một số thuốc cần tránh hoặc hỏi bác sĩ trong thai kỳ.', placeholder: '', options: [{ label: 'Không', value: 'không mang thai và không cho con bú' }, { label: 'Đang mang thai', value: 'đang mang thai' }, { label: 'Đang cho con bú', value: 'đang cho con bú' }] },
};

function buildSteps(missing: string[], questions: string[]): Step[] {
  const steps = missing.filter(Boolean).map(k => STEPS[k] || { key: k, type: 'text' as const, title: questions[0] || 'Bổ sung thông tin', helper: '', placeholder: 'Nhập thông tin...', options: [] });
  if (!steps.length && questions.length) return questions.map((q, i) => ({ key: `q${i}`, type: 'text' as const, title: q, helper: '', placeholder: 'Nhập câu trả lời...', options: [] }));
  return steps;
}

export default function ElicitationWidget({ missingContext = [], questions = [], disabled = false, onSubmit }: ElicitationWidgetProps) {
  const steps = useMemo(() => buildSteps(missingContext, questions), [missingContext, questions]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | string[]>>({});
  const [dismissed, setDismissed] = useState(false);

  if (dismissed || !steps.length) return null;

  const step = steps[current];
  const isLast = current === steps.length - 1;
  const answer = answers[step.key];
  const selectedArr = Array.isArray(answer) ? answer : [];
  const hasAnswer = Array.isArray(answer) ? answer.length > 0 : Boolean(answer);

  const setAnswer = (val: string | string[]) => setAnswers(prev => ({ ...prev, [step.key]: val }));

  const selectSingle = (val: string) => {
    setAnswer(val);
    if (isLast) {
      submit({ ...answers, [step.key]: val });
    } else {
      setCurrent(c => c + 1);
    }
  };

  const toggleMulti = (val: string) => {
    const cur = selectedArr;
    setAnswer(cur.includes(val) ? cur.filter(v => v !== val) : [...cur, val]);
  };

  const submit = (finalAnswers: Record<string, string | string[]>) => {
    const parts: string[] = [];
    steps.forEach(s => {
      const a = finalAnswers[s.key];
      if (!a || (Array.isArray(a) && a.length === 0)) return;
      if (s.key === 'conditions_confirmed' && Array.isArray(a)) {
        parts.push(a.includes('không có bệnh nền') ? 'không có bệnh nền' : `có bệnh nền: ${a.join(', ')}`);
      } else {
        parts.push(Array.isArray(a) ? a.join(', ') : a);
      }
    });
    if (parts.length) onSubmit(parts.join('; ') + '.');
  };

  const goNext = () => {
    if (isLast) submit(answers);
    else setCurrent(c => c + 1);
  };

  return (
    <div className="mt-3 w-full max-w-[600px] rounded-2xl border border-slate-700 bg-slate-900 text-white shadow-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-blue-500 flex items-center justify-center">
            <HelpCircle className="w-4 h-4" />
          </div>
          <div>
            <p className="text-sm font-semibold">Có từng dị ứng thuốc không?</p>
            <p className="text-xs text-slate-400">Câu {current + 1} / {steps.length}</p>
          </div>
        </div>
        <button type="button" onClick={() => setDismissed(true)} className="p-1 rounded hover:bg-white/10">
          <X className="w-4 h-4 text-slate-400" />
        </button>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-slate-800">
        <div className="h-1 bg-blue-500 transition-all" style={{ width: `${((current + 1) / steps.length) * 100}%` }} />
      </div>

      {/* Step content */}
      <div className="p-4">
        <h3 className="text-base font-semibold mb-1">{step.title}</h3>
        {step.helper && <p className="text-xs text-slate-400 mb-3">{step.helper}</p>}

        {step.options.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {step.options.map(opt => {
              const isSel = step.type === 'multi' ? selectedArr.includes(opt.value) : answer === opt.value;
              return (
                <button
                  key={opt.value}
                  type="button"
                  disabled={disabled}
                  onClick={() => step.type === 'multi' ? toggleMulti(opt.value) : selectSingle(opt.value)}
                  className={[
                    'flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition',
                    isSel ? 'border-blue-400 bg-blue-500/20 text-blue-300' : 'border-white/15 bg-white/5 text-slate-200 hover:bg-white/10',
                    disabled ? 'opacity-50' : '',
                  ].join(' ')}
                >
                  {step.type === 'multi' && (
                    <span className={['flex h-4 w-4 shrink-0 items-center justify-center rounded border', isSel ? 'border-blue-400 bg-blue-500' : 'border-white/30'].join(' ')}>
                      {isSel && <Check className="h-3 w-3" />}
                    </span>
                  )}
                  {opt.label}
                </button>
              );
            })}
          </div>
        )}

        {step.type === 'text' && (
          <textarea
            value={typeof answer === 'string' ? answer : ''}
            disabled={disabled}
            onChange={e => setAnswer(e.target.value)}
            placeholder={step.placeholder}
            className="w-full rounded-xl bg-black/30 border border-white/10 text-sm text-white placeholder:text-slate-500 p-3 outline-none resize-none min-h-[60px] mb-3"
          />
        )}

        {/* Footer: next/submit */}
        <div className="flex items-center justify-between pt-2">
          <button type="button" onClick={() => setCurrent(c => c + 1)} disabled={isLast || disabled} className="text-xs text-slate-500 hover:text-slate-300 disabled:hidden">
            Bỏ qua
          </button>
          {(step.type === 'multi' || step.type === 'text') && (
            <button
              type="button"
              disabled={disabled || !hasAnswer}
              onClick={goNext}
              className="flex items-center gap-1 rounded-lg bg-blue-500 px-3 py-1.5 text-sm font-semibold hover:bg-blue-400 disabled:opacity-40 ml-auto"
            >
              {isLast ? 'Xác nhận và tiếp tục' : 'Tiếp theo'} <ChevronRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
