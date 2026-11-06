import json
import re
from typing import List, Dict, Any, Set, Optional
from backend.app.ai.gemini_provider import GeminiProvider

_gemini_resume = GeminiProvider()

COMMON_TECH_SKILLS = [
    "python", "sql", "dsa", "data structures", "algorithms", "fastapi", "react", "typescript",
    "postgresql", "sqlite", "docker", "git", "rest", "api", "oop", "dbms", "operating systems",
    "computer networks", "rag", "retrieval augmented generation", "llm", "embeddings", "vector database",
    "opencv", "computer vision", "machine learning", "deep learning", "pandas", "numpy",
    "linux", "ci/cd", "cloud run", "gcp", "aws", "unit testing", "pytest"
]

PROJECT_QUESTIONS_CATALOG = {
    "rag": {
        "architecture_questions": [
            "What embedding model did you choose for your RAG chatbot, and how did you benchmark its semantic similarity against technical domain queries?",
            "How did you design the text chunking strategy (fixed size, recursive character, or semantic split) to avoid cutting context mid-concept?",
            "What vector indexing algorithm (HNSW, IVFFlat, Flat) did you configure in your vector store, and how does it balance recall vs query latency?"
        ],
        "deep_dive_questions": [
            "How do you handle out-of-domain queries or hallucination when the retriever returns chunks with low similarity scores?",
            "Did you implement re-ranking (e.g. cross-encoders) after the initial vector retrieval stage? If so, what was the latency impact?"
        ],
        "tradeoff_challenges": [
            "In a production system with 5,000 queries/minute, how would you cache frequent semantic questions to minimize LLM token costs?"
        ],
        "recommended_talking_points": [
            "Explain your context window optimization and metadata filtering strategy.",
            "Quantify retrieval latency (e.g. sub-100ms vector search) and context relevance."
        ]
    },
    "attendance": {
        "architecture_questions": [
            "Which face detection and feature extraction pipeline (e.g. MTCNN, MediaPipe, FaceNet, Dlib) did you implement in your attendance system?",
            "How does your system store facial embeddings securely, and how do you prevent vector template inversion attacks?"
        ],
        "deep_dive_questions": [
            "How does the model handle extreme lighting variations, angled poses, or medical face masks in real-world classrooms?",
            "What Euclidean distance or cosine threshold did you set to balance False Acceptance Rate (FAR) against False Rejection Rate (FRR)?"
        ],
        "tradeoff_challenges": [
            "How did you prevent photo/video spoofing attacks (e.g., student holding up a picture on a smartphone)? Did you implement liveness detection?"
        ],
        "recommended_talking_points": [
            "Emphasize the end-to-end pipeline: camera stream capture -> landmark detection -> embedding generation -> database match -> attendance timestamp log."
        ]
    }
}

def analyze_resume_alignment(
    resume_text: str,
    job_description: str,
    target_role: str = "Software Development Engineer"
) -> Dict[str, Any]:
    """
    Analyzes resume text against a job description deterministically.
    Never fabricates experiences, credentials, or achievements.
    """
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()

    # Find which tech skills are mentioned in the JD
    jd_skills = set()
    for skill in COMMON_TECH_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, jd_lower):
            jd_skills.add(skill)

    if not jd_skills:
        # Default baseline expectations for SDE
        jd_skills = {"python", "sql", "dsa", "git", "rest", "oop", "dbms"}

    # Determine matched vs missing
    matched = []
    missing_critical = []
    missing_bonus = []

    for skill in sorted(jd_skills):
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, resume_lower):
            matched.append(skill.upper() if len(skill) <= 4 else skill.title())
        else:
            formatted = skill.upper() if len(skill) <= 4 else skill.title()
            if skill in ["python", "sql", "dsa", "git", "oop", "dbms"]:
                missing_critical.append(formatted)
            else:
                missing_bonus.append(formatted)

    total_jd = len(jd_skills)
    matched_count = len(matched)
    match_percentage = round((matched_count / total_jd * 100), 1) if total_jd > 0 else 100.0

    # Concrete bullet point recommendations
    bullet_recommendations = [
        "Include concrete metrics: Instead of 'Built RAG chatbot', write 'Engineered RAG pipeline with FastAPI and vector embeddings, reducing response latency by 35% across 200+ test queries.'",
        "Highlight deterministic testing: Instead of 'Implemented attendance system', write 'Developed facial recognition attendance module achieving 96% accuracy on classroom benchmarks with anti-spoofing checks.'",
        "Emphasize production readiness: Detail data persistence, schema design, and Docker deployment on Google Cloud Run."
    ]

    action_items = []
    if missing_critical:
        action_items.append(f"Explicitly mention your project usage of: {', '.join(missing_critical)}.")
    if missing_bonus:
        action_items.append(f"Consider exploring or documenting foundational knowledge of: {', '.join(missing_bonus)}.")
    action_items.append("Format resume with standard one-column ATS-friendly layout avoiding multi-column tables or graphics.")

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_critical_skills": missing_critical,
        "missing_bonus_skills": missing_bonus,
        "recommended_bullet_points": bullet_recommendations,
        "action_items": action_items
    }

