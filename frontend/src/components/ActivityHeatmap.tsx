import React, { useState } from 'react';
import { Flame, CheckCircle, Calendar, Sparkles } from 'lucide-react';

interface ActivityHeatmapProps {
  activityCounts: Record<string, number>;
  streakDays: number;
}

export const ActivityHeatmap: React.FC<ActivityHeatmapProps> = ({
  activityCounts = {},
  streakDays = 0
}) => {
  const [hoveredDay, setHoveredDay] = useState<{ date: string; count: number } | null>(null);

  // Generate the last 84 days (12 weeks) ending today
  const today = new Date();
  const days: Array<{ dateStr: string; count: number; dayOfWeek: number }> = [];

  for (let i = 83; i >= 0; i--) {
    const d = new Date();
    d.setDate(today.getDate() - i);
    const dateStr = d.toISOString().split('T')[0];
    days.push({
      dateStr,
      count: activityCounts[dateStr] || 0,
      dayOfWeek: d.getDay() // 0 = Sun, 1 = Mon ...
    });
  }

  // Calculate total completed in the window
  const totalCompleted = Object.values(activityCounts).reduce((acc, curr) => acc + curr, 0);

  const getColor = (count: number) => {
    if (count === 0) return 'rgba(255, 255, 255, 0.06)';
    if (count === 1) return 'rgba(16, 185, 129, 0.35)';
    if (count === 2) return 'rgba(16, 185, 129, 0.60)';
    if (count >= 3) return 'var(--emerald-500)';
    return 'rgba(255, 255, 255, 0.06)';
  };

  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div style={{ padding: '6px', borderRadius: '8px', background: 'rgba(245, 158, 11, 0.15)', color: 'var(--amber-500)' }}>
            <Flame size={18} />
          </div>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800 }}>Preparation Discipline & Consistency</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>
              Your 12-week study task commit record. High streaks correlate with 3.4x faster placement offers.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '4px 12px',
            borderRadius: '20px',
            background: streakDays > 0 ? 'rgba(245, 158, 11, 0.15)' : 'rgba(255, 255, 255, 0.05)',
            border: `1px solid ${streakDays > 0 ? 'rgba(245, 158, 11, 0.35)' : 'var(--border-subtle)'}`,
            color: streakDays > 0 ? 'var(--amber-500)' : 'var(--text-muted)',
            fontWeight: 700,
            fontSize: '0.82rem'
          }}>
            <Flame size={15} />
            <span>{streakDays} Day{streakDays === 1 ? '' : 's'} Streak</span>
          </div>

          <div style={{
            fontSize: '0.8rem',
            color: 'var(--text-secondary)',
            padding: '4px 10px',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--border-subtle)'
          }}>
            <strong>{totalCompleted}</strong> tasks completed
          </div>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div style={{ overflowX: 'auto', paddingBottom: '0.5rem' }}>
        <div style={{
          display: 'grid',
          gridAutoFlow: 'column',
          gridTemplateRows: 'repeat(7, 13px)',
          gap: '4px',
          width: 'max-content'
        }}>
          {days.map((day) => (
            <div
              key={day.dateStr}
              onMouseEnter={() => setHoveredDay({ date: day.dateStr, count: day.count })}
              onMouseLeave={() => setHoveredDay(null)}
              style={{
                width: '13px',
                height: '13px',
                borderRadius: '3px',
                background: getColor(day.count),
                border: day.count > 0 ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid transparent',
                cursor: 'pointer',
                transition: 'transform 0.15s ease, background 0.15s ease'
              }}
            />
          ))}
        </div>
      </div>

      {/* Tooltip & Legend */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        <div>
          {hoveredDay ? (
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
              {hoveredDay.count} task{hoveredDay.count === 1 ? '' : 's'} on {hoveredDay.date}
            </span>
          ) : (
            <span>Hover squares to view day details</span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <span>Less</span>
          <div style={{ width: '10px', height: '10px', borderRadius: '2px', background: 'rgba(255, 255, 255, 0.06)' }} />
          <div style={{ width: '10px', height: '10px', borderRadius: '2px', background: 'rgba(16, 185, 129, 0.35)' }} />
          <div style={{ width: '10px', height: '10px', borderRadius: '2px', background: 'rgba(16, 185, 129, 0.60)' }} />
          <div style={{ width: '10px', height: '10px', borderRadius: '2px', background: 'var(--emerald-500)' }} />
          <span>More</span>
        </div>
      </div>
    </div>
  );
};

