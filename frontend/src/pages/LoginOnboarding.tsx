import React, { useState } from 'react';
import { Sparkles, ArrowRight, ShieldCheck, CheckCircle2, User, Lock, Mail } from 'lucide-react';
import { api } from '../api/client';

interface LoginOnboardingProps {
  onSuccess: () => void;
}

export const LoginOnboarding: React.FC<LoginOnboardingProps> = ({ onSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('student@careerforge.ai');
  const [password, setPassword] = useState('CareerForge2027!');
  const [fullName, setFullName] = useState('Adhithian S');
  const [degree, setDegree] = useState('B.Tech Artificial Intelligence and Data Science');
  const [graduationYear, setGraduationYear] = useState(2027);
  const [studyHours, setStudyHours] = useState(4);
  const [targetCompanies, setTargetCompanies] = useState('Zoho, TCS, Amazon, Google, PayPal');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setLoading(true);

    try {
      if (isRegister) {
        await api.register({
          email,
          password,
          full_name: fullName,
          degree,
          graduation_year: graduationYear,
          daily_study_hours: studyHours,
          preferred_companies: targetCompanies,
          python_confidence: 3,
          sql_confidence: 3,
          dsa_confidence: 1
        });
      } else {
        await api.login(email, password);
      }
      onSuccess();
    } catch (err: any) {
      setErrorMessage(err.message || 'Authentication error.');
    } finally {
      setLoading(false);
    }
  };

  const fillDefaultPersonalAccount = () => {
    setIsRegister(false);
    setEmail('student@careerforge.ai');
    setPassword('CareerForge2027!');
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem',
      background: 'radial-gradient(circle at 50% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 60%), #090d16'
    }}>
      <div className="glass-card" style={{ width: '100%', maxWidth: '520px', padding: '2.5rem', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
        {/* Brand Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '52px',
            height: '52px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--gradient-brand)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            margin: '0 auto 1rem',
            boxShadow: '0 6px 20px var(--indigo-glow)'
          }}>
            <Sparkles size={28} />
          </div>
          <h1 style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            CareerForge AI
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', marginTop: '0.25rem' }}>
            Autonomous Career Intelligence & SDE Preparation Engine
          </p>
        </div>

        {errorMessage && (
          <div style={{
            padding: '0.85rem 1rem',
            background: 'rgba(244, 63, 94, 0.12)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            borderRadius: 'var(--radius-sm)',
            color: '#fca5a5',
            fontSize: '0.85rem',
            marginBottom: '1.25rem'
          }}>
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {isRegister && (
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Full Name
              </label>
              <input
                type="text"
                className="form-input"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </div>
          )}

          <div>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
              Email Address
            </label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
              Password
            </label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {isRegister && (
            <>
              <div>
                <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                  Degree & Specialization
                </label>
                <input
                  type="text"
                  className="form-input"
                  value={degree}
                  onChange={(e) => setDegree(e.target.value)}
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                    Graduation Year
                  </label>
                  <input
                    type="number"
                    className="form-input"
                    value={graduationYear}
                    onChange={(e) => setGraduationYear(parseInt(e.target.value) || 2027)}
                    required
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                    Daily Study Hours
                  </label>
                  <input
                    type="number"
                    className="form-input"
                    min={1}
                    max={10}
                    value={studyHours}
                    onChange={(e) => setStudyHours(parseInt(e.target.value) || 4)}
                    required
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                  Target Companies
                </label>
                <input
                  type="text"
                  className="form-input"
                  value={targetCompanies}
                  onChange={(e) => setTargetCompanies(e.target.value)}
                />
              </div>
            </>
          )}

          <button type="submit" className="btn btn-primary" style={{ marginTop: '0.75rem', width: '100%', padding: '0.8rem' }} disabled={loading}>
            {loading ? 'Authenticating...' : isRegister ? 'Complete Onboarding & Enter' : 'Sign In to CareerForge'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          <button
            onClick={() => setIsRegister(!isRegister)}
            style={{ background: 'none', border: 'none', color: 'var(--indigo-500)', fontSize: '0.85rem', cursor: 'pointer', fontWeight: 600 }}
          >
            {isRegister ? 'Already have a profile? Sign In' : 'Need a new student profile? Register here'}
          </button>
        </div>

        {/* Quick Personal Access Button */}
        <div style={{ marginTop: '1.25rem', paddingTop: '1.25rem', borderTop: '1px solid var(--border-subtle)', textAlign: 'center' }}>
          <button
            onClick={fillDefaultPersonalAccount}
            className="btn btn-secondary btn-sm"
            style={{ width: '100%', fontSize: '0.78rem' }}
          >
            Use Default Profile: student@careerforge.ai
          </button>
        </div>
      </div>
    </div>
  );
};
