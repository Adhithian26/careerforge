from typing import List, Dict, Any, Optional

def generate_fallback_coach_reply(
    message: str,
    user_profile: Optional[Dict[str, Any]] = None,
    skill_metrics: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Deterministic persona-rich fallback coach that responds with tailored, verified advice
    grounded in the student's profile:
    - B.Tech AI & Data Science (2027)
    - Python: 3/5, SQL: 3/5, DSA: 1/5
    - 4 hours daily study time
    - Goal: 2-4 years industry experience -> financial stability -> professorship
    """
    lower_msg = message.lower()
    
    # Context summary
    dsa_metric = next((m for m in (skill_metrics or []) if m.get("topic") == "DSA"), None)
    dsa_score = f"{dsa_metric['measured_proficiency']:.1f}%" if dsa_metric else "1/5 subjective confidence (unassessed)"

    if any(k in lower_msg for k in ["dsa", "data structure", "algorithm", "leetcode"]):
        reply = (
            "### 🎯 DSA Mastery Strategy (Your Highest Priority)\n\n"
            f"Your current DSA rating is **{dsa_score}**. With 4 hours of daily study time and a 2027 graduation target, "
            "we have sufficient runway if we build fundamental patterns systematically rather than jumping directly into hard problems.\n\n"
            "**Recommended Immediate Plan:**\n"
            "1. **Week 1-2**: Two Pointers & Sliding Window (Arrays and Strings). Master fast/slow pointers.\n"
            "2. **Week 3-4**: Hash Maps & Prefix Sums. Focus on complement lookups and frequency maps.\n"
            "3. **Week 5-6**: Binary Search on Sorted Arrays & Search Space reduction.\n"
            "4. **Week 7-8**: Linked Lists, Stacks & Monotonic Stack pattern.\n\n"
            "💡 *Rule of thumb for your 4h daily split:* Dedicate **75-80 minutes** every single day exclusively to DSA. "
            "Spend 20 mins understanding the pattern, 40 mins implementing without peeking at solutions, and 15 mins analyzing Big-O time and auxiliary space."
        )
        actions = ["Open Coding Practice", "Take DSA Assessment", "Review Today's Study Tasks"]

    elif any(k in lower_msg for k in ["plan", "schedule", "routine", "time", "hours"]):
        reply = (
            "### ⏱️ Your 4-Hour Daily Execution Protocol\n\n"
            "Here is how your 4 daily study hours are optimally apportioned to balance interview readiness with your academic coursework:\n\n"
            "| Time Slot | Module | Target Focus | Priority |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **75 mins** | **DSA Practice** | Arrays, Strings, HashMaps, Two Pointers | 🔴 Urgent |\n"
            "| **45 mins** | **SQL & Databases** | Multi-table JOINs, GROUP BY, Window Functions | 🟡 High |\n"
            "| **45 mins** | **Python In-Depth** | OOP, Generators, Memory model, Concurrency | 🟡 High |\n"
            "| **45 mins** | **Core CS / Aptitude** | OS (Deadlocks/Paging), DBMS (ACID), Networks | 🟢 Medium |\n"
            "| **30 mins** | **Project & Job Prep** | RAG Chatbot & Face Attendance architecture docs | 🟢 Medium |\n\n"
            "⚠️ *Reminder:* Time spent is not proof of mastery. Focus on verified problem submissions in the sandbox and passing assessment benchmarks."
        )
        actions = ["View Study Planner", "Start Practice Session", "Log Study Hours"]

    elif any(k in lower_msg for k in ["project", "rag", "attendance", "facial", "portfolio"]):
        reply = (
            "### 💼 Leveraging Your Existing Projects for SDE Interviews\n\n"
            "You already possess two impressive practical projects: **RAG Chatbot** and **Facial Recognition Attendance System**.\n\n"
            "Here is how interviewers at top companies (Zoho, Amazon, PayPal) will probe these:\n\n"
            "**1. RAG Chatbot Deep-Dive:**\n"
            "- *Chunking & Embeddings:* What chunk size and overlap did you use? Why?\n"
            "- *Vector Retrieval:* Did you evaluate cosine similarity vs dot product? How do you handle hallucination and context window overflow?\n"
            "- *Production Scaling:* How would you handle 10,000 concurrent queries without hitting LLM rate limits?\n\n"
            "**2. Facial Recognition Attendance System:**\n"
            "- *Edge Cases:* How does your model handle low-light conditions, camera angle shifts, or occlusion?\n"
            "- *Latency vs Accuracy:* What was the inference time per frame? Did you run on CPU or edge hardware?\n"
            "- *Security:* How do you prevent spoofing (e.g., holding up a smartphone photo)?"
        )
        actions = ["Generate Project Interview Qs", "Tailor Resume", "Start Mock Interview"]

    elif any(k in lower_msg for k in ["company", "zoho", "amazon", "google", "tcs", "paypal", "eligibility"]):
        reply = (
            "### 🏢 Target Company Preparation Roadmap\n\n"
            "Based on your target list (Zoho, TCS, Amazon, Google, PayPal, Tech Mahindra):\n\n"
            "1. **Zoho**: Emphasizes pure problem-solving without external libraries, C/Java/Python logic, Advanced Programming rounds (designing splitwise, railway reservation), and DBMS.\n"
            "2. **TCS (Digital / Prime)**: High cutoff on Aptitude + Coding (2 problems in 45 mins) + Core CS (OS, DBMS, CN).\n"
            "3. **Amazon & PayPal**: DSA (Medium/Hard graphs, trees, DP), clean OOP design, and Behavioral Leadership Principles (STAR method).\n\n"
            "📌 *Current Action:* Keep tracking application dates in your **Job Application Tracker** and ensure all eligibility notes (CGPA criteria, eligible batches) are verified before applying."
        )
        actions = ["Open Job Tracker", "Take Aptitude Assessment", "Practice SQL Sandbox"]

    elif any(k in lower_msg for k in ["professor", "academia", "phd", "mtech", "future", "career"]):
        reply = (
            "### 🎓 Your Long-Term Roadmap: SDE Industry Experience to Professorship\n\n"
            "Your dual-phase plan (2–4 years in software industry for financial stability, followed by academia) is exceptionally strong and respected:\n\n"
            "1. **Phase 1 (2027 - 2030): Industry Software Engineer**\n"
            "   - Build production-grade distributed systems, scalable APIs, and real-world AI pipelines.\n"
            "   - Establish financial independence, clear any educational obligations, and save for higher studies.\n"
            "2. **Phase 2 (2030+): Postgraduate & Doctorate Pathway**\n"
            "   - Prepare for GATE / GRE to enter premier research institutes (IITs, IISc, or top global universities).\n"
            "   - Your real-world engineering background will make your academic research far more grounded, impactful, and grant-worthy than theoretical-only candidates.\n\n"
            "Right now, excelling in your campus placements before 2027 is step one to unlock that entire future."
        )
        actions = ["View Dashboard", "Check Study Plan", "Assess Core CS"]

    else:
        reply = (
            "Hello! I am your **CareerForge AI Coach**.\n\n"
            "I'm calibrated specifically for your journey: securing a high-impact Software Development Engineer role before your **2027 B.Tech AI & Data Science graduation**, "
            "optimizing your **4 daily study hours**, and leveling up your DSA (currently at 1/5) and core competencies.\n\n"
            "What would you like to focus on right now?\n"
            "- 📚 Review your **adaptive study plan for today**\n"
            "- 💻 Solve a **Python coding exercise** in the restricted sandbox\n"
            "- 🗄️ Query the **SQL sandbox** to master JOINs and GROUP BY\n"
            "- 🎯 Take a **Skill Assessment** to measure your true proficiency\n"
            "- 🎙️ Run a **Mock Interview** simulation for Zoho or Amazon"
        )
        actions = ["Today's Study Plan", "Skill Assessment", "Coding Practice", "SQL Practice"]

    return {
        "reply": reply,
        "suggested_actions": actions,
        "agent_name": "Career Coach (ADK Persona)",
        "model_used": "Deterministic ADK Persona (Gemini Offline Fallback)"
    }
