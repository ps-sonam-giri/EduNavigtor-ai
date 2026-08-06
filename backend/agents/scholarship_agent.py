"""
Scholarship Agent – uses Gemini with Google Search for current scholarship data.
Finds real scholarships for Indian students based on their exact profile.
"""

import json
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState

SCHOLARSHIP_SEARCH_PROMPT = """You are a scholarship advisor for Indian students going abroad for postgraduate studies.
Use Google Search to find CURRENT, REAL scholarship information.

Student Profile:
- CGPA: {cgpa}/10 | Backlogs: {backlogs} | IELTS: {ielts}
- Budget: ${budget_usd} USD | Course: {course_interest}
- Preferred Countries: {preferred_countries}
- Work Experience: {work_exp} years

User asked: "{user_query}"

Known scholarships from our database:
{db_scholarships}

Find ALL scholarships this student is REALISTICALLY eligible for. Include:
1. Government scholarships (DAAD, Chevening, Australia Awards, GKFS, etc.)
2. University-specific scholarships for Indian students
3. Indian government scholarships (ICCR, Inlaks, JN Tata, etc.)
4. Private foundation scholarships

For EACH scholarship be SPECIFIC about eligibility based on CGPA {cgpa} and backlogs {backlogs}.

Respond ONLY with JSON:
{{
  "matched_scholarships": [
    {{
      "name": "Scholarship Name",
      "provider": "Provider Organisation",
      "country": "Target Country",
      "scholarship_basis": "Merit-based | Need-based | Country-specific | Government",
      "amount_usd": 50000,
      "amount_description": "Full tuition + €934/month living stipend + travel",
      "eligibility_criteria": "• Indian nationals only\\n• Minimum CGPA 7.0\\n• Under 35 years old",
      "eligibility_match": "High",
      "why_good_fit": "• Your CGPA {cgpa} exceeds the minimum requirement\\n• Indian nationals specifically eligible\\n• Your {course_interest} program is covered",
      "gap_to_address": "• Need strong research proposal\\n• Leadership essay required",
      "action_steps": [
        "Visit official website and register",
        "Prepare Statement of Purpose highlighting research interests",
        "Obtain 2 academic recommendation letters"
      ],
      "deadline": "October 2025",
      "application_url": "https://scholarship-official-url.org",
      "priority_rank": 1
    }}
  ],
  "total_potential_savings_usd": 75000,
  "strategy": "• Apply to DAAD first — highest value for German universities\\n• Chevening for UK — prestigious and fully funded\\n• Start 8 months before deadlines"
}}

Search for current 2025-2026 scholarship deadlines and amounts.
Return at least 6 scholarships matched to this student's profile.
"""