def get_project_interview_prep(
    project_title: str,
    project_description: Optional[str] = None,
    tech_stack: Optional[str] = None
) -> Dict[str, Any]:
    """Generates rigorous technical interview questions tailored to the student's actual projects."""
    p_lower = project_title.lower()

    # Attempt AI-powered tailored question generation via Gemini if configured
    if _gemini_resume.is_configured():
        try:
            prompt = f"""Generate technical interview prep questions for an SDE candidate presenting this project:
Project Title: {project_title}
Project Description: {project_description or 'Software engineering project'}
Tech Stack: {tech_stack or 'Python, REST APIs, Databases'}

Respond with ONLY a valid JSON object matching this schema:
{{
  "architecture_questions": ["q1", "q2", "q3"],
  "deep_dive_questions": ["q1", "q2"],
  "tradeoff_challenges": ["q1"],
  "recommended_talking_points": ["point 1", "point 2"]
}}
Do NOT output markdown code fences or other text."""
            raw = _gemini_resume.generate_text(prompt=prompt, system_instruction="You are a senior technical interviewer at top tech firms.").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            parsed = json.loads(raw)
            if all(k in parsed for k in ["architecture_questions", "deep_dive_questions", "tradeoff_challenges", "recommended_talking_points"]):
                return parsed
        except Exception:
            pass

    # Deterministic catalog fallback
    if "rag" in p_lower or "chat" in p_lower or "retrieval" in p_lower:
        return PROJECT_QUESTIONS_CATALOG["rag"]
    elif "face" in p_lower or "attend" in p_lower or "vision" in p_lower:
        return PROJECT_QUESTIONS_CATALOG["attendance"]
    else:
        # Combined project question suite
        return {
            "architecture_questions": [
                f"What was the high-level system architecture of '{project_title}'? Walk me through how data flows from input to persistent output.",
                f"How did you modularize the frontend, backend API, and database layers in {project_title}?"
            ],
            "deep_dive_questions": [
                "What was the most challenging technical bug or bottleneck you encountered during implementation, and how did you isolate it?",
                "How did you validate correctness and ensure security across API endpoints?"
            ],
            "tradeoff_challenges": [
                "If you had to scale this application from 100 users to 100,000 users, what would break first?"
            ],
            "recommended_talking_points": [
                "Structure answers using the STAR method (Situation, Task, Action, Result).",
                "Quantify results with real measured numbers (response times, error reduction, test coverage)."
            ]
        }

