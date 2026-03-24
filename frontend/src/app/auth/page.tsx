"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/store";
import toast from "react-hot-toast";
import { Terminal, Zap, Lock, Mail, User } from "lucide-react";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ email: "", password: "", username: "" });
  const router = useRouter();
  const { setAuth } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      let data;
      if (isLogin) {
        data = await api.login(form.email, form.password);
      } else {
        data = await api.register(form.email, form.username, form.password);
      }
      setAuth(data.access_token, data.user);
      toast.success(`Добро пожаловать, ${data.user.username}!`);
      router.push("/dashboard");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Ошибка авторизации");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-black bg-cyber-grid bg-cyber-grid flex items-center justify-center p-4">
      {/* Background glow */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-neon-purple opacity-5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-neon-blue opacity-5 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-4">
            <Terminal className="text-neon-purple w-10 h-10" />
            <h1 className="text-4xl font-display font-black text-white neon-text-purple">
              PyNeon
            </h1>
          </div>
          <p className="text-gray-400 text-sm font-mono">
            // Обучение Python нового уровня
          </p>
        </div>

        {/* Form Card */}
        <div className="cyber-card rounded-xl p-8">
          {/* Tab Switch */}
          <div className="flex mb-8 bg-cyber-dark rounded-lg p-1">
            {["Вход", "Регистрация"].map((tab, i) => (
              <button
                key={tab}
                onClick={() => setIsLogin(i === 0)}
                className={`flex-1 py-2 rounded-md text-sm font-mono transition-all duration-300 ${
                  isLogin === (i === 0)
                    ? "bg-neon-purple text-white shadow-neon-purple"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <AnimatePresence mode="wait">
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <label className="block text-xs text-neon-blue font-mono mb-2 uppercase tracking-wider">
                    // Username
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                    <input
                      type="text"
                      value={form.username}
                      onChange={(e) => setForm({ ...form, username: e.target.value })}
                      className="w-full bg-cyber-dark border border-cyber-border focus:border-neon-blue text-white pl-10 pr-4 py-3 rounded-lg font-mono text-sm focus:outline-none focus:shadow-neon-blue transition-all"
                      placeholder="hacker_name"
                      required={!isLogin}
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div>
              <label className="block text-xs text-neon-blue font-mono mb-2 uppercase tracking-wider">
                // Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full bg-cyber-dark border border-cyber-border focus:border-neon-blue text-white pl-10 pr-4 py-3 rounded-lg font-mono text-sm focus:outline-none focus:shadow-neon-blue transition-all"
                  placeholder="user@matrix.net"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs text-neon-purple font-mono mb-2 uppercase tracking-wider">
                // Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="password"
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                  className="w-full bg-cyber-dark border border-cyber-border focus:border-neon-purple text-white pl-10 pr-4 py-3 rounded-lg font-mono text-sm focus:outline-none focus:shadow-neon-purple transition-all"
                  placeholder="••••••••"
                  required
                  minLength={6}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-neon-gradient py-3 rounded-lg font-mono font-bold text-white hover:shadow-neon-purple transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Загрузка...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4" />
                  {isLogin ? "ВОЙТИ В СИСТЕМУ" : "ЗАРЕГИСТРИРОВАТЬСЯ"}
                </>
              )}
            </button>
          </form>
        </div>

        <p className="text-center text-gray-600 text-xs font-mono mt-6">
          Powered by gpt4free • No paid APIs
        </p>
      </motion.div>
    </div>
  );
}