async def scholarship_agent(state: AgentState) -> AgentState:
    profile = state.get("student_profile", {})
    universities = state.get("recommended_universities", [])
    user_query = state.get("user_query", "")

    db_scholarships = await _fetch_db_scholarships(profile)

    cgpa = profile.get("cgpa", "Not specified")
    ielts = profile.get("ielts_score", "Not specified")
    budget = profile.get("total_budget_usd", "Not specified")
    backlogs = profile.get("backlogs", 0)
    preferred = profile.get("preferred_countries", [])
    course = profile.get("course_interest", "Not specified")
    work_exp = profile.get("work_experience_years", 0)

    # Perform Tavily Live Web Search for scholarships
    tavily_context = ""
    try:
        from tools.tavily_tools import search_tavily_web
        search_query = f"scholarships for Indian students studying {course} in {', '.join(preferred) if preferred else 'USA UK Germany Canada'} 2025 2026 application deadline"
        tavily_res = await search_tavily_web(query=search_query, max_results=5)
        if tavily_res.get("status") == "success":
            snippets = []
            if tavily_res.get("answer"):
                snippets.append(f"Summary: {tavily_res['answer']}")
            for r in tavily_res.get("results", []):
                snippets.append(f"- [{r.get('title')}]({r.get('url')}): {r.get('content')[:250]}")
            tavily_context = "\nLive Web Search Results (Tavily):\n" + "\n".join(snippets)
    except Exception:
        tavily_context = ""

    prompt = SCHOLARSHIP_SEARCH_PROMPT.format(
        cgpa=cgpa, backlogs=backlogs, ielts=ielts,
        budget_usd=budget, course_interest=course,
        preferred_countries=json.dumps(preferred),
        work_exp=work_exp, user_query=user_query + tavily_context,
        db_scholarships=json.dumps(db_scholarships[:5], indent=2),
    )

    # Use Google Search / Tavily for current scholarship data
    response_text, tokens = await ainvoke_llm(prompt, use_search=True)
    data = extract_json_from_response(response_text)
    matched: List[Dict[str, Any]] = data.get("matched_scholarships", [])

    if not matched:
        matched = db_scholarships[:6]

    executed = list(state.get("agents_executed", []))
    executed.append("scholarship_agent")

    # Build structured message
    msg_lines = ["**🏆 Scholarships You Are Eligible For (Live Data)**\n"]

    if matched:
        msg_lines.append("| Scholarship | Provider | Basis | Amount | Eligibility |")
        msg_lines.append("|-------------|----------|-------|--------|-------------|")
        for s in matched[:6]:
            icon = "🟢" if s.get("eligibility_match") == "High" else "🟡" if s.get("eligibility_match") == "Medium" else "🔴"
            msg_lines.append(
                f"| **{s.get('name','N/A')}** | {s.get('provider','N/A')} | "
                f"{s.get('scholarship_basis','Merit')} | {s.get('amount_description','N/A')} | "
                f"{icon} {s.get('eligibility_match','Medium')} |"
            )
        msg_lines.append("")

        for s in matched[:5]:
            msg_lines.append(f"**{s.get('name')}** — {s.get('provider')}")
            msg_lines.append(f"• Basis: **{s.get('scholarship_basis','Merit-based')}**")
            msg_lines.append(f"• Amount: {s.get('amount_description','N/A')}")
            if s.get("eligibility_criteria"):
                msg_lines.append(f"• Eligibility:")
                for line in str(s["eligibility_criteria"]).split("\\n"):
                    if line.strip():
                        msg_lines.append(f"  {line.strip()}")
            if s.get("why_good_fit"):
                msg_lines.append(s["why_good_fit"])
            if s.get("gap_to_address"):
                msg_lines.append(f"⚠️ Gap: {s['gap_to_address']}")
            if s.get("deadline"):
                msg_lines.append(f"• Deadline: **{s['deadline']}**")
            if s.get("application_url"):
                msg_lines.append(f"• Apply: {s['application_url']}")
            msg_lines.append("")

        total = data.get("total_potential_savings_usd", 0)
        if total:
            msg_lines.append(f"**💰 Total potential savings: ${total:,.0f}**\n")
        if data.get("strategy"):
            msg_lines.append("**📋 Application Strategy**")
            msg_lines.append(data["strategy"])
    else:
        msg_lines.append("No scholarships found matching your current profile. Consider improving CGPA or IELTS score.")

    return {
        **state,
        "matched_scholarships": matched,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
        "message": "\n".join(msg_lines),
    }


async def _fetch_db_scholarships(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.scholarship import Scholarship

        engine = create_async_engine(settings.database_url, echo=False)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        cgpa = profile.get("cgpa") or 0.0
        ielts = profile.get("ielts_score") or 0.0

        async with session_factory() as session:
            result = await session.execute(
                select(Scholarship).where(Scholarship.is_active == True)
                .where((Scholarship.min_cgpa == None) | (Scholarship.min_cgpa <= cgpa))
                .where((Scholarship.min_ielts == None) | (Scholarship.min_ielts <= ielts))
                .limit(10)
            )
            rows = result.scalars().all()
            await engine.dispose()
            return [{"name": s.name, "provider": s.provider,
                     "amount_description": s.amount_description,
                     "scholarship_basis": s.scholarship_type,
                     "min_cgpa": s.min_cgpa, "description": s.description}
                    for s in rows]
    except Exception:
        return []
