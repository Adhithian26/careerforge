import React from 'react';
import { Menu, Clock, Sun, Moon, Bell, CheckCircle } from 'lucide-react';
import { User } from '../types';

interface HeaderProps {
  activeTab: string;
  onToggleSidebar: () => void;
  currentUser: User | null;
  isLightTheme: boolean;
  onToggleTheme: () => void;
}

const PAGE_TITLES: Record<string, { title: string; subtitle: string }> = {
  dashboard: { title: 'Career Intelligence Dashboard', subtitle: 'Real-time performance, today\'s plan, and skill matrix' },
  coach: { title: 'AI Career Coach', subtitle: 'Google ADK conversational agent powered by Gemini' },
  planner: { title: '4-Hour Adaptive Study Planner', subtitle: 'Curated 7-day preparation schedule tailored to your weak areas' },
  assessment: { title: 'Skill Assessment Engine', subtitle: 'Topic-wise benchmarks distinguishing confidence from measured proficiency' },
  coding: { title: 'Python Coding Sandbox', subtitle: 'Isolated deterministic execution environment with AST safety' },
  sql: { title: 'SQL Relational Sandbox', subtitle: 'Query evaluator on departments, employees, and academic schemas' },
  interview: { title: 'Mock Interview Simulator', subtitle: 'Multi-round technical, HR, and project interviews with scoring rubrics' },
  jobs: { title: 'Job Application Tracker', subtitle: 'Verified openings from permitted employer portals & application stages' },
  resume: { title: 'Resume & Project Assistant', subtitle: 'JD keyword alignment & deep-dive project interview questions' },
  weekly: { title: 'Weekly Progress Review', subtitle: 'Verified completion rates, weakness deep-dive, and 3 priorities' },
  settings: { title: 'Profile & Settings', subtitle: 'Academic degree, graduation year, target roles, and credentials' }
};

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  onToggleSidebar,
  currentUser,
  isLightTheme,
  onToggleTheme
}) => {
  const info = PAGE_TITLES[activeTab] || { title: 'CareerForge AI', subtitle: 'Autonomous Career Preparation' };

  return (
    <header className="top-header">
      <div className="header-left">
        <button className="mobile-menu-btn" onClick={onToggleSidebar} aria-label="Toggle Navigation">
          <Menu size={20} />
        </button>
        <div>
          <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            {info.title}
          </h2>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            {info.subtitle}
          </p>
        </div>
      </div>

      <div className="header-right">
        <div className="header-metric-pill" title="Daily study time budget">
          <Clock size={15} style={{ color: 'var(--indigo-500)' }} />
          <span>4h Daily Allocation</span>
        </div>

        <div className="header-metric-pill" title="Verified Target Graduation">
          <CheckCircle size={15} style={{ color: 'var(--emerald-500)' }} />
          <span>2027 SDE Track</span>
        </div>

        <button
          onClick={onToggleTheme}
          className="btn btn-secondary btn-sm"
          style={{ padding: '0.45rem', borderRadius: '50%' }}
          title={isLightTheme ? "Switch to Dark Mode" : "Switch to Light Mode"}
        >
          {isLightTheme ? <Moon size={16} /> : <Sun size={16} />}
        </button>
      </div>
    </header>
  );
};
