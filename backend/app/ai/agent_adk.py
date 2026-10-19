import os
from typing import List, Dict, Any, Optional
from backend.app.config import settings
from backend.app.ai.gemini_provider import GeminiProvider
from backend.app.ai.fallback_coach import generate_fallback_coach_reply

CAREER_COACH_SYSTEM_PROMPT = """You are CareerForge AI, a dedicated, rigorous, and supportive senior AI career coach.
You are coaching a student preparing for campus and off-campus Software Development Engineer (SDE) roles:
- Degree: B.Tech Artificial Intelligence and Data Science (graduating 2027).
- Python confidence: 3/5.
- SQL confidence: 3/5.
- DSA confidence: 1/5 (Requires systematic focus on arrays, two pointers, sliding window, and basic patterns).
- Available study time: 4 hours daily.
- Target companies: Zoho, TCS, Amazon, Google, PayPal, Tech Mahindra.
- Existing projects: RAG chatbot and facial recognition attendance system.
- Long-term goal: 2-4 years industry software engineering experience to build financial stability, followed by academia (Ph.D. / Professorship).

Core Principles:
1. Be realistic and encouraging, but never flatter or invent mastery.
2. Distinguish subjective confidence from demonstrated proficiency.
3. Ground plans in the student's 4-hour daily budget.
4. Never claim that a job was submitted or test passed without verified proof.
5. Provide actionable advice with concrete code or study steps.
"""

class CareerCoachOrchestrator:
    """
    Orchestrates Google ADK Agents and Gemini Model Providers
    with seamless graceful degradation.
    """
    def __init__(self):
        self.provider = GeminiProvider()
        self.adk_agent = None
        self._init_adk()

    def _init_adk(self):
        """Attempts to initialize Google ADK Agent if Gemini API key is configured."""
        if self.provider.is_configured():
            try:
                from google.adk import Agent
                self.adk_agent = Agent(
                    name="career_coach",
                    model=settings.GEMINI_MODEL,
                    instruction=CAREER_COACH_SYSTEM_PROMPT
                )
            except Exception:
                self.adk_agent = None

    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        skill_metrics: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Processes a chat interaction. If Gemini API is available and succeeds, returns live LLM response.
        Otherwise degrades gracefully to the deterministic persona coach.
        """
        # If configured, attempt Gemini API call
        if self.provider.is_configured():
            try:
                messages = list(conversation_history or [])
                messages.append({"role": "user", "content": message})
                
                # Context enrichment
                profile_context = ""
                if user_profile:
                    profile_context = (
                        f"\nStudent Profile:\n"
                        f"- Degree: {user_profile.get('degree')}\n"
                        f"- Graduation: {user_profile.get('graduation_year')}\n"
                        f"- Daily Study Hours: {user_profile.get('daily_study_hours')}\n"
                        f"- Confidence: Python={user_profile.get('python_confidence')}/5, SQL={user_profile.get('sql_confidence')}/5, DSA={user_profile.get('dsa_confidence')}/5\n"
                    )

                full_instruction = CAREER_COACH_SYSTEM_PROMPT + profile_context
                reply_text = self.provider.generate_chat_reply(
                    messages=messages,
                    system_instruction=full_instruction
                )
                
                return {
                    "reply": reply_text,
                    "suggested_actions": ["Review Study Plan", "Solve Coding Problem", "Take Skill Assessment"],
                    "agent_name": "Career Coach (Google ADK / Gemini)",
                    "model_used": settings.GEMINI_MODEL
                }
            except Exception as e:
                # Log or handle error, fall back seamlessly
                print(f"[CareerCoach] Gemini call failed, utilizing ADK persona fallback: {e}")

        # Fallback to rich deterministic persona coach
        return generate_fallback_coach_reply(
            message=message,
            user_profile=user_profile,
            skill_metrics=skill_metrics
        )

# Global singleton
coach_orchestrator = CareerCoachOrchestrator()
