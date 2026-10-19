import React, { useState, useEffect } from 'react';
import { Calendar as CalendarIcon, CheckCircle2, Clock, Plus, RefreshCw, AlertCircle, BookOpen } from 'lucide-react';
import { api } from '../api/client';
import { StudyPlan, StudyTask } from '../types';

export const StudyPlanner: React.FC = () => {
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [tasks, setTasks] = useState<StudyTask[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [dailyHours, setDailyHours] = useState<number>(4.0);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [logTimeMinutes, setLogTimeMinutes] = useState<number>(45);
  const [reflectionNotes, setReflectionNotes] = useState<string>('');
  const [selectedTaskForLog, setSelectedTaskForLog] = useState<string>('');

  const loadPlan = async () => {
    try {
      setLoading(true);
      const active = await api.getActivePlan();
      setPlan(active);
      const allTasks = await api.getTasks();
      setTasks(allTasks);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlan();
  }, []);

  const handleGeneratePlan = async () => {
    try {
      setGenerating(true);
      const newPlan = await api.generatePlan(dailyHours);
      setPlan(newPlan);
      const allTasks = await api.getTasks();
      setTasks(allTasks);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleUpdateStatus = async (taskId: string, newStatus: string) => {
    try {
      await api.updateTaskStatus(taskId, newStatus);
      const allTasks = await api.getTasks();
      setTasks(allTasks);
    } catch (err) {
      console.error(err);
    }
  };

  const handleRecordSession = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.recordStudySession(logTimeMinutes, reflectionNotes, selectedTaskForLog || undefined);
      setReflectionNotes('');
      setSelectedTaskForLog('');
      const allTasks = await api.getTasks();
      setTasks(allTasks);
      alert('Session logged and progress updated successfully!');
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <Clock className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Loading 4-hour adaptive schedule...</p>
      </div>
    );
  }

  // Filter tasks for the selected date
  const filteredTasks = tasks.filter(t => t.scheduled_date === selectedDate);
  const totalAllocatedMins = filteredTasks.reduce((acc, t) => acc + t.duration_minutes, 0);

  // Collect unique dates from tasks
  const uniqueDates = Array.from(new Set(tasks.map(t => t.scheduled_date))).sort();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Top Banner: Plan Controls */}
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <span className="badge badge-success">Active 7-Day Sprint</span>
              <span className="badge badge-medium">{dailyHours}h Daily Protocol</span>
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{plan?.title || '4-Hour Daily Curriculum'}</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              Allocates time across DSA (highest priority at 1/5), Python, SQL, Aptitude, Core CS, and Projects.
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Daily Hours:</label>
              <select
                className="form-select"
                style={{ width: '80px', padding: '0.35rem' }}
                value={dailyHours}
                onChange={(e) => setDailyHours(parseFloat(e.target.value))}
              >
                <option value={3.0}>3.0h</option>
                <option value={4.0}>4.0h</option>
                <option value={5.0}>5.0h</option>
                <option value={6.0}>6.0h</option>
              </select>
            </div>
            <button
              className="btn btn-primary btn-sm"
              onClick={handleGeneratePlan}
              disabled={generating}
            >
              <RefreshCw size={14} className={generating ? 'animate-spin' : ''} />
              {generating ? 'Regenerating...' : 'Regenerate Sprint'}
            </button>
          </div>
        </div>
      </div>

      {/* Date Filter Tabs */}
      <div className="glass-card" style={{ padding: '0.75rem 1rem', display: 'flex', gap: '0.5rem', overflowX: 'auto' }}>
        {uniqueDates.map(dStr => {
          const isSelected = dStr === selectedDate;
          const dayName = new Date(dStr).toLocaleDateString('en-US', { weekday: 'short', month: 'numeric', day: 'numeric' });
          return (
            <button
              key={dStr}
              onClick={() => setSelectedDate(dStr)}
              className={`btn btn-sm ${isSelected ? 'btn-primary' : 'btn-secondary'}`}
              style={{ flexShrink: 0 }}
            >
              <CalendarIcon size={13} />
              <span>{dayName}</span>
            </button>
          );
        })}
      </div>

      <div className="grid-2">
        {/* Scheduled Tasks for Selected Date */}
        <div className="glass-card">
          <div className="glass-card-header">
            <div>
              <h4 style={{ fontSize: '1.1rem', fontWeight: 800 }}>Schedule for {selectedDate}</h4>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Total Allocated: {Math.floor(totalAllocatedMins / 60)}h {totalAllocatedMins % 60}m ({filteredTasks.length} tasks)
              </div>
            </div>
          </div>

          {filteredTasks.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', padding: '2rem 0', textAlign: 'center' }}>
              No tasks scheduled for this day. Click Regenerate Sprint to build a 7-day curriculum.
            </p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {filteredTasks.map(t => (
                <div
                  key={t.id}
                  style={{
                    padding: '1rem',
                    background: t.status === 'completed' ? 'rgba(16, 185, 129, 0.05)' : 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid',
                    borderColor: t.status === 'completed' ? 'rgba(16, 185, 129, 0.25)' : 'var(--border-subtle)',
                    borderRadius: 'var(--radius-md)'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                    <div style={{
                      fontWeight: 700,
                      fontSize: '0.92rem',
                      textDecoration: t.status === 'completed' ? 'line-through' : 'none',
                      color: t.status === 'completed' ? 'var(--text-muted)' : 'var(--text-primary)'
                    }}>
                      {t.title}
                    </div>
                    <span className={`badge ${t.priority === 'Urgent' ? 'badge-urgent' : t.priority === 'High' ? 'badge-high' : 'badge-medium'}`}>
                      {t.priority}
                    </span>
                  </div>

                  <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '0.75rem' }}>
                    {t.notes}
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      <Clock size={13} /> {t.duration_minutes} mins • <strong>{t.topic}</strong>
                    </div>

                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      {t.status !== 'completed' && (
                        <button
                          className="btn btn-emerald btn-sm"
                          onClick={() => handleUpdateStatus(t.id, 'completed')}
                        >
                          <CheckCircle2 size={13} /> Mark Completed
                        </button>
                      )}
                      {t.status === 'completed' && (
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => handleUpdateStatus(t.id, 'pending')}
                        >
                          Reset to Pending
                        </button>
                      )}
                      {t.status !== 'skipped' && t.status !== 'completed' && (
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => handleUpdateStatus(t.id, 'skipped')}
                        >
                          Skip
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Log Actual Study Session Form */}
        <div className="glass-card">
          <div className="glass-card-header">
            <h4 style={{ fontSize: '1.1rem', fontWeight: 800 }}>Log Study Session Reflection</h4>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
            Time spent is tracked for self-regulation, but remember that passing tests and writing clean code is the true measure of mastery.
          </p>

          <form onSubmit={handleRecordSession} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.35rem', display: 'block' }}>
                Associate with Scheduled Task (Optional):
              </label>
              <select
                className="form-select"
                value={selectedTaskForLog}
                onChange={(e) => setSelectedTaskForLog(e.target.value)}
              >
                <option value="">-- General Unscheduled Practice --</option>
                {filteredTasks.map(t => (
                  <option key={t.id} value={t.id}>{t.title} ({t.duration_minutes}m)</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.35rem', display: 'block' }}>
                Minutes Studied:
              </label>
              <input
                type="number"
                className="form-input"
                min={5}
                max={480}
                value={logTimeMinutes}
                onChange={(e) => setLogTimeMinutes(parseInt(e.target.value) || 0)}
                required
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.35rem', display: 'block' }}>
                Reflection / Topics Covered & Gotchas:
              </label>
              <textarea
                className="form-textarea"
                rows={4}
                placeholder="What did you learn? E.g., struggled with off-by-one errors on binary search upper bound, resolved with inclusive boundaries..."
                value={reflectionNotes}
                onChange={(e) => setReflectionNotes(e.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-primary" style={{ marginTop: '0.5rem' }}>
              Log Session & Update Progress
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
