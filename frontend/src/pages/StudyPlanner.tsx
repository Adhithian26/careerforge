import React, { useState, useEffect } from 'react';
import { Calendar as CalendarIcon, CheckCircle2, Clock, Plus, RefreshCw, AlertCircle, BookOpen, Compass, CheckSquare, Square, Layers, Flame, Award } from 'lucide-react';
import { api } from '../api/client';
import { StudyPlan, StudyTask, User } from '../types';

interface RoadmapMilestone {
  id: string;
  phase: string;
  timeframe: string;
  title: string;
  description: string;
  keySkills: string[];
  recommendedHours: number;
}

const ROADMAP_MILESTONES: RoadmapMilestone[] = [
  {
    id: 'm1',
    phase: 'Phase 1: Foundations',
    timeframe: 'Weeks 1 - 2',
    title: 'Core DSA Patterns & Big-O Rigor',
    description: 'Master Sliding Window, Two Pointers, Prefix Sums, and HashMaps with strict Big-O time and space tracking.',
    keySkills: ['Two Pointers', 'Sliding Window', 'HashMaps', 'Time Complexity'],
    recommendedHours: 25
  },
  {
    id: 'm2',
    phase: 'Phase 1: Foundations',
    timeframe: 'Weeks 2 - 3',
    title: 'Linear Structures & Backtracking',
    description: 'Linked list manipulation (Fast & Slow pointers), Monotonic Stacks, and recursive permutation backtracking.',
    keySkills: ['Fast & Slow Pointers', 'Monotonic Stack', 'Recursion', 'Backtracking'],
    recommendedHours: 20
  },
  {
    id: 'm3',
    phase: 'Phase 2: Complex Structures',
    timeframe: 'Weeks 3 - 5',
    title: 'Trees & Binary Search Trees',
    description: 'BFS level-order traversal, DFS tree recursion, Lowest Common Ancestor (LCA), and BST search/insertion.',
    keySkills: ['Binary Trees', 'BST', 'Tree BFS/DFS', 'Lowest Common Ancestor'],
    recommendedHours: 30
  },
  {
    id: 'm4',
    phase: 'Phase 2: Complex Structures',
    timeframe: 'Weeks 5 - 7',
    title: 'Graph Theory & Topological Sort',
    description: 'Adjacency list representation, Connected Components, Cycle Detection, Kahn’s Topological Sort, and Dijkstra.',
    keySkills: ['Graphs', 'BFS/DFS', 'Topological Sort', 'Dijkstra Algorithm'],
    recommendedHours: 35
  },
  {
    id: 'm5',
    phase: 'Phase 3: Optimization',
    timeframe: 'Weeks 7 - 9',
    title: 'Dynamic Programming Core Patterns',
    description: '0/1 Knapsack patterns, Longest Common Subsequence (LCS), Grid path transitions, and state memoization.',
    keySkills: ['DP Memoization', 'Tabulation', 'Knapsack Pattern', 'Subsequences'],
    recommendedHours: 35
  },
  {
    id: 'm6',
    phase: 'Phase 4: Design & Architecture',
    timeframe: 'Weeks 9 - 10',
    title: 'Object-Oriented & Low-Level Design (LLD)',
    description: 'SOLID design principles, Factory & Observer design patterns, and clean modular class hierarchy design.',
    keySkills: ['SOLID Principles', 'Factory Pattern', 'Observer Pattern', 'UML / OOP'],
    recommendedHours: 20
  },
  {
    id: 'm7',
    phase: 'Phase 4: Design & Architecture',
    timeframe: 'Weeks 10 - 11',
    title: 'Database Indexing & High-Level Scalability',
    description: 'B-Tree vs Hash indexing, SQL Query Optimization, Redis caching, pagination, and API rate limiting.',
    keySkills: ['B-Tree Indexing', 'SQL Optimization', 'Redis Caching', 'API Scalability'],
    recommendedHours: 20
  },
  {
    id: 'm8',
    phase: 'Phase 5: Placement Assets',
    timeframe: 'Weeks 11 - 12',
    title: 'Production Projects & Google XYZ Resume',
    description: 'Deploy full-stack projects with automated tests, rewrite bullets using the Google XYZ formula, achieve 85%+ ATS alignment.',
    keySkills: ['Production Deployment', 'Google XYZ Formula', 'ATS Tuning', 'Clean Code'],
    recommendedHours: 25
  },
  {
    id: 'm9',
    phase: 'Phase 6: Placement Sprint',
    timeframe: 'Weeks 12 - 13',
    title: 'Mock Interviews & Behavioral STAR Mastery',
    description: 'Timed live mock interviews with voice mode, Amazon Leadership Principles practice, and referral pipeline submissions.',
    keySkills: ['Voice Mock Interviews', 'STAR Method', 'Leadership Principles', 'Live Problem Solving'],
    recommendedHours: 30
  }
];

interface StudyPlannerProps {
  currentUser?: User | null;
}

