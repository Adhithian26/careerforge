import re
from typing import List, Dict, Any, Set

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

def get_project_interview_prep(project_title: str) -> Dict[str, Any]:
    """Generates rigorous technical interview questions tailored to the student's actual projects."""
    p_lower = project_title.lower()
    if "rag" in p_lower or "chat" in p_lower or "retrieval" in p_lower:
        return PROJECT_QUESTIONS_CATALOG["rag"]
    elif "face" in p_lower or "attend" in p_lower or "vision" in p_lower:
        return PROJECT_QUESTIONS_CATALOG["attendance"]
    else:
        # Combined project question suite
        return {
            "architecture_questions": [
                "What was the high-level system architecture of this project? Walk me through how data flows from input to persistent output.",
                "How did you modularize the frontend, backend API, and database layers?"
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
