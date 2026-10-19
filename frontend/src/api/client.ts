import {
  User,
  UserProfile,
  SkillMetric,
  AssessmentQuestion,
  AssessmentResult,
  CodingProblem,
  CodingExecutionResponse,
  SqlProblem,
  SqlExecutionResponse,
  StudyPlan,
  StudyTask,
  JobApplication,
  JobPipelineStats,
  WeeklyReport,
  InterviewSession
} from '../types';

export function getApiBase(): string {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('careerforge_api_base');
    if (saved) return saved;
    if ((window as any).__CAREERFORGE_API_BASE__) return (window as any).__CAREERFORGE_API_BASE__;
  }
  if (import.meta.env.VITE_API_BASE) {
    return import.meta.env.VITE_API_BASE as string;
  }
  if (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    return 'http://localhost:8000/api/v1';
  }
  return 'https://careerforge-backend-psvc.onrender.com/api/v1';
}

export function setApiBase(url: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('careerforge_api_base', url.trim().replace(/\/+$/, ''));
  }
}

export const authStorage = {
  getToken: () => localStorage.getItem('careerforge_token'),
  setToken: (token: string) => localStorage.setItem('careerforge_token', token),
  clearToken: () => localStorage.removeItem('careerforge_token'),
  getUser: () => {
    const raw = localStorage.getItem('careerforge_user');
    return raw ? JSON.parse(raw) : null;
  },
  setUser: (user: any) => localStorage.setItem('careerforge_user', JSON.stringify(user)),
};

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = authStorage.getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const base = getApiBase();
  try {
    const response = await fetch(`${base}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorDetail = 'An error occurred';
      try {
        const errJson = await response.json();
        errorDetail = errJson.detail || errJson.error || JSON.stringify(errJson);
      } catch {
        errorDetail = `${response.status} ${response.statusText}`;
      }
      throw new Error(errorDetail);
    }

    return response.json();
  } catch (err: any) {
    if (err.name === 'TypeError' && err.message.toLowerCase().includes('fetch')) {
      throw new Error(`Cannot reach backend server at: ${base}. Verify backend is live.`);
    }
    throw err;
  }
}

export const api = {
  // Auth
  login: async (email: string, password: string) => {
    const data = await request<{ access_token: string; email: string; full_name: string; user_id: string }>(
      '/auth/login',
      { method: 'POST', body: JSON.stringify({ email, password }) }
    );
    authStorage.setToken(data.access_token);
    authStorage.setUser(data);
    return data;
  },
  register: async (payload: any) => {
    const data = await request<{ access_token: string; email: string; full_name: string; user_id: string }>(
      '/auth/register',
      { method: 'POST', body: JSON.stringify(payload) }
    );
    authStorage.setToken(data.access_token);
    authStorage.setUser(data);
    return data;
  },
  getMe: () => request<User>('/auth/me'),

  // Profile
  getProfile: () => request<UserProfile>('/profile'),
  updateProfile: (profile: Partial<UserProfile>) =>
    request<UserProfile>('/profile', { method: 'PUT', body: JSON.stringify(profile) }),

  // Dashboard
  getDashboard: () => request<any>('/dashboard'),

  // Assessment
  getTopics: () => request<string[]>('/assessment/topics'),
  getSkillMetrics: () => request<SkillMetric[]>('/assessment/metrics'),
  updateConfidence: (topic: string, confidence: number) =>
    request<any>('/assessment/confidence', { method: 'PUT', body: JSON.stringify({ topic, confidence }) }),
  getQuestions: (topic: string) => request<AssessmentQuestion[]>(`/assessment/questions/${topic}`),
  submitAssessment: (topic: string, answers: Array<{ question_id: string; selected_option_index: number }>, timeSpent: number) =>
    request<AssessmentResult>('/assessment/submit', {
      method: 'POST',
      body: JSON.stringify({ topic, answers, time_spent_seconds: timeSpent }),
    }),

  // Coding Practice
  getCodingProblems: () => request<Array<{ id: string; slug: string; title: string; difficulty: string; category: string }>>('/coding/problems'),
  getCodingProblemDetail: (slug: string) => request<CodingProblem>(`/coding/problems/${slug}`),
  runCodingSample: (slug: string, code: string) =>
    request<CodingExecutionResponse>(`/coding/problems/${slug}/run`, { method: 'POST', body: JSON.stringify({ code }) }),
  submitCoding: (slug: string, code: string) =>
    request<CodingExecutionResponse>(`/coding/problems/${slug}/submit`, { method: 'POST', body: JSON.stringify({ code }) }),

  // SQL Practice
  getSqlProblems: () => request<Array<{ id: string; slug: string; title: string; difficulty: string; category: string }>>('/sql/problems'),
  getSqlProblemDetail: (slug: string) => request<SqlProblem>(`/sql/problems/${slug}`),
  executeSql: (slug: string, query: string) =>
    request<SqlExecutionResponse>(`/sql/problems/${slug}/execute`, { method: 'POST', body: JSON.stringify({ query }) }),

  // AI Career Coach
  chatWithCoach: (message: string, history?: any[]) =>
    request<{ reply: string; suggested_actions: string[]; agent_name: string; model_used: string }>('/coach/chat', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_history: history }),
    }),

  // Mock Interview
  startInterview: (role: string, target_company: string, interview_mode: string) =>
    request<InterviewSession>('/interview/start', {
      method: 'POST',
      body: JSON.stringify({ role, target_company, interview_mode }),
    }),
  answerInterviewQuestion: (sessionId: string, answer: string) =>
    request<InterviewSession>(`/interview/sessions/${sessionId}/answer`, {
      method: 'POST',
      body: JSON.stringify({ user_answer: answer }),
    }),
  getPastInterviews: () => request<InterviewSession[]>('/interview/sessions'),

  // Study Planner
  getActivePlan: () => request<StudyPlan>('/planner/active-plan'),
  generatePlan: (daily_hours: number = 4.0, focus_objective?: string) =>
    request<StudyPlan>('/planner/generate', { method: 'POST', body: JSON.stringify({ daily_hours, focus_objective }) }),
  getTasks: (dateFilter?: string) =>
    request<StudyTask[]>(`/planner/tasks${dateFilter ? `?date_filter=${dateFilter}` : ''}`),
  updateTaskStatus: (taskId: string, status: string, notes?: string) =>
    request<StudyTask>(`/planner/tasks/${taskId}`, { method: 'PATCH', body: JSON.stringify({ status, notes }) }),
  recordStudySession: (duration_minutes: number, reflection_notes?: string, task_id?: string) =>
    request<any>('/planner/record-session', {
      method: 'POST',
      body: JSON.stringify({ duration_minutes, reflection_notes, task_id }),
    }),

  // Job Tracker
  getJobs: (statusFilter?: string, search?: string) => {
    const params = new URLSearchParams();
    if (statusFilter) params.append('status', statusFilter);
    if (search) params.append('search', search);
    return request<JobApplication[]>(`/jobs?${params.toString()}`);
  },
  getPipelineStats: () => request<JobPipelineStats>('/jobs/pipeline-stats'),
  createJob: (job: Partial<JobApplication>) =>
    request<JobApplication>('/jobs', { method: 'POST', body: JSON.stringify(job) }),
  updateJob: (id: string, job: Partial<JobApplication>) =>
    request<JobApplication>(`/jobs/${id}`, { method: 'PUT', body: JSON.stringify(job) }),
  deleteJob: (id: string) => request<any>(`/jobs/${id}`, { method: 'DELETE' }),
  getApprovedSources: (query?: string) =>
    request<any[]>(`/jobs/approved-sources${query ? `?query=${query}` : ''}`),

  // Resume & Project Assistant
  analyzeResume: (resume_text: string, job_description: string, target_role?: string) =>
    request<any>('/resume/analyze', {
      method: 'POST',
      body: JSON.stringify({ resume_text, job_description, target_role }),
    }),
  getProjectPrep: (project_title: string, project_description: string = '', tech_stack: string = '') =>
    request<any>('/resume/project-prep', {
      method: 'POST',
      body: JSON.stringify({ project_title, project_description, tech_stack }),
    }),

  // Weekly Review
  getLatestWeeklyReport: () => request<WeeklyReport>('/weekly/latest'),
  generateWeeklyReport: (start_date?: string, end_date?: string) =>
    request<WeeklyReport>('/weekly/generate', { method: 'POST', body: JSON.stringify({ start_date, end_date }) }),

  // MCP Tools
  listMcpTools: () => request<any[]>('/mcp/tools'),
  invokeMcpTool: (tool_name: string, args: Record<string, any>) =>
    request<any>('/mcp/invoke', { method: 'POST', body: JSON.stringify({ tool_name, arguments: args }) }),
};
