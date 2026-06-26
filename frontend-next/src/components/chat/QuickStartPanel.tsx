'use client';

import { Baby, HeartPulse, Pill, ShieldCheck, Sparkles, Stethoscope } from 'lucide-react';

const TOPICS = [
  { title: 'Hạ sốt / giảm đau', prompt: 'Tôi bị đau đầu và muốn hỏi thuốc hạ sốt hoặc giảm đau nào phù hợp?', icon: Pill },
  { title: 'Cảm cúm / ho', prompt: 'Tôi bị cảm cúm, ho và nghẹt mũi thì nên dùng thuốc gì an toàn?', icon: Stethoscope },
  { title: 'Vitamin & TPCN', prompt: 'Tôi muốn mua vitamin hoặc thực phẩm chức năng, cần lưu ý gì?', icon: Sparkles },
  { title: 'Kiểm tra tương tác', prompt: 'Tôi muốn kiểm tra hai thuốc dùng chung có tương tác nguy hiểm không.', icon: ShieldCheck },
  { title: 'Thuốc cho trẻ em', prompt: 'Bé nhà tôi bị sốt, tôi cần hỏi thuốc dùng cho trẻ em.', icon: Baby },
  { title: 'Phụ nữ mang thai', prompt: 'Tôi đang mang thai và muốn hỏi thuốc nào dùng được an toàn.', icon: HeartPulse },
];

export default function QuickStartPanel({ disabled = false, onSelect }: { disabled?: boolean; onSelect: (msg: string) => void }) {
  return (
    <div className="py-6 space-y-4">
      <div className="text-center space-y-1">
        <h3 className="text-white/80 font-semibold">Chọn chủ đề để bắt đầu</h3>
        <p className="text-xs text-white/40">Hoặc nhập câu hỏi bên dưới</p>
      </div>
      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {TOPICS.map(topic => {
          const Icon = topic.icon;
          return (
            <button
              key={topic.title}
              type="button"
              disabled={disabled}
              onClick={() => onSelect(topic.prompt)}
              className="flex items-start gap-3 p-3 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20 text-left transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white/10 text-white/70">
                <Icon className="h-4 w-4" />
              </span>
              <span>
                <span className="block text-sm font-medium text-white/80">{topic.title}</span>
                <span className="block text-xs text-white/40 mt-0.5">Nhấn để gửi</span>
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
