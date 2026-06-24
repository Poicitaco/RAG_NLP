import React, { useState } from 'react';
import { UserCircle, Activity, Heart, Edit3 } from 'lucide-react';

interface PatientContextProps {
  onSave: (context: any) => void;
  onReset?: () => void;
}

export default function PatientProfile({ onSave, onReset }: PatientContextProps) {
  const [isOpen, setIsOpen] = useState(true);
  const [age, setAge] = useState('');
  const [weight, setWeight] = useState('');
  const [conditions, setConditions] = useState<string[]>([]);
  
  const commonConditions = [
    { id: 'hypertension', label: 'Huyết áp cao' },
    { id: 'diabetes', label: 'Tiểu đường' },
    { id: 'stomach_ulcer', label: 'Đau dạ dày' },
    { id: 'asthma', label: 'Hen suyễn' },
    { id: 'kidney_disease', label: 'Suy thận/gan' },
    { id: 'pregnancy', label: 'Đang mang thai' },
  ];

  const toggleCondition = (id: string) => {
    setConditions(prev => 
      prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]
    );
  };

  React.useEffect(() => {
    onSave({
      age: age ? parseInt(age) : undefined,
      weight_kg: weight ? parseInt(weight) : undefined,
      conditions: conditions
    });
  }, [age, weight, conditions]);

  const handleSave = () => {
    onSave({
      age: age ? parseInt(age) : undefined,
      weight_kg: weight ? parseInt(weight) : undefined,
      conditions: conditions
    });
    if (onReset) onReset();
    setIsOpen(false);
  };

  return (
    <div className="bg-white rounded-3xl border border-gray-200 shadow-lg overflow-hidden h-fit">
      <div 
        className="bg-blue-600 p-4 text-white flex justify-between items-center cursor-pointer md:cursor-default"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-2">
          <UserCircle className="w-6 h-6" />
          <h3 className="font-bold text-lg">Hồ sơ Bệnh nền</h3>
        </div>
        <button className="md:hidden">
          <Edit3 className="w-5 h-5" />
        </button>
      </div>
      
      <div className={`p-5 transition-all ${isOpen ? 'block' : 'hidden md:block'}`}>
        <p className="text-sm text-gray-500 mb-4">
          Hãy cho AI biết một chút về bạn để có câu trả lời an toàn và chính xác nhất.
        </p>

        <div className="space-y-5">
          {/* Tuổi */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Độ tuổi</label>
            <input 
              type="number" 
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder="Ví dụ: 45"
              className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          {/* Cân nặng */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Cân nặng (kg)</label>
            <input 
              type="number" 
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              placeholder="Ví dụ: 60 (trẻ em: 15)"
              className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          {/* Bệnh nền */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-1.5">
              <Heart className="w-4 h-4 text-red-500" />
              Lưu ý y tế (Bệnh nền)
            </label>
            <div className="flex flex-wrap gap-2">
              {commonConditions.map((cond) => (
                <button
                  key={cond.id}
                  onClick={() => toggleCondition(cond.id)}
                  className={`px-3 py-1.5 text-sm rounded-lg border font-medium transition-colors ${
                    conditions.includes(cond.id) 
                      ? 'bg-red-50 border-red-200 text-red-700' 
                      : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {cond.label}
                </button>
              ))}
            </div>
          </div>

          <button 
            onClick={handleSave}
            className="w-full bg-gray-900 hover:bg-black text-white font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition-colors mt-6"
          >
            <Activity className="w-5 h-5" />
            Lưu & Bắt đầu tư vấn mới
          </button>
        </div>
      </div>
    </div>
  );
}
