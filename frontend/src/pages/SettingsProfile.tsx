import React, { useState, useEffect } from 'react';
import { Settings, Save, ShieldCheck, AlertTriangle, CheckCircle2, User, Key } from 'lucide-react';
import { api } from '../api/client';
import { UserProfile } from '../types';

export const SettingsProfile: React.FC = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await api.getProfile();
      setProfile(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!profile) return;
    try {
      setSaving(true);
      await api.updateProfile(profile);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading || !profile) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <p>Loading profile configurations...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div className="glass-card">
        <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '0.25rem' }}>
          Academic & Career Profile Configuration
        </h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
          Calibrates the Google ADK AI Coach and the 4-Hour Study Planner.
        </p>
      </div>

      <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        {/* Academic Degree & Target Year */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', color: 'var(--indigo-500)' }}>
            Academic Profile
          </h4>
          <div className="grid-2">
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Degree & Major:
              </label>
              <input
                type="text"
                className="form-input"
                value={profile.degree}
                onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
                required
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Target Graduation Year:
              </label>
              <input
                type="number"
                className="form-input"
                value={profile.graduation_year}
                onChange={(e) => setProfile({ ...profile, graduation_year: parseInt(e.target.value) || 2027 })}
                required
              />
            </div>
          </div>

          <div style={{ marginTop: '1rem' }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
              Daily Study Time Available (Hours):
            </label>
            <input
              type="number"
              className="form-input"
              min={1}
              max={12}
              value={profile.daily_study_hours}
              onChange={(e) => setProfile({ ...profile, daily_study_hours: parseInt(e.target.value) || 4 })}
              required
            />
          </div>
        </div>

        {/* Target Roles & Companies */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', color: 'var(--emerald-500)' }}>
            Placement Targets
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Target Job Roles:
              </label>
              <input
                type="text"
                className="form-input"
                value={profile.target_roles}
                onChange={(e) => setProfile({ ...profile, target_roles: e.target.value })}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Target Companies:
              </label>
              <input
                type="text"
                className="form-input"
                value={profile.preferred_companies}
                onChange={(e) => setProfile({ ...profile, preferred_companies: e.target.value })}
              />
            </div>
          </div>
        </div>

        {/* Subjective Confidence (1-5) */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--amber-500)' }}>
            Subjective Confidence Ratings (1 to 5)
          </h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Your self-assessment. (DSA is calibrated at 1/5 to ensure intensive array/pointer focus).
          </p>

          <div className="grid-3">
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                DSA Confidence: {profile.dsa_confidence}/5
              </label>
              <input
                type="range"
                min={1}
                max={5}
                value={profile.dsa_confidence}
                onChange={(e) => setProfile({ ...profile, dsa_confidence: parseInt(e.target.value) })}
                style={{ width: '100%', accentColor: 'var(--indigo-500)' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                Python Confidence: {profile.python_confidence}/5
              </label>
              <input
                type="range"
                min={1}
                max={5}
                value={profile.python_confidence}
                onChange={(e) => setProfile({ ...profile, python_confidence: parseInt(e.target.value) })}
                style={{ width: '100%', accentColor: 'var(--emerald-500)' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                SQL Confidence: {profile.sql_confidence}/5
              </label>
              <input
                type="range"
                min={1}
                max={5}
                value={profile.sql_confidence}
                onChange={(e) => setProfile({ ...profile, sql_confidence: parseInt(e.target.value) })}
                style={{ width: '100%', accentColor: 'var(--cyan-500)' }}
              />
            </div>
          </div>
        </div>

        {/* Existing Projects & Long-term Objective */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem' }}>
            Projects & Long-Term Career Vision
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Existing Portfolio Projects:
              </label>
              <input
                type="text"
                className="form-input"
                value={profile.existing_projects}
                onChange={(e) => setProfile({ ...profile, existing_projects: e.target.value })}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Long-Term Objective:
              </label>
              <textarea
                className="form-textarea"
                rows={3}
                value={profile.career_goals}
                onChange={(e) => setProfile({ ...profile, career_goals: e.target.value })}
              />
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '1rem' }}>
          {saveSuccess && (
            <div style={{ color: 'var(--emerald-500)', fontSize: '0.88rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <CheckCircle2 size={16} /> Profile settings updated successfully!
            </div>
          )}
          <button type="submit" className="btn btn-primary" disabled={saving}>
            <Save size={16} /> {saving ? 'Saving...' : 'Save Profile Changes'}
          </button>
        </div>
      </form>

      {/* Security & Data Deletion Workflow */}
      <div className="glass-card" style={{ borderColor: 'rgba(244, 63, 94, 0.25)', background: 'rgba(244, 63, 94, 0.03)' }}>
        <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--rose-500)', marginBottom: '0.5rem' }}>
          Privacy Notice & Data Security
        </h4>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          All your assessment scores, coding submissions, SQL queries, and job applications are protected by user-level authorization checks.
          Your credentials and API keys are stored exclusively in environment variables and never exposed to client browsers or committed to Git.
        </p>
      </div>
    </div>
  );
};
