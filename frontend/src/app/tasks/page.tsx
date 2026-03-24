"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Filter, Code2, ChevronRight, Loader2, Zap, Terminal } from "lucide-react";
import { api } from "@/lib/api";
import Navbar from "@/components/ui/Navbar";
import CodeEditor from "@/components/editor/CodeEditor";
import SubmissionResult from "@/components/editor/SubmissionResult";
import ReactMarkdown from "react-markdown";
import toast from "react-hot-toast";

/** Безопасный парсинг hints: принимает массив, JSON-строку или plain text */
function parseHints(hints: unknown): string[] {
  if (!hints) return [];
  if (Array.isArray(hints)) return hints as string[];
  if (typeof hints === "string") {
    try {
      const parsed = JSON.parse(hints);
      if (Array.isArray(parsed)) return parsed;
      return [hints];
    } catch {
      return hints.length > 0 ? [hints] : [];
    }
  }
  return [];
}

const DIFFICULTIES = ["all", "easy", "medium", "hard"];
const CATEGORIES = ["all", "strings", "lists", "loops", "functions", "oop", "algorithms", "numbers"];

const difficultyColors: Record<string, string> = {
  easy: "text-neon-green border-neon-green/40 bg-neon-green/5",
  medium: "text-yellow-400 border-yellow-400/40 bg-yellow-400/5",
  hard: "text-neon-pink border-neon-pink/40 bg-neon-pink/5",
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [selectedTask, setSelectedTask] = useState<any | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("all");
  const [category, setCategory] = useState("all");
  const [generating, setGenerating] = useState(false);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const params: any = { limit: 50 };
      if (difficulty !== "all") params.difficulty = difficulty;
      if (category !== "all") params.category = category;
      if (search.trim()) params.search = search;
      const data = await api.getTasks(params);
      setTasks(data);
    } catch {
      toast.error("Не удалось загрузить задачи");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [difficulty, category]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchTasks();
  };

  const handleSelectTask = async (task: any) => {
    const full = await api.getTask(task.id);
    setSelectedTask(full);
    setResult(null);
  };

  const handleSubmit = async (code: string) => {
    if (!selectedTask) return;
    setSubmitting(true);
    try {
      const res = await api.submitCode(selectedTask.id, code);
      setResult(res);
      if (res.is_correct) {
        toast.success("Задача решена!");
      } else {
        toast("Не верно. Смотри рекомендации.", { icon: "💡" });
      }
    } catch {
      toast.error("Ошибка при отправке");
    } finally {
      setSubmitting(false);
    }
  };

  const generateNewTask = async () => {
    setGenerating(true);
    try {
      const diff = difficulty === "all" ? "medium" : difficulty;
      const cat = category === "all" ? "algorithms" : category;
      const newTask = await api.generateTask(cat, diff);
      setTasks((prev) => [newTask, ...prev]);
      setSelectedTask(newTask);
      setResult(null);
      toast.success("Новая задача создана!");
    } catch {
      toast.error("Не удалось сгенерировать задачу");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-black bg-cyber-grid">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 pt-20 pb-12">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="pt-4 mb-6">
          <h1 className="font-display text-2xl font-bold text-white md:text-neon-purple mb-1">Задачи</h1>
          <p className="text-gray-500 text-sm font-mono">Тренируйся на задачах уровня Yandex CodeRun</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {/* LEFT: Task list */}
          <div className="lg:col-span-2 space-y-4">
            {/* Search & filters */}
            <div className="card-cyber space-y-3">
              <form onSubmit={handleSearch} className="flex gap-2">
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Поиск задач..."
                  className="input-cyber flex-1 text-sm"
                />
                <button type="submit" className="px-3 py-2 border border-neon-blue text-neon-blue rounded hover:bg-neon-blue/10 transition-colors">
                  <Search size={16} />
                </button>
              </form>

              {/* Difficulty filter */}
              <div>
                <div className="text-xs text-gray-600 font-mono mb-2">Сложность</div>
                <div className="flex flex-wrap gap-2">
                  {DIFFICULTIES.map((d) => (
                    <button
                      key={d}
                      onClick={() => setDifficulty(d)}
                      className={`text-xs px-3 py-1 rounded-full border font-mono transition-all ${
                        difficulty === d
                          ? d === "all"
                            ? "bg-neon-purple text-cyber-black border-neon-purple font-bold"
                            : difficultyColors[d] + " font-bold"
                          : "border-cyber-border text-gray-500 hover:border-gray-500"
                      }`}
                    >
                      {d === "all" ? "Все" : d.toUpperCase()}
                    </button>
                  ))}
                </div>
              </div>

              {/* Category filter */}
              <div>
                <div className="text-xs text-gray-600 font-mono mb-2">Категория</div>
                <div className="flex flex-wrap gap-2">
                  {CATEGORIES.map((c) => (
                    <button
                      key={c}
                      onClick={() => setCategory(c)}
                      className={`text-xs px-2 py-1 rounded border font-mono transition-all ${
                        category === c
                          ? "bg-neon-blue/20 border-neon-blue text-neon-blue"
                          : "border-cyber-border text-gray-500 hover:border-gray-500"
                      }`}
                    >
                      {c}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Generate button */}
            <motion.button
              whileHover={{ scale: 1.01 }}
              onClick={generateNewTask}
              disabled={generating}
              className="w-full flex items-center justify-center gap-2 py-2.5 border border-neon-purple text-neon-purple rounded font-mono text-sm hover:bg-neon-purple/10 transition-all disabled:opacity-50"
            >
              {generating ? (
                <><Loader2 size={16} className="animate-spin" /> Генерирую...</>
              ) : (
                <><Zap size={16} /> AI: создать задачу</>
              )}
            </motion.button>

            {/* Task list */}
            <div className="space-y-2">
              {loading ? (
                <div className="text-center py-8 text-gray-600 font-mono animate-pulse">
                  Загрузка задач...
                </div>
              ) : tasks.length === 0 ? (
                <div className="text-center py-8 text-gray-600 font-mono">
                  Задач не найдено
                </div>
              ) : (
                tasks.map((task, i) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.03 }}
                    onClick={() => handleSelectTask(task)}
                    className={`card-cyber cursor-pointer group flex items-center gap-3 transition-all ${
                      selectedTask?.id === task.id
                        ? "border-neon-purple/60 bg-neon-purple/5"
                        : ""
                    }`}
                  >
                    <div className={`w-2 h-2 rounded-full flex-shrink-0 ${
                      task.difficulty === "easy" ? "bg-neon-green" :
                      task.difficulty === "medium" ? "bg-yellow-400" : "bg-neon-pink"
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-mono text-gray-200 truncate">{task.title}</div>
                      <div className="text-xs text-gray-600 font-mono">{task.category}</div>
                    </div>
                    <ChevronRight size={14} className="text-gray-600 group-hover:text-neon-purple transition-colors flex-shrink-0" />
                  </motion.div>
                ))
              )}
            </div>
          </div>

          {/* RIGHT: Task + Editor */}
          <div className="lg:col-span-3">
            <AnimatePresence mode="wait">
              {selectedTask ? (
                <motion.div
                  key={selectedTask.id}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  {/* Task header */}
                  <div className="card-cyber border-neon-blue/20">
                    <div className="flex items-center gap-3 mb-3">
                      <span className={`text-xs px-3 py-1 rounded-full border font-mono ${
                        difficultyColors[selectedTask.difficulty] || ""
                      }`}>
                        {selectedTask.difficulty?.toUpperCase()}
                      </span>
                      <span className="text-xs text-gray-600 font-mono">{selectedTask.category}</span>
                    </div>
                    <h2 className="font-mono font-bold text-lg text-gray-100 mb-3">
                      {selectedTask.title}
                    </h2>
                    <div className="prose prose-invert prose-sm max-w-none">
                      <ReactMarkdown>{selectedTask.description}</ReactMarkdown>
                    </div>
                  </div>

                  {/* Code editor */}
                  <CodeEditor
                    defaultValue={selectedTask.solution_template || "# Решение\n"}
                    onSubmit={handleSubmit}
                    loading={submitting}
                    hints={parseHints(selectedTask.hints)}
                  />

                  {/* Result */}
                  {result && <SubmissionResult result={result} />}
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="h-96 flex flex-col items-center justify-center text-center card-cyber"
                >
                  <Code2 className="text-gray-700 mb-4" size={48} />
                  <p className="text-gray-600 font-mono text-sm">Выбери задачу из списка</p>
                  <p className="text-gray-700 font-mono text-xs mt-1">или сгенерируй новую с помощью AI</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
