"""
Timeline Agent
Generates a personalized month-by-month application roadmap
based on target intake, current date, and profile completeness.
"""

import json
from datetime import datetime
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from prompts.timeline_prompts import TIMELINE_GENERATION_PROMPT


async def timeline_agent(state: AgentState) -> AgentState:
    """
    Generates a personalised application timeline with:
    - Test preparation milestones
    - Document preparation
    - Application deadlines
    - Visa process
    - Travel preparation
    """
    profile = state.get("student_profile", {})
    universities = state.get("recommended_universities", [])
    scholarships = state.get("matched_scholarships", [])

    current_date = datetime.now().strftime("%B %Y")
    target_intake = profile.get("target_intake", "Fall 2025")

    # Gather intake months from recommended universities
    intake_windows = list(
        {
            month
            for uni in universities[:3]
            for month in (uni.get("intake_months") or [])
        }
    )

    prompt = TIMELINE_GENERATION_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        current_date=current_date,
        target_intake=target_intake,
        universities=json.dumps(
            [{"name": u.get("name"), "intake_months": u.get("intake_months")} for u in universities[:5]],
            indent=2,
        ),
        scholarships=json.dumps(
            [{"name": s.get("name"), "deadline": s.get("application_deadline")} for s in scholarships[:3]],
            indent=2,
        ),
        has_ielts=profile.get("ielts_score") is not None,
        has_gre=profile.get("gre_score") is not None,
    )

    response_text, tokens = await ainvoke_llm(prompt)
    timeline_data = extract_json_from_response(response_text)

    if not timeline_data or not timeline_data.get("timeline"):
        timeline_data = _generate_fallback_timeline(profile, target_intake)

    executed = list(state.get("agents_executed", []))
    executed.append("timeline_agent")

    # Build message for timeline-only queries
    if timeline_data.get("timeline"):
        tl = timeline_data["timeline"]
        msg_lines = ["**📅 Your Application Timeline**\n"]
        current_phase = None
        for item in tl[:10]:
            if item.get("phase") != current_phase:
                current_phase = item.get("phase")
                msg_lines.append(f"\n**{current_phase}**")
            priority_icon = "🔴" if item.get("priority") == "critical" else "🟡" if item.get("priority") == "high" else "🟢"
            msg_lines.append(
                f"• {priority_icon} Month {item.get('month_offset', 0) + 1}: **{item.get('milestone')}**"
            )
            msg_lines.append(f"  {item.get('description', '')}")

        if timeline_data.get("critical_path_summary"):
            msg_lines.append(f"\n**🗺️ Critical Path**")
            msg_lines.append(timeline_data["critical_path_summary"])

        message = "\n".join(msg_lines)
    else:
        message = "Could not generate timeline. Please complete your profile first."

    return {
        **state,
        "application_timeline": timeline_data.get("timeline", []),
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
        "message": message,
    }


def _generate_fallback_timeline(profile: Dict[str, Any], target_intake: str) -> Dict:
    """Rule-based timeline as fallback."""
    has_ielts = profile.get("ielts_score") is not None
    has_gre = profile.get("gre_score") is not None

    timeline = []
    month_offset = 0

    if not has_ielts:
        timeline.append(
            {
                "month_offset": month_offset,
                "phase": "Test Preparation",
                "milestone": "IELTS / TOEFL Preparation",
                "description": "Enroll in IELTS coaching. Target band 7.0+. Duration: 2-3 months.",
                "duration_weeks": 10,
                "priority": "critical",
                "category": "test_prep",
            }
        )
        month_offset += 3

    if not has_gre:
        timeline.append(
            {
                "month_offset": month_offset,
                "phase": "Test Preparation",
                "milestone": "GRE / GMAT Preparation",
                "description": "Start GRE preparation if applying to US/Canada programs. Target 310+.",
                "duration_weeks": 8,
                "priority": "high",
                "category": "test_prep",
            }
        )
        month_offset += 2

    timeline += [
        {
            "month_offset": month_offset,
            "phase": "Document Preparation",
            "milestone": "SOP & LOR Drafting",
            "description": "Draft Statement of Purpose (SOP) tailored to each university. Request 3 Letters of Recommendation.",
            "duration_weeks": 4,
            "priority": "critical",
            "category": "documents",
        },
        {
            "month_offset": month_offset + 1,
            "phase": "Document Preparation",
            "milestone": "Resume / CV Update",
            "description": "Update academic CV with projects, internships, publications, and awards.",
            "duration_weeks": 1,
            "priority": "high",
            "category": "documents",
        },
        {
            "month_offset": month_offset + 2,
            "phase": "Application",
            "milestone": "University Applications",
            "description": "Submit applications to shortlisted universities. Apply to safety, match, and reach schools.",
            "duration_weeks": 6,
            "priority": "critical",
            "category": "applications",
        },
        {
            "month_offset": month_offset + 3,
            "phase": "Scholarship",
            "milestone": "Scholarship Applications",
            "description": "Apply for matched scholarships. Prepare scholarship-specific essays.",
            "duration_weeks": 4,
            "priority": "high",
            "category": "scholarships",
        },
        {
            "month_offset": month_offset + 5,
            "phase": "Decision",
            "milestone": "Offer Letters & Decision",
            "description": "Evaluate offer letters. Compare financial aid packages. Make final decision.",
            "duration_weeks": 2,
            "priority": "critical",
            "category": "decision",
        },
        {
            "month_offset": month_offset + 6,
            "phase": "Visa",
            "milestone": "Student Visa Application",
            "description": "Gather visa documents: offer letter, financial proof, accommodation, travel insurance. Submit visa application.",
            "duration_weeks": 6,
            "priority": "critical",
            "category": "visa",
        },
        {
            "month_offset": month_offset + 8,
            "phase": "Pre-Departure",
            "milestone": "Pre-Departure Preparation",
            "description": "Book flights, arrange accommodation, open bank account, get forex card, attend pre-departure orientation.",
            "duration_weeks": 4,
            "priority": "medium",
            "category": "travel",
        },
    ]

    return {"timeline": timeline, "target_intake": target_intake}
