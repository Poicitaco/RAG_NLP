'use client';

import React, { useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight, HelpCircle, X } from 'lucide-react';

interface ElicitationWidgetProps {
  missingContext?: string[];
  questions?: string[];
  disabled?: boolean;
  onSubmit: (message: string) => void;
}

interface ElicitationStep {
  key: string;
  title: string;
  helper: string;
  placeholder: string;
  options: Array<{
    label: string;
    value: string;
  }>;
}

const STEP_DEFINITIONS: Record<string, ElicitationStep> = {
  age: {
    key: 'age',
    title: 'Người dùng thuốc bao nhiêu tuổi?',
    helper: 'Tuổi giúp hệ thống tránh nhầm liều người lớn, trẻ em hoặc người cao tuổi.',
    placeholder: 'Ví dụ: Tôi 21 tuổi',
    options: [
      { label: 'Tôi 21 tuổi', value: 'Tôi 21 tuổi.' },
      { label: 'Người lớn', value: 'Tôi là người lớn, 21 tuổi.' },
      { label: 'Dùng cho trẻ em', value: 'Thuốc này dùng cho trẻ em, cần tôi bổ sung tuổi và cân nặng.' },
    ],
  },
  age_or_age_months: {
    key: 'age_or_age_months',
    title: 'Trẻ bao nhiêu tuổi?',
    helper: 'Với trẻ em, tuổi theo tháng/năm là dữ kiện bắt buộc trước khi hỏi liều.',
    placeholder: 'Ví dụ: Bé 3 tuổi',
    options: [
      { label: 'Bé 3 tuổi', value: 'Người dùng thuốc là trẻ 3 tuổi.' },
      { label: 'Bé 12 tháng', value: 'Người dùng thuốc là trẻ 12 tháng tuổi.' },
      { label: 'Tôi sẽ nhập tuổi', value: '' },
    ],
  },
  weight_kg: {
    key: 'weight_kg',
    title: 'Cân nặng khoảng bao nhiêu kg?',
    helper: 'Cân nặng rất quan trọng nếu hỏi thuốc cho trẻ em hoặc hỏi liều dùng.',
    placeholder: 'Ví dụ: Bé nặng 15kg',
    options: [
      { label: '15kg', value: 'Người dùng thuốc nặng 15kg.' },
      { label: '25kg', value: 'Người dùng thuốc nặng 25kg.' },
      { label: '60kg', value: 'Người dùng thuốc nặng 60kg.' },
    ],
  },
  conditions_confirmed: {
    key: 'conditions_confirmed',
    title: 'Có bệnh nền đáng chú ý không?',
    helper: 'Bệnh gan, thận, dạ dày, tim mạch, huyết áp, tiểu đường hoặc hen có thể đổi lựa chọn thuốc.',
    placeholder: 'Ví dụ: Tôi không có bệnh nền',
    options: [
      { label: 'Không bệnh nền', value: 'Tôi không có bệnh nền.' },
      { label: 'Tăng huyết áp', value: 'Tôi có tăng huyết áp.' },
      { label: 'Đau dạ dày', value: 'Tôi có đau dạ dày hoặc viêm loét dạ dày.' },
      { label: 'Suy gan/thận', value: 'Tôi có bệnh gan hoặc bệnh thận.' },
    ],
  },
  current_medications_confirmed: {
    key: 'current_medications_confirmed',
    title: 'Có đang dùng thuốc nào khác không?',
    helper: 'Thông tin này giúp kiểm tra tương tác thuốc và tránh phối hợp nguy hiểm.',
    placeholder: 'Ví dụ: Tôi không dùng thuốc nào khác',
    options: [
      { label: 'Không dùng thuốc khác', value: 'Tôi không đang dùng thuốc nào khác.' },
      { label: 'Đang dùng thuốc khác', value: 'Tôi đang dùng thuốc khác, tôi sẽ nhập tên thuốc.' },
      { label: 'Có thực phẩm chức năng', value: 'Tôi đang dùng thực phẩm chức năng.' },
    ],
  },
  allergies_confirmed: {
    key: 'allergies_confirmed',
    title: 'Có từng dị ứng thuốc không?',
    helper: 'Dị ứng thuốc là dữ kiện an toàn tối thiểu trước khi gợi ý thuốc.',
    placeholder: 'Ví dụ: Tôi không dị ứng thuốc',
    options: [
      { label: 'Không dị ứng thuốc', value: 'Tôi không dị ứng thuốc.' },
      { label: 'Có dị ứng thuốc', value: 'Tôi có dị ứng thuốc, tôi sẽ nhập tên thuốc.' },
      { label: 'Không rõ', value: 'Tôi không rõ mình có dị ứng thuốc nào không.' },
    ],
  },
  pregnancy_breastfeeding_confirmed: {
    key: 'pregnancy_breastfeeding_confirmed',
    title: 'Có mang thai hoặc cho con bú không?',
    helper: 'Một số thuốc OTC cần tránh hoặc hỏi bác sĩ nếu đang mang thai/cho con bú.',
    placeholder: 'Ví dụ: Tôi không mang thai và không cho con bú',
    options: [
      { label: 'Không', value: 'Tôi không mang thai và không cho con bú.' },
      { label: 'Đang mang thai', value: 'Tôi đang mang thai.' },
      { label: 'Đang cho con bú', value: 'Tôi đang cho con bú.' },
    ],
  },
  clarify_vague_symptom: {
    key: 'clarify_vague_symptom',
    title: 'Triệu chứng cụ thể hơn là gì?',
    helper: 'Triệu chứng quá chung khiến hệ thống không nên chọn thuốc ngay.',
    placeholder: 'Ví dụ: Tôi đau đầu nhẹ, không sốt, không nôn',
    options: [
      { label: 'Đau đầu nhẹ', value: 'Tôi đau đầu nhẹ, không sốt, không nôn.' },
      { label: 'Có sốt', value: 'Tôi có sốt kèm triệu chứng này.' },
      { label: 'Đau nhiều/kéo dài', value: 'Triệu chứng đau nhiều hoặc kéo dài.' },
    ],
  },
};

