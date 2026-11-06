import React, { useEffect, useState } from 'react';
import {
  Calendar,
  Code2,
  Database,
  Briefcase,
  AlertCircle,
  TrendingUp,
  CheckCircle2,
  Clock,
  ArrowRight,
  ShieldCheck,
  Award,
  Sliders
} from 'lucide-react';
import { api } from '../api/client';
import { PersonalizeMetricsModal } from '../components/PersonalizeMetricsModal';
import { ActivityHeatmap } from '../components/ActivityHeatmap';
import { CompanyReadinessCard } from '../components/CompanyReadinessCard';

interface DashboardProps {
  onNavigate: (tab: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showPersonalizeModal, setShowPersonalizeModal] = useState(false);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.getDashboard();
      setData(res);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleToggleTask = async (taskId: string, currentStatus: string) => {
    try {
      const nextStatus = currentStatus === 'completed' ? 'pending' : 'completed';
      await api.updateTaskStatus(taskId, nextStatus);
      fetchDashboard();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0', color: 'var(--text-secondary)' }}>
        <Clock className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Loading real-time career intelligence...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="glass-card" style={{ borderColor: 'rgba(244, 63, 94, 0.3)', padding: '2rem' }}>
        <h3 style={{ color: 'var(--rose-500)', marginBottom: '0.5rem' }}>Failed to load dashboard</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>{error}</p>
        <button className="btn btn-secondary" onClick={fetchDashboard}>Retry</button>
      </div>
    );
  }