def enhance_resume_bullet(
    raw_bullet: str,
    project_context: Optional[str] = None,
    target_role: Optional[str] = "Software Development Engineer"
) -> Dict[str, Any]:
    """
    Transforms passive college resume bullet points into Google XYZ-formula bullet points:
    'Accomplished [X], as measured by [Y], by doing [Z]'.
    """
    raw_clean = raw_bullet.strip()
    if not raw_clean:
        raw_clean = "Built a web application for user management"

    # AI-assisted rewrite if Gemini is enabled
    if _gemini_resume.is_configured():
        try:
            prompt = f"""You are a senior tech recruiter and engineering manager at Google/Amazon.
Rewrite this candidate's raw resume bullet point using Google's XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]'.
Target Role: {target_role}
Project Context: {project_context or 'Computer science software project'}
Raw Bullet Point: "{raw_clean}"

Return ONLY a JSON object matching this schema:
{{
  "critique": "Brief 1-2 sentence critique explaining why the original was weak.",
  "variants": [
    {{
      "label": "Metric & Impact-Driven (Google XYZ Formula)",
      "bullet": "Accomplished X, as measured by Y, by doing Z",
      "impact_focus": "Quantified efficiency and user throughput",
      "action_verb": "Engineered"
    }},
    {{
      "label": "System Architecture & Scale",
      "bullet": "Architected modular Z, reducing system latency by Y and supporting X",
      "impact_focus": "System modularity and latency reduction",
      "action_verb": "Architected"
    }},
    {{
      "label": "Code Reliability & Production Rigor",
      "bullet": "Designed robust Z with automated test coverage, eliminating X errors and boosting reliability to Y%",
      "impact_focus": "Fault-tolerance and high test coverage",
      "action_verb": "Spearheaded"
    }}
  ],
  "power_verbs": ["Architected", "Engineered", "Optimized", "Refactored", "Benchmarked"],
  "tips": [
    "Always place strong action verbs at the beginning of each bullet.",
    "Quantify impact with concrete metrics (latency in ms, % speedup, user volume).",
    "Never write 'helped with' or 'worked on'—take ownership of your direct code contributions."
  ]
}}
Do NOT output any markdown backticks or other text."""
            raw = _gemini_resume.generate_text(prompt=prompt, system_instruction="You write elite SDE resume bullet points.").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            parsed = json.loads(raw)
            if "variants" in parsed and len(parsed["variants"]) >= 2:
                parsed["original"] = raw_clean
                return parsed
        except Exception:
            pass

    # Deterministic high-quality XYZ formula generator
    # Strip common weak starting phrases
    core_text = raw_clean
    weak_prefixes = [
        "i worked on", "worked on", "helped to", "helped build", "helped create",
        "created an", "created a", "built an", "built a", "made an", "made a",
        "responsible for", "developed an", "developed a", "wrote code for"
    ]
    core_lower = core_text.lower()
    for prefix in weak_prefixes:
        if core_lower.startswith(prefix):
            core_text = core_text[len(prefix):].strip()
            break
    if not core_text:
        core_text = raw_clean

    return {
        "original": raw_clean,
        "critique": "Original bullet lacks quantified outcomes and active ownership verbs. Recruiters cannot see the scale, efficiency gain, or exact technical trade-offs.",
        "variants": [
            {
                "label": "Metric & Impact-Driven (Google XYZ Formula)",
                "bullet": f"Engineered {core_text}, boosting throughput by 38% and reducing round-trip execution latency from 850ms to 210ms via optimized algorithmic workflows.",
                "impact_focus": "Measurable performance speedup & latency reduction",
                "action_verb": "Engineered"
            },
            {
                "label": "System Architecture & Scalability",
                "bullet": f"Architected modular micro-services for {core_text}, decoupling core processing pipelines and sustaining 1,200+ concurrent requests with zero packet drop.",
                "impact_focus": "High concurrency & decoupled architecture",
                "action_verb": "Architected"
            },
            {
                "label": "Production Rigor & Reliability",
                "bullet": f"Spearheaded implementation of {core_text} with 92% automated unit test coverage, eliminating edge-case regression bugs and hardening API fault-tolerance.",
                "impact_focus": "Test coverage, clean code, and zero production regressions",
                "action_verb": "Spearheaded"
            }
        ],
        "power_verbs": ["Architected", "Engineered", "Benchmarked", "Refactored", "Containerized", "Optimized"],
        "tips": [
            "Use the Google XYZ Formula: 'Accomplished [X], as measured by [Y], by doing [Z]'.",
            "Eliminate passive verbs ('worked on', 'helped')—use precision action verbs ('Engineered', 'Benchmarked').",
            "Quantify results: mention percentage speedups, latency in milliseconds, or concurrent request capacity."
        ]
    }

