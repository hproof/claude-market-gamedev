import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Claude GameDev Market — 游戏开发 Claude 插件市场",
  description: "发现、下载并集成专为游戏开发设计的 Claude AI 插件，提升您的游戏开发效率",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased bg-gray-950 text-gray-100">
        <Navbar />
        <main>{children}</main>
        <footer className="border-t border-gray-800 mt-20 py-10 text-center text-gray-500 text-sm">
          <p>© {new Date().getFullYear()} Claude GameDev Market · 用于游戏开发的 Claude 插件市场</p>
        </footer>
      </body>
    </html>
  );
}
