import React, { useState, useEffect, useRef } from 'react';
import { FileText, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck, HelpCircle, Plus, UploadCloud, Loader2 } from 'lucide-react';
import { api } from '../api/client';
import { User } from '../types';

interface ResumeAssistantProps {
  currentUser?: User | null;
}

export const ResumeAssistant: React.FC<ResumeAssistantProps> = ({ currentUser }) => {
  const [activeTab, setActiveTab] = useState<'resume_match' | 'project_prep'>('resume_match');

  const studentName = currentUser?.full_name || 'Student Candidate';
  const studentDegree = currentUser?.profile?.degree || 'B.Tech AI & Data Science';
  const studentYear = currentUser?.profile?.graduation_year || 2027;
  const targetRole = currentUser?.profile?.target_roles || 'Software Development Engineer';
  const targetCompanies = currentUser?.profile?.preferred_companies || 'Zoho, TCS, Amazon, PayPal';
  const rawProjects = currentUser?.profile?.existing_projects || 'RAG Chatbot, Facial Recognition Attendance';
  const parsedProjects = rawProjects.split(',').map(p => p.trim()).filter(Boolean);

  // Resume Matcher State
  const [resumeText, setResumeText] = useState(
`${studentName} - ${studentDegree} (${studentYear})
Skills: Python, SQL, REST APIs, Git, Data Structures & Algorithms, OOP, Relational Databases.
Projects:
${parsedProjects.map((p, idx) => `${idx + 1}. ${p}: Designed and implemented modular architecture with automated test suites and error handling.`).join('\n')}`
  );

  const [jobDescription, setJobDescription] = useState(
`${targetRole} - ${targetCompanies}
Requirements:
- Strong proficiency in Python, SQL, and Object-Oriented Programming (OOP)
- Solid foundation in Data Structures and Algorithms (DSA)
- Experience designing RESTful APIs with FastAPI, Django, or modern frameworks
- Knowledge of relational databases and system modularity
- Clear technical communication and systematic analytical problem-solving skills.`
  );

  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [analyzing, setAnalyzing] = useState(false);

  // Resume Upload State
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileUpload = async (file: File) => {
    if (!file) return;
    setUploadError(null);
    setUploadSuccess(null);
    setUploadingFile(true);
    try {
      const res = await api.uploadResumePdf(file);
      if (res.extracted_text) {
        setResumeText(res.extracted_text);
        setUploadSuccess(res.message || `Successfully extracted ${res.word_count || ''} words from ${file.name}`);
      } else {
        setUploadError('Could not extract text from this document. Please ensure it is not scanned/empty.');
      }
    } catch (err: any) {
      setUploadError(err.message || 'Failed to process document');
    } finally {
      setUploadingFile(false);
    }
  };

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  // Project Interview Questions State
  const [selectedProject, setSelectedProject] = useState(parsedProjects[0] || 'Technical Project');
  const [customProjectInput, setCustomProjectInput] = useState('');
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
    if (!title.trim()) return;
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

  useEffect(() => {
    if (activeTab === 'project_prep' && !projectQuestions) {
      handleFetchProjectQuestions(selectedProject);
    }
  }, [activeTab]);

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
          {/* Input Textareas & File Upload */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {/* File Dropzone */}
            <div
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={(e) => { e.preventDefault(); setIsDragging(false); }}
              onDrop={handleFileDrop}
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: isDragging ? '2px dashed var(--indigo-500)' : '2px dashed var(--border-subtle)',
                backgroundColor: isDragging ? 'rgba(99, 102, 241, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                borderRadius: 'var(--radius-md)',
                padding: '1.25rem 1rem',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              <input
                type="file"
                ref={fileInputRef}
                accept=".pdf,.txt,.md"
                style={{ display: 'none' }}
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFileUpload(e.target.files[0]);
                  }
                }}
              />
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.4rem' }}>
                {uploadingFile ? (
                  <>
                    <Loader2 size={24} className="spin" style={{ color: 'var(--indigo-400)' }} />
                    <span style={{ fontSize: '0.88rem', fontWeight: 600 }}>Extracting resume text...</span>
                  </>
                ) : (
                  <>
                    <UploadCloud size={28} style={{ color: 'var(--indigo-400)' }} />
                    <div>
                      <span style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                        Drag & drop your Resume PDF, TXT, or MD
                      </span>
                      <p style={{ fontSize: '0.76rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                        Click to browse file from your device (Pure Client/Backend Parsing)
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Upload Feedback */}
            {uploadSuccess && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '0.55rem 0.85rem',
                background: 'rgba(16, 185, 129, 0.12)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.82rem',
                color: 'var(--emerald-400)',
              }}>
                <CheckCircle2 size={16} />
                <span>{uploadSuccess}</span>
              </div>
            )}
            {uploadError && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '0.55rem 0.85rem',
                background: 'rgba(239, 68, 68, 0.12)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.82rem',
                color: 'var(--rose-400)',
              }}>
                <AlertTriangle size={16} />
                <span>{uploadError}</span>
              </div>
            )}

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)' }}>
                  Your Resume Plaintext:
                </label>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {resumeText.split(/\s+/).filter(Boolean).length} words
                </span>
              </div>
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
          {/* Project Choice Buttons & Custom Project Input */}
          <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)' }}>Your Projects:</span>
              {parsedProjects.map((proj, idx) => (
                <button
                  key={idx}
                  className={`btn btn-sm ${selectedProject === proj ? 'btn-primary' : 'btn-secondary'}`}
                  onClick={() => handleFetchProjectQuestions(proj)}
                >
                  {idx + 1}. {proj}
                </button>
              ))}
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.85rem' }}>
              <input
                type="text"
                className="form-input"
                placeholder="Or type any project title (e.g. Distributed Key-Value Store, E-commerce Microservice)..."
                value={customProjectInput}
                onChange={(e) => setCustomProjectInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && customProjectInput.trim()) {
                    handleFetchProjectQuestions(customProjectInput.trim());
                  }
                }}
                style={{ flex: 1 }}
              />
              <button
                className="btn btn-sm btn-primary"
                onClick={() => handleFetchProjectQuestions(customProjectInput.trim())}
                disabled={loadingQuestions || !customProjectInput.trim()}
              >
                <Plus size={14} /> Generate Questions
              </button>
            </div>
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
