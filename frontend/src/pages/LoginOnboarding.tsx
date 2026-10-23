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
  Check
} from 'lucide-react';
import { api, getApiBase, setApiBase } from '../api/client';

interface LoginOnboardingProps {
  onSuccess: () => void;
}

export const LoginOnboarding: React.FC<LoginOnboardingProps> = ({ onSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('adhithian260506@gmail.com');
  const [password, setPassword] = useState('Adhi@2656');
  const [showPassword, setShowPassword] = useState(false);
  const [fullName, setFullName] = useState('Adhithian S');
  const [degree, setDegree] = useState('B.Tech Artificial Intelligence and Data Science');
  const [graduationYear, setGraduationYear] = useState(2027);
  const [studyHours, setStudyHours] = useState(4);
  const [targetCompanies, setTargetCompanies] = useState('Zoho, TCS, Amazon, Google, PayPal');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [showServerConfig, setShowServerConfig] = useState(false);
  const [serverUrl, setServerUrl] = useState(getApiBase());
  const [serverStatus, setServerStatus] = useState<string | null>(null);

  const testServerConnection = async () => {
    setServerStatus('Testing connection...');
    try {
      const cleanUrl = serverUrl.trim().replace(/\/+$/, '');
      setApiBase(cleanUrl);
      const res = await fetch(`${cleanUrl}/health`);
      if (res.ok) {
        setServerStatus('✅ Connected to CareerForge Backend (Healthy)');
      } else {
        setServerStatus(`⚠️ Server returned HTTP ${res.status}`);
      }
    } catch (e: any) {
      setServerStatus(`❌ Connection failed: ${e.message || 'Offline'}`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setLoading(true);

    try {
      if (isRegister) {
        await api.register({
          email: email.trim(),
          password,
          full_name: fullName.trim(),
          degree,
          graduation_year: graduationYear,
          daily_study_hours: studyHours,
          preferred_companies: targetCompanies,
          python_confidence: 3,
          sql_confidence: 3,
          dsa_confidence: 1
        });
      } else {
        await api.login(email.trim(), password);
      }
      onSuccess();
    } catch (err: any) {
      setErrorMessage(err.message || 'Authentication failed. Please check credentials or backend server.');
    } finally {
      setLoading(false);
    }
  };

  const fillAdhithianCredentials = () => {
    setIsRegister(false);
    setEmail('adhithian260506@gmail.com');
    setPassword('Adhi@2656');
    setErrorMessage(null);
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
              Student Onboarding
            </button>
          </div>

          {/* Error Banner */}
          {errorMessage && (
            <div className="login-error-banner" role="alert">
              <div className="login-error-text">{errorMessage}</div>
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
                    placeholder="Adhithian S"
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
                  placeholder="adhithian260506@gmail.com"
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
                    <span>Target Companies</span>
                  </label>
                  <input
                    type="text"
                    className="form-input"
                    value={targetCompanies}
                    onChange={(e) => setTargetCompanies(e.target.value)}
                    placeholder="Zoho, TCS, Amazon, Google, PayPal"
                  />
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

          {/* Quick Credential Card */}
          <div className="login-quick-card">
            <div className="quick-card-header">
              <span className="quick-badge">Verified Credentials</span>
              <button
                type="button"
                onClick={fillAdhithianCredentials}
                className="quick-fill-btn"
              >
                <Zap size={14} />
                <span>Auto-Fill Credentials</span>
              </button>
            </div>
            <div className="quick-info-row">
              <span className="quick-label">Email:</span>
              <span className="quick-value">adhithian260506@gmail.com</span>
            </div>
            <div className="quick-info-row">
              <span className="quick-label">Password:</span>
              <span className="quick-value">Adhi@2656</span>
            </div>
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
                    onClick={testServerConnection}
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
