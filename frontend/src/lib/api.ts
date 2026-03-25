/**
 * API client — all requests to the FastAPI backend go through here.
 * Uses axios with JWT auth headers automatically applied.
 */
import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const stored = localStorage.getItem("auth-storage");
    if (stored) {
      try {
        const { state } = JSON.parse(stored);
        if (state?.token) {
          config.headers.Authorization = `Bearer ${state.token}`;
        }
      } catch {}
    }
  }
  return config;
});

// Auto-logout on 401
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("auth-storage");
      window.location.href = "/auth";
    }
    return Promise.reject(err);
  }
);

export const api = {
  // Auth
  login: async (email: string, password: string) => {
    const { data } = await apiClient.post("/api/v1/auth/login/json", { email, password });
    return data;
  },
  register: async (email: string, username: string, password: string) => {
    const { data } = await apiClient.post("/api/v1/auth/register", { email, username, password });
    return data;
  },
  forgotPassword: async (email: string) => {
    const { data } = await apiClient.post("/api/v1/auth/forgot-password", { email });
    return data;
  },

  // Lessons
  getCourse: async () => {
    const { data } = await apiClient.get("/api/v1/lessons/course");
    return data;
  },
  getLessonTheory: async (lessonId: number, regenerate = false) => {
    const { data } = await apiClient.get(`/api/v1/lessons/${lessonId}/theory`, {
      params: { regenerate },
    });
    return data;
  },
  getLessonTask: async (lessonId: number) => {
    const { data } = await apiClient.get(`/api/v1/lessons/${lessonId}/task`);
    return data;
  },
  initializeCourse: async () => {
    const { data } = await apiClient.post("/api/v1/lessons/initialize");
    return data;
  },

  // Tasks
  getTasks: async (params?: {
    difficulty?: string;
    category?: string;
    lesson_id?: number;
    search?: string;
    limit?: number;
    offset?: number;
  }) => {
    const { data } = await apiClient.get("/api/v1/tasks/", { params });
    return data;
  },
  getTask: async (id: number) => {
    const { data } = await apiClient.get(`/api/v1/tasks/${id}`);
    return data;
  },
  generateTask: async (topic: string, difficulty: string, lessonId?: number) => {
    const { data } = await apiClient.post("/api/v1/tasks/generate", null, {
      params: { topic, difficulty, lesson_id: lessonId },
    });
    return data;
  },
  regenerateLessonTask: async (lessonId: number) => {
    const { data } = await apiClient.post(`/api/v1/tasks/lessons/${lessonId}/regenerate`);
    return data;
  },

  // Submissions
  submitCode: async (taskId: number, code: string) => {
    const { data } = await apiClient.post("/api/v1/submissions/", { task_id: taskId, code });
    return data;
  },
  getMySubmissions: async (taskId?: number) => {
    const { data } = await apiClient.get("/api/v1/submissions/my", {
      params: taskId ? { task_id: taskId } : {},
    });
    return data;
  },

  // Progress
  getDashboard: async () => {
    const { data } = await apiClient.get("/api/v1/progress/dashboard");
    return data;
  },
  getLeaderboard: async () => {
    const { data } = await apiClient.get("/api/v1/progress/leaderboard");
    return data;
  },

  // Achievements
  getMyAchievements: async () => {
    const { data } = await apiClient.get("/api/v1/achievements/");
    return data;
  },
  getAllAchievements: async () => {
    const { data } = await apiClient.get("/api/v1/achievements/all");
    return data;
  },
  seedAchievements: async () => {
    const { data } = await apiClient.post("/api/v1/achievements/seed");
    return data;
  },
};
