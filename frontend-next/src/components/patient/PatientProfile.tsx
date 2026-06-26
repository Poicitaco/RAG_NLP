'use client';

import React, { useState, useCallback, useEffect } from 'react';
import { UserCircle, Heart, Activity } from 'lucide-react';
import { JsonObject } from '@/lib/api';

interface Props {
  onSave: (ctx: JsonObject) => void;
  onReset?: () => void;
}

const CONDITIONS = [
  { id: 'hypertension', label: 'Huyết áp cao' },
  { id: 'diabetes', label: 'Tiểu đường' },
  { id: 'stomach_ulcer', label: 'Đau dạ dày' },
  { id: 'asthma', label: 'Hen suyễn' },
  { id: 'kidney_disease', label: 'Suy thận/gan' },
  { id: 'pregnancy', label: 'Mang thai' },
];

export default function PatientProfile({ onSave, onReset }: Props) {
  const [age, setAge] = useState('');
  const [weight, setWeight] = useState('');
  const [conditions, setConditions] = useState<string[]>([]);

  const buildContext = useCallback((): JsonObject => {
    const ctx: JsonObject = { conditions };
    if (age) ctx.age = parseInt(age);
    if (weight) ctx.weight_kg = parseInt(weight);
    return ctx;
  }, [age, weight, conditions]);

  useEffect(() => {
    onSave(buildContext());
  }, [buildContext, onSave]);

  const toggle = (id: string) =>
    setConditions(prev => prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]);

  const handleSave = () => {
    onSave(buildContext());
    onReset?.();
  };

  const inputCls = "w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:border-white/30 transition-colors";

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 text-white/70">
        <UserCircle className="w-4 h-4" />
        <span className="text-xs font-semibold uppercase tracking-wider">Hồ sơ bệnh nhân</span>
      </div>

      <p className="text-xs text-white/40 leading-relaxed">
        Cung cấp thông tin để nhận tư vấn an toàn và chính xác hơn.
      </p>

      <div className="space-y-3">
        <div>
          <label className="block text-xs text-white/50 mb-1.5">Độ tuổi</label>
          <input type="number" value={age} onChange={e => setAge(e.target.value)}
            placeholder="Ví dụ: 45" className={inputCls} />
        </div>
        <div>
          <label className="block text-xs text-white/50 mb-1.5">Cân nặng (kg)</label>
          <input type="number" value={weight} onChange={e => setWeight(e.target.value)}
            placeholder="Ví dụ: 60" className={inputCls} />
        </div>
        <div>
          <label className="flex items-center gap-1.5 text-xs text-white/50 mb-2">
            <Heart className="w-3.5 h-3.5 text-red-400" />
            Bệnh nền
          </label>
          <div className="flex flex-wrap gap-1.5">
            {CONDITIONS.map(c => (
              <button
                key={c.id}
                onClick={() => toggle(c.id)}
                className={`text-xs px-2.5 py-1 rounded-lg border transition-colors ${
                  conditions.includes(c.id)
                    ? 'bg-red-500/20 border-red-500/40 text-red-300'
                    : 'bg-white/5 border-white/10 text-white/50 hover:text-white/70 hover:border-white/20'
                }`}
              >
                {c.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <button
        onClick={handleSave}
        className="w-full flex items-center justify-center gap-2 bg-white/10 hover:bg-white/15 text-white text-sm font-medium py-2.5 rounded-xl transition-colors"
      >
        <Activity className="w-4 h-4" />
        Lưu & Bắt đầu mới
      </button>
    </div>
  );
}
