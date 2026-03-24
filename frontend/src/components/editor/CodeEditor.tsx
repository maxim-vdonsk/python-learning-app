"use client";
import { useRef, useState } from "react";
import Editor, { OnMount } from "@monaco-editor/react";
import { Play, Loader2, RotateCcw, Lightbulb } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface CodeEditorProps {
  defaultValue?: string;
  language?: string;
  onSubmit: (code: string) => Promise<void>;
  loading?: boolean;
  hints?: string[];
}

export default function CodeEditor({
  defaultValue = "# Напишите ваше решение здесь\n",
  language = "python",
  onSubmit,
  loading = false,
  hints = [],
}: CodeEditorProps) {
  const editorRef = useRef<any>(null);
  const [showHints, setShowHints] = useState(false);
  const [currentHint, setCurrentHint] = useState(0);

  const handleMount: OnMount = (editor) => {
    editorRef.current = editor;
    // Add Ctrl+Enter shortcut
    editor.addCommand(
      // eslint-disable-next-line no-bitwise
      (window as any).monaco?.KeyMod?.CtrlCmd | (window as any).monaco?.KeyCode?.Enter,
      () => handleSubmit()
    );
  };

  const handleSubmit = async () => {
    if (!editorRef.current || loading) return;
    const code = editorRef.current.getValue();
    await onSubmit(code);
  };

  const handleReset = () => {
    if (editorRef.current) {
      editorRef.current.setValue(defaultValue);
    }
  };

  const showNextHint = () => {
    setCurrentHint((prev) => (prev + 1) % hints.length);
    setShowHints(true);
  };

  return (
    <div className="flex flex-col gap-3">
      {/* Editor container */}
      <div className="rounded-lg overflow-hidden border border-cyber-border">
        {/* Editor toolbar */}
        <div className="bg-cyber-dark border-b border-cyber-border px-4 py-2 flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-neon-pink opacity-70" />
            <div className="w-3 h-3 rounded-full bg-yellow-400 opacity-70" />
            <div className="w-3 h-3 rounded-full bg-neon-green opacity-70" />
          </div>
          <span className="text-xs text-gray-500 font-mono ml-2">solution.py</span>
          <div className="ml-auto text-xs text-gray-600 font-mono">Ctrl+Enter — запустить</div>
        </div>

        <Editor
          height="350px"
          language={language}
          defaultValue={defaultValue}
          onMount={handleMount}
          options={{
            fontSize: 14,
            fontFamily: "JetBrains Mono, Fira Code, monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            wordWrap: "on",
            lineNumbers: "on",
            renderLineHighlight: "line",
            cursorBlinking: "smooth",
            smoothScrolling: true,
            contextmenu: false,
            theme: "vs-dark",
            padding: { top: 12, bottom: 12 },
          }}
          theme="vs-dark"
        />
      </div>

      {/* Action bar */}
      <div className="flex items-center gap-3 flex-wrap">
        {/* Submit button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleSubmit}
          disabled={loading}
          className="flex items-center gap-2 px-6 py-2.5 bg-neon-purple text-cyber-black rounded font-mono font-bold text-sm hover:opacity-90 transition-all shadow-neon-purple disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Проверяем...
            </>
          ) : (
            <>
              <Play size={16} />
              Отправить
            </>
          )}
        </motion.button>

        {/* Reset button */}
        <button
          onClick={handleReset}
          className="flex items-center gap-2 px-4 py-2.5 border border-cyber-border text-gray-400 rounded font-mono text-sm hover:border-gray-500 hover:text-gray-300 transition-all"
        >
          <RotateCcw size={14} />
          Сброс
        </button>

        {/* Hint button */}
        {hints.length > 0 && (
          <button
            onClick={showNextHint}
            className="flex items-center gap-2 px-4 py-2.5 border border-yellow-500/40 text-yellow-400 rounded font-mono text-sm hover:border-yellow-500 transition-all ml-auto"
          >
            <Lightbulb size={14} />
            Подсказка {currentHint + 1}/{hints.length}
          </button>
        )}
      </div>

      {/* Hint display */}
      <AnimatePresence>
        {showHints && hints[currentHint] && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4"
          >
            <div className="flex items-start gap-2">
              <Lightbulb size={16} className="text-yellow-400 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-yellow-200 font-mono">{hints[currentHint]}</p>
              <button
                onClick={() => setShowHints(false)}
                className="ml-auto text-yellow-500/50 hover:text-yellow-400 text-lg leading-none"
              >
                ×
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
