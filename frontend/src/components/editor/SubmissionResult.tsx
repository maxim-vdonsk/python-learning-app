"use client";
import { motion } from "framer-motion";
import { CheckCircle2, XCircle, Clock, Cpu, Star, ChevronDown, ChevronUp, Trophy } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

interface TestResult {
  test_num: number;
  input: string;
  expected: string;
  actual: string;
  passed: boolean;
  error?: string;
}

interface SubmissionResultProps {
  result: {
    is_correct: boolean;
    execution_time_ms?: number;
    passed_tests: number;
    total_tests: number;
    ai_feedback: string;
    ai_score: number;
    recommendations: string[];
    test_results?: TestResult[];
    xp_earned?: number;
    new_achievements?: Array<{ icon: string; title: string; xp_reward: number }>;
  };
}

export default function SubmissionResult({ result }: SubmissionResultProps) {
  const [showTests, setShowTests] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* Main verdict */}
      <div
        className={`rounded-lg border p-4 ${
          result.is_correct
            ? "border-neon-green/40 bg-neon-green/5"
            : "border-neon-pink/40 bg-neon-pink/5"
        }`}
      >
        <div className="flex items-center gap-3">
          {result.is_correct ? (
            <CheckCircle2 className="text-neon-green" size={28} />
          ) : (
            <XCircle className="text-neon-pink" size={28} />
          )}
          <div>
            <div
              className={`font-display font-bold text-lg ${
                result.is_correct ? "text-neon-green" : "text-neon-pink"
              }`}
            >
              {result.is_correct ? "ACCEPTED" : "WRONG ANSWER"}
            </div>
            <div className="text-sm text-gray-400 font-mono">
              Тестов пройдено: {result.passed_tests}/{result.total_tests}
            </div>
          </div>

          {/* Stats */}
          <div className="ml-auto flex items-center gap-4 text-sm font-mono text-gray-400">
            {result.execution_time_ms && (
              <div className="flex items-center gap-1">
                <Clock size={14} />
                {result.execution_time_ms.toFixed(1)}мс
              </div>
            )}
            <div className="flex items-center gap-1">
              <Star size={14} className="text-yellow-400" />
              <span className="text-yellow-400">{result.ai_score.toFixed(0)}/100</span>
            </div>
          </div>
        </div>
      </div>

      {/* XP earned */}
      {result.xp_earned && result.xp_earned > 0 && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="flex items-center gap-2 text-yellow-400 font-mono font-bold text-sm"
        >
          <Trophy size={16} />
          +{result.xp_earned} XP получено!
        </motion.div>
      )}

      {/* New achievements */}
      {result.new_achievements && result.new_achievements.length > 0 && (
        <div className="flex gap-3 flex-wrap">
          {result.new_achievements.map((ach, i) => (
            <motion.div
              key={i}
              initial={{ scale: 0, rotate: -10 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ delay: i * 0.1, type: "spring" }}
              className="flex items-center gap-2 bg-neon-purple/10 border border-neon-purple/40 rounded-lg px-3 py-2"
            >
              <span className="text-lg">{ach.icon}</span>
              <div>
                <div className="text-xs font-bold text-neon-purple">{ach.title}</div>
                <div className="text-xs text-yellow-400">+{ach.xp_reward} XP</div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* AI Feedback */}
      {result.ai_feedback && (
        <div className="card-cyber">
          <div className="flex items-center gap-2 mb-3 text-neon-blue text-sm font-mono font-bold">
            <Cpu size={16} />
            AI-анализ кода
          </div>
          <div className="text-sm text-gray-300 prose prose-invert max-w-none prose-sm">
            <ReactMarkdown>{result.ai_feedback}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <div className="card-cyber border-neon-blue/20">
          <div className="text-xs font-mono font-bold text-neon-blue mb-3">РЕКОМЕНДАЦИИ</div>
          <ul className="space-y-2">
            {result.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                <span className="text-neon-blue font-mono mt-0.5">→</span>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Test results toggle */}
      {result.test_results && result.test_results.length > 0 && (
        <div className="card-cyber">
          <button
            onClick={() => setShowTests(!showTests)}
            className="w-full flex items-center justify-between text-sm font-mono text-gray-400 hover:text-gray-200 transition-colors"
          >
            <span>Детали тестов ({result.passed_tests}/{result.total_tests} прошли)</span>
            {showTests ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>

          {showTests && (
            <div className="mt-3 space-y-2">
              {result.test_results.map((test) => (
                <div
                  key={test.test_num}
                  className={`rounded p-3 text-xs font-mono ${
                    test.passed
                      ? "bg-neon-green/5 border border-neon-green/20"
                      : "bg-neon-pink/5 border border-neon-pink/20"
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    {test.passed ? (
                      <CheckCircle2 size={12} className="text-neon-green" />
                    ) : (
                      <XCircle size={12} className="text-neon-pink" />
                    )}
                    <span className="text-gray-400">Тест #{test.test_num}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-gray-400">
                    <div>
                      <div className="text-gray-600">Ввод:</div>
                      <div className="text-gray-200">{test.input || "(пусто)"}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Ожидалось:</div>
                      <div className="text-neon-green">{test.expected}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Получено:</div>
                      <div className={test.passed ? "text-neon-green" : "text-neon-pink"}>
                        {test.error ? `Ошибка: ${test.error}` : test.actual}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
}
