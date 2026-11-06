import React from 'react';
import {
  LayoutDashboard,
  Bot,
  Calendar,
  CheckCircle2,
  Code2,
  Database,
  Mic,
  Briefcase,
  FileText,
  TrendingUp,
  Settings,
  LogOut,
  Sparkles,
  X
} from 'lucide-react';
import { User } from '../types';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  currentUser: User | null;
  onLogout: () => void;
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  currentUser,
  onLogout,
  isOpen,
  onClose
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Main Dashboard', icon: LayoutDashboard },
    { id: 'coach', label: 'AI Career Coach', icon: Bot, badge: 'ADK' },
    { id: 'planner', label: 'Study Planner', icon: Calendar, badge: `${currentUser?.profile?.daily_study_hours || 4}h/day` },
    { id: 'assessment', label: 'Skill Assessment', icon: CheckCircle2 },
    { id: 'coding', label: 'Coding Practice', icon: Code2 },
    { id: 'sql', label: 'SQL Practice', icon: Database },
    { id: 'interview', label: 'Mock Interview', icon: Mic },
    { id: 'jobs', label: 'Job Tracker', icon: Briefcase },
    { id: 'resume', label: 'Resume & Projects', icon: FileText },
    { id: 'weekly', label: 'Weekly Review', icon: TrendingUp },
    { id: 'settings', label: 'Settings & Profile', icon: Settings },
  ];

  const degreeSnippet = currentUser?.profile?.degree
    ? `${currentUser.profile.degree.slice(0, 18)} • ${currentUser.profile.graduation_year || 2027}`
    : (currentUser?.profile?.graduation_year ? `Cohort of ${currentUser.profile.graduation_year}` : 'Autonomous Prep');

  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`} aria-label="Main Navigation">
      <div className="sidebar-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>
          <div className="brand-text">
            <h1>CareerForge AI</h1>
            <span>{degreeSnippet}</span>
          </div>
        </div>
        <button
          className="sidebar-close-btn"
          onClick={onClose}
          aria-label="Close navigation menu"
          title="Close Menu"
        >
          <X size={20} />
        </button>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Core Modules</div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-link ${isActive ? 'active' : ''}`}
              onClick={() => {
                setActiveTab(item.id);
                onClose();
              }}
              style={{ width: '100%', textAlign: 'left', background: 'none' }}
            >
              <Icon size={18} />
              <span>{item.label}</span>
              {item.badge && <span className="nav-badge">{item.badge}</span>}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="user-mini-card">
          <div className="user-avatar">
            {currentUser?.full_name ? currentUser.full_name[0].toUpperCase() : 'U'}
          </div>
          <div className="user-details">
            <div className="name">{currentUser?.full_name || 'Student'}</div>
            <div className="target">
              Target: {currentUser?.profile?.target_roles ? currentUser.profile.target_roles.split(' ')[0] : 'SDE'} {currentUser?.profile?.graduation_year || 2027}
            </div>
          </div>
        </div>
        <button
          onClick={onLogout}
          title="Sign Out"
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '6px'
          }}
        >
          <LogOut size={18} />
        </button>
      </div>
    </aside>
  );
};
