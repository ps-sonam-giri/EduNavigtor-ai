"""
Scholarship Agent
Finds scholarships matching the student profile,
explains eligibility, and ranks by value and likelihood.
"""

import json
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from prompts.scholarship_prompts import SCHOLARSHIP_MATCH_PROMPT


async def scholarship_agent(state: AgentState) -> AgentState:
    """
    1. Fetch scholarships from DB that the student is eligible for.
    2. LLM explains why each scholarship is a good match.
    3. Ranks by value × eligibility probability.
    """
    profile = state.get("student_profile", {})
    universities = state.get("recommended_universities", [])

    # ── Step 1: Fetch matching scholarships ───────────────────────────────────
    scholarships = await _fetch_matching_scholarships(profile)

    if not scholarships:
        executed = list(state.get("agents_executed", []))
        executed.append("scholarship_agent")
        return {
            **state,
            "matched_scholarships": [],
            "agents_executed": executed,
        }

    # ── Step 2: LLM evaluates and explains matches ────────────────────────────
    match_prompt = SCHOLARSHIP_MATCH_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        scholarships=json.dumps(scholarships, indent=2),
        universities=json.dumps([u.get("name") for u in universities[:5]], indent=2),
    )
    match_text, tokens = await ainvoke_llm(match_prompt)
    matched_raw = extract_json_from_response(match_text)
    matched: List[Dict[str, Any]] = matched_raw.get("matched_scholarships", scholarships[:5])

    executed = list(state.get("agents_executed", []))
    executed.append("scholarship_agent")

    # Build message for scholarship-only queries
    if matched:
        msg_lines = ["**🏆 Matched Scholarships**\n"]
        # Summary table
        msg_lines.append("| Scholarship | Provider | Basis | Amount | Eligibility |")
        msg_lines.append("|-------------|----------|-------|--------|-------------|")
        for s in matched[:6]:
            name = s.get('name', 'N/A')
            provider = s.get('provider', 'N/A')
            basis = s.get('scholarship_basis', 'Merit-based')
            amount = s.get('amount_description', 'N/A')
            match = s.get('eligibility_match', 'Medium')
            icon = "🟢" if match == "High" else "🟡" if match == "Medium" else "🔴"
            msg_lines.append(f"| **{name}** | {provider} | {basis} | {amount} | {icon} {match} |")

        msg_lines.append("")

        # Detailed breakdown
        for s in matched[:5]:
            msg_lines.append(f"**{s.get('name')}** — {s.get('provider')}")
            msg_lines.append(f"• Basis: **{s.get('scholarship_basis', 'Merit-based')}**")
            msg_lines.append(f"• Amount: {s.get('amount_description', 'N/A')}")
            if s.get('eligibility_criteria'):
                msg_lines.append(f"• Eligibility criteria:")
                for line in s.get('eligibility_criteria', '').split('\n'):
                    if line.strip():
                        msg_lines.append(f"  {line}")
            msg_lines.append(f"{s.get('why_good_fit', '')}")
            if s.get('gap_to_address'):
                msg_lines.append(f"⚠️ Gap to address: {s.get('gap_to_address', '')}")
            if s.get('deadline'):
                msg_lines.append(f"• Deadline: **{s.get('deadline')}**")
            if s.get('application_url'):
                msg_lines.append(f"• Apply: {s.get('application_url')}")
            msg_lines.append("")

        total = matched_raw.get("total_potential_savings_usd", 0)
        if total:
            msg_lines.append(f"**💰 Total potential savings: ${total:,.0f}**\n")
        if matched_raw.get("advice"):
            msg_lines.append("**📋 Strategy**")
            msg_lines.append(matched_raw.get("advice", ""))

        message = "\n".join(msg_lines)
    else:
        message = "No matching scholarships found for your current profile."

    return {
        **state,
        "matched_scholarships": matched,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
        "message": message,
    }


async def _fetch_matching_scholarships(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Query scholarships from PostgreSQL matching student eligibility."""
    try:
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.scholarship import Scholarship

        engine = create_async_engine(settings.database_url, echo=False)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        cgpa = profile.get("cgpa") or 0.0
        ielts = profile.get("ielts_score") or 0.0

        async with async_session() as session:
            q = (
                select(Scholarship)
                .where(Scholarship.is_active == True)
                .where(
                    (Scholarship.min_cgpa == None) | (Scholarship.min_cgpa <= cgpa)
                )
                .where(
                    (Scholarship.min_ielts == None) | (Scholarship.min_ielts <= ielts)
                )
                .limit(20)
            )
            result = await session.execute(q)
            rows = result.scalars().all()
            await engine.dispose()

            return [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "provider": s.provider,
                    "scholarship_type": s.scholarship_type,
                    "amount_usd": s.amount_usd,
                    "amount_description": s.amount_description,
                    "eligible_countries": s.eligible_countries,
                    "eligible_courses": s.eligible_courses,
                    "min_cgpa": s.min_cgpa,
                    "min_ielts": s.min_ielts,
                    "description": s.description,
                    "application_deadline": s.application_deadline,
                    "application_url": s.application_url,
                }
                for s in rows
            ]
    except Exception:
        return []
