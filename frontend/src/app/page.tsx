"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/store";

export default function Home() {
  const router = useRouter();
  const { token } = useAuthStore();

  useEffect(() => {
    if (token) {
      router.push("/dashboard");
    } else {
      router.push("/auth");
    }
  }, [token, router]);

  return (
    <div className="min-h-screen bg-cyber-black flex items-center justify-center">
      <div className="text-neon-purple animate-pulse text-xl font-mono">
        Инициализация системы...
      </div>
    </div>
  );
}
