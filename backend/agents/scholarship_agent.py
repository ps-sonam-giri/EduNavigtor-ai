"""
Scholarship Agent – uses Gemini with Google Search for current scholarship data.
Finds real scholarships for Indian students based on their exact profile.
"""

import json
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState

SCHOLARSHIP_SEARCH_PROMPT = """You are a scholarship advisor. Use Tavily live web search data to find CURRENT 2025/2026 REAL scholarship information.

Student Profile:
- CGPA: {cgpa}/10 | Backlogs: {backlogs} | IELTS: {ielts}
- Budget: ${budget_usd} USD | Course: {course_interest}
- Preferred Countries: {preferred_countries}
- Work Experience: {work_exp} years

User asked: "{user_query}"

Find ALL scholarships this student is REALISTICALLY eligible for based on LIVE WEB SEARCH:
1. Government scholarships (DAAD, Chevening, Australia Awards, Fulbright, etc.)
2. University-specific scholarships for international students
3. Foundation and endowment grants (JN Tata, Inlaks Shivdasani, NOS, etc.)

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
      "eligibility_criteria": "• Minimum CGPA 7.0\\n• Under 35 years old",
      "eligibility_match": "High",
      "why_good_fit": "• Your CGPA {cgpa} exceeds requirement\\n• Covers your {course_interest} program",
      "gap_to_address": "• Need strong research proposal",
      "action_steps": [
        "Visit official website and register",
        "Prepare Statement of Purpose",
        "Obtain 2 academic recommendation letters"
      ],
      "deadline": "October 2025",
      "application_url": "https://scholarship-official-url.org",
      "priority_rank": 1
    }}
  ],
  "total_potential_savings_usd": 75000,
  "strategy": "• Apply to DAAD first for Germany\\n• Chevening for UK\\n• Start 8 months before deadlines"
}}
"""


async def scholarship_agent(state: AgentState) -> AgentState:
    profile = state.get("student_profile", {})
    user_query = state.get("user_query", "")

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
        search_query = f"scholarships for international students studying {course} in {', '.join(preferred) if preferred else 'USA UK Germany Canada Australia'} 2025 2026 application deadline eligibility"
        tavily_res = await search_tavily_web(query=search_query, max_results=7)
        if tavily_res.get("status") == "success":
            snippets = []
            if tavily_res.get("answer"):
                snippets.append(f"Summary: {tavily_res['answer']}")
            for r in tavily_res.get("results", []):
                snippets.append(f"- [{r.get('title')}]({r.get('url')}): {r.get('content')[:300]}")
            tavily_context = "\nLive Web Search Results (Tavily Engine):\n" + "\n".join(snippets)
    except Exception:
        tavily_context = ""

    prompt = SCHOLARSHIP_SEARCH_PROMPT.format(
        cgpa=cgpa, backlogs=backlogs, ielts=ielts,
        budget_usd=budget, course_interest=course,
        preferred_countries=json.dumps(preferred),
        work_exp=work_exp, user_query=user_query + tavily_context,
    )

    response_text, tokens = await ainvoke_llm(prompt, use_search=True)
    data = extract_json_from_response(response_text)
    matched: List[Dict[str, Any]] = data.get("matched_scholarships", [])

    executed = list(state.get("agents_executed", []))
    executed.append("scholarship_agent")

    # Build structured message
    msg_lines = ["**🏆 Scholarships You Are Eligible For (Tavily Live Web Data)**\n"]

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
        msg_lines.append("No live scholarships found matching your profile currently.")

    return {
        **state,
        "matched_scholarships": matched,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
        "message": "\n".join(msg_lines),
    }
