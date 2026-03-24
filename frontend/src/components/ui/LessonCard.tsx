"use client";
import { motion } from "framer-motion";
import { CheckCircle2, Circle, BookOpen, Code2, ChevronRight } from "lucide-react";
import Link from "next/link";

interface LessonCardProps {
  lesson: {
    id: number;
    title: string;
    description?: string;
    topic: string;
    completed: boolean;
    theory_read: boolean;
    tasks_completed: number;
    total_tasks: number;
    order: number;
  };
  index: number;
}

export default function LessonCard({ lesson, index }: LessonCardProps) {
  const progress =
    lesson.total_tasks > 0 ? (lesson.tasks_completed / lesson.total_tasks) * 100 : 0;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ scale: 1.01 }}
    >
      <Link href={`/lessons/${lesson.id}`}>
        <div
          className={`card-cyber cursor-pointer group relative overflow-hidden ${
            lesson.completed ? "border-neon-green/30" : "border-cyber-border"
          }`}
        >
          {/* Completed glow */}
          {lesson.completed && (
            <div className="absolute inset-0 bg-neon-green/3 pointer-events-none" />
          )}

          <div className="flex items-center gap-4">
            {/* Status icon */}
            <div className="flex-shrink-0">
              {lesson.completed ? (
                <CheckCircle2 className="text-neon-green" size={22} />
              ) : lesson.theory_read ? (
                <Code2 className="text-neon-blue" size={22} />
              ) : (
                <Circle className="text-gray-600" size={22} />
              )}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-600 font-mono">#{lesson.order}</span>
                <h3
                  className={`font-mono font-semibold truncate ${
                    lesson.completed ? "text-neon-green" : "text-gray-200"
                  }`}
                >
                  {lesson.title}
                </h3>
              </div>
              {lesson.description && (
                <p className="text-xs text-gray-500 mt-0.5 truncate">{lesson.description}</p>
              )}

              {/* Mini progress */}
              {lesson.total_tasks > 0 && (
                <div className="mt-2 flex items-center gap-2">
                  <div className="flex-1 h-1 bg-cyber-border rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-neon-blue rounded-full"
                      animate={{ width: `${progress}%` }}
                      transition={{ duration: 0.8 }}
                    />
                  </div>
                  <span className="text-xs text-gray-600 font-mono whitespace-nowrap">
                    {lesson.tasks_completed}/{lesson.total_tasks} задач
                  </span>
                </div>
              )}
            </div>

            {/* Arrow */}
            <ChevronRight
              size={18}
              className="text-gray-600 group-hover:text-neon-purple transition-colors flex-shrink-0"
            />
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
