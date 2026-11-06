import React, { useState } from 'react';
import { Sliders, X, Plus, Trash2, CheckCircle2, Sparkles, RefreshCw, AlertCircle } from 'lucide-react';
import { api } from '../api/client';

export interface SkillScoreItem {
  topic: string;
  measured_proficiency: number;
  subjective_confidence: number;
}

interface PersonalizeMetricsModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialMetrics: SkillScoreItem[];
  onMetricsSaved: () => void;
}

export const PersonalizeMetricsModal: React.FC<PersonalizeMetricsModalProps> = ({
  isOpen,
  onClose,
  initialMetrics,
  onMetricsSaved
}) => {
  const [metrics, setMetrics] = useState<SkillScoreItem[]>(() => {
    if (initialMetrics && initialMetrics.length > 0) {
      return initialMetrics.map(m => ({
        topic: m.topic,
        measured_proficiency: Math.round(m.measured_proficiency),
        subjective_confidence: m.subjective_confidence || 3
      }));
    }
    return [
      { topic: 'Python', measured_proficiency: 65, subjective_confidence: 3 },
      { topic: 'SQL', measured_proficiency: 60, subjective_confidence: 3 },
      { topic: 'DSA', measured_proficiency: 30, subjective_confidence: 1 },
      { topic: 'Aptitude', measured_proficiency: 60, subjective_confidence: 3 },
      { topic: 'OOP', measured_proficiency: 70, subjective_confidence: 3 },
      { topic: 'DBMS', measured_proficiency: 65, subjective_confidence: 3 },
      { topic: 'Operating Systems', measured_proficiency: 50, subjective_confidence: 2 },
      { topic: 'Computer Networks', measured_proficiency: 50, subjective_confidence: 2 }
    ];
  });

  const [newTopic, setNewTopic] = useState('');
  const [regeneratePlan, setRegeneratePlan] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Sync when initialMetrics change
  React.useEffect(() => {
    if (initialMetrics && initialMetrics.length > 0) {
      setMetrics(initialMetrics.map(m => ({
        topic: m.topic,
        measured_proficiency: Math.round(m.measured_proficiency),
        subjective_confidence: m.subjective_confidence || 3
      })));
    }
  }, [initialMetrics]);

  if (!isOpen) return null;

  const handleScoreChange = (index: number, val: number) => {
    const updated = [...metrics];
    updated[index].measured_proficiency = Math.min(100, Math.max(0, val));
    setMetrics(updated);
  };

  const handleConfidenceChange = (index: number, val: number) => {
    const updated = [...metrics];
    updated[index].subjective_confidence = Math.min(5, Math.max(1, val));
    setMetrics(updated);
  };

  const handleAddTopic = () => {
    const trimmed = newTopic.trim();
    if (!trimmed) return;
    if (metrics.some(m => m.topic.toLowerCase() === trimmed.toLowerCase())) {
      setError(`Topic "${trimmed}" already exists.`);
      return;
    }
    setMetrics([
      ...metrics,
      { topic: trimmed, measured_proficiency: 50, subjective_confidence: 3 }
    ]);
    setNewTopic('');
    setError(null);
  };

  const handleRemoveTopic = (index: number) => {
    const updated = metrics.filter((_, i) => i !== index);
    setMetrics(updated);
  };

  const handleApplyPreset = (level: 'beginner' | 'intermediate' | 'advanced') => {
    setMetrics(prev => prev.map(m => {
      if (level === 'beginner') {
        return { ...m, measured_proficiency: 35, subjective_confidence: 2 };
      } else if (level === 'intermediate') {
        return { ...m, measured_proficiency: 65, subjective_confidence: 3 };
      } else {
        return { ...m, measured_proficiency: 85, subjective_confidence: 4 };
      }
    }));
  };

  const handleSave = async () => {
    if (metrics.length === 0) {
      setError('Please have at least one skill topic configured.');
      return;
    }
    try {
      setSaving(true);
      setError(null);
      await api.calibrateSkillMetrics(metrics, regeneratePlan);
      onMetricsSaved();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to update skill metrics.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(5, 7, 15, 0.82)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999,
      padding: '1rem'
    }}>
      <div
        className="glass-card"
        style={{
          width: '100%',
          maxWidth: '680px',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          padding: 0,
          overflow: 'hidden',
          borderRadius: 'var(--radius-lg)',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.65)',
          border: '1px solid var(--border-glow)'
        }}
      >
        {/* Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          background: 'rgba(255, 255, 255, 0.02)'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <div style={{ padding: '6px', borderRadius: '8px', background: 'rgba(99, 102, 241, 0.15)', color: 'var(--indigo-500)' }}>
                <Sliders size={18} />
              </div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>
                Personalize Skill Metrics & Confidence
              </h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: '0.35rem' }}>
              Input your genuine scores and confidence levels. The AI Career Coach and Study Planner calibrate instantly to your exact inputs.
            </p>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '4px',
              borderRadius: '6px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Quick Presets Bar */}
        <div style={{
          padding: '0.65rem 1.5rem',
          background: 'rgba(255, 255, 255, 0.01)',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '0.5rem',
          fontSize: '0.78rem'
        }}>
          <span style={{ color: 'var(--text-muted)', fontWeight: 600 }}>Quick Presets:</span>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
              onClick={() => handleApplyPreset('beginner')}
            >
              Beginner Baseline (35%)
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
              onClick={() => handleApplyPreset('intermediate')}
            >
              Intermediate (65%)
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
              onClick={() => handleApplyPreset('advanced')}
            >
              Advanced Mastery (85%)
            </button>
          </div>
        </div>

        {error && (
          <div style={{
            margin: '0.75rem 1.5rem 0',
            padding: '0.65rem 0.85rem',
            background: 'rgba(244, 63, 94, 0.1)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--rose-500)',
            fontSize: '0.82rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {/* Scrollable Topic Metrics Form */}
        <div style={{
          padding: '1.25rem 1.5rem',
          overflowY: 'auto',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {metrics.map((item, idx) => {
            const score = item.measured_proficiency;
            const scoreColor = score >= 70 ? 'var(--emerald-500)' : score >= 50 ? 'var(--amber-500)' : 'var(--rose-500)';
            return (
              <div
                key={item.topic}
                style={{
                  padding: '0.85rem 1rem',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.65rem'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.92rem' }}>{item.topic}</span>
                    <span
                      style={{
                        fontSize: '0.72rem',
                        padding: '2px 8px',
                        borderRadius: '12px',
                        background: score >= 70 ? 'rgba(16, 185, 129, 0.15)' : score >= 50 ? 'rgba(245, 158, 11, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                        color: scoreColor,
                        fontWeight: 600
                      }}
                    >
                      {score >= 70 ? 'Proficient' : score >= 50 ? 'Intermediate' : 'Needs Focus'}
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveTopic(idx)}
                    title="Remove topic"
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'var(--text-muted)',
                      cursor: 'pointer',
                      padding: '4px',
                      borderRadius: '4px'
                    }}
                  >
                    <Trash2 size={15} />
                  </button>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '1.25rem', alignItems: 'center' }}>
                  {/* Measured Proficiency Slider */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Measured Score:</span>
                      <strong style={{ color: scoreColor, fontSize: '0.85rem' }}>{score}%</strong>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                      <input
                        type="range"
                        min={0}
                        max={100}
                        step={1}
                        value={score}
                        onChange={(e) => handleScoreChange(idx, parseInt(e.target.value) || 0)}
                        style={{
                          width: '100%',
                          accentColor: scoreColor,
                          cursor: 'pointer'
                        }}
                      />
                      <input
                        type="number"
                        min={0}
                        max={100}
                        value={score}
                        onChange={(e) => handleScoreChange(idx, parseInt(e.target.value) || 0)}
                        style={{
                          width: '48px',
                          padding: '2px 4px',
                          borderRadius: '4px',
                          background: 'rgba(255, 255, 255, 0.05)',
                          border: '1px solid var(--border-subtle)',
                          color: scoreColor,
                          fontSize: '0.78rem',
                          textAlign: 'center',
                          fontWeight: 700
                        }}
                      />
                    </div>
                  </div>

                  {/* Confidence (1-5) Pills */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Confidence:</span>
                      <strong style={{ color: 'var(--indigo-500)', fontSize: '0.85rem' }}>
                        {item.subjective_confidence}/5
                      </strong>
                    </div>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      {[1, 2, 3, 4, 5].map((lvl) => (
                        <button
                          key={lvl}
                          type="button"
                          onClick={() => handleConfidenceChange(idx, lvl)}
                          style={{
                            flex: 1,
                            height: '26px',
                            borderRadius: '4px',
                            border: '1px solid',
                            borderColor: item.subjective_confidence === lvl ? 'var(--indigo-500)' : 'var(--border-subtle)',
                            background: item.subjective_confidence === lvl ? 'var(--gradient-brand)' : 'transparent',
                            color: item.subjective_confidence === lvl ? '#fff' : 'var(--text-muted)',
                            cursor: 'pointer',
                            fontSize: '0.75rem',
                            fontWeight: 700
                          }}
                        >
                          {lvl}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}

          {/* Add New Custom Skill Row */}
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            padding: '0.75rem 1rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(255, 255, 255, 0.015)',
            border: '1px dashed var(--border-subtle)',
            alignItems: 'center'
          }}>
            <input
              type="text"
              className="form-input"
              placeholder="Add Custom Topic (e.g. React, Docker, Machine Learning, AWS, System Design)..."
              value={newTopic}
              onChange={(e) => setNewTopic(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddTopic(); } }}
              style={{ fontSize: '0.82rem', padding: '0.45rem 0.75rem' }}
            />
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={handleAddTopic}
              style={{ whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              <Plus size={15} /> Add Skill
            </button>
          </div>
        </div>

        {/* Footer Actions */}
        <div style={{
          padding: '1rem 1.5rem',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          background: 'rgba(255, 255, 255, 0.02)',
          flexWrap: 'wrap',
          gap: '0.75rem'
        }}>
          <label style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.78rem',
            color: 'var(--text-secondary)',
            cursor: 'pointer'
          }}>
            <input
              type="checkbox"
              checked={regeneratePlan}
              onChange={(e) => setRegeneratePlan(e.target.checked)}
              style={{ accentColor: 'var(--indigo-500)' }}
            />
            Re-prioritize study plan around my weakest skills
          </label>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>
            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={handleSave}
              disabled={saving}
              style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              {saving ? (
                <>
                  <RefreshCw size={15} className="animate-spin" /> Saving...
                </>
              ) : (
                <>
                  <Sparkles size={15} /> Save & Calibrate Workspace
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

