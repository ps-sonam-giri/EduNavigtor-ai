"""
Reflection & Verification Node.
Audits candidate agent outputs against hard constraints:
1. CGPA eligibility
2. Budget compliance
3. Factual grounding in raw tool observations
"""

import json
from typing import Any, Dict, List
from agents.llm import ainvoke_llm
from agents.state import AgentState


async def verifier_node(state: AgentState) -> AgentState:
    """
    Audits accumulated agent state & outputs against student constraints.
    Returns updated state with verifier_passed boolean and verifier_critique text.
    """
    profile = state.get("student_profile", {})
    unis = state.get("recommended_universities", [])
    scholarships = state.get("matched_scholarships", [])
    observations = state.get("observations", [])

    student_cgpa = profile.get("cgpa") or 0.0
    student_budget = profile.get("total_budget_usd") or 999999.0

    violations = []

    # 1. CGPA Rule Verification
    for u in unis:
        min_cgpa = u.get("min_cgpa") or 0.0
        if min_cgpa > 0 and student_cgpa > 0 and student_cgpa < min_cgpa:
            violations.append(
                f"CGPA Violation: Recommended university '{u.get('name')}' requires minimum CGPA {min_cgpa}, "
                f"but student CGPA is only {student_cgpa}."
            )

    # 2. Budget Rule Verification
    for u in unis:
        tuition = u.get("avg_tuition_usd_per_year") or 0.0
        if tuition > student_budget:
            violations.append(
                f"Budget Violation: University '{u.get('name')}' tuition (${tuition:,.0f}/yr) exceeds "
                f"student budget (${student_budget:,.0f}/yr)."
            )

    # 3. Grounding Verification against raw observations
    observed_names = set()
    for obs in observations:
        data = obs.get("observation", [])
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "name" in item:
                    observed_names.add(item["name"].lower())

    for u in unis:
        uni_name = u.get("name", "").lower()
        # If DB search ran but university was not in observations
        if observed_names and uni_name not in observed_names:
            violations.append(
                f"Grounding Warning: '{u.get('name')}' was not returned by database observations."
            )

    executed = list(state.get("agents_executed", []))
    executed.append("verifier")

    if violations:
        critique = "Critique / Constraints Flagged:\n" + "\n".join(f"• {v}" for v in violations)
        return {
            **state,
            "verifier_passed": False,
            "verifier_critique": critique,
            "agents_executed": executed,
        }

    return {
        **state,
        "verifier_passed": True,
        "verifier_critique": "All constraints verified successfully.",
        "agents_executed": executed,
    }
