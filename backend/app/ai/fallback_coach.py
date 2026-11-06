from typing import List, Dict, Any, Optional

def generate_fallback_coach_reply(
    message: str,
    user_profile: Optional[Dict[str, Any]] = None,
    skill_metrics: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Deterministic persona-rich fallback coach that responds with tailored, verified advice
    grounded in the student's actual profile and inputs.
    """
    lower_msg = message.lower()
    prof = user_profile or {}
    degree = prof.get("degree") or "Engineering"
    grad_year = prof.get("graduation_year") or 2027
    hours = prof.get("daily_study_hours") or 4
    target_role = prof.get("target_roles") or "Software Development Engineer"
    companies = prof.get("preferred_companies") or "Zoho, TCS, Amazon, Google, PayPal"
    first_company = [c.strip() for c in companies.split(",") if c.strip()][0] if companies else "Tier-1 Product Companies"
    projects = prof.get("existing_projects") or "Technical Portfolio Projects"
    goals = prof.get("career_goals") or "Industry Experience & Engineering Mastery"
    
    # Context summary
    dsa_metric = next((m for m in (skill_metrics or []) if m.get("topic") == "DSA"), None)
    dsa_score = f"{dsa_metric['measured_proficiency']:.1f}%" if dsa_metric else f"{prof.get('dsa_confidence', 1)}/5 subjective confidence (unassessed)"

    if any(k in lower_msg for k in ["dsa", "data structure", "algorithm", "leetcode"]):
        dsa_mins = max(30, int(hours * 60 * 0.35))
        reply = (
            "### 🎯 DSA Mastery Strategy (Your Highest Priority)\n\n"
            f"Your current DSA rating is **{dsa_score}**. With {hours} hours of daily study time and your {grad_year} {degree} graduation target, "
            f"we have sufficient runway if we build fundamental patterns systematically for your {target_role} bar.\n\n"
            "**Recommended Immediate Plan:**\n"
            "1. **Week 1-2**: Two Pointers & Sliding Window (Arrays and Strings). Master fast/slow pointers.\n"
            "2. **Week 3-4**: Hash Maps & Prefix Sums. Focus on complement lookups and frequency maps.\n"
            "3. **Week 5-6**: Binary Search on Sorted Arrays & Search Space reduction.\n"
            "4. **Week 7-8**: Linked Lists, Stacks & Monotonic Stack pattern.\n\n"
            f"💡 *Rule of thumb for your {hours}h daily split:* Dedicate **{dsa_mins} minutes** every single day exclusively to DSA. "
            "Spend 20 mins understanding the pattern, 40 mins implementing without peeking at solutions, and 15 mins analyzing Big-O time and auxiliary space."
        )
        actions = ["Open Coding Practice", "Take DSA Assessment", "Review Today's Study Tasks"]

    elif any(k in lower_msg for k in ["plan", "schedule", "routine", "time", "hours"]):
        dsa_mins = max(30, int(hours * 60 * 0.35))
        sql_mins = max(20, int(hours * 60 * 0.20))
        py_mins = max(20, int(hours * 60 * 0.20))
        cs_mins = max(20, int(hours * 60 * 0.15))
        proj_mins = max(15, int(hours * 60 * 0.10))
        reply = (
            f"### ⏱️ Your {hours}-Hour Daily Execution Protocol\n\n"
            f"Here is how your {hours} daily study hours are optimally apportioned to balance interview readiness for {target_role} with your {degree} coursework:\n\n"
            "| Time Slot | Module | Target Focus | Priority |\n"
            "| :--- | :--- | :--- | :--- |\n"
            f"| **{dsa_mins} mins** | **DSA Practice** | Arrays, Strings, HashMaps, Two Pointers | 🔴 Urgent |\n"
            f"| **{sql_mins} mins** | **SQL & Databases** | Multi-table JOINs, GROUP BY, Window Functions | 🟡 High |\n"
            f"| **{py_mins} mins** | **Python In-Depth** | OOP, Generators, Memory model, Concurrency | 🟡 High |\n"
            f"| **{cs_mins} mins** | **Core CS / Aptitude** | OS (Deadlocks/Paging), DBMS (ACID), Networks | 🟢 Medium |\n"
            f"| **{proj_mins} mins** | **Project & Job Prep** | Portfolio & Application Tracking | 🟢 Medium |\n\n"
            "⚠️ *Reminder:* Time spent is not proof of mastery. Focus on verified problem submissions in the sandbox and passing assessment benchmarks."
        )
        actions = ["View Study Planner", "Start Practice Session", "Log Study Hours"]

    elif any(k in lower_msg for k in ["project", "rag", "attendance", "facial", "portfolio"]):
        reply = (
            f"### 💼 Leveraging Your Projects for {target_role} Interviews\n\n"
            f"Your portfolio projects ({projects}) provide solid concrete discussion points for hiring rounds at {companies}.\n\n"
            "Here is how interviewers will probe these technical topics:\n\n"
            "**1. Core Architecture & System Design:**\n"
            "- *Trade-offs:* Why did you choose this architecture over simpler or distributed alternatives?\n"
            "- *Data Flow:* How does data enter the system, where is it transformed, and how is state cached?\n"
            "- *Production Scaling:* How would you handle 10,000 concurrent queries without latency spikes?\n\n"
            "**2. Reliability, Edge Cases & Verification:**\n"
            "- *Failure Modes:* What happens if third-party APIs or databases timeout during execution?\n"
            "- *Latency vs Accuracy:* What was the benchmark runtime or inference time per request?\n"
            "- *Security & Validation:* How do you sanitize untrusted inputs and prevent injections?"
        )
        actions = ["Generate Project Interview Qs", "Tailor Resume", "Start Mock Interview"]

    elif any(k in lower_msg for k in ["company", "zoho", "amazon", "google", "tcs", "paypal", "eligibility"]):
        reply = (
            f"### 🏢 Target Company Preparation Roadmap\n\n"
            f"Based on your target list ({companies}) for {target_role} roles ({grad_year} batch):\n\n"
            "1. **Primary Focus Employers**: Target recruiters looking for strong fundamentals in DSA, clean code architecture, and SQL query optimization.\n"
            "2. **Online Assessments**: High cutoff on Aptitude + Coding (2 problems within time limit) + Core CS (OS, DBMS, Networks).\n"
            "3. **Technical Interviews**: Systematic problem breakdown, code efficiency, edge case verification, and behavioral STAR stories.\n\n"
            "📌 *Current Action:* Keep tracking application dates in your **Job Application Tracker** and ensure all eligibility notes are verified before applying."
        )
        actions = ["Open Job Tracker", "Take Aptitude Assessment", "Practice SQL Sandbox"]

    elif any(k in lower_msg for k in ["professor", "academia", "phd", "mtech", "future", "career", "goal"]):
        reply = (
            f"### 🎓 Your Long-Term Roadmap: {goals}\n\n"
            f"Your strategy for transitioning through {target_role} industry experience towards {goals} is structured:\n\n"
            f"1. **Phase 1 ({grad_year} onwards): High-Performance Industry Engineer**\n"
            "   - Build production-grade systems, scalable APIs, and real-world pipelines.\n"
            "   - Establish financial independence, expand your engineering reputation, and lead technical deliverables.\n"
            "2. **Phase 2: Advanced Mastery & Leadership**\n"
            "   - Leverage your hands-on industry credentials for higher studies, technical publications, or senior engineering research.\n"
            "   - Your real-world background will make your expertise far more grounded, impactful, and competitive than theoretical candidates.\n\n"
            f"Right now, excelling in your placements before {grad_year} is step one to unlock this roadmap."
        )
        actions = ["View Dashboard", "Check Study Plan", "Assess Core CS"]

    else:
        reply = (
            f"Hello! I am your **CareerForge AI Coach**.\n\n"
            f"I'm calibrated specifically for your journey: securing a high-impact **{target_role}** role for your **{grad_year} {degree}** batch, "
            f"optimizing your **{hours} daily study hours**, and targeting **{companies}**.\n\n"
            "What would you like to focus on right now?\n"
            "- 📚 Review your **adaptive study plan for today**\n"
            "- 💻 Solve a **Python coding exercise** in the restricted sandbox\n"
            "- 🗄️ Query the **SQL sandbox** to master JOINs and GROUP BY\n"
            "- 🎯 Take a **Skill Assessment** to measure your true proficiency\n"
            f"- 🎙️ Run a **Mock Interview** simulation for {first_company}"
        )
        actions = ["Today's Study Plan", "Skill Assessment", "Coding Practice", "SQL Practice"]

    return {
        "reply": reply,
        "suggested_actions": actions,
        "agent_name": "Career Coach (ADK Persona)",
        "model_used": "Deterministic ADK Persona (Gemini Offline Fallback)"
    }
