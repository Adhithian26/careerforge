import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send, Sparkles, User as UserIcon, RefreshCw } from 'lucide-react';
import { api } from '../api/client';

export const AiCareerCoach: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'coach'; text: string; agent?: string }>>([
    {
      role: 'coach',
      text: `### 🎯 Greetings! I am your CareerForge AI Coach.\n\nI am configured for your exact goal: securing a Software Development Engineer role before your **2027 B.Tech AI & Data Science graduation**, optimizing your **4 daily study hours**, and leveling up your DSA (currently 1/5) and core competencies.\n\nHow can I accelerate your preparation today?`,
      agent: 'Career Coach (Google ADK / Gemini)'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [quickPrompts] = useState([
    "How should I split my 4 hours daily between DSA, Python, and SQL?",
    "Why is Two Pointers better than a brute force O(N^2) search on sorted arrays?",
    "What deep-dive questions will interviewers ask about my RAG Chatbot project?",
    "What are the specific technical rounds at Zoho vs Amazon SDE?",
    "How do I explain my long-term goal of industry experience leading to academia?"
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputValue;
    if (!text.trim() || loading) return;

    const userMsg = { role: 'user' as const, text };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setLoading(true);

    try {
      const historyPayload = messages.map(m => ({
        role: m.role === 'coach' ? 'model' : 'user',
        content: m.text
      }));

      const res = await api.chatWithCoach(text, historyPayload);
      setMessages(prev => [
        ...prev,
        {
          role: 'coach',
          text: res.reply,
          agent: `${res.agent_name} (${res.model_used})`
        }
      ]);
    } catch (err: any) {
      setMessages(prev => [
        ...prev,
        {
          role: 'coach',
          text: `⚠️ Error contacting agent: ${err.message || 'Unable to connect to AI server'}. Please ensure backend is running.`,
          agent: 'System'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-card" style={{ padding: '1.25rem 1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--gradient-brand)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              boxShadow: '0 4px 14px var(--indigo-glow)'
            }}>
              <Bot size={24} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>Career Coach Agent (Google ADK)</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Gemini Orchestrated • Context: B.Tech AI & DS '27 • 4h/day • SDE Placements
              </p>
            </div>
          </div>
          <span className="badge badge-success">Verified Evidence Policy Enforced</span>
        </div>
      </div>

      {/* Interactive Chat Pane */}
      <div className="chat-window">
        <div className="chat-messages">
          {messages.map((m, idx) => (
            <div key={idx} className={`chat-bubble ${m.role}`}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', marginBottom: '0.4rem', fontSize: '0.75rem', opacity: 0.8 }}>
                {m.role === 'coach' ? <Bot size={14} /> : <UserIcon size={14} />}
                <strong>{m.role === 'coach' ? (m.agent || 'Career Coach') : 'You'}</strong>
              </div>
              <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                {m.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="chat-bubble coach">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
                <RefreshCw size={14} className="animate-spin" />
                <span>Coach is analyzing your profile and formulating guidance...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestion Chips */}
        <div style={{
          padding: '0.65rem 1.25rem',
          background: 'rgba(11, 16, 28, 0.95)',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          gap: '0.5rem',
          overflowX: 'auto',
          whiteSpace: 'nowrap'
        }}>
          {quickPrompts.map((p, i) => (
            <button
              key={i}
              onClick={() => handleSendMessage(p)}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.75rem', padding: '0.35rem 0.75rem', flexShrink: 0 }}
            >
              <Sparkles size={12} style={{ color: 'var(--indigo-500)' }} />
              <span>{p}</span>
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="chat-input-bar">
          <input
            type="text"
            className="form-input"
            placeholder="Ask your coach about DSA roadmaps, interview tactics, or your 4h daily plan..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSendMessage();
            }}
            disabled={loading}
          />
          <button
            className="btn btn-primary"
            onClick={() => handleSendMessage()}
            disabled={loading || !inputValue.trim()}
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};
