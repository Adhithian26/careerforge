import React from 'react';
import { Target, ArrowUpRight, Award, ShieldCheck } from 'lucide-react';

interface CompanyReadinessItem {
  company: string;
  readiness_percentage: number;
  focus_area: string;
}

interface CompanyReadinessCardProps {
  readiness: CompanyReadinessItem[];
  onNavigate: (tab: string) => void;
}

export const CompanyReadinessCard: React.FC<CompanyReadinessCardProps> = ({
  readiness = [],
  onNavigate
}) => {
  if (!readiness || readiness.length === 0) return null;

  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div className="glass-card-header">
        <div className="card-title">
          <Target size={18} style={{ color: 'var(--amber-500)' }} />
          <span>Target Company SDE Readiness Index</span>
        </div>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => onNavigate('interview')}
          style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
        >
          <Award size={14} /> Mock Interview Simulation
        </button>
      </div>

      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0 }}>
        Calibrated against historical interview clearance thresholds for your target companies.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
        {readiness.map((item) => {
          const pct = Math.round(item.readiness_percentage);
          const color = pct >= 80 ? 'var(--emerald-500)' : pct >= 65 ? 'var(--amber-500)' : 'var(--indigo-500)';
          const statusText = pct >= 80 ? 'Interview Ready' : pct >= 65 ? 'Target In Reach' : 'Foundation Building';

          return (
            <div
              key={item.company}
              style={{
                padding: '1rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid var(--border-subtle)',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.65rem'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '1rem', fontWeight: 700 }}>{item.company}</span>
                <span style={{
                  fontSize: '0.72rem',
                  padding: '2px 8px',
                  borderRadius: '10px',
                  background: pct >= 80 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                  color: color,
                  fontWeight: 600
                }}>
                  {statusText}
                </span>
              </div>

              {/* Meter */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '4px' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Readiness Score</span>
                  <strong style={{ color, fontSize: '0.9rem' }}>{pct}%</strong>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: '3px', transition: 'width 0.4s ease' }} />
                </div>
              </div>

              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.4 }}>
                <strong style={{ color: 'var(--text-primary)' }}>Focus:</strong> {item.focus_area}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