export const StudyPlanner: React.FC<StudyPlannerProps> = ({ currentUser }) => {
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [tasks, setTasks] = useState<StudyTask[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [dailyHours, setDailyHours] = useState<number>(currentUser?.profile?.daily_study_hours || 4.0);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [logTimeMinutes, setLogTimeMinutes] = useState<number>(45);
  const [reflectionNotes, setReflectionNotes] = useState<string>('');
  const [selectedTaskForLog, setSelectedTaskForLog] = useState<string>('');

  // 90-Day Placement Roadmap State
  const [activeView, setActiveView] = useState<'schedule' | 'roadmap'>('schedule');
  const [completedMilestones, setCompletedMilestones] = useState<string[]>(() => {
    try {
      const saved = localStorage.getItem('careerforge_roadmap_milestones');
      return saved ? JSON.parse(saved) : ['m1'];
    } catch {
      return ['m1'];
    }
  });

  const toggleMilestone = (id: string) => {
    setCompletedMilestones(prev => {
      const next = prev.includes(id) ? prev.filter(m => m !== id) : [...prev, id];
      try {
        localStorage.setItem('careerforge_roadmap_milestones', JSON.stringify(next));
      } catch (e) {
        console.error(e);
      }
      return next;
    });
  };

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
      {/* View Switcher: Daily 4-Hour vs 90-Day Roadmap */}
      <div className="glass-card" style={{ padding: '0.85rem 1.25rem', display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
        <button
          className={`btn btn-sm ${activeView === 'schedule' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveView('schedule')}
        >
          <Clock size={15} /> 4-Hour Daily Curriculum
        </button>
        <button
          className={`btn btn-sm ${activeView === 'roadmap' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveView('roadmap')}
        >
          <Compass size={15} /> 90-Day SDE Placement Sprint Roadmap
        </button>
      </div>

      {activeView === 'schedule' ? (
        <>
          {/* Top Banner: Plan Controls */}
          <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <span className="badge badge-success">Active 7-Day Sprint</span>
              <span className="badge badge-medium">{dailyHours}h Daily Protocol</span>
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{plan?.title || `${dailyHours}-Hour Daily Curriculum`}</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              Allocates time across DSA, Python, SQL, Aptitude, Core CS, and Projects based on your {dailyHours}h daily budget.
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
      </>
      ) : (
        /* 90-Day Placement Sprint Roadmap View */
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Roadmap Header & Progress Summary */}
          <div className="glass-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                  <span className="badge badge-primary">Class of 2027 SDE Track</span>
                  <span className="badge badge-success">{completedMilestones.length} of {ROADMAP_MILESTONES.length} Milestones Cleared</span>
                </div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>90-Day Autonomous Placement Roadmap</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                  A structured path from core algorithmic mechanics to production architecture and placement offers.
                </p>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', minWidth: '220px' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Sprint Completion:</span>
                    <span style={{ fontWeight: 800, color: 'var(--emerald-400)' }}>
                      {Math.round((completedMilestones.length / ROADMAP_MILESTONES.length) * 100)}%
                    </span>
                  </div>
                  <div style={{ height: '8px', background: 'rgba(255,255,255,0.08)', borderRadius: '999px', overflow: 'hidden' }}>
                    <div
                      style={{
                        height: '100%',
                        width: `${(completedMilestones.length / ROADMAP_MILESTONES.length) * 100}%`,
                        background: 'linear-gradient(90deg, var(--indigo-500), var(--emerald-500))',
                        borderRadius: '999px',
                        transition: 'width 0.4s ease'
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Milestone List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {ROADMAP_MILESTONES.map((m, idx) => {
              const isChecked = completedMilestones.includes(m.id);
              return (
                <div
                  key={m.id}
                  className="glass-card"
                  style={{
                    borderLeft: isChecked ? '4px solid var(--emerald-500)' : '4px solid var(--indigo-500)',
                    padding: '1.25rem',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.75rem',
                    opacity: isChecked ? 0.9 : 1,
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <button
                        type="button"
                        onClick={() => toggleMilestone(m.id)}
                        style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, display: 'flex', alignItems: 'center' }}
                        title={isChecked ? 'Mark incomplete' : 'Mark completed'}
                      >
                        {isChecked ? (
                          <CheckCircle2 size={24} style={{ color: 'var(--emerald-500)' }} />
                        ) : (
                          <Square size={24} style={{ color: 'var(--text-muted)' }} />
                        )}
                      </button>

                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                          <span className={`badge ${isChecked ? 'badge-success' : 'badge-primary'}`} style={{ fontSize: '0.72rem' }}>
                            {m.phase}
                          </span>
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                            {m.timeframe}
                          </span>
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            • ~{m.recommendedHours} hours
                          </span>
                        </div>
                        <h4 style={{
                          fontSize: '1.05rem',
                          fontWeight: 700,
                          margin: '4px 0 0 0',
                          textDecoration: isChecked ? 'line-through' : 'none',
                          color: isChecked ? 'var(--text-muted)' : 'var(--text-primary)'
                        }}>
                          {idx + 1}. {m.title}
                        </h4>
                      </div>
                    </div>

                    <span className="badge badge-secondary" style={{ fontSize: '0.75rem' }}>
                      {isChecked ? 'Completed' : 'In Progress'}
                    </span>
                  </div>

                  <p style={{
                    fontSize: '0.85rem',
                    color: isChecked ? 'var(--text-muted)' : 'var(--text-secondary)',
                    lineHeight: 1.6,
                    margin: 0,
                    paddingLeft: '2.25rem'
                  }}>
                    {m.description}
                  </p>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', paddingLeft: '2.25rem' }}>
                    {m.keySkills.map(s => (
                      <span key={s} className="badge badge-secondary" style={{ fontSize: '0.7rem' }}>
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
