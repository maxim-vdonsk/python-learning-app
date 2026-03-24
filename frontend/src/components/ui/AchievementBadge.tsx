"use client";
import { motion } from "framer-motion";

interface AchievementBadgeProps {
  achievement: {
    icon: string;
    title: string;
    description: string;
    xp_reward: number;
    earned_at?: string;
  };
  earned?: boolean;
  index?: number;
}

export default function AchievementBadge({
  achievement,
  earned = false,
  index = 0,
}: AchievementBadgeProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: earned ? 1 : 0.4, scale: 1 }}
      transition={{ delay: index * 0.05 }}
      whileHover={earned ? { scale: 1.05 } : {}}
      className={`card-cyber text-center p-4 ${
        earned ? "border-neon-purple/40" : "border-cyber-border grayscale"
      }`}
    >
      <div className="text-3xl mb-2">{achievement.icon}</div>
      <div className="font-mono font-bold text-sm text-gray-200 mb-1">{achievement.title}</div>
      <div className="text-xs text-gray-500 mb-2">{achievement.description}</div>
      <div className="text-xs text-yellow-400 font-mono">+{achievement.xp_reward} XP</div>
      {achievement.earned_at && (
        <div className="text-xs text-gray-600 mt-1">
          {new Date(achievement.earned_at).toLocaleDateString("ru-RU")}
        </div>
      )}
    </motion.div>
  );
}
