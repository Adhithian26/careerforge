export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  profile?: UserProfile;
}

export interface UserProfile {
  id: string;
  user_id: string;
  degree: string;
  graduation_year: number;
  daily_study_hours: number;
  target_roles: string;
  preferred_companies: string;
  python_confidence: number;
  sql_confidence: number;
  dsa_confidence: number;
  existing_projects: string;
  career_goals: string;
}

export interface SkillMetric {
  topic: string;
  measured_proficiency: number;
  subjective_confidence: number;
  attempts_count: number;
  total_questions_answered: number;
  total_correct_answered: number;
  weak_subtopics: string[];
  strong_subtopics: string[];
  last_assessed_at: string | null;
}

export interface AssessmentQuestion {
  id: string;
  topic: string;
  subtopic?: string;
  difficulty: string;
  question_text: string;
  code_snippet?: string;
  options: string[];
}

export interface AnswerResultDetail {
  question_id: string;
  question_text: string;
  selected_option_index: number;
  correct_option_index: number;
  is_correct: boolean;
  explanation: string;
}

export interface AssessmentResult {
  id: string;
  topic: string;
  total_questions: number;
  correct_count: number;
  score_percentage: number;
  time_spent_seconds: number;
  completed_at: string;
  breakdown: AnswerResultDetail[];
  updated_measured_proficiency: number;
  recommendation: string;
}

export interface CodingProblem {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  category: string;
  description: string;
  starter_code: string;
  function_name: string;
  hints: string[];
  sample_tests: Array<{ input: any; expected: any; is_sample: boolean }>;
}

export interface TestResultItem {
  test_index: number;
  passed: boolean;
  input_str?: string;
  expected_str?: string;
  actual_str?: string;
  error?: string;
}

export interface CodingExecutionResponse {
  passed: boolean;
  passed_tests: number;
  total_tests: number;
  runtime_ms: number;
  output?: string;
  error?: string;
  results: TestResultItem[];
  solution_approach?: string;
}

export interface SqlProblem {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  category: string;
  prompt: string;
  schema_info: string;
  hints: string[];
}

export interface SqlExecutionResponse {
  passed: boolean;
  columns: string[];
  rows: any[][];
  row_count: number;
  execution_time_ms: number;
  error?: string;
  expected_rows_sample?: any[][];
  explanation?: string;
}

export interface StudyTask {
  id: string;
  plan_id?: string;
  scheduled_date: string;
  title: string;
  topic: string;
  duration_minutes: number;
  priority: string;
  status: "pending" | "in_progress" | "completed" | "skipped" | "rescheduled";
  notes?: string;
  completed_at?: string;
}

export interface StudyPlan {
  id: string;
  title: string;
  start_date: string;
  end_date: string;
  daily_allocated_hours: number;
  focus_objective?: string;
  is_active: boolean;
  tasks: StudyTask[];
}

export interface JobApplication {
  id: string;
  company: string;
  role: string;
  job_url?: string;
  location?: string;
  salary_range?: string;
  eligibility_notes?: string;
  status: "saved" | "planned" | "applied" | "assessment" | "interview" | "offer" | "rejected" | "withdrawn";
  application_date?: string;
  deadline?: string;
  follow_up_date?: string;
  is_verified_opening: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface JobPipelineStats {
  total_saved: number;
  total_planned: number;
  total_applied: number;
  total_assessment: number;
  total_interview: number;
  total_offer: number;
  total_rejected: number;
  total_withdrawn: number;
}

export interface WeeklyReport {
  id: string;
  week_start_date: string;
  week_end_date: string;
  planned_tasks_count: number;
  completed_tasks_count: number;
  completion_rate_percentage: number;
  coding_problems_solved: number;
  sql_exercises_completed: number;
  assessments_completed: number;
  average_assessment_score: number;
  applications_submitted: number;
  interviews_completed: number;
  key_weaknesses: string[];
  top_strengths: string[];
  next_week_priorities: string[];
  ai_coach_summary?: string;
  created_at: string;
}

export interface InterviewExchange {
  id: string;
  round_number: number;
  question: string;
  user_answer?: string;
  clarity_score?: number;
  correctness_score?: number;
  communication_score?: number;
  feedback?: string;
  key_improvements: string[];
}

export interface InterviewSession {
  id: string;
  role: string;
  target_company: string;
  interview_mode: string;
  status: string;
  overall_score?: number;
  summary_report?: string;
  created_at: string;
  completed_at?: string;
  exchanges: InterviewExchange[];
}
