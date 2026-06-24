'use client';

import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import { sendMessage, Message } from '@/lib/api';
import { Send, Loader2 } from 'lucide-react';

interface ChatWindowProps {
  sessionId: string;
  patientContext?: any;
}

export default function ChatWindow({ sessionId, patientContext }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Xin chào! Tôi là Trợ lý Y tế ảo chuyên tư vấn về các loại thuốc phổ thông (OTC). Bạn đang gặp triệu chứng gì, hoặc muốn hỏi về loại thuốc nào hôm nay?',
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: 'Xin chào! Tôi là Trợ lý Y tế ảo chuyên tư vấn về các loại thuốc phổ thông (OTC). Bạn đang gặp triệu chứng gì, hoặc muốn hỏi về loại thuốc nào hôm nay?',
        timestamp: new Date().toISOString()
      }
    ]);
  }, [sessionId]);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage(userMessage.content, sessionId, patientContext);
      
      const botMessage: Message = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
        metadata: {
          warnings: response.warnings,
          suggestions: response.suggestions,
          sources: response.sources,
          agentType: response.agent_type,
          rawLog: response.metadata
        }
      };
      
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Lỗi khi gửi tin nhắn:', error);
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Xin lỗi, tôi đang gặp sự cố kết nối. Vui lòng thử lại sau.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] max-h-[800px] bg-gray-50 rounded-3xl overflow-hidden border border-gray-200 shadow-xl">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-gray-800">Trợ lý Dược phẩm</h2>
          <p className="text-sm text-gray-500">Tư vấn an toàn dựa trên Dược thư Quốc gia</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
          </span>
          <span className="text-xs font-medium text-gray-600">Trực tuyến</span>
        </div>
      </div>

      {/* Message List */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-2">
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            role={msg.role}
            content={msg.content}
            warnings={msg.metadata?.warnings}
            suggestions={msg.metadata?.suggestions}
            sources={msg.metadata?.sources}
            agentType={msg.metadata?.agentType}
            rawLog={msg.metadata?.rawLog}
          />
        ))}
        {isLoading && (
          <div className="flex justify-start mb-6">
            <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center gap-3">
              <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
              <span className="text-gray-500 font-medium">Đang tra cứu dữ liệu an toàn...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Bạn muốn hỏi về thuốc gì? (Ví dụ: Uống Panadol bị đau dạ dày không?)"
            className="w-full bg-gray-50 border border-gray-200 text-gray-800 rounded-full pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow text-base md:text-lg"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <p className="text-center text-xs text-gray-400 mt-3">
          Trợ lý AI chỉ mang tính chất tham khảo dựa trên dữ liệu chuẩn. Không thay thế chẩn đoán của Bác sĩ.
        </p>
      </div>
    </div>
  );
}
