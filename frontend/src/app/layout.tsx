import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "react-hot-toast";

export const metadata: Metadata = {
  title: "PyNeon — Python Learning Platform",
  description: "AI-powered Python learning with cyberpunk neon design",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@400;700;900&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-cyber-black text-gray-100 font-mono antialiased">
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#111128",
              color: "#e2e8f0",
              border: "1px solid #1a1a3e",
              fontFamily: "JetBrains Mono, monospace",
            },
            success: { iconTheme: { primary: "#00ff88", secondary: "#111128" } },
            error: { iconTheme: { primary: "#ff2d78", secondary: "#111128" } },
          }}
        />
      </body>
    </html>
  );
}
