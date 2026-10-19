import React, { useState, useEffect } from 'react';
import { CheckCircle2, Award, Clock, ArrowRight, RotateCcw, AlertCircle, Sliders } from 'lucide-react';
import { api } from '../api/client';
import { SkillMetric, AssessmentQuestion, AssessmentResult } from '../types';

export const SkillAssessment: React.FC = () => {
  const [topics, setTopics] = useState<string[]>([]);
  const [metrics, setMetrics] = useState<SkillMetric[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>('Python');
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [isTestActive, setIsTestActive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);

  const loadData = async () => {
    try {
      setLoading(true);
      const [tList, mList] = await Promise.all([
        api.getTopics(),
        api.getSkillMetrics()
      ]);
      setTopics(tList);
      setMetrics(mList);
      if (tList.length > 0) setSelectedTopic(tList[0]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Timer when test is active
  useEffect(() => {
    let interval: any;
    if (isTestActive) {
      interval = setInterval(() => {
        setTimeSpent(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTestActive]);

  const handleStartTest = async (topic: string) => {
    try {
      setLoading(true);
      setSelectedTopic(topic);
      const qList = await api.getQuestions(topic);
      setQuestions(qList);
      setCurrentQuestionIndex(0);
      setSelectedAnswers({});
      setResult(null);
      setTimeSpent(0);
      setIsTestActive(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId: string, optionIndex: number) => {
    setSelectedAnswers(prev => ({ ...prev, [questionId]: optionIndex }));
  };

  const handleSubmitTest = async () => {
    try {
      setSubmitting(true);
      const answersPayload = Object.entries(selectedAnswers).map(([qid, optIdx]) => ({
        question_id: qid,
        selected_option_index: optIdx
      }));
      const res = await api.submitAssessment(selectedTopic, answersPayload, timeSpent);
      setResult(res);
      setIsTestActive(false);
      // Refresh metrics to reflect new measured proficiency
      const updatedMetrics = await api.getSkillMetrics();
      setMetrics(updatedMetrics);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfidenceChange = async (topic: string, newConfidence: number) => {
    try {
      await api.updateConfidence(topic, newConfidence);
      const updated = await api.getSkillMetrics();
      setMetrics(updated);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading && !isTestActive) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <Clock className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Loading questions and skill metrics...</p>
      </div>
    );
  }

  // Active Assessment Mode
  if (isTestActive && questions.length > 0) {
    const currentQ = questions[currentQuestionIndex];
    const totalQ = questions.length;
    const isAnswered = selectedAnswers[currentQ.id] !== undefined;

    return (
      <div style={{ maxWidth: '850px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="glass-card" style={{ padding: '1.25rem 1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span className="badge badge-medium">{selectedTopic} Skill Assessment</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '0.25rem' }}>
                Question {currentQuestionIndex + 1} of {totalQ}
              </h3>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              <Clock size={16} />
              <span>{Math.floor(timeSpent / 60)}:{(timeSpent % 60).toString().padStart(2, '0')}</span>
            </div>
          </div>
          {/* Progress Bar */}
          <div style={{ width: '100%', height: '6px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '3px', marginTop: '1rem' }}>
            <div style={{
              width: `${((currentQuestionIndex + 1) / totalQ) * 100}%`,
              height: '100%',
              background: 'var(--gradient-brand)',
              borderRadius: '3px',
              transition: 'width 0.3s ease'
            }} />
          </div>
        </div>

        {/* Question Card */}
        <div className="glass-card">
          <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '1.25rem', lineHeight: 1.6 }}>
            {currentQ.question_text}
          </div>

          {currentQ.code_snippet && (
            <div className="code-pane" style={{ marginBottom: '1.5rem' }}>
              <div className="code-header">Python Snippet</div>
              <pre style={{ padding: '1rem', color: '#e2e8f0', fontSize: '0.9rem', overflowX: 'auto' }}>
                <code>{currentQ.code_snippet}</code>
              </pre>
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {currentQ.options.map((option, idx) => {
              const isSelected = selectedAnswers[currentQ.id] === idx;
              return (
                <button
                  key={idx}
                  onClick={() => handleSelectOption(currentQ.id, idx)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1rem',
                    padding: '1rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid',
                    borderColor: isSelected ? 'var(--indigo-500)' : 'var(--border-subtle)',
                    background: isSelected ? 'rgba(99, 102, 241, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                    color: 'var(--text-primary)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    fontSize: '0.92rem',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{
                    width: '28px',
                    height: '28px',
                    borderRadius: '50%',
                    border: '1px solid',
                    borderColor: isSelected ? 'var(--indigo-500)' : 'var(--border-subtle)',
                    background: isSelected ? 'var(--gradient-brand)' : 'transparent',
                    color: isSelected ? 'white' : 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    fontSize: '0.8rem',
                    flexShrink: 0
                  }}>
                    {String.fromCharCode(65 + idx)}
                  </div>
                  <span>{option}</span>
                </button>
              );
            })}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
            <button
              className="btn btn-secondary"
              disabled={currentQuestionIndex === 0}
              onClick={() => setCurrentQuestionIndex(prev => prev - 1)}
            >
              Previous
            </button>

            {currentQuestionIndex < totalQ - 1 ? (
              <button
                className="btn btn-primary"
                onClick={() => setCurrentQuestionIndex(prev => prev + 1)}
              >
                Next Question
              </button>
            ) : (
              <button
                className="btn btn-emerald"
                disabled={submitting || Object.keys(selectedAnswers).length === 0}
                onClick={handleSubmitTest}
              >
                {submitting ? 'Scoring Answers...' : 'Submit Assessment'}
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Result View
  if (result) {
    const isPassing = result.score_percentage >= 70;
    return (
      <div style={{ maxWidth: '850px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="glass-card" style={{
          textAlign: 'center',
          padding: '2.5rem',
          border: `1px solid ${isPassing ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            background: isPassing ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)',
            color: isPassing ? 'var(--emerald-500)' : 'var(--rose-500)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1rem'
          }}>
            <Award size={36} />
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800 }}>
            {isPassing ? 'Assessment Completed!' : 'Assessment Completed — Growth Needed'}
          </h2>
          <div style={{ fontSize: '3rem', fontWeight: 900, color: isPassing ? 'var(--emerald-500)' : 'var(--rose-500)', margin: '0.5rem 0' }}>
            {result.score_percentage}%
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '600px', margin: '0 auto' }}>
            {result.correct_count} of {result.total_questions} questions correct • Time Spent: {result.time_spent_seconds}s
          </p>
          <div style={{
            marginTop: '1.25rem',
            padding: '1rem',
            background: 'rgba(255, 255, 255, 0.03)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--text-primary)',
            fontSize: '0.88rem'
          }}>
            <strong>Recommendation:</strong> {result.recommendation}
          </div>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '1.5rem' }}>
            <button className="btn btn-primary" onClick={() => handleStartTest(result.topic)}>
              Retake Assessment
            </button>
            <button className="btn btn-secondary" onClick={() => setResult(null)}>
              Back to Skill Overview
            </button>
          </div>
        </div>

        {/* Detailed Mistake Breakdown */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '1rem' }}>
            Question-by-Question Breakdown & Explanations
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {result.breakdown.map((item, idx) => (
              <div
                key={idx}
                style={{
                  padding: '1.25rem',
                  borderRadius: 'var(--radius-md)',
                  background: item.is_correct ? 'rgba(16, 185, 129, 0.05)' : 'rgba(244, 63, 94, 0.05)',
                  border: `1px solid ${item.is_correct ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)'}`
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>
                    Q{idx + 1}: {item.question_text}
                  </span>
                  <span className={`badge ${item.is_correct ? 'badge-success' : 'badge-urgent'}`}>
                    {item.is_correct ? 'Correct' : 'Incorrect'}
                  </span>
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.5rem', lineHeight: 1.6 }}>
                  <strong>Explanation:</strong> {item.explanation}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Default Overview: All Topics & Confidence Sliders
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div className="glass-card">
        <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '0.35rem' }}>
          Measured Skill Proficiency vs Subjective Confidence
        </h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
          Take topic assessments to verify your true competence. Adjust your subjective confidence ratings to align study priorities.
        </p>
      </div>

      <div className="grid-2">
        {metrics.map((m) => {
          const prof = m.measured_proficiency || 0;
          const profColor = prof >= 70 ? 'var(--emerald-500)' : prof >= 50 ? 'var(--amber-500)' : 'var(--rose-500)';
          return (
            <div key={m.topic} className="glass-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <h4 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{m.topic}</h4>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    {m.attempts_count > 0 ? `${m.attempts_count} attempts • ${m.total_questions_answered} questions answered` : 'Not yet assessed'}
                  </div>
                </div>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => handleStartTest(m.topic)}
                >
                  Start Assessment
                </button>
              </div>

              {/* Measured Proficiency Bar */}
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.3rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Measured Proficiency (Verified)</span>
                  <strong style={{ color: profColor }}>{prof.toFixed(1)}%</strong>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${Math.max(5, prof)}%`, height: '100%', background: profColor, borderRadius: '4px' }} />
                </div>
              </div>

              {/* Subjective Confidence Selector */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  Subjective Confidence:
                </span>
                <div style={{ display: 'flex', gap: '4px' }}>
                  {[1, 2, 3, 4, 5].map((lvl) => (
                    <button
                      key={lvl}
                      onClick={() => handleConfidenceChange(m.topic, lvl)}
                      style={{
                        width: '28px',
                        height: '28px',
                        borderRadius: '6px',
                        border: '1px solid',
                        borderColor: m.subjective_confidence === lvl ? 'var(--indigo-500)' : 'var(--border-subtle)',
                        background: m.subjective_confidence === lvl ? 'var(--gradient-brand)' : 'transparent',
                        color: m.subjective_confidence === lvl ? 'white' : 'var(--text-muted)',
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
          );
        })}
      </div>
    </div>
  );
};
