"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, Lock, ChevronRight, Terminal } from "lucide-react";
import { api } from "@/lib/api";
import Navbar from "@/components/ui/Navbar";
import LessonCard from "@/components/ui/LessonCard";
import ProgressBar from "@/components/ui/ProgressBar";
import toast from "react-hot-toast";

export default function LessonsPage() {
  const [course, setCourse] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [openWeek, setOpenWeek] = useState<number>(1);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const data = await api.getCourse();
        setCourse(data);
        // Open the first incomplete week
        const firstIncomplete = data.find((w: any) =>
          w.lessons.some((l: any) => !l.completed)
        );
        if (firstIncomplete) setOpenWeek(firstIncomplete.number);
      } catch {
        toast.error("Не удалось загрузить курс");
      } finally {
        setLoading(false);
      }
    };
    fetchCourse();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-cyber-black flex items-center justify-center">
        <div className="flex items-center gap-3 text-neon-purple font-mono animate-pulse">
          <Terminal size={24} />
          Загрузка курса...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cyber-black bg-cyber-grid">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 pt-32 md:pt-24 pb-12">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <h1 className="font-display text-2xl font-bold text-neon-purple mb-2">Курс Python</h1>
          <p className="text-gray-500 text-sm font-mono">12 недель · 60 тем · 240 уроков · от нуля до Yandex CodeRun</p>
        </motion.div>

        <div className="space-y-4">
          {course.map((week: any, wi: number) => {
            const completedLessons = week.lessons.filter((l: any) => l.completed).length;
            const weekProgress = week.lessons.length > 0
              ? (completedLessons / week.lessons.length) * 100 : 0;
            const isOpen = openWeek === week.number;

            return (
              <motion.div
                key={week.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: wi * 0.05 }}
                className="card-cyber overflow-hidden"
              >
                {/* Week header */}
                <button
                  onClick={() => setOpenWeek(isOpen ? 0 : week.number)}
                  className="w-full flex items-center gap-4 p-2 hover:bg-white/3 rounded transition-colors"
                >
                  <div className="w-12 h-12 rounded-lg border border-cyber-border flex flex-col items-center justify-center flex-shrink-0">
                    <span className="text-[9px] text-gray-500 font-mono leading-none">НЕД.</span>
                    <span className="font-display font-bold text-neon-purple text-lg leading-none">{week.number}</span>
                  </div>
                  <div className="flex-1 text-left min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-gray-200">{week.title}</span>
                      <span className="text-xs text-gray-600 font-mono">
                        {completedLessons}/{week.lessons.length}
                      </span>
                    </div>
                    {week.description && (
                      <p className="text-xs text-gray-500 font-mono truncate">{week.description}</p>
                    )}
                    <ProgressBar value={weekProgress} color="blue" showValue={false} height={3} animated={false} />
                  </div>
                  <ChevronRight
                    size={18}
                    className={`text-gray-500 transition-transform flex-shrink-0 ${isOpen ? "rotate-90" : ""}`}
                  />
                </button>

                {/* Lessons grouped by day (4 lessons per day) */}
                {isOpen && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mt-2 pl-2"
                  >
                    {Array.from({ length: Math.ceil(week.lessons.length / 4) }, (_, dayIdx) => {
                      const dayLessons = week.lessons.slice(dayIdx * 4, dayIdx * 4 + 4);
                      const dayCompleted = dayLessons.every((l: any) => l.completed);
                      return (
                        <div key={dayIdx} className="mb-3">
                          <div className="flex items-center gap-2 px-1 mb-1">
                            <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${dayCompleted ? "text-neon-green border-neon-green/40 bg-neon-green/5" : "text-gray-600 border-gray-700"}`}>
                              ДЕНЬ {dayIdx + 1}
                            </span>
                            <div className="flex-1 h-px bg-gray-800" />
                          </div>
                          <div className="space-y-2">
                            {dayLessons.map((lesson: any, li: number) => (
                              <LessonCard key={lesson.id} lesson={lesson} index={li} />
                            ))}
                          </div>
                        </div>
                      );
                    })}
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
