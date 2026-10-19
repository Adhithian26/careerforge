import React, { useState, useEffect } from 'react';
import { Mic, CheckCircle2, Award, Clock, ArrowRight, RefreshCw, MessageSquare } from 'lucide-react';
import { api } from '../api/client';
import { InterviewSession } from '../types';

export const MockInterview: React.FC = () => {
  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [activeSession, setActiveSession] = useState<InterviewSession | null>(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [selectedMode, setSelectedMode] = useState('Technical');
  const [targetCompany, setTargetCompany] = useState('Zoho / Amazon / General Product');
  const [roleTitle, setRoleTitle] = useState('Software Development Engineer');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const loadPastSessions = async () => {
    try {
      setLoading(true);
      const past = await api.getPastInterviews();
      setSessions(past);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPastSessions();
  }, []);

  const handleStartInterview = async () => {
    try {
      setSubmitting(true);
      const newSession = await api.startInterview(roleTitle, targetCompany, selectedMode);
      setActiveSession(newSession);
      setUserAnswer('');
    } catch (err: any) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleAnswerQuestion = async () => {
    if (!activeSession || !userAnswer.trim()) return;
    try {
      setSubmitting(true);
      const updated = await api.answerInterviewQuestion(activeSession.id, userAnswer);
      setActiveSession(updated);
      setUserAnswer('');
      if (updated.status === 'completed') {
        loadPastSessions();
      }
    } catch (err: any) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading && !activeSession) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <Clock className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Loading mock interview simulator...</p>
      </div>
    );
  }

  // Active Interview Session Mode
  if (activeSession) {
    const isCompleted = activeSession.status === 'completed';
    const pendingExchange = activeSession.exchanges.find(e => !e.user_answer);

    return (
      <div style={{ maxWidth: '850px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="glass-card" style={{ padding: '1.25rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <span className="badge badge-medium">{activeSession.interview_mode} Mode</span>
              <span className="badge badge-success">{activeSession.target_company}</span>
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>{activeSession.role}</h3>
          </div>
          {isCompleted ? (
            <span className="badge badge-success">Completed</span>
          ) : (
            <span className="badge badge-high">Round {activeSession.exchanges.length} in Progress</span>
          )}
        </div>

        {/* Completed Final Report Card */}
        {isCompleted && (
          <div className="glass-card" style={{ textAlign: 'center', padding: '2.5rem', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: 'rgba(16, 185, 129, 0.2)',
              color: 'var(--emerald-500)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 1rem'
            }}>
              <Award size={36} />
            </div>
            <h2 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Mock Interview Performance Report</h2>
            <div style={{ fontSize: '3rem', fontWeight: 900, color: 'var(--emerald-500)', margin: '0.5rem 0' }}>
              {activeSession.overall_score || 85} / 100
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '650px', margin: '0 auto' }}>
              {activeSession.summary_report}
            </p>
            <div style={{ marginTop: '1.5rem' }}>
              <button className="btn btn-primary" onClick={() => setActiveSession(null)}>
                Start Another Simulation
              </button>
            </div>
          </div>
        )}

        {/* Question & Exchange History */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {activeSession.exchanges.map((ex) => (
            <div key={ex.id} className="glass-card">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.65rem' }}>
                <span className="badge badge-medium">Round {ex.round_number}</span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Interviewer Question</span>
              </div>
              <div style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '1rem' }}>
                {ex.question}
              </div>

              {ex.user_answer ? (
                <div style={{ padding: '1rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--indigo-500)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Your Answer:</div>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                    {ex.user_answer}
                  </div>

                  {/* Rubric Scores */}
                  <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(255, 255, 255, 0.04)', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '0.8rem' }}>Clarity: <strong>{ex.clarity_score}/10</strong></span>
                    <span style={{ fontSize: '0.8rem' }}>Technical Correctness: <strong>{ex.correctness_score}/10</strong></span>
                    <span style={{ fontSize: '0.8rem' }}>Communication: <strong>{ex.communication_score}/10</strong></span>
                  </div>

                  {ex.feedback && (
                    <div style={{ marginTop: '0.75rem', fontSize: '0.82rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                      <strong>Feedback:</strong> {ex.feedback}
                    </div>
                  )}
                </div>
              ) : null}
            </div>
          ))}
        </div>

        {/* Pending Question Answer Box */}
        {!isCompleted && pendingExchange && (
          <div className="glass-card">
            <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>
              Your Response (Round {pendingExchange.round_number}):
            </h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
              Structure your answer with technical mechanics, trade-offs, and concrete examples (e.g. STAR method).
            </p>
            <textarea
              className="form-textarea"
              rows={6}
              placeholder="Type your response here as if in a live technical or HR round..."
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
            />
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button
                className="btn btn-emerald"
                onClick={handleAnswerQuestion}
                disabled={submitting || !userAnswer.trim()}
              >
                {submitting ? 'Evaluating Rubrics...' : 'Submit Answer'}
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  // Session Setup & History Overview
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div className="grid-2">
        {/* Start New Interview Card */}
        <div className="glass-card">
          <div className="glass-card-header">
            <div className="card-title">
              <Mic size={20} style={{ color: 'var(--indigo-500)' }} />
              <span>Configure Mock Interview Session</span>
            </div>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
            Simulates actual company interview styles (Zoho coding rounds, Amazon STAR behavioural, Technical system discussions).
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Interview Mode:
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem' }}>
                {['Technical', 'HR', 'Project', 'Aptitude'].map((m) => (
                  <button
                    key={m}
                    onClick={() => setSelectedMode(m)}
                    className={`btn btn-sm ${selectedMode === m ? 'btn-primary' : 'btn-secondary'}`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Target Company Profile:
              </label>
              <select
                className="form-select"
                value={targetCompany}
                onChange={(e) => setTargetCompany(e.target.value)}
              >
                <option value="Zoho">Zoho Corporation (Logic & Problem Solving)</option>
                <option value="Amazon">Amazon (DSA & Leadership Principles)</option>
                <option value="TCS">TCS Digital / Prime (Aptitude & Core CS)</option>
                <option value="PayPal">PayPal (System Design & Code Quality)</option>
                <option value="General Product Company">General Tier-1 Product Company</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Target Role:
              </label>
              <input
                type="text"
                className="form-input"
                value={roleTitle}
                onChange={(e) => setRoleTitle(e.target.value)}
              />
            </div>

            <button
              className="btn btn-emerald"
              style={{ marginTop: '0.5rem' }}
              onClick={handleStartInterview}
              disabled={submitting}
            >
              <Mic size={16} /> Begin Mock Interview
            </button>
          </div>
        </div>

        {/* Past Sessions Summary */}
        <div className="glass-card">
          <div className="glass-card-header">
            <h4 style={{ fontSize: '1.1rem', fontWeight: 800 }}>Past Interview Sessions ({sessions.length})</h4>
          </div>

          {sessions.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', padding: '2rem 0', textAlign: 'center' }}>
              No mock interviews completed yet. Start your first session on the left!
            </p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxHeight: '420px', overflowY: 'auto' }}>
              {sessions.map(s => (
                <div
                  key={s.id}
                  style={{
                    padding: '0.85rem 1rem',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>{s.interview_mode} • {s.target_company}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {new Date(s.created_at).toLocaleDateString()} • {s.exchanges.length} rounds
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontWeight: 800, color: 'var(--emerald-500)', fontSize: '1.1rem' }}>
                      {s.overall_score ? `${s.overall_score}%` : 'In Progress'}
                    </div>
                    <button
                      className="btn btn-secondary btn-sm"
                      style={{ marginTop: '4px', fontSize: '0.72rem', padding: '0.2rem 0.5rem' }}
                      onClick={() => setActiveSession(s)}
                    >
                      View Report
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