  const { today_plan, skill_scores, practice_stats, job_pipeline, weekly_progress, missed_tasks, recommended_next_steps } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Top Welcome / Profile Hero */}
      <div className="glass-card" style={{
        background: 'linear-gradient(135deg, rgba(22, 31, 52, 0.9) 0%, rgba(30, 41, 70, 0.7) 100%)',
        border: '1px solid rgba(99, 102, 241, 0.25)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.35rem' }}>
              <span className="badge badge-success">Target: Class of {data.user.graduation_year || 2027}</span>
              <span className="badge badge-medium">{data.user.daily_study_hours || 4} Hours Daily</span>
            </div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              Welcome back, {data.user.name}
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: '650px' }}>
              {data.user.degree} • Target: {data.user.target_roles || 'SDE'} at {data.user.preferred_companies || 'Target Companies'} • Goal: {data.user.career_goals || 'Industry Mastery'}
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button className="btn btn-primary btn-sm" onClick={() => onNavigate('coach')}>
              Consult AI Coach
            </button>
            <button className="btn btn-secondary btn-sm" onClick={() => onNavigate('planner')}>
              View 7-Day Plan
            </button>
          </div>
        </div>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid-4">
        {/* Card 1: Today's Tasks */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>TODAY'S STUDY TASKS</p>
              <h3 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.2rem' }}>
                {today_plan.completed_tasks} / {today_plan.total_tasks}
              </h3>
            </div>
            <div style={{ padding: '8px', background: 'rgba(99, 102, 241, 0.15)', borderRadius: '10px', color: 'var(--indigo-500)' }}>
              <Calendar size={20} />
            </div>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {today_plan.total_tasks > 0 && today_plan.completed_tasks === today_plan.total_tasks
              ? `🎉 All ${data.user.daily_study_hours || 4} hours completed today!`
              : `${today_plan.total_tasks - today_plan.completed_tasks} tasks remaining today`}
          </p>
        </div>

        {/* Card 2: Coding Practice */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>PYTHON CODING SOLVED</p>
              <h3 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--emerald-500)', marginTop: '0.2rem' }}>
                {practice_stats.coding_passed} <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>/ {practice_stats.coding_total_attempts} tries</span>
              </h3>
            </div>
            <div style={{ padding: '8px', background: 'rgba(16, 185, 129, 0.15)', borderRadius: '10px', color: 'var(--emerald-500)' }}>
              <Code2 size={20} />
            </div>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            Isolated sandbox execution
          </p>
        </div>

        {/* Card 3: SQL Practice */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>SQL QUERIES VERIFIED</p>
              <h3 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--cyan-500)', marginTop: '0.2rem' }}>
                {practice_stats.sql_passed} <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>/ {practice_stats.sql_total_attempts} queries</span>
              </h3>
            </div>
            <div style={{ padding: '8px', background: 'rgba(6, 182, 212, 0.15)', borderRadius: '10px', color: 'var(--cyan-500)' }}>
              <Database size={20} />
            </div>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            Relational SQLite sandbox
          </p>
        </div>

        {/* Card 4: Job Pipeline */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>ACTIVE APPLICATIONS</p>
              <h3 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--amber-500)', marginTop: '0.2rem' }}>
                {job_pipeline.applied + job_pipeline.planned} <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>active</span>
              </h3>
            </div>
            <div style={{ padding: '8px', background: 'rgba(245, 158, 11, 0.15)', borderRadius: '10px', color: 'var(--amber-500)' }}>
              <Briefcase size={20} />
            </div>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {job_pipeline.saved} saved • {job_pipeline.applied} applied • {job_pipeline.offer} offers
          </p>
        </div>
      </div>

      {/* Target Company SDE Readiness Index */}
      <CompanyReadinessCard readiness={data.company_readiness || []} onNavigate={onNavigate} />

      {/* Main 2-Column Section: Today's Plan & Skill Proficiency */}
      <div className="grid-2">
        {/* Left Column: Today's 4-Hour Study Plan */}
        <div className="glass-card">
          <div className="glass-card-header">
            <div className="card-title">
              <Calendar size={18} style={{ color: 'var(--indigo-500)' }} />
              <span>Today's Study Plan ({today_plan?.daily_allocated_hours || data?.user?.daily_study_hours || 4} Hours)</span>
            </div>
            <button className="btn btn-secondary btn-sm" onClick={() => onNavigate('planner')}>
              Manage Plan
            </button>
          </div>

          {today_plan.tasks.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem 0', color: 'var(--text-muted)' }}>
              <p>No tasks scheduled for today.</p>
              <button className="btn btn-primary btn-sm" style={{ marginTop: '0.75rem' }} onClick={() => onNavigate('planner')}>
                Generate 7-Day Plan
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
              {today_plan.tasks.map((task: any) => (
                <div
                  key={task.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.85rem 1rem',
                    background: task.status === 'completed' ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid',
                    borderColor: task.status === 'completed' ? 'rgba(16, 185, 129, 0.3)' : 'var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                    <button
                      onClick={() => handleToggleTask(task.id, task.status)}
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        color: task.status === 'completed' ? 'var(--emerald-500)' : 'var(--text-muted)',
                        padding: 0
                      }}
                    >
                      <CheckCircle2 size={20} />
                    </button>
                    <div>
                      <div style={{
                        fontSize: '0.88rem',
                        fontWeight: 600,
                        textDecoration: task.status === 'completed' ? 'line-through' : 'none',
                        color: task.status === 'completed' ? 'var(--text-muted)' : 'var(--text-primary)'
                      }}>
                        {task.title}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {task.topic} • {task.duration_minutes} mins
                      </div>
                    </div>
                  </div>
                  <span className={`badge ${task.priority === 'Urgent' ? 'badge-urgent' : task.priority === 'High' ? 'badge-high' : 'badge-medium'}`}>
                    {task.priority}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Measured Skill Matrix vs Subjective Confidence */}
        <div className="glass-card">
          <div className="glass-card-header">
            <div className="card-title">
              <Award size={18} style={{ color: 'var(--emerald-500)' }} />
              <span>Skill Level (Measured vs Subjective)</span>
            </div>
            <div style={{ display: 'flex', gap: '0.45rem', flexWrap: 'wrap' }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => setShowPersonalizeModal(true)}
                style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
                title="Input your real scores and confidence for each skill"
              >
                <Sliders size={13} /> Personalize Metrics
              </button>
              <button className="btn btn-secondary btn-sm" onClick={() => onNavigate('assessment')}>
                Take Assessment
              </button>
            </div>
          </div>

          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Calculated from your inputs & verified assessments. Click any metric to calibrate.
          </p>

          {/* Quick Personalize Callout */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0.55rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(99, 102, 241, 0.08)',
            border: '1px solid rgba(99, 102, 241, 0.25)',
            marginBottom: '0.85rem',
            fontSize: '0.78rem'
          }}>
            <span style={{ color: 'var(--text-secondary)' }}>
              Want to calibrate your actual skill levels?
            </span>
            <button
              className="btn btn-primary btn-sm"
              onClick={() => setShowPersonalizeModal(true)}
              style={{ fontSize: '0.72rem', padding: '0.25rem 0.65rem', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              <Sliders size={12} /> Set My Real Scores
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {skill_scores.map((s: any) => {
              const proficiency = s.measured_proficiency || 0;
              const color = proficiency >= 70 ? 'var(--emerald-500)' : proficiency >= 50 ? 'var(--amber-500)' : 'var(--rose-500)';
              return (
                <div
                  key={s.topic}
                  onClick={() => setShowPersonalizeModal(true)}
                  title={`Click to personalize ${s.topic} score or confidence`}
                  style={{ cursor: 'pointer', padding: '2px 4px', borderRadius: '4px', transition: 'background 0.2s' }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)')}
                  onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.25rem' }}>
                    <span style={{ fontWeight: 600 }}>{s.topic}</span>
                    <span>
                      <strong style={{ color }}>{proficiency.toFixed(1)}%</strong>
                      <span style={{ color: 'var(--text-muted)', marginLeft: '6px' }}>(Confidence: {s.subjective_confidence}/5)</span>
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '7px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                    <div
                      style={{
                        width: `${Math.max(5, proficiency)}%`,
                        height: '100%',
                        background: color,
                        borderRadius: '4px',
                        transition: 'width 0.4s ease'
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* 12-Week Preparation Discipline & Activity Heatmap */}
      <ActivityHeatmap
        activityCounts={data.activity_counts || {}}
        streakDays={data.streak_days || 0}
      />

      {/* Missed Tasks & Recommended Next Steps */}
      <div className="grid-2">
        {/* Missed Tasks Alert */}
        <div className="glass-card">
          <div className="glass-card-header">
            <div className="card-title">
              <AlertCircle size={18} style={{ color: 'var(--rose-500)' }} />
              <span>Missed / Pending Schedule</span>
            </div>
            <span className="badge badge-urgent">{missed_tasks.length} overdue</span>
          </div>

          {missed_tasks.length === 0 ? (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', padding: '1rem 0' }}>
              ✨ Outstanding discipline! No missed or overdue tasks currently recorded.
            </p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {missed_tasks.map((mt: any) => (
                <div
                  key={mt.id}
                  style={{
                    padding: '0.75rem',
                    background: 'rgba(244, 63, 94, 0.06)',
                    border: '1px solid rgba(244, 63, 94, 0.2)',
                    borderRadius: 'var(--radius-sm)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}
                >
                  <div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{mt.title}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Scheduled: {mt.scheduled_date}</div>
                  </div>
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => handleToggleTask(mt.id, mt.status)}
                  >
                    Mark Done
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recommended Next Steps */}
        <div className="glass-card">
          <div className="glass-card-header">
            <div className="card-title">
              <TrendingUp size={18} style={{ color: 'var(--indigo-500)' }} />
              <span>Actionable Next Steps</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {recommended_next_steps.map((step: string, idx: number) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.8rem 1rem',
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)'
                }}
              >
                <div style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  background: 'var(--gradient-brand)',
                  color: 'white',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  {idx + 1}
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)', lineHeight: 1.5 }}>
                  {step}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <PersonalizeMetricsModal
        isOpen={showPersonalizeModal}
        onClose={() => setShowPersonalizeModal(false)}
        initialMetrics={skill_scores}
        onMetricsSaved={fetchDashboard}
      />
    </div>
  );
};
