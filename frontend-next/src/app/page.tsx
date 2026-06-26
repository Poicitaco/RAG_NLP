'use client';

import { useCallback, useState } from 'react';
import ChatWindow from '@/components/chat/ChatWindow';
import PatientProfile from '@/components/patient/PatientProfile';
import { ShieldCheck, SidebarOpen, SidebarClose } from 'lucide-react';
import { JsonObject } from '@/lib/api';

export default function Home() {
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substr(2, 9));
  const [patientContext, setPatientContext] = useState<JsonObject | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleSavePatientContext = useCallback((ctx: JsonObject) => {
    setPatientContext(ctx);
  }, []);

  const handleResetSession = useCallback(() => {
    setSessionId('sess_' + Math.random().toString(36).substr(2, 9));
  }, []);

  return (
    <div className="flex h-full bg-[#212121] text-white">
      
      {/* Sidebar */}
      <aside className={`
        flex-shrink-0 flex flex-col border-r border-white/10 transition-all duration-300 overflow-hidden
        ${sidebarOpen ? 'w-72' : 'w-0'}
      `}>
        <div className="w-72 flex flex-col h-full p-4 gap-4">
          {/* Logo */}
          <div className="flex items-center gap-2.5 px-1 pt-1">
            <div className="bg-blue-500 p-1.5 rounded-lg">
              <ShieldCheck className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="font-bold text-sm leading-tight">SafeRAG Pharma</div>
              <div className="text-xs text-white/50">Dược thư Quốc gia</div>
            </div>
          </div>

          {/* Patient Profile */}
          <div className="flex-1 overflow-y-auto">
            <PatientProfile onSave={handleSavePatientContext} onReset={handleResetSession} />
          </div>

          {/* Disclaimer */}
          <div className="text-xs text-white/40 leading-relaxed border-t border-white/10 pt-3">
            Chỉ mang tính tham khảo. Không thay thế chẩn đoán chuyên khoa.
          </div>
        </div>
      </aside>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="flex items-center gap-3 px-4 py-3 border-b border-white/10">
          <button
            onClick={() => setSidebarOpen(v => !v)}
            className="p-1.5 rounded-lg hover:bg-white/10 transition-colors text-white/60 hover:text-white"
            aria-label="Toggle sidebar"
          >
            {sidebarOpen ? <SidebarClose className="w-5 h-5" /> : <SidebarOpen className="w-5 h-5" />}
          </button>
          <span className="text-sm font-medium text-white/70">Trợ lý Dược phẩm An toàn</span>
          <div className="ml-auto flex items-center gap-3">
            <a href="/admin" className="text-xs text-white/30 hover:text-white/60 transition-colors">Admin</a>
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            <span className="text-xs text-white/50">Online</span>
          </div>
        </header>

        <ChatWindow key={sessionId} sessionId={sessionId} patientContext={patientContext} />
      </div>
    </div>
  );
}
