import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cyberpunk palette
        neon: {
          purple: "#b026ff",
          blue: "#00d4ff",
          green: "#00ff88",
          pink: "#ff2d78",
          yellow: "#ffee00",
        },
        cyber: {
          black: "#0a0a0f",
          dark: "#0d0d1a",
          card: "#111128",
          border: "#1a1a3e",
          "border-bright": "#2a2a6e",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Fira Code", "Courier New", "monospace"],
        display: ["Orbitron", "sans-serif"],
      },
      boxShadow: {
        "neon-purple": "0 0 20px rgba(176, 38, 255, 0.5), 0 0 40px rgba(176, 38, 255, 0.2)",
        "neon-blue": "0 0 20px rgba(0, 212, 255, 0.5), 0 0 40px rgba(0, 212, 255, 0.2)",
        "neon-green": "0 0 20px rgba(0, 255, 136, 0.5), 0 0 40px rgba(0, 255, 136, 0.2)",
        "neon-pink": "0 0 20px rgba(255, 45, 120, 0.5), 0 0 40px rgba(255, 45, 120, 0.2)",
      },
      animation: {
        "pulse-neon": "pulse-neon 2s ease-in-out infinite",
        "scan": "scan 2s linear infinite",
        "glow": "glow 1.5s ease-in-out infinite alternate",
        "float": "float 3s ease-in-out infinite",
      },
      keyframes: {
        "pulse-neon": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
        "scan": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" },
        },
        "glow": {
          "from": { textShadow: "0 0 10px #b026ff, 0 0 20px #b026ff" },
          "to": { textShadow: "0 0 20px #00d4ff, 0 0 40px #00d4ff" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
      backgroundImage: {
        "cyber-grid": "linear-gradient(rgba(176, 38, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(176, 38, 255, 0.03) 1px, transparent 1px)",
        "cyber-gradient": "linear-gradient(135deg, #0d0d1a 0%, #111128 50%, #0a0a1f 100%)",
        "neon-gradient": "linear-gradient(135deg, #b026ff, #00d4ff)",
      },
      backgroundSize: {
        "cyber-grid": "50px 50px",
      },
    },
  },
  plugins: [],
};
export default config;
