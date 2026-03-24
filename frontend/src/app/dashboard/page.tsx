"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Flame, Zap, Trophy, BookOpen, Star, TrendingUp, Users,
  ChevronRight, Terminal, Target,
} from "lucide-react";
import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/store";
import ProgressBar from "@/components/ui/ProgressBar";
import Navbar from "@/components/ui/Navbar";
import AchievementBadge from "@/components/ui/AchievementBadge";
import Link from "next/link";
import toast from "react-hot-toast";

interface DashboardStats {
  total_lessons: number;
  completed_lessons: number;
  completion_percentage: number;
  current_streak: number;
  total_xp: number;
  level: number;
  rating: number;
  motivation_phrase: string;
}

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [achievements, setAchievements] = useState<any[]>([]);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, achData, lbData] = await Promise.all([
          api.getDashboard(),
          api.getMyAchievements(),
          api.getLeaderboard(),
        ]);
        setStats(statsData);
        setAchievements(achData);
        setLeaderboard(lbData);
      } catch {
        toast.error("Не удалось загрузить данные");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-cyber-black flex items-center justify-center">
        <div className="flex items-center gap-3 text-neon-purple font-mono">
          <Terminal className="animate-pulse" size={24} />
          <span className="animate-pulse">Загрузка данных...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cyber-black bg-cyber-grid">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 pt-32 md:pt-24 pb-12">
        {/* Welcome header */}
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <h1 className="font-display text-2xl md:text-3xl font-bold text-neon-purple text-neon-glow mb-2">
            Привет, {user?.username}
          </h1>
          {stats?.motivation_phrase && (
            <p className="text-gray-400 text-sm font-mono border-l-2 border-neon-purple/50 pl-3">
              {stats.motivation_phrase}
            </p>
          )}
        </motion.div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            {
              icon: Flame, label: "Стрик", value: `${stats?.current_streak || 0} дн`,
              color: "text-orange-400", border: "border-orange-500/30",
            },
            {
              icon: Zap, label: "XP очки", value: stats?.total_xp || 0,
              color: "text-yellow-400", border: "border-yellow-500/30",
            },
            {
              icon: Star, label: "Уровень", value: stats?.level || 1,
              color: "text-neon-blue", border: "border-neon-blue/30",
            },
            {
              icon: Trophy, label: "Рейтинг", value: (stats?.rating || 0).toFixed(1),
              color: "text-neon-purple", border: "border-neon-purple/30",
            },
          ].map(({ icon: Icon, label, value, color, border }, i) => (
            <motion.div
              key={label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`card-cyber ${border} text-center`}
            >
              <Icon className={`${color} mx-auto mb-2`} size={24} />
              <div className={`text-2xl font-bold font-display ${color}`}>{value}</div>
              <div className="text-xs text-gray-500 font-mono mt-1">{label}</div>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Course progress */}
          <div className="lg:col-span-2 space-y-6">
            {/* Overall progress */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="card-cyber border-neon-purple/20"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2 text-neon-purple font-mono font-bold">
                  <TrendingUp size={18} />
                  Прогресс курса
                </div>
                <span className="text-xs text-gray-500 font-mono">
                  {stats?.completed_lessons}/{stats?.total_lessons} уроков
                </span>
              </div>
              <ProgressBar
                value={stats?.completion_percentage || 0}
                color="purple"
                height={10}
              />
              <div className="mt-4 flex gap-3">
                <Link
                  href="/lessons"
                  className="flex-1 btn-neon-purple text-sm flex items-center justify-center gap-2"
                >
                  <BookOpen size={16} />
                  Продолжить обучение
                </Link>
                <Link
                  href="/tasks"
                  className="flex-1 btn-neon-blue text-sm flex items-center justify-center gap-2"
                >
                  <Target size={16} />
                  Задачи
                </Link>
              </div>
            </motion.div>

            {/* Achievements */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="card-cyber"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2 text-neon-blue font-mono font-bold">
                  <Trophy size={18} />
                  Достижения
                </div>
                <span className="text-xs text-gray-500">{achievements.length} получено</span>
              </div>
              {achievements.length === 0 ? (
                <p className="text-gray-600 text-sm font-mono text-center py-4">
                  Выполняй задания, чтобы получить достижения
                </p>
              ) : (
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-3">
                  {achievements.slice(0, 8).map((ach, i) => (
                    <AchievementBadge key={i} achievement={ach} earned={true} index={i} />
                  ))}
                </div>
              )}
            </motion.div>
          </div>

          {/* Leaderboard */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="card-cyber h-fit"
          >
            <div className="flex items-center gap-2 text-neon-green font-mono font-bold mb-4">
              <Users size={18} />
              Топ игроков
            </div>
            <div className="space-y-3">
              {leaderboard.map((player: any, i: number) => (
                <div
                  key={i}
                  className={`flex items-center gap-3 p-2 rounded transition-colors ${
                    player.username === user?.username
                      ? "bg-neon-purple/10 border border-neon-purple/30"
                      : "hover:bg-white/3"
                  }`}
                >
                  <span
                    className={`text-sm font-bold font-mono w-6 text-center ${
                      i === 0 ? "text-yellow-400" : i === 1 ? "text-gray-300" : i === 2 ? "text-orange-400" : "text-gray-600"
                    }`}
                  >
                    {i + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-mono text-gray-200 truncate">{player.username}</div>
                    <div className="text-xs text-gray-600">Lv.{player.level}</div>
                  </div>
                  <div className="flex items-center gap-1 text-yellow-400 text-xs font-mono">
                    <Zap size={10} />
                    {player.xp_points}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
