import React, { useState, useEffect } from 'react';
import { TrendingUp, CheckCircle2, AlertCircle, RefreshCw, Calendar, Award, Code2, Database } from 'lucide-react';
import { api } from '../api/client';
import { WeeklyReport } from '../types';

export const WeeklyReview: React.FC = () => {
  const [report, setReport] = useState<WeeklyReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const loadReport = async () => {
    try {
      setLoading(true);
      const rep = await api.getLatestWeeklyReport();
      setReport(rep);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, []);

  const handleGenerateFresh = async () => {
    try {
      setGenerating(true);
      const rep = await api.generateWeeklyReport();
      setReport(rep);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <RefreshCw className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Synthesizing verified weekly metrics...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Top Banner */}
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <span className="badge badge-success">Verified Progress Synthesis</span>
              <span className="badge badge-medium">
                {report?.week_start_date} to {report?.week_end_date}
              </span>
            </div>
            <h3 style={{ fontSize: '1.35rem', fontWeight: 800 }}>Weekly Performance Audit</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              Built strictly from recorded application events, completed sandbox runs, and assessment attempts.
            </p>
          </div>

          <button
            className="btn btn-primary"
            onClick={handleGenerateFresh}
            disabled={generating}
          >
            <RefreshCw size={15} className={generating ? 'animate-spin' : ''} />
            {generating ? 'Auditing Events...' : 'Generate New Weekly Audit'}
          </button>
        </div>
      </div>

      {report && (
        <>
          {/* Quantitative Metrics Grid */}
          <div className="grid-4">
            <div className="glass-card">
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)' }}>TASKS COMPLETION RATE</span>
              <div style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--indigo-500)', marginTop: '0.2rem' }}>
                {report.completion_rate_percentage}%
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.35rem' }}>
                {report.completed_tasks_count} of {report.planned_tasks_count} study tasks finished
              </div>
            </div>

            <div className="glass-card">
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--emerald-500)' }}>CODING PROBLEMS SOLVED</span>
              <div style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--emerald-500)', marginTop: '0.2rem' }}>
                {report.coding_problems_solved}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.35rem' }}>
                Passed all deterministic test cases
              </div>
            </div>

            <div className="glass-card">
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--cyan-500)' }}>SQL CHALLENGES VERIFIED</span>
              <div style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--cyan-500)', marginTop: '0.2rem' }}>
                {report.sql_exercises_completed}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.35rem' }}>
                Matched sandbox ground truth
              </div>
            </div>

            <div className="glass-card">
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--amber-500)' }}>APPLICATIONS SUBMITTED</span>
              <div style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--amber-500)', marginTop: '0.2rem' }}>
                {report.applications_submitted}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.35rem' }}>
                Confirmed on official portals
              </div>
            </div>
          </div>

          <div className="grid-2">
            {/* Left: Identified Weaknesses & Top Strengths */}
            <div className="glass-card">
              <h4 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '0.75rem', color: 'var(--rose-500)' }}>
                Demonstrated Weaknesses (Needs Focus)
              </h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                Topics where assessment proficiency or submission success fell below target threshold.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                {report.key_weaknesses.map((w, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '0.85rem',
                      background: 'rgba(244, 63, 94, 0.08)',
                      border: '1px solid rgba(244, 63, 94, 0.25)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '0.88rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}
                  >
                    <AlertCircle size={16} style={{ color: 'var(--rose-500)', flexShrink: 0 }} />
                    <span>{w}</span>
                  </div>
                ))}
              </div>

              <h4 style={{ fontSize: '1.1rem', fontWeight: 800, marginTop: '1.75rem', marginBottom: '0.75rem', color: 'var(--emerald-500)' }}>
                Demonstrated Strengths
              </h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {report.top_strengths.length > 0 ? (
                  report.top_strengths.map((s, idx) => (
                    <span key={idx} className="badge badge-success">{s}</span>
                  ))
                ) : (
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    Complete more assessments above 75% to register verified strengths.
                  </span>
                )}
              </div>
            </div>

            {/* Right: Three Priorities for Next Week */}
            <div className="glass-card">
              <h4 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '0.75rem', color: 'var(--indigo-500)' }}>
                Top 3 Priorities for Next Week
              </h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
                Algorithmic targets formulated to address recorded gaps in your 2027 SDE readiness.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {report.next_week_priorities.map((p, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '0.85rem',
                      padding: '1rem',
                      background: 'rgba(99, 102, 241, 0.08)',
                      border: '1px solid rgba(99, 102, 241, 0.25)',
                      borderRadius: 'var(--radius-md)'
                    }}
                  >
                    <div style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: '50%',
                      background: 'var(--gradient-brand)',
                      color: 'white',
                      fontWeight: 800,
                      fontSize: '0.85rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      {idx + 1}
                    </div>
                    <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                      {p}
                    </div>
                  </div>
                ))}
              </div>

              {/* Coach Evaluation Text */}
              {report.ai_coach_summary && (
                <div style={{
                  marginTop: '1.5rem',
                  padding: '1rem',
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.85rem',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.6
                }}>
                  <strong style={{ color: 'var(--text-primary)' }}>Coach Audit Note:</strong> {report.ai_coach_summary}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
