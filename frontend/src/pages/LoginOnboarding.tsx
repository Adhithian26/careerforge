import React, { useState } from 'react';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  User,
  Lock,
  Mail,
  Eye,
  EyeOff,
  GraduationCap,
  Briefcase,
  Clock,
  Server,
  Zap,
  Check,
  Target
} from 'lucide-react';
import { api, getApiBase, setApiBase } from '../api/client';

interface LoginOnboardingProps {
  onSuccess: () => void;
}

export const LoginOnboarding: React.FC<LoginOnboardingProps> = ({ onSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [fullName, setFullName] = useState('');
  const [degree, setDegree] = useState('B.Tech Artificial Intelligence and Data Science');
  const [graduationYear, setGraduationYear] = useState(2027);
  const [studyHours, setStudyHours] = useState(4);
  const [targetRoles, setTargetRoles] = useState('Software Development Engineer');
  const [targetCompanies, setTargetCompanies] = useState('Zoho, TCS, Amazon, Google, PayPal');
  const [existingProjects, setExistingProjects] = useState('RAG Chatbot, Facial Recognition Attendance');
  const [careerGoals, setCareerGoals] = useState('SDE Placement then Advanced Engineering Leadership');
  const [skillInputs, setSkillInputs] = useState<Array<{ topic: string; measured_proficiency: number; subjective_confidence: number }>>([
    { topic: 'DSA', measured_proficiency: 35, subjective_confidence: 2 },
    { topic: 'Python', measured_proficiency: 65, subjective_confidence: 3 },
    { topic: 'SQL', measured_proficiency: 60, subjective_confidence: 3 },
    { topic: 'Aptitude', measured_proficiency: 65, subjective_confidence: 3 },
    { topic: 'OOP', measured_proficiency: 70, subjective_confidence: 3 },
    { topic: 'DBMS', measured_proficiency: 65, subjective_confidence: 3 },
    { topic: 'Operating Systems', measured_proficiency: 55, subjective_confidence: 2 },
    { topic: 'Computer Networks', measured_proficiency: 50, subjective_confidence: 2 }
  ]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [showServerConfig, setShowServerConfig] = useState(false);
  const [serverUrl, setServerUrl] = useState(getApiBase());
  const [serverStatus, setServerStatus] = useState<string | null>(null);

  const testServerConnection = async (targetOverride?: string) => {
    const urlToTest = (targetOverride || serverUrl).trim().replace(/\/+$/, '');
    setServerStatus('Testing connection...');
    try {
      setApiBase(urlToTest);
      setServerUrl(urlToTest);
      const res = await fetch(`${urlToTest}/health`);
      if (res.ok) {
        setServerStatus(`✅ Connected (${urlToTest.includes('localhost') ? 'Local Server' : 'Cloud Server'})`);
      } else {
        setServerStatus(`⚠️ Server returned HTTP ${res.status}`);
      }
    } catch (e: any) {
      setServerStatus(`❌ Connection failed: ${e.message || 'Offline'}`);
    }
  };

  const handleSelectServerPreset = (presetUrl: string) => {
    setServerUrl(presetUrl);
    testServerConnection(presetUrl);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setLoading(true);

    const cleanEmail = email.trim().toLowerCase();
    const cleanPassword = password.trim();

    try {
      if (isRegister) {
        const dsaItem = skillInputs.find(s => s.topic === 'DSA');
        const pyItem = skillInputs.find(s => s.topic === 'Python');
        const sqlItem = skillInputs.find(s => s.topic === 'SQL');

        await api.register({
          email: cleanEmail,
          password: cleanPassword,
          full_name: fullName.trim() || 'Student',
          degree: degree.trim() || 'Engineering',
          graduation_year: graduationYear,
          daily_study_hours: studyHours,
          target_roles: targetRoles.trim() || 'Software Development Engineer',
          preferred_companies: targetCompanies.trim() || 'Zoho, TCS, Amazon',
          existing_projects: existingProjects.trim(),
          career_goals: careerGoals.trim(),
          python_confidence: pyItem ? pyItem.subjective_confidence : 3,
          sql_confidence: sqlItem ? sqlItem.subjective_confidence : 3,
          dsa_confidence: dsaItem ? dsaItem.subjective_confidence : 1,
          skill_metrics: skillInputs
        });
      } else {
        await api.login(cleanEmail, cleanPassword);
      }
      onSuccess();
    } catch (err: any) {
      setErrorMessage(err.message || 'Authentication failed. Please check credentials or backend server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page-wrapper">
      <div className="login-container">
        {/* Decorative Top Accent Glow */}
        <div className="login-accent-glow" />

        <div className="glass-card login-card">
          {/* Header & Logo */}
          <div className="login-header">
            <div className="login-brand-icon">
              <Sparkles size={28} />
            </div>
            <div className="login-status-tag">
              <span className="login-status-dot" />
              <span>SDE Preparation Engine • Class of 2027</span>
            </div>
            <h1 className="login-title">CareerForge AI</h1>
            <p className="login-subtitle">
              Autonomous Career Intelligence, Adaptive 4-Hour Daily Curriculum & SDE Mastery
            </p>
          </div>

          {/* Mode Switcher Tabs */}
          <div className="login-tabs">
            <button
              type="button"
              className={`login-tab ${!isRegister ? 'active' : ''}`}
              onClick={() => {
                setIsRegister(false);
                setErrorMessage(null);
              }}
            >
              Sign In
            </button>
            <button
              type="button"
              className={`login-tab ${isRegister ? 'active' : ''}`}
              onClick={() => {
                setIsRegister(true);
                setErrorMessage(null);
              }}
            >
              Create Account
            </button>
          </div>

          {/* Error Banner */}
          {errorMessage && (
            <div className="login-error-banner" role="alert">
              <div className="login-error-text">{errorMessage}</div>
              {errorMessage.toLowerCase().includes('already exists') && (
                <button
                  type="button"
                  onClick={() => {
                    setIsRegister(false);
                    setErrorMessage(null);
                  }}
                  className="btn btn-sm btn-secondary"
                  style={{ marginTop: '0.5rem', width: '100%', fontSize: '0.75rem' }}
                >
                  Switch to Sign In with this Email
                </button>
              )}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="login-form">
            {isRegister && (
              <div className="form-group">
                <label className="form-label">
                  <User size={14} />
                  <span>Full Name</span>
                </label>
                <div className="input-with-icon">
                  <input
                    type="text"
                    className="form-input"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Alex Morgan"
                    required
                  />
                </div>
              </div>
            )}

            <div className="form-group">
              <label className="form-label">
                <Mail size={14} />
                <span>Email Address</span>
              </label>
              <div className="input-with-icon">
                <input
                  type="email"
                  className="form-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="student@university.edu"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="label-row">
                <label className="form-label">
                  <Lock size={14} />
                  <span>Password</span>
                </label>
              </div>
              <div className="input-with-icon password-input-wrap">
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  className="password-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {isRegister && (
              <>
                <div className="form-group">
                  <label className="form-label">
                    <GraduationCap size={14} />
                    <span>Degree & Department</span>
                  </label>
                  <input
                    type="text"
                    className="form-input"
                    value={degree}
                    onChange={(e) => setDegree(e.target.value)}
                    required
                  />
                </div>

                <div className="form-row-2">
                  <div className="form-group">
                    <label className="form-label">
                      <span>Graduation Year</span>
                    </label>
                    <input
                      type="number"
                      className="form-input"
                      value={graduationYear}
                      onChange={(e) => setGraduationYear(parseInt(e.target.value) || 2027)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">
                      <Clock size={14} />
                      <span>Study Hours/Day</span>
                    </label>
                    <input
                      type="number"
                      className="form-input"
                      min={1}
                      max={12}
                      value={studyHours}
                      onChange={(e) => setStudyHours(parseInt(e.target.value) || 4)}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">
                    <Briefcase size={14} />
                    <span>Target Roles</span>
                  </label>
                  <input
                    type="text"
                    className="form-input"
                    value={targetRoles}
                    onChange={(e) => setTargetRoles(e.target.value)}
                    placeholder="e.g. Software Development Engineer, AI Engineer"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">
                    <Briefcase size={14} />
                    <span>Target Companies</span>
                  </label>
                  <input
                    type="text"
                    className="form-input"
                    value={targetCompanies}
                    onChange={(e) => setTargetCompanies(e.target.value)}
                    placeholder="e.g. Zoho, TCS, Amazon, Google, PayPal"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">
                    <Sparkles size={14} />
                    <span>Your Projects / Portfolio</span>
                  </label>
                  <input
                    type="text"
                    className="form-input"
                    value={existingProjects}
                    onChange={(e) => setExistingProjects(e.target.value)}
                    placeholder="e.g. RAG Chatbot, Portfolio Web App"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">
                    <Target size={14} />
                    <span>Primary Career Goal</span>
                  </label>
                  <input
                    type="text"
                    className="form-input"
                    value={careerGoals}
                    onChange={(e) => setCareerGoals(e.target.value)}
                    placeholder="e.g. Tier-1 SDE Placement, Research & Academia"
                  />
                </div>

                {/* Baseline Skill Self-Evaluation */}
                <div style={{
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  marginTop: '0.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.85rem'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <label className="form-label" style={{ margin: 0, fontWeight: 700, fontSize: '0.85rem' }}>
                      <Zap size={14} style={{ color: 'var(--amber-500)' }} />
                      <span>Your Baseline Skill Metrics (%)</span>
                    </label>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      Adjust your starting proficiency
                    </span>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                    {skillInputs.map((sk, sidx) => {
                      const color = sk.measured_proficiency >= 70 ? 'var(--emerald-500)' : sk.measured_proficiency >= 50 ? 'var(--amber-500)' : 'var(--rose-500)';
                      return (
                        <div key={sk.topic} style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem' }}>
                            <span style={{ fontWeight: 600 }}>{sk.topic}</span>
                            <span>
                              <strong style={{ color }}>{sk.measured_proficiency}%</strong>
                              <span style={{ color: 'var(--text-muted)', marginLeft: '6px' }}>(Confidence: {sk.subjective_confidence}/5)</span>
                            </span>
                          </div>
                          <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '0.65rem', alignItems: 'center' }}>
                            <input
                              type="range"
                              min={0}
                              max={100}
                              value={sk.measured_proficiency}
                              onChange={(e) => {
                                const val = parseInt(e.target.value) || 0;
                                const updated = [...skillInputs];
                                updated[sidx].measured_proficiency = val;
                                updated[sidx].subjective_confidence = Math.max(1, Math.min(5, Math.ceil(val / 20)));
                                setSkillInputs(updated);
                              }}
                              style={{ width: '100%', accentColor: color }}
                            />
                            <div style={{ display: 'flex', gap: '2px' }}>
                              {[1, 2, 3, 4, 5].map((lvl) => (
                                <button
                                  key={lvl}
                                  type="button"
                                  onClick={() => {
                                    const updated = [...skillInputs];
                                    updated[sidx].subjective_confidence = lvl;
                                    setSkillInputs(updated);
                                  }}
                                  style={{
                                    width: '22px',
                                    height: '22px',
                                    borderRadius: '3px',
                                    border: '1px solid',
                                    borderColor: sk.subjective_confidence === lvl ? 'var(--indigo-500)' : 'var(--border-subtle)',
                                    background: sk.subjective_confidence === lvl ? 'var(--gradient-brand)' : 'transparent',
                                    color: sk.subjective_confidence === lvl ? '#fff' : 'var(--text-muted)',
                                    fontSize: '0.68rem',
                                    fontWeight: 700,
                                    cursor: 'pointer',
                                    padding: 0
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
              </>
            )}

            <button
              type="submit"
              className="btn btn-primary login-submit-btn"
              disabled={loading}
            >
              {loading ? (
                <span>Authenticating with Engine...</span>
              ) : isRegister ? (
                <>
                  <span>Create Account & Start Curriculum</span>
                  <ArrowRight size={18} />
                </>
              ) : (
                <>
                  <span>Sign In to CareerForge</span>
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          {/* Mode Switch Helper Card */}
          <div className="login-quick-card">
            <div className="quick-card-header">
              <span className="quick-badge">{isRegister ? 'New Student Registration' : 'Autonomous SDE Preparation'}</span>
            </div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', margin: '0.5rem 0 0.85rem 0', lineHeight: 1.5 }}>
              {isRegister
                ? 'Creating an account customizes your 4-hour daily curriculum, topic benchmarks (Python, SQL, DSA), mock interview simulator, and verified job tracker.'
                : 'Sign in with your registered email to continue your daily preparation sprint and track your SDE readiness.'}
            </p>
            <button
              type="button"
              onClick={() => {
                setIsRegister(!isRegister);
                setErrorMessage(null);
              }}
              className="quick-fill-btn"
              style={{ width: '100%', justifyContent: 'center', cursor: 'pointer' }}
            >
              <Zap size={14} />
              <span>{isRegister ? 'Already registered? Switch to Sign In' : 'New student? Create a New Account'}</span>
            </button>
          </div>

          {/* Server Config Accordion */}
          <div className="server-config-section">
            <button
              type="button"
              className="server-config-toggle"
              onClick={() => setShowServerConfig(!showServerConfig)}
            >
              <Server size={14} />
              <span>{showServerConfig ? 'Hide Backend Endpoint' : 'Backend Server Settings'}</span>
            </button>

            {showServerConfig && (
              <div className="server-config-box">
                <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    onClick={() => handleSelectServerPreset('http://localhost:8000/api/v1')}
                    className="btn btn-secondary btn-sm"
                    style={{ fontSize: '0.7rem', padding: '0.2rem 0.5rem' }}
                  >
                    Local (localhost:8000)
                  </button>
                  <button
                    type="button"
                    onClick={() => handleSelectServerPreset('https://careerforge-3s9a.onrender.com/api/v1')}
                    className="btn btn-secondary btn-sm"
                    style={{ fontSize: '0.7rem', padding: '0.2rem 0.5rem' }}
                  >
                    Cloud (Render live)
                  </button>
                </div>
                <label className="form-label">Active API Base URL:</label>
                <input
                  type="text"
                  className="form-input"
                  value={serverUrl}
                  onChange={(e) => setServerUrl(e.target.value)}
                  placeholder="http://localhost:8000/api/v1"
                />
                <div className="server-status-row">
                  <button
                    type="button"
                    onClick={() => testServerConnection()}
                    className="btn btn-secondary btn-sm"
                  >
                    Test & Save URL
                  </button>
                  {serverStatus && (
                    <span className="server-status-text">
                      {serverStatus}
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
