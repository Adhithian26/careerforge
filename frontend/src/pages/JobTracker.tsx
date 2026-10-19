import React, { useState, useEffect } from 'react';
import {
  Briefcase,
  Plus,
  ExternalLink,
  Search,
  Filter,
  CheckCircle2,
  Trash2,
  ShieldCheck,
  Building,
  Calendar
} from 'lucide-react';
import { api } from '../api/client';
import { JobApplication, JobPipelineStats } from '../types';

export const JobTracker: React.FC = () => {
  const [jobs, setJobs] = useState<JobApplication[]>([]);
  const [stats, setStats] = useState<JobPipelineStats | null>(null);
  const [approvedSources, setApprovedSources] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);

  // New Job Form State
  const [newCompany, setNewCompany] = useState('');
  const [newRole, setNewRole] = useState('Software Development Engineer');
  const [newUrl, setNewUrl] = useState('');
  const [newLocation, setNewLocation] = useState('Chennai / Bengaluru / Hybrid');
  const [newStatus, setNewStatus] = useState<JobApplication['status']>('planned');
  const [newEligibility, setNewEligibility] = useState('Eligible: B.Tech AI & Data Science (2027 batch)');
  const [newDeadline, setNewDeadline] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [jList, sStats, sources] = await Promise.all([
        api.getJobs(statusFilter || undefined, searchQuery || undefined),
        api.getPipelineStats(),
        api.getApprovedSources()
      ]);
      setJobs(jList);
      setStats(sStats);
      setApprovedSources(sources);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [statusFilter, searchQuery]);

  const handleCreateJob = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createJob({
        company: newCompany,
        role: newRole,
        job_url: newUrl,
        location: newLocation,
        status: newStatus,
        eligibility_notes: newEligibility,
        deadline: newDeadline || undefined,
        is_verified_opening: true
      });
      setShowAddModal(false);
      setNewCompany('');
      setNewUrl('');
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleStatusChange = async (id: string, nextStatus: JobApplication['status']) => {
    try {
      await api.updateJob(id, { status: nextStatus });
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteJob = async (id: string) => {
    if (!confirm('Are you sure you want to remove this application record?')) return;
    try {
      await api.deleteJob(id);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const statusOptions: Array<JobApplication['status']> = [
    'saved', 'planned', 'applied', 'assessment', 'interview', 'offer', 'rejected', 'withdrawn'
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Top Pipeline Stats Strip */}
      {stats && (
        <div className="grid-4">
          <div className="glass-card" style={{ padding: '1rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)' }}>SAVED / RESEARCH</span>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, marginTop: '0.2rem' }}>{stats.total_saved}</div>
          </div>
          <div className="glass-card" style={{ padding: '1rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--indigo-500)' }}>PLANNED APPLICATION</span>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--indigo-500)', marginTop: '0.2rem' }}>{stats.total_planned}</div>
          </div>
          <div className="glass-card" style={{ padding: '1rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--amber-500)' }}>APPLIED & ASSESSMENT</span>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--amber-500)', marginTop: '0.2rem' }}>
              {stats.total_applied + stats.total_assessment}
            </div>
          </div>
          <div className="glass-card" style={{ padding: '1rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--emerald-500)' }}>INTERVIEW & OFFER</span>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--emerald-500)', marginTop: '0.2rem' }}>
              {stats.total_interview + stats.total_offer}
            </div>
          </div>
        </div>
      )}

      {/* Filter and Action Bar */}
      <div className="glass-card" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div style={{ display: 'flex', gap: '0.75rem', flex: 1, minWidth: '260px', maxWidth: '500px' }}>
          <div style={{ position: 'relative', width: '100%' }}>
            <Search size={16} style={{ position: 'absolute', left: '12px', top: '11px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              className="form-input"
              style={{ paddingLeft: '2.25rem' }}
              placeholder="Search by company or role..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <select
            className="form-select"
            style={{ width: '160px' }}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Statuses</option>
            {statusOptions.map(s => (
              <option key={s} value={s}>{s.toUpperCase()}</option>
            ))}
          </select>
        </div>

        <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>
          <Plus size={16} /> Track New Opportunity
        </button>
      </div>

      {/* Job Records Table */}
      <div className="glass-card" style={{ padding: '0', overflow: 'hidden' }}>
        <div style={{ padding: '1.25rem 1.5rem', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 800 }}>Application Pipeline ({jobs.length} Records)</h3>
          <span className="badge badge-success">
            <ShieldCheck size={12} /> Verified Openings Policy
          </span>
        </div>

        {jobs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
            <Briefcase size={32} style={{ margin: '0 auto 0.5rem', opacity: 0.4 }} />
            <p>No job applications found matching your criteria.</p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
              <thead>
                <tr style={{ background: 'rgba(255, 255, 255, 0.02)', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)', fontSize: '0.78rem', textTransform: 'uppercase' }}>
                  <th style={{ padding: '0.85rem 1.5rem' }}>Company & Role</th>
                  <th style={{ padding: '0.85rem 1rem' }}>Location</th>
                  <th style={{ padding: '0.85rem 1rem' }}>Eligibility Notes</th>
                  <th style={{ padding: '0.85rem 1rem' }}>Deadline</th>
                  <th style={{ padding: '0.85rem 1rem' }}>Status</th>
                  <th style={{ padding: '0.85rem 1.5rem', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map(job => (
                  <tr key={job.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <td style={{ padding: '1rem 1.5rem' }}>
                      <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{job.company}</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{job.role}</div>
                      {job.job_url && (
                        <a
                          href={job.job_url}
                          target="_blank"
                          rel="noreferrer"
                          style={{ fontSize: '0.72rem', color: 'var(--indigo-500)', display: 'inline-flex', alignItems: 'center', gap: '3px', marginTop: '2px' }}
                        >
                          Career Link <ExternalLink size={10} />
                        </a>
                      )}
                    </td>
                    <td style={{ padding: '1rem', color: 'var(--text-secondary)' }}>{job.location}</td>
                    <td style={{ padding: '1rem', color: 'var(--text-secondary)', fontSize: '0.82rem', maxWidth: '240px' }}>
                      {job.eligibility_notes || '2027 batch'}
                    </td>
                    <td style={{ padding: '1rem', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                      {job.deadline ? job.deadline : 'Open / Unannounced'}
                    </td>
                    <td style={{ padding: '1rem' }}>
                      <select
                        className="form-select"
                        style={{ padding: '0.3rem 0.6rem', fontSize: '0.78rem', width: '130px' }}
                        value={job.status}
                        onChange={(e) => handleStatusChange(job.id, e.target.value as any)}
                      >
                        {statusOptions.map(opt => (
                          <option key={opt} value={opt}>{opt.toUpperCase()}</option>
                        ))}
                      </select>
                    </td>
                    <td style={{ padding: '1rem 1.5rem', textAlign: 'right' }}>
                      <button
                        onClick={() => handleDeleteJob(job.id)}
                        style={{ background: 'none', border: 'none', color: 'var(--rose-500)', cursor: 'pointer', padding: '4px' }}
                        title="Delete application"
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Approved Employer Portals (Permitted sources) */}
      <div className="glass-card">
        <h4 style={{ fontSize: '1.05rem', fontWeight: 800, marginBottom: '0.35rem' }}>
          Approved Permitted Employer Portals
        </h4>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', marginBottom: '1rem' }}>
          Verified primary hiring sites for your target companies. External applications require user confirmation on the portal.
        </p>

        <div className="grid-3">
          {approvedSources.map((source, i) => (
            <div
              key={i}
              style={{
                padding: '1rem',
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{source.company}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{source.roles?.join(', ')}</div>
              </div>
              <a
                href={source.portal}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
              >
                Official Portal <ExternalLink size={12} />
              </a>
            </div>
          ))}
        </div>
      </div>

      {/* Add Job Modal */}
      {showAddModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 200,
          padding: '1rem'
        }}>
          <div className="glass-card" style={{ width: '100%', maxWidth: '520px', background: '#121929' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '1rem' }}>Track New Job Opening</h3>
            <form onSubmit={handleCreateJob} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '3px' }}>Company Name *</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Zoho, Amazon, PayPal"
                  value={newCompany}
                  onChange={(e) => setNewCompany(e.target.value)}
                  required
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '3px' }}>Role Title *</label>
                <input
                  type="text"
                  className="form-input"
                  value={newRole}
                  onChange={(e) => setNewRole(e.target.value)}
                  required
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '3px' }}>Official Job URL</label>
                <input
                  type="url"
                  className="form-input"
                  placeholder="https://..."
                  value={newUrl}
                  onChange={(e) => setNewUrl(e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '3px' }}>Initial Stage</label>
                  <select
                    className="form-select"
                    value={newStatus}
                    onChange={(e) => setNewStatus(e.target.value as any)}
                  >
                    {statusOptions.map(s => (
                      <option key={s} value={s}>{s.toUpperCase()}</option>
                    ))}
                  </select>
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '3px' }}>Deadline</label>
                  <input
                    type="date"
                    className="form-input"
                    value={newDeadline}
                    onChange={(e) => setNewDeadline(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '3px' }}>Eligibility & Batch Notes</label>
                <input
                  type="text"
                  className="form-input"
                  value={newEligibility}
                  onChange={(e) => setNewEligibility(e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1rem' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save Application Record
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
