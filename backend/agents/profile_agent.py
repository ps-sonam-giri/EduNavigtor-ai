"""
Profile Agent – Extracts and enriches the student's academic/personal profile.
Produces a structured StudentProfileData dict and a human-readable summary.
"""

import json
from typing import Any, Dict

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from prompts.profile_prompts import PROFILE_EXTRACTION_PROMPT, PROFILE_SUMMARY_PROMPT


async def profile_agent(state: AgentState) -> AgentState:
    """
    Reads the raw student profile from state, validates/enriches it using LLM,
    and produces a clean profile_summary string.
    """
    profile = state.get("student_profile", {})
    query = state.get("user_query", "")

    # ── Step 1: Use LLM to extract any missing fields from the user query ─────
    extraction_prompt = PROFILE_EXTRACTION_PROMPT.format(
        existing_profile=json.dumps(profile, indent=2),
        user_query=query,
    )
    extraction_text, tokens1 = await ainvoke_llm(extraction_prompt, use_search=False)
    extracted = extract_json_from_response(extraction_text)

    # Merge extracted fields into profile (only update fields not already set)
    merged_profile = {**profile}
    for key, value in extracted.items():
        if value is not None and (key not in merged_profile or merged_profile[key] is None):
            merged_profile[key] = value

    # ── Step 2: Generate a human-readable profile summary ────────────────────
    summary_prompt = PROFILE_SUMMARY_PROMPT.format(
        profile=json.dumps(merged_profile, indent=2)
    )
    summary_text, tokens2 = await ainvoke_llm(summary_prompt)

    # ── Step 3: Determine if profile is complete enough to proceed ────────────
    required_fields = ["cgpa", "course_interest", "total_budget_usd"]
    profile_complete = all(
        merged_profile.get(f) is not None for f in required_fields
    )

    executed = list(state.get("agents_executed", []))
    executed.append("profile_agent")

    return {
        **state,
        "student_profile": merged_profile,
        "profile_summary": summary_text.strip(),
        "profile_complete": profile_complete,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens1 + tokens2,
    }

