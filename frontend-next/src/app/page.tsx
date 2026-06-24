'use client';

import { useState } from 'react';
import ChatWindow from '@/components/chat/ChatWindow';
import PatientProfile from '@/components/patient/PatientProfile';
import { ShieldCheck } from 'lucide-react';

export default function Home() {
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substr(2, 9));
  const [patientContext, setPatientContext] = useState<any>(null);

  return (
    <main className="min-h-screen bg-[#F8FAFC] text-gray-900 font-sans selection:bg-blue-200">
      <div className="max-w-[1600px] mx-auto p-4 md:p-6 lg:p-8">
        
        {/* Header */}
        <header className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2.5 rounded-xl text-white shadow-md">
              <ShieldCheck className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-gray-900">
                SafeRAG <span className="text-blue-600">Pharma</span>
              </h1>
              <p className="text-sm md:text-base font-medium text-gray-500">Tra cứu An toàn Thuốc dựa trên Dược thư Quốc gia</p>
            </div>
          </div>
        </header>

        {/* Layout Chính */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Cột Trái: Hồ sơ & Thông tin */}
          <div className="lg:col-span-1 space-y-6">
            <PatientProfile 
              onSave={(ctx) => setPatientContext(ctx)} 
              onReset={() => setSessionId('sess_' + Math.random().toString(36).substr(2, 9))}
            />
            
            <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hidden md:block">
              <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-amber-500"></span> 
                Lưu ý quan trọng
              </h4>
              <p className="text-sm text-gray-600 leading-relaxed mb-4">
                Hệ thống chỉ cung cấp thông tin tham khảo từ các nguồn chính thống (Cục Quản Lý Dược, Dược thư Quốc gia). 
              </p>
              <div className="bg-amber-50 text-amber-800 text-xs font-semibold p-3 rounded-xl border border-amber-100">
                Tuyệt đối không dùng AI để thay thế chẩn đoán của Bác sĩ chuyên khoa. Mọi quyết định dùng thuốc cần có sự đồng ý của chuyên gia y tế.
              </div>
            </div>
          </div>

          {/* Cột Phải: Chat Window */}
          <div className="lg:col-span-3">
            <ChatWindow sessionId={sessionId} patientContext={patientContext} />
          </div>

        </div>
      </div>
    </main>
  );
}
