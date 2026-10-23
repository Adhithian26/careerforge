import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { AiCareerCoach } from './pages/AiCareerCoach';
import { StudyPlanner } from './pages/StudyPlanner';
import { SkillAssessment } from './pages/SkillAssessment';
import { CodingPractice } from './pages/CodingPractice';
import { SqlPractice } from './pages/SqlPractice';
import { MockInterview } from './pages/MockInterview';
import { JobTracker } from './pages/JobTracker';
import { ResumeAssistant } from './pages/ResumeAssistant';
import { WeeklyReview } from './pages/WeeklyReview';
import { SettingsProfile } from './pages/SettingsProfile';
import { LoginOnboarding } from './pages/LoginOnboarding';
import { api, authStorage } from './api/client';
import { User } from './types';

export const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(false);
  const [isLightTheme, setIsLightTheme] = useState<boolean>(false);
  const [initializing, setInitializing] = useState<boolean>(true);

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (sidebarOpen) {
      document.body.classList.add('sidebar-open-locked');
    } else {
      document.body.classList.remove('sidebar-open-locked');
    }
    return () => {
      document.body.classList.remove('sidebar-open-locked');
    };
  }, [sidebarOpen]);

  const checkAuth = async () => {
    const token = authStorage.getToken();
    if (token) {
      try {
        const user = await api.getMe();
        setCurrentUser(user);
        setIsAuthenticated(true);
      } catch {
        authStorage.clearToken();
        setIsAuthenticated(false);
      }
    } else {
      setIsAuthenticated(false);
    }
    setInitializing(false);
  };

  const handleLogout = () => {
    authStorage.clearToken();
    setIsAuthenticated(false);
    setCurrentUser(null);
  };

  const toggleTheme = () => {
    setIsLightTheme(prev => {
      const next = !prev;
      if (next) {
        document.body.classList.add('light-theme');
      } else {
        document.body.classList.remove('light-theme');
      }
      return next;
    });
  };

  if (initializing) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#090d16', color: '#94a3b8' }}>
        <p>Connecting to CareerForge AI Engine...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginOnboarding onSuccess={() => checkAuth()} />;
  }

  return (
    <div className="app-container">
      {/* Mobile Slide Navigation Backdrop */}
      <div
        className={`sidebar-backdrop ${sidebarOpen ? 'active' : ''}`}
        onClick={() => setSidebarOpen(false)}
        aria-hidden={!sidebarOpen}
      />

      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentUser={currentUser}
        onLogout={handleLogout}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="main-content">
        <Header
          activeTab={activeTab}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          currentUser={currentUser}
          isLightTheme={isLightTheme}
          onToggleTheme={toggleTheme}
        />

        <main className="content-body">
          {activeTab === 'dashboard' && <Dashboard onNavigate={setActiveTab} />}
          {activeTab === 'coach' && <AiCareerCoach />}
          {activeTab === 'planner' && <StudyPlanner />}
          {activeTab === 'assessment' && <SkillAssessment />}
          {activeTab === 'coding' && <CodingPractice />}
          {activeTab === 'sql' && <SqlPractice />}
          {activeTab === 'interview' && <MockInterview />}
          {activeTab === 'jobs' && <JobTracker />}
          {activeTab === 'resume' && <ResumeAssistant />}
          {activeTab === 'weekly' && <WeeklyReview />}
          {activeTab === 'settings' && <SettingsProfile />}
        </main>
      </div>
    </div>
  );
};

export default App;
