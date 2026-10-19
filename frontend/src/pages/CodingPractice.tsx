import React, { useState, useEffect } from 'react';
import { Code2, Play, CheckCircle2, XCircle, Clock, ShieldAlert, Sparkles, Lightbulb } from 'lucide-react';
import { api } from '../api/client';
import { CodingProblem, CodingExecutionResponse } from '../types';

export const CodingPractice: React.FC = () => {
  const [problems, setProblems] = useState<Array<{ id: string; slug: string; title: string; difficulty: string; category: string }>>([]);
  const [activeProblem, setActiveProblem] = useState<CodingProblem | null>(null);
  const [userCode, setUserCode] = useState<string>('');
  const [executionResult, setExecutionResult] = useState<CodingExecutionResponse | null>(null);
  const [executing, setExecuting] = useState(false);
  const [activeTab, setActiveTab] = useState<'description' | 'hints' | 'solution'>('description');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async () => {
    try {
      setLoading(true);
      const list = await api.getCodingProblems();
      setProblems(list);
      if (list.length > 0) {
        selectProblem(list[0].slug);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const selectProblem = async (slug: string) => {
    try {
      const detail = await api.getCodingProblemDetail(slug);
      setActiveProblem(detail);
      setUserCode(detail.starter_code);
      setExecutionResult(null);
      setActiveTab('description');
    } catch (err) {
      console.error(err);
    }
  };

  const handleRunSample = async () => {
    if (!activeProblem) return;
    try {
      setExecuting(true);
      const res = await api.runCodingSample(activeProblem.slug, userCode);
      setExecutionResult(res);
    } catch (err: any) {
      setExecutionResult({
        passed: false,
        passed_tests: 0,
        total_tests: 0,
        runtime_ms: 0,
        error: err.message,
        results: []
      });
    } finally {
      setExecuting(false);
    }
  };

  const handleSubmit = async () => {
    if (!activeProblem) return;
    try {
      setExecuting(true);
      const res = await api.submitCoding(activeProblem.slug, userCode);
      setExecutionResult(res);
    } catch (err: any) {
      setExecutionResult({
        passed: false,
        passed_tests: 0,
        total_tests: 0,
        runtime_ms: 0,
        error: err.message,
        results: []
      });
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <Clock className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Loading coding problems...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Problem Selector Bar */}
      <div className="glass-card" style={{ padding: '0.85rem 1.25rem', display: 'flex', alignItems: 'center', gap: '0.75rem', overflowX: 'auto' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
          Exercises:
        </span>
        {problems.map((p) => {
          const isSelected = activeProblem?.slug === p.slug;
          return (
            <button
              key={p.slug}
              onClick={() => selectProblem(p.slug)}
              className={`btn btn-sm ${isSelected ? 'btn-primary' : 'btn-secondary'}`}
              style={{ flexShrink: 0 }}
            >
              <span>{p.title}</span>
              <span className={`badge ${p.difficulty === 'Easy' ? 'badge-success' : 'badge-high'}`} style={{ marginLeft: '4px' }}>
                {p.difficulty}
              </span>
            </button>
          );
        })}
      </div>

      {activeProblem && (
        <div className="grid-2">
          {/* Left Column: Problem Details & Hints */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '620px' }}>
            {/* Tabs */}
            <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
              <button
                className={`btn btn-sm ${activeTab === 'description' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveTab('description')}
              >
                Description
              </button>
              <button
                className={`btn btn-sm ${activeTab === 'hints' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveTab('hints')}
              >
                <Lightbulb size={14} /> Hints ({activeProblem.hints.length})
              </button>
              {executionResult?.solution_approach && (
                <button
                  className={`btn btn-sm ${activeTab === 'solution' ? 'btn-emerald' : 'btn-secondary'}`}
                  onClick={() => setActiveTab('solution')}
                >
                  <Sparkles size={14} /> Official Approach
                </button>
              )}
            </div>

            <div style={{ flex: 1, overflowY: 'auto', paddingRight: '0.5rem' }}>
              {activeTab === 'description' && (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{activeProblem.title}</h3>
                    <span className={`badge ${activeProblem.difficulty === 'Easy' ? 'badge-success' : 'badge-high'}`}>
                      {activeProblem.difficulty}
                    </span>
                    <span className="badge badge-medium">{activeProblem.category}</span>
                  </div>
                  <div style={{ whiteSpace: 'pre-wrap', color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.9rem' }}>
                    {activeProblem.description}
                  </div>

                  <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginTop: '1.5rem', marginBottom: '0.5rem' }}>
                    Sample Test Cases
                  </h4>
                  {activeProblem.sample_tests.map((st, i) => (
                    <div key={i} style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '0.75rem 1rem', borderRadius: 'var(--radius-sm)', marginBottom: '0.5rem', fontSize: '0.85rem', fontFamily: 'var(--font-mono)' }}>
                      <div><strong>Input:</strong> {JSON.stringify(st.input)}</div>
                      <div style={{ color: 'var(--emerald-500)', marginTop: '2px' }}><strong>Expected:</strong> {JSON.stringify(st.expected)}</div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'hints' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {activeProblem.hints.map((hint, idx) => (
                    <div key={idx} style={{ padding: '1rem', background: 'rgba(99, 102, 241, 0.08)', border: '1px solid rgba(99, 102, 241, 0.2)', borderRadius: 'var(--radius-md)' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--indigo-500)', marginBottom: '0.35rem' }}>
                        💡 Hint {idx + 1}
                      </div>
                      <div style={{ fontSize: '0.88rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                        {hint}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'solution' && executionResult?.solution_approach && (
                <div style={{ padding: '1rem', background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: 'var(--radius-md)' }}>
                  <h4 style={{ color: 'var(--emerald-500)', fontWeight: 800, marginBottom: '0.5rem' }}>
                    Optimized Engineering Solution
                  </h4>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.7 }}>
                    {executionResult.solution_approach}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Code Editor & Execution Results */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', height: '620px' }}>
            <div className="code-pane" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div className="code-header">
                <span>Python 3.14 Sandbox (AST Protected)</span>
                <span>Function: <code>def {activeProblem.function_name}(...)</code></span>
              </div>
              <textarea
                className="code-textarea"
                style={{ flex: 1 }}
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                spellCheck={false}
              />
            </div>

            {/* Run & Submit Action Controls */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                <Clock size={14} /> 3.0s Timeout Limit • No Arbitrary Process Access
              </div>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <button
                  className="btn btn-secondary"
                  onClick={handleRunSample}
                  disabled={executing}
                >
                  <Play size={15} /> Run Sample Tests
                </button>
                <button
                  className="btn btn-emerald"
                  onClick={handleSubmit}
                  disabled={executing}
                >
                  <CheckCircle2 size={16} /> Submit Solution
                </button>
              </div>
            </div>

            {/* Execution Result Terminal */}
            {executionResult && (
              <div className="glass-card" style={{
                padding: '1rem',
                maxHeight: '200px',
                overflowY: 'auto',
                border: `1px solid ${executionResult.passed ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    {executionResult.passed ? (
                      <CheckCircle2 size={18} style={{ color: 'var(--emerald-500)' }} />
                    ) : (
                      <XCircle size={18} style={{ color: 'var(--rose-500)' }} />
                    )}
                    <strong style={{ color: executionResult.passed ? 'var(--emerald-500)' : 'var(--rose-500)', fontSize: '0.9rem' }}>
                      {executionResult.passed ? 'Accepted (All Tests Passed)' : 'Execution Failed'}
                    </strong>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {executionResult.passed_tests}/{executionResult.total_tests} tests • {executionResult.runtime_ms}ms
                  </span>
                </div>

                {executionResult.error && (
                  <div style={{ color: 'var(--rose-500)', fontSize: '0.82rem', fontFamily: 'var(--font-mono)', whiteSpace: 'pre-wrap' }}>
                    {executionResult.error}
                  </div>
                )}

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', marginTop: '0.5rem' }}>
                  {executionResult.results.map((r, i) => (
                    <div key={i} style={{ fontSize: '0.78rem', display: 'flex', justifyContent: 'space-between', fontFamily: 'var(--font-mono)', color: r.passed ? 'var(--emerald-500)' : 'var(--rose-500)' }}>
                      <span>Test Case {r.test_index}: {r.passed ? 'PASSED' : 'FAILED'}</span>
                      {r.actual_str && <span>Got: {r.actual_str}</span>}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
