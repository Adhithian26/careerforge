import React, { useState } from 'react';
import { FileText, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react';
import { api } from '../api/client';

export const ResumeAssistant: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'resume_match' | 'project_prep'>('resume_match');

  // Resume Matcher State
  const [resumeText, setResumeText] = useState(
`Adhithian S - B.Tech Artificial Intelligence & Data Science (2027)
Skills: Python, SQL, REST APIs, Git, Data Structures, OOP, SQLite.
Projects:
1. RAG Chatbot: Engineered a retrieval-augmented generation assistant with LangChain, embeddings, and vector similarity search.
2. Facial Recognition Attendance System: Built computer vision face detection pipeline with OpenCV and Euclidean distance verification.`
  );
  const [jobDescription, setJobDescription] = useState(
`Software Development Engineer I (SDE 1) - Zoho / Amazon / PayPal
Requirements:
- Strong proficiency in Python, SQL, and Object-Oriented Programming (OOP)
- Solid foundation in Data Structures and Algorithms (DSA)
- Experience designing RESTful APIs with FastAPI or Django
- Knowledge of relational databases (PostgreSQL/SQLite) and Docker containers
- Excellent communication and systematic problem-solving skills.`
  );
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [analyzing, setAnalyzing] = useState(false);

  // Project Interview Questions State
  const [selectedProject, setSelectedProject] = useState('RAG Chatbot');
  const [projectQuestions, setProjectQuestions] = useState<any>(null);
  const [loadingQuestions, setLoadingQuestions] = useState(false);

  const handleAnalyzeResume = async () => {
    try {
      setAnalyzing(true);
      const res = await api.analyzeResume(resumeText, jobDescription);
      setAnalysisResult(res);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleFetchProjectQuestions = async (title: string) => {
    try {
      setLoadingQuestions(true);
      setSelectedProject(title);
      const res = await api.getProjectPrep(title);
      setProjectQuestions(res);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoadingQuestions(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Navigation Sub-Tabs */}
      <div className="glass-card" style={{ padding: '0.85rem 1.25rem', display: 'flex', gap: '0.75rem' }}>
        <button
          className={`btn btn-sm ${activeTab === 'resume_match' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('resume_match')}
        >
          <FileText size={15} /> Resume & Job Description Alignment
        </button>
        <button
          className={`btn btn-sm ${activeTab === 'project_prep' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => {
            setActiveTab('project_prep');
            if (!projectQuestions) handleFetchProjectQuestions('RAG Chatbot');
          }}
        >
          <Sparkles size={15} /> Project Interview Question Generator
        </button>
      </div>

      {activeTab === 'resume_match' && (
        <div className="grid-2">
          {/* Input Textareas */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
                Your Resume Plaintext:
              </label>
              <textarea
                className="form-textarea"
                rows={9}
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
                Target Job Description (JD):
              </label>
              <textarea
                className="form-textarea"
                rows={9}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            </div>

            <button
              className="btn btn-emerald"
              onClick={handleAnalyzeResume}
              disabled={analyzing || !resumeText.trim() || !jobDescription.trim()}
            >
              {analyzing ? 'Analyzing Alignment...' : 'Analyze Keyword Alignment'}
            </button>
          </div>

          {/* Alignment Output */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', overflowY: 'auto', maxHeight: '680px' }}>
            {analysisResult ? (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>ATS Keyword Alignment</h3>
                  <div style={{ fontSize: '1.6rem', fontWeight: 900, color: analysisResult.match_percentage >= 70 ? 'var(--emerald-500)' : 'var(--amber-500)' }}>
                    {analysisResult.match_percentage}%
                  </div>
                </div>

                {/* Matched Skills */}
                <div>
                  <h4 style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--emerald-500)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                    Matched Skills ({analysisResult.matched_skills.length})
                  </h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {analysisResult.matched_skills.map((s: string) => (
                      <span key={s} className="badge badge-success">{s}</span>
                    ))}
                  </div>
                </div>

                {/* Missing Critical Skills */}
                {analysisResult.missing_critical_skills.length > 0 && (
                  <div>
                    <h4 style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--rose-500)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                      Missing Core SDE Keywords ({analysisResult.missing_critical_skills.length})
                    </h4>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {analysisResult.missing_critical_skills.map((s: string) => (
                        <span key={s} className="badge badge-urgent">{s}</span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Actionable Recommendations */}
                <div>
                  <h4 style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                    Actionable Improvement Guidelines
                  </h4>
                  <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                    {analysisResult.action_items.map((item: string, i: number) => (
                      <li key={i} style={{ marginBottom: '0.35rem' }}>{item}</li>
                    ))}
                  </ul>
                </div>

                {/* Bullet Points Suggestions */}
                <div style={{ padding: '1rem', background: 'rgba(99, 102, 241, 0.08)', borderRadius: 'var(--radius-md)' }}>
                  <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--indigo-500)', marginBottom: '0.35rem' }}>
                    Recommended XYZ Formula Bullets:
                  </h4>
                  <ul style={{ paddingLeft: '1.25rem', fontSize: '0.82rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                    {analysisResult.recommended_bullet_points.map((pt: string, i: number) => (
                      <li key={i} style={{ marginBottom: '0.35rem' }}>{pt}</li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <div style={{ textAlign: 'center', margin: 'auto', color: 'var(--text-muted)', padding: '3rem 0' }}>
                <FileText size={32} style={{ margin: '0 auto 0.5rem', opacity: 0.4 }} />
                <p>Paste your resume and job description to inspect verified alignment without fabricated skills.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'project_prep' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Project Choice Buttons */}
          <div className="glass-card" style={{ padding: '1rem 1.5rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)' }}>Select Project:</span>
            <button
              className={`btn btn-sm ${selectedProject === 'RAG Chatbot' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => handleFetchProjectQuestions('RAG Chatbot')}
            >
              1. RAG Chatbot (LangChain & Vector Store)
            </button>
            <button
              className={`btn btn-sm ${selectedProject === 'Facial Recognition Attendance' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => handleFetchProjectQuestions('Facial Recognition Attendance')}
            >
              2. Facial Recognition Attendance System (OpenCV)
            </button>
          </div>

          {projectQuestions && (
            <div className="grid-2">
              {/* Architecture & Tradeoff Questions */}
              <div className="glass-card">
                <h4 style={{ fontSize: '1.05rem', fontWeight: 800, marginBottom: '0.75rem', color: 'var(--indigo-500)' }}>
                  System Architecture & Deep Dive Questions
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                  {projectQuestions.architecture_questions?.map((q: string, i: number) => (
                    <div key={i} style={{ padding: '0.85rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.88rem' }}>
                      <strong>Q{i + 1}:</strong> {q}
                    </div>
                  ))}
                  {projectQuestions.deep_dive_questions?.map((q: string, i: number) => (
                    <div key={i} style={{ padding: '0.85rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.88rem' }}>
                      <strong>Q{i + 1}:</strong> {q}
                    </div>
                  ))}
                </div>
              </div>

              {/* Edge Cases & Interview Talking Points */}
              <div className="glass-card">
                <h4 style={{ fontSize: '1.05rem', fontWeight: 800, marginBottom: '0.75rem', color: 'var(--emerald-500)' }}>
                  Production Trade-Offs & Recommended Talking Points
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                  {projectQuestions.tradeoff_challenges?.map((q: string, i: number) => (
                    <div key={i} style={{ padding: '0.85rem', background: 'rgba(245, 158, 11, 0.08)', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(245, 158, 11, 0.2)', fontSize: '0.88rem' }}>
                      <strong>Challenge:</strong> {q}
                    </div>
                  ))}
                  <div style={{ padding: '1rem', background: 'rgba(16, 185, 129, 0.08)', borderRadius: 'var(--radius-md)' }}>
                    <h5 style={{ fontWeight: 700, color: 'var(--emerald-500)', marginBottom: '0.5rem' }}>Recommended Interview Talking Points:</h5>
                    <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', lineHeight: 1.6 }}>
                      {projectQuestions.recommended_talking_points?.map((pt: string, i: number) => (
                        <li key={i}>{pt}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
