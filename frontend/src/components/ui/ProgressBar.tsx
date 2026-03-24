"use client";
import { motion } from "framer-motion";

interface ProgressBarProps {
  value: number; // 0-100
  color?: "purple" | "blue" | "green" | "pink";
  label?: string;
  showValue?: boolean;
  height?: number;
  animated?: boolean;
}

const colorMap = {
  purple: { bar: "bg-neon-purple", glow: "shadow-neon-purple", text: "text-neon-purple" },
  blue: { bar: "bg-neon-blue", glow: "shadow-neon-blue", text: "text-neon-blue" },
  green: { bar: "bg-neon-green", glow: "shadow-neon-green", text: "text-neon-green" },
  pink: { bar: "bg-neon-pink", glow: "shadow-neon-pink", text: "text-neon-pink" },
};

export default function ProgressBar({
  value,
  color = "purple",
  label,
  showValue = true,
  height = 6,
  animated = true,
}: ProgressBarProps) {
  const colors = colorMap[color];
  const clamped = Math.min(100, Math.max(0, value));

  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="flex justify-between items-center mb-1">
          {label && <span className="text-xs text-gray-400 font-mono">{label}</span>}
          {showValue && (
            <span className={`text-xs font-mono font-bold ${colors.text}`}>
              {clamped.toFixed(0)}%
            </span>
          )}
        </div>
      )}
      <div
        className="w-full bg-cyber-border rounded-full overflow-hidden"
        style={{ height: `${height}px` }}
      >
        <motion.div
          className={`h-full rounded-full ${colors.bar} ${colors.glow}`}
          initial={animated ? { width: 0 } : { width: `${clamped}%` }}
          animate={{ width: `${clamped}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          style={{
            boxShadow: `0 0 8px currentColor`,
          }}
        />
      </div>
    </div>
  );
}
