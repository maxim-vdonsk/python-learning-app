"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen, Code2, RefreshCw, ChevronLeft, Loader2, Terminal, Sparkles,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { api } from "@/lib/api";
import Navbar from "@/components/ui/Navbar";
import CodeEditor from "@/components/editor/CodeEditor";
import SubmissionResult from "@/components/editor/SubmissionResult";
import toast from "react-hot-toast";
import Link from "next/link";

type Tab = "theory" | "practice";

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

export default function LessonPage() {
  const { id } = useParams();
  const lessonId = Number(id);

  const [tab, setTab] = useState<Tab>("theory");
  const [theory, setTheory] = useState<{ title: string; theory: string; examples: any[] } | null>(null);
  const [task, setTask] = useState<any | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [loadingTheory, setLoadingTheory] = useState(true);
  const [loadingTask, setLoadingTask] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Load theory
  useEffect(() => {
    const fetchTheory = async () => {
      setLoadingTheory(true);
      try {
        const data = await api.getLessonTheory(lessonId);
        setTheory(data);
      } catch {
        toast.error("Не удалось загрузить урок");
      } finally {
        setLoadingTheory(false);
      }
    };
    if (lessonId) fetchTheory();
  }, [lessonId]);

  // Load task when switching to practice
  useEffect(() => {
    if (tab === "practice" && !task) loadTask();
  }, [tab]);

  const loadTask = async () => {
    setLoadingTask(true);
    setResult(null);
    try {
      // Единый endpoint: возвращает существующее задание или генерирует один раз
      const t = await api.getLessonTask(lessonId);
      setTask(t);
    } catch {
      toast.error("Не удалось загрузить задачу");
    } finally {
      setLoadingTask(false);
    }
  };

  const regenerateTask = async () => {
    setLoadingTask(true);
    setResult(null);
    try {
      // Генерируем новое задание для этого урока
      const t = await api.regenerateLessonTask(lessonId);
      setTask(t);
      toast.success("Новая задача сгенерирована!");
    } catch (error: any) {
      toast.error(error.message || "Не удалось сгенерировать задачу");
    } finally {
      setLoadingTask(false);
    }
  };

  const handleSubmit = async (code: string) => {
    if (!task) return;
    setSubmitting(true);
    setResult(null);
    try {
      const res = await api.submitCode(task.id, code);
      setResult(res);
      if (res.is_correct) {
        toast.success("Правильно! Задача решена!");
      } else {
        toast.error("Не совсем верно. Посмотри на рекомендации AI.");
      }
    } catch {
      toast.error("Ошибка при отправке решения");
    } finally {
      setSubmitting(false);
    }
  };

  const regenerateTheory = async () => {
    setLoadingTheory(true);
    try {
      const data = await api.getLessonTheory(lessonId, true);
      setTheory(data);
      toast.success("Теория обновлена");
    } catch {
      toast.error("Не удалось обновить теорию");
    } finally {
      setLoadingTheory(false);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-black bg-cyber-grid">
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 pt-32 md:pt-20 pb-12">
        {/* Back + Title */}
        <div className="flex items-center gap-3 mb-6 pt-4">
          <Link href="/lessons">
            <button className="flex items-center gap-1 text-gray-500 hover:text-neon-blue text-sm font-mono transition-colors">
              <ChevronLeft size={16} />
              Курс
            </button>
          </Link>
          <span className="text-gray-700">/</span>
          <h1 className="font-display text-lg font-bold text-neon-purple truncate">
            {theory?.title || "Загрузка..."}
          </h1>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-cyber-card rounded-lg p-1 w-fit">
          {(["theory", "practice"] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex items-center gap-2 px-5 py-2 rounded text-sm font-mono transition-all ${
                tab === t
                  ? "bg-neon-purple text-cyber-black font-bold"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              {t === "theory" ? <BookOpen size={15} /> : <Code2 size={15} />}
              {t === "theory" ? "Теория" : "Практика"}
            </button>
          ))}
        </div>

        {/* THEORY TAB */}
        <AnimatePresence mode="wait">
          {tab === "theory" && (
            <motion.div
              key="theory"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              {loadingTheory ? (
                <div className="card-cyber flex flex-col items-center gap-4 py-16">
                  <Sparkles className="text-neon-purple animate-pulse" size={36} />
                  <div className="text-neon-purple font-mono animate-pulse">
                    AI генерирует объяснение для вас...
                  </div>
                  <div className="text-gray-600 text-sm font-mono">Это займёт несколько секунд</div>
                </div>
              ) : theory ? (
                <div className="space-y-6">
                  {/* Theory content */}
                  <div className="card-cyber border-neon-purple/20">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-2 text-neon-blue font-mono font-bold text-sm">
                        <Terminal size={16} />
                        Теория урока
                      </div>
                      <button
                        onClick={regenerateTheory}
                        className="flex items-center gap-1 text-xs text-gray-500 hover:text-neon-purple transition-colors font-mono"
                      >
                        <RefreshCw size={12} />
                        Обновить
                      </button>
                    </div>
                    <div className="prose prose-invert prose-sm max-w-none prose-code:text-neon-green prose-code:bg-cyber-dark prose-code:px-1 prose-code:rounded prose-pre:bg-cyber-dark prose-pre:border prose-pre:border-cyber-border">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {theory.theory}
                      </ReactMarkdown>
                    </div>
                  </div>

                  {/* Code examples */}
                  {theory.examples && theory.examples.length > 0 && (
                    <div className="space-y-4">
                      <h3 className="font-mono font-bold text-neon-blue text-sm flex items-center gap-2">
                        <Code2 size={16} />
                        Примеры кода
                      </h3>
                      {theory.examples.map((ex: any, i: number) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="card-cyber border-neon-blue/20"
                        >
                          <div className="text-sm font-mono font-bold text-neon-blue mb-2">
                            {ex.title}
                          </div>
                          <pre className="bg-cyber-dark rounded p-4 overflow-x-auto text-sm font-mono text-neon-green border border-cyber-border">
                            <code>{ex.code}</code>
                          </pre>
                          {ex.explanation && (
                            <p className="mt-2 text-xs text-gray-400">{ex.explanation}</p>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  )}

                  {/* Go to practice */}
                  <motion.button
                    whileHover={{ scale: 1.01 }}
                    onClick={() => setTab("practice")}
                    className="w-full btn-solid-purple flex items-center justify-center gap-2 py-3"
                  >
                    <Code2 size={18} />
                    Перейти к практике
                  </motion.button>
                </div>
              ) : null}
            </motion.div>
          )}

          {/* PRACTICE TAB */}
          {tab === "practice" && (
            <motion.div
              key="practice"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              {loadingTask ? (
                <div className="card-cyber flex flex-col items-center gap-4 py-16">
                  <Sparkles className="text-neon-blue animate-pulse" size={36} />
                  <div className="text-neon-blue font-mono animate-pulse">
                    AI создаёт задачу по этой теме...
                  </div>
                </div>
              ) : task ? (
                <>
                  {/* Task description */}
                  <div className="card-cyber border-neon-blue/20">
                    <div className="flex items-center justify-between mb-3">
                      <span
                        className={`text-xs font-mono px-3 py-1 rounded-full border ${
                          task.difficulty === "easy"
                            ? "text-neon-green border-neon-green/40 bg-neon-green/5"
                            : task.difficulty === "medium"
                            ? "text-yellow-400 border-yellow-400/40 bg-yellow-400/5"
                            : "text-neon-pink border-neon-pink/40 bg-neon-pink/5"
                        }`}
                      >
                        {task.difficulty?.toUpperCase()}
                      </span>
                      <button
                        onClick={regenerateTask}
                        disabled={loadingTask}
                        className="flex items-center gap-1 text-xs text-gray-500 hover:text-neon-blue transition-colors font-mono disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {loadingTask ? <Loader2 size={12} className="animate-spin" /> : <RefreshCw size={12} />}
                        {loadingTask ? "Генерация..." : "Другая задача"}
                      </button>
                    </div>
                    <h2 className="font-mono font-bold text-gray-100 text-lg mb-3">{task.title}</h2>
                    <div className="prose prose-invert prose-sm max-w-none prose-code:text-neon-green">
                      <ReactMarkdown>{task.description}</ReactMarkdown>
                    </div>
                  </div>

                  {/* Code editor */}
                  <CodeEditor
                    defaultValue={task.solution_template || "# Напишите решение здесь\n"}
                    onSubmit={handleSubmit}
                    loading={submitting}
                    hints={parseHints(task.hints)}
                  />

                  {/* Submission result */}
                  {result && <SubmissionResult result={result} />}
                </>
              ) : (
                <div className="card-cyber text-center py-12">
                  <p className="text-gray-500 font-mono mb-4">Задача не найдена</p>
                  <button onClick={loadTask} className="btn-neon-blue text-sm">
                    Сгенерировать задачу
                  </button>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
