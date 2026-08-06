"""
LangGraph shared state definition for EduPilot AI.
Supports ReAct trajectory, observations, reflection critiques, and HITL flags.
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
    # ── Identifiers & Query ───────────────────────────────────
    user_query: str
    session_id: str
    user_id: str
    chat_history: List[Dict[str, str]]

    # ── ReAct Trajectory & Execution ─────────────────────────
    turn_count: int
    max_turns: int
    current_thought: str
    pending_action: Optional[Dict[str, Any]]
    observations: List[Dict[str, Any]]
    agents_executed: List[str]
    orchestrator_reasoning: str

    # ── Reflection & Verification ────────────────────────────
    verifier_passed: bool
    verifier_critique: Optional[str]

    # ── Human-in-the-Loop Flags ──────────────────────────────
    requires_approval: bool
    approval_action: Optional[str]
    approval_granted: Optional[bool]

    # ── Student Profile & Data Store ──────────────────────────
    student_profile: StudentProfileData
    profile_summary: str
    profile_complete: bool

    # ── Domain Agent Results ─────────────────────────────────
    recommended_countries: List[Dict[str, Any]]
    recommended_universities: List[Dict[str, Any]]
    matched_scholarships: List[Dict[str, Any]]
    finance_breakdown: Dict[str, Any]
    application_timeline: List[Dict[str, Any]]

    # ── Output & Reporting ───────────────────────────────────
    final_report: Dict[str, Any]
    report_id: Optional[str]
    message: str
    total_tokens_used: int
    errors: List[str]
