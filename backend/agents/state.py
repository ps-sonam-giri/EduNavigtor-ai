"""
LangGraph shared state definition.
Every agent reads from and writes to this typed state dict.
"""

from typing import Any, Dict, List, Optional, TypedDict


class StudentProfileData(TypedDict, total=False):
    cgpa: Optional[float]
    cgpa_scale: float
    backlogs: int
    degree: Optional[str]
    specialization: Optional[str]
    ielts_score: Optional[float]
    toefl_score: Optional[int]
    gre_score: Optional[int]
    gmat_score: Optional[int]
    preferred_countries: List[str]
    course_interest: Optional[str]
    career_goal: Optional[str]
    target_intake: Optional[str]
    total_budget_usd: Optional[float]
    financial_background: Optional[str]
    work_experience_years: int


class AgentState(TypedDict, total=False):
    # ── Routing ───────────────────────────────────────────────
    user_query: str
    session_id: str
    user_id: str
    chat_history: List[Dict[str, str]]

    # ── Orchestrator decisions ────────────────────────────────
    agents_to_run: List[str]
    agents_executed: List[str]
    orchestrator_reasoning: str

    # ── Student profile ───────────────────────────────────────
    student_profile: StudentProfileData
    profile_summary: str
    profile_complete: bool

    # ── Country & university recommendations ──────────────────
    recommended_countries: List[Dict[str, Any]]
    recommended_universities: List[Dict[str, Any]]
    university_comparison: Dict[str, Any]

    # ── Scholarships ──────────────────────────────────────────
    matched_scholarships: List[Dict[str, Any]]

    # ── Finance ───────────────────────────────────────────────
    finance_breakdown: Dict[str, Any]

    # ── Timeline ─────────────────────────────────────────────
    application_timeline: List[Dict[str, Any]]

    # ── Final report ─────────────────────────────────────────
    final_report: Dict[str, Any]
    report_id: Optional[str]

    # ── Per-agent messages (each agent stores its own) ────────
    agent_messages: Dict[str, str]   # {"scholarship_agent": "...", "university_agent": "..."}

    # ── Final message (picked by run_orchestrator) ────────────
    message: str
