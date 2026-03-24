"use client";
import { useRouter, usePathname } from "next/navigation";
import { useAuthStore } from "@/lib/store";
import { motion } from "framer-motion";
import { Terminal, BookOpen, Code2, BarChart3, LogOut, Zap, Flame } from "lucide-react";
import Link from "next/link";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    router.push("/auth");
  };

  const navItems = [
    { href: "/dashboard", label: "Дашборд", icon: BarChart3 },
    { href: "/lessons", label: "Курс", icon: BookOpen },
    { href: "/tasks", label: "Задачи", icon: Code2 },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-cyber-dark border-b border-cyber-border backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/dashboard" className="flex items-center gap-2">
          <Terminal className="text-neon-purple" size={22} />
          <span className="font-display text-lg font-bold text-neon-purple text-neon-glow tracking-wider">
            PyNeon
          </span>
        </Link>

        {/* Nav links */}
        <div className="hidden md:flex items-center gap-1">
          {navItems.map(({ href, label, icon: Icon }) => (
            <Link key={href} href={href}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className={`flex items-center gap-2 px-4 py-2 rounded text-sm transition-all duration-200 ${
                  pathname.startsWith(href)
                    ? "text-neon-blue border border-neon-blue bg-neon-blue/10"
                    : "text-gray-400 hover:text-neon-blue hover:bg-white/5"
                }`}
              >
                <Icon size={16} />
                {label}
              </motion.div>
            </Link>
          ))}
        </div>

        {/* User info */}
        {user && (
          <div className="flex items-center gap-3">
            {/* Streak */}
            <div className="hidden sm:flex items-center gap-1 text-orange-400 text-sm">
              <Flame size={14} />
              <span>{user.streak_days}</span>
            </div>

            {/* XP */}
            <div className="flex items-center gap-1 text-neon-yellow text-sm">
              <Zap size={14} className="text-yellow-400" />
              <span className="text-yellow-400">{user.xp_points} XP</span>
            </div>

            {/* Level badge */}
            <div className="w-8 h-8 rounded-full border border-neon-purple flex items-center justify-center text-xs text-neon-purple font-bold">
              {user.level}
            </div>

            {/* Logout */}
            <button
              onClick={handleLogout}
              className="text-gray-500 hover:text-neon-pink transition-colors"
              title="Выйти"
            >
              <LogOut size={18} />
            </button>
          </div>
        )}
      </div>

      {/* Mobile nav */}
      <div className="md:hidden flex border-t border-cyber-border">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link key={href} href={href} className="flex-1">
            <div
              className={`flex flex-col items-center gap-1 py-2 text-xs transition-all ${
                pathname.startsWith(href) ? "text-neon-blue" : "text-gray-500"
              }`}
            >
              <Icon size={16} />
              {label}
            </div>
          </Link>
        ))}
      </div>
    </nav>
  );
}
