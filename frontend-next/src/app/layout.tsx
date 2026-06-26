import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist" });

export const metadata: Metadata = {
  title: "SafeRAG Pharma — Tra cứu An toàn Thuốc",
  description: "Hệ thống tư vấn thuốc OTC an toàn dựa trên Dược thư Quốc gia Việt Nam.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={`${geist.variable} h-full`}>
      <body className="h-full bg-[#212121] text-white antialiased">{children}</body>
    </html>
  );
}
