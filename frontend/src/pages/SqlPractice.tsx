import React, { useState, useEffect } from 'react';
import { Database, Play, CheckCircle2, XCircle, Clock, Table, Lightbulb, Sparkles } from 'lucide-react';
import { api } from '../api/client';
import { SqlProblem, SqlExecutionResponse } from '../types';

export const SqlPractice: React.FC = () => {
  const [problems, setProblems] = useState<Array<{ id: string; slug: string; title: string; difficulty: string; category: string }>>([]);
  const [activeProblem, setActiveProblem] = useState<SqlProblem | null>(null);
  const [userQuery, setUserQuery] = useState<string>('SELECT * FROM employees LIMIT 5;');
  const [executionResult, setExecutionResult] = useState<SqlExecutionResponse | null>(null);
  const [executing, setExecuting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async () => {
    try {
      setLoading(true);
      const list = await api.getSqlProblems();
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
      const detail = await api.getSqlProblemDetail(slug);
      setActiveProblem(detail);
      setUserQuery('SELECT ...');
      setExecutionResult(null);
    } catch (err) {
      console.error(err);
    }
  };

  const handleExecute = async () => {
    if (!activeProblem) return;
    try {
      setExecuting(true);
      const res = await api.executeSql(activeProblem.slug, userQuery);
      setExecutionResult(res);
    } catch (err: any) {
      setExecutionResult({
        passed: false,
        columns: [],
        rows: [],
        row_count: 0,
        execution_time_ms: 0,
        error: err.message
      });
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <Clock className="animate-spin" size={32} style={{ margin: '0 auto 1rem', color: 'var(--indigo-500)' }} />
        <p>Loading SQL exercises and relational sandbox schema...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Exercise Selector */}
      <div className="glass-card" style={{ padding: '0.85rem 1.25rem', display: 'flex', alignItems: 'center', gap: '0.75rem', overflowX: 'auto' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
          SQL Tasks:
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
          {/* Left Column: Problem Prompt & Schema Info */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '640px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{activeProblem.title}</h3>
              <span className={`badge ${activeProblem.difficulty === 'Easy' ? 'badge-success' : 'badge-high'}`}>
                {activeProblem.difficulty}
              </span>
              <span className="badge badge-medium">{activeProblem.category}</span>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', paddingRight: '0.5rem' }}>
              <div style={{ fontSize: '0.92rem', color: 'var(--text-primary)', lineHeight: 1.7, marginBottom: '1.25rem' }}>
                {activeProblem.prompt}
              </div>

              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                Available Database Schema
              </h4>
              <div className="code-pane" style={{ marginBottom: '1.25rem' }}>
                <pre style={{ padding: '0.85rem', color: '#94a3b8', fontSize: '0.82rem', whiteSpace: 'pre-wrap' }}>
                  <code>{activeProblem.schema_info}</code>
                </pre>
              </div>

              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                Concept Hints
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {activeProblem.hints.map((hint, idx) => (
                  <div key={idx} style={{ padding: '0.75rem 1rem', background: 'rgba(99, 102, 241, 0.08)', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem' }}>
                    💡 {hint}
                  </div>
                ))}
              </div>

              {executionResult?.explanation && (
                <div style={{ marginTop: '1.25rem', padding: '1rem', background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: 'var(--radius-md)' }}>
                  <h4 style={{ color: 'var(--emerald-500)', fontWeight: 800, marginBottom: '0.35rem' }}>
                    Query Mechanics Breakdown
                  </h4>
                  <div style={{ fontSize: '0.88rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                    {executionResult.explanation}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: SQL Query Editor & Interactive Result Table */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', height: '640px' }}>
            <div className="code-pane" style={{ flex: '0 0 240px', display: 'flex', flexDirection: 'column' }}>
              <div className="code-header">
                <span>SQLite Read-Only Sandbox Console</span>
                <span>(SELECT & WITH only)</span>
              </div>
              <textarea
                className="code-textarea"
                style={{ flex: 1, minHeight: 'unset' }}
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
                placeholder="Write your SELECT query here..."
                spellCheck={false}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                🔒 Strict read-only transaction • Non-destructive
              </span>
              <button
                className="btn btn-emerald"
                onClick={handleExecute}
                disabled={executing || !userQuery.trim()}
              >
                <Play size={16} /> {executing ? 'Executing...' : 'Run & Validate Query'}
              </button>
            </div>

            {/* Results Grid Table */}
            <div className="glass-card" style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
              {executionResult ? (
                <>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {executionResult.passed ? (
                        <CheckCircle2 size={18} style={{ color: 'var(--emerald-500)' }} />
                      ) : (
                        <XCircle size={18} style={{ color: 'var(--rose-500)' }} />
                      )}
                      <strong style={{ color: executionResult.passed ? 'var(--emerald-500)' : 'var(--rose-500)', fontSize: '0.9rem' }}>
                        {executionResult.passed ? 'Query Result Matches Ground Truth!' : 'Result Mismatch or Error'}
                      </strong>
                    </div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {executionResult.row_count} rows • {executionResult.execution_time_ms}ms
                    </span>
                  </div>

                  {executionResult.error && (
                    <div style={{ color: 'var(--rose-500)', fontSize: '0.82rem', fontFamily: 'var(--font-mono)', marginBottom: '0.75rem' }}>
                      {executionResult.error}
                    </div>
                  )}

                  {executionResult.columns.length > 0 && (
                    <div style={{ overflowX: 'auto', flex: 1 }}>
                      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', fontFamily: 'var(--font-mono)' }}>
                        <thead>
                          <tr style={{ background: 'rgba(255, 255, 255, 0.05)', textAlign: 'left' }}>
                            {executionResult.columns.map((col, i) => (
                              <th key={i} style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {executionResult.rows.map((row, rIdx) => (
                            <tr key={rIdx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.03)' }}>
                              {row.map((cell, cIdx) => (
                                <td key={cIdx} style={{ padding: '0.45rem 0.75rem', color: 'var(--text-primary)' }}>
                                  {cell !== null ? String(cell) : 'NULL'}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </>
              ) : (
                <div style={{ textAlign: 'center', margin: 'auto', color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                  <Table size={28} style={{ margin: '0 auto 0.5rem', opacity: 0.5 }} />
                  <p>Execute your query to inspect the output table rows.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