const FALLBACK_STEP: ElicitationStep = {
  key: 'custom',
  title: 'Bổ sung thông tin còn thiếu',
  helper: 'Hãy trả lời ngắn gọn để hệ thống tiếp tục tư vấn an toàn.',
  placeholder: 'Nhập thông tin bổ sung...',
  options: [],
};

function buildSteps(missingContext: string[] = [], questions: string[] = []): ElicitationStep[] {
  const unique = Array.from(new Set(missingContext.filter(Boolean)));
  const steps = unique.map((key) => STEP_DEFINITIONS[key] || {
    ...FALLBACK_STEP,
    key,
    title: questions[0] || FALLBACK_STEP.title,
  });

  if (!steps.length && questions.length) {
    return [{
      ...FALLBACK_STEP,
      title: questions[0],
    }];
  }

  return steps;
}

export default function ElicitationWidget({
  missingContext = [],
  questions = [],
  disabled = false,
  onSubmit,
}: ElicitationWidgetProps) {
  const steps = useMemo(() => buildSteps(missingContext, questions), [missingContext, questions]);
  const [current, setCurrent] = useState(0);
  const [draft, setDraft] = useState('');
  const [dismissed, setDismissed] = useState(false);

  if (dismissed || !steps.length) {
    return null;
  }

  const step = steps[Math.min(current, steps.length - 1)];
  const progress = `${current + 1} / ${steps.length}`;

  const submit = (message: string) => {
    const cleaned = message.trim();
    if (!cleaned || disabled) return;
    setDraft('');
    onSubmit(cleaned);
  };

  return (
    <div className="mt-3 w-full max-w-[680px] rounded-2xl border border-slate-200 bg-slate-950 text-white shadow-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center">
            <HelpCircle className="w-4 h-4" />
          </div>
          <div>
            <p className="text-sm font-semibold">Cần bổ sung dữ kiện an toàn</p>
            <p className="text-xs text-slate-400">Trả lời nhanh để hệ thống tiếp tục tư vấn.</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-400">
          <button
            type="button"
            onClick={() => setCurrent((value) => Math.max(0, value - 1))}
            disabled={current === 0}
            className="p-1 rounded-md hover:bg-white/10 disabled:opacity-30"
            aria-label="Câu hỏi trước"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-xs tabular-nums">{progress}</span>
          <button
            type="button"
            onClick={() => setCurrent((value) => Math.min(steps.length - 1, value + 1))}
            disabled={current >= steps.length - 1}
            className="p-1 rounded-md hover:bg-white/10 disabled:opacity-30"
            aria-label="Câu hỏi sau"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
          <button
            type="button"
            onClick={() => setDismissed(true)}
            className="p-1 rounded-md hover:bg-white/10"
            aria-label="Ẩn bảng hỏi"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="p-4">
        <h3 className="text-base font-semibold mb-1">{step.title}</h3>
        <p className="text-sm text-slate-300 mb-3">{step.helper}</p>

        {step.options.length > 0 && (
          <div className="space-y-2 mb-3">
            {step.options.map((option, index) => (
              <button
                key={`${step.key}-${option.label}`}
                type="button"
                disabled={disabled || !option.value}
                onClick={() => submit(option.value)}
                className="w-full flex items-center gap-3 rounded-xl bg-white/8 hover:bg-white/14 border border-white/10 px-3 py-2.5 text-left transition disabled:opacity-50"
              >
                <span className="w-7 h-7 rounded-lg bg-white/10 text-sm font-semibold flex items-center justify-center">
                  {index + 1}
                </span>
                <span className="text-sm font-medium">{option.label}</span>
                <span className="ml-auto text-slate-400">→</span>
              </button>
            ))}
          </div>
        )}

        <div className="rounded-xl bg-black/20 border border-white/10 p-2">
          <textarea
            value={draft}
            disabled={disabled}
            onChange={(event) => setDraft(event.target.value)}
            placeholder={step.placeholder}
            className="w-full min-h-16 bg-transparent text-sm text-white placeholder:text-slate-500 outline-none resize-none px-2 py-1"
          />
          <div className="flex justify-between items-center gap-3 pt-2 border-t border-white/10">
            <button
              type="button"
              onClick={() => setCurrent((value) => Math.min(steps.length - 1, value + 1))}
              disabled={current >= steps.length - 1}
              className="text-xs text-slate-400 hover:text-white disabled:opacity-30"
            >
              Bỏ qua câu này
            </button>
            <button
              type="button"
              disabled={disabled || !draft.trim()}
              onClick={() => submit(draft)}
              className="rounded-lg bg-blue-500 px-3 py-2 text-sm font-semibold hover:bg-blue-400 disabled:opacity-40"
            >
              Gửi bổ sung
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
