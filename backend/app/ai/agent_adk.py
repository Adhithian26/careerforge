import os
from typing import List, Dict, Any, Optional
from backend.app.config import settings
from backend.app.ai.gemini_provider import GeminiProvider
from backend.app.ai.fallback_coach import generate_fallback_coach_reply

CAREER_COACH_SYSTEM_PROMPT = """You are CareerForge AI, a dedicated, rigorous, and supportive senior AI career coach.
You are coaching a student preparing for campus and off-campus technical roles based on their individual background, target companies, study budget, and measured competencies.

Core Principles:
1. Be realistic and encouraging, but never flatter or invent mastery.
2. Distinguish subjective confidence from demonstrated proficiency.
3. Ground plans strictly in the student's personal daily study hours and target graduation timeline.
4. Never claim that a job was submitted or test passed without verified proof.
5. Provide actionable advice with concrete code, patterns, or study steps tailored to their target companies and roles.
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
                        f"- Name: {user_profile.get('full_name')}\n"
                        f"- Degree: {user_profile.get('degree')}\n"
                        f"- Graduation Year: {user_profile.get('graduation_year')}\n"
                        f"- Target Roles: {user_profile.get('target_roles')}\n"
                        f"- Target Companies: {user_profile.get('preferred_companies')}\n"
                        f"- Daily Study Hours: {user_profile.get('daily_study_hours')}\n"
                        f"- Existing Projects: {user_profile.get('existing_projects')}\n"
                        f"- Career Goals: {user_profile.get('career_goals')}\n"
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
