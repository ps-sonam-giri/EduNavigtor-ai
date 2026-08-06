"""
University Recommendation Agent
Uses Gemini with Google Search grounding for real-time university data.
Returns 5 globally relevant universities with current rankings, costs, scholarships.
"""

import json
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from prompts.university_prompts import UNIVERSITY_COMPARISON_PROMPT

GLOBAL_RECOMMENDATION_PROMPT = """You are an expert study abroad counsellor. Use Tavily live web search data to find REAL, CURRENT 2025/2026 university information.

Student Profile:
- CGPA: {cgpa}/10 | Backlogs: {backlogs} | IELTS: {ielts}
- Budget: ${budget_usd} USD total | Course: {course_interest}
- Career Goal: {career_goal}
- Preferred Countries: {preferred_countries}

User asked: "{user_query}"

REQUIREMENTS:
1. Return EXACTLY {num_universities} universities from AT LEAST {num_countries} DIFFERENT COUNTRIES based on LIVE WEB SEARCH
2. Use REAL, CURRENT data — QS rankings, tuition fees, and deadlines
3. Match universities specifically to CGPA {cgpa}, backlogs {backlogs}, budget, and career goal
4. Include at least 1 budget-friendly option (under $10,000/yr tuition or free tuition)
5. For EACH university include at least 2-3 REAL scholarships with current amounts, deadlines, and official URLs
6. Reference the student's actual profile numbers in why_recommended

Respond ONLY with valid JSON:
{{
  "recommendations": [
    {{
      "name": "Full Official University Name",
      "country": "Country Name",
      "city": "City Name",
      "qs_world_rank": 150,
      "category": "safe",
      "match_score": 80,
      "why_recommended": "• Your CGPA {cgpa} exceeds requirement\\n• Tuition $X/yr fits your ${budget_usd} budget\\n• Strong {course_interest} program",
      "admission_chances": "High",
      "avg_tuition_usd_per_year": 500,
      "avg_living_cost_usd_per_month": 900,
      "total_cost_year1_usd": 14000,
      "min_cgpa": 6.0,
      "min_ielts": 6.0,
      "backlog_policy": "Accepts up to 10 backlogs with SOP explanation",
      "programs": ["MSc Artificial Intelligence", "MSc Computer Science"],
      "intake_months": ["October", "April"],
      "scholarships": [
        {{
          "name": "DAAD Scholarship",
          "basis": "Merit-based",
          "amount_description": "€934/month stipend + travel allowance",
          "eligibility": "Good academic record, motivation letter",
          "deadline": "October 2025",
          "url": "https://www.daad.de"
        }}
      ],
      "graduate_employment_rate": 88,
      "website": "https://university.edu"
    }}
  ]
}}
"""


async def university_agent(state: AgentState) -> AgentState:
    profile = state.get("student_profile", {})
    countries = state.get("recommended_countries", [])
    user_query = state.get("user_query", "")

    cgpa = profile.get("cgpa", "Not specified")
    ielts = profile.get("ielts_score", "Not specified")
    budget = profile.get("total_budget_usd", "Not specified")
    backlogs = profile.get("backlogs", 0)
    preferred = profile.get("preferred_countries", [])
    course = profile.get("course_interest", "Not specified")
    career = profile.get("career_goal", "Not specified")

    # Detect how many universities the user wants
    import re as _re
    count_match = _re.search(r'\b(\d+)\b', user_query)
    requested_count = int(count_match.group(1)) if count_match else 5
    requested_count = min(max(requested_count, 3), 15)  # clamp 3–15
    num_countries = min(requested_count, 5)

    # Perform Tavily Live Web Search for real-time university data
    tavily_context = ""
    try:
        from tools.tavily_tools import search_tavily_web
        search_query = f"top {course} universities in {', '.join(preferred) if preferred else 'USA UK Germany Canada Australia'} tuition fees QS rank 2025 2026 application process"
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

    prompt = GLOBAL_RECOMMENDATION_PROMPT.format(
        cgpa=cgpa, backlogs=backlogs, ielts=ielts,
        budget_usd=budget, course_interest=course, career_goal=career,
        preferred_countries=json.dumps(preferred),
        user_query=user_query + tavily_context,
        num_universities=requested_count,
        num_countries=num_countries,
    )

    response_text, tokens1 = await ainvoke_llm(prompt, use_search=True)
    data = extract_json_from_response(response_text)
    recommendations: List[Dict[str, Any]] = data.get("recommendations", [])

    # Comparison summary
    comparison = {}
    tokens2 = 0
    if len(recommendations) >= 2:
        cmp_prompt = UNIVERSITY_COMPARISON_PROMPT.format(
            universities=json.dumps(recommendations[:5], indent=2),
            profile=json.dumps(profile, indent=2),
        )
        cmp_text, tokens2 = await ainvoke_llm(cmp_prompt)
        comparison = extract_json_from_response(cmp_text)

    executed = list(state.get("agents_executed", []))
    executed.append("university_agent")

    # Build structured table message
    msg_lines = [f"**🎓 University Recommendations (Live Web Grounded — {len(recommendations)} universities)**\n"]
    msg_lines.append("| # | University | Country | City | Tuition/yr | Living/mo | Chances |")
    msg_lines.append("|---|-----------|---------|------|-----------|-----------|---------|")
    for i, uni in enumerate(recommendations, 1):
        tuition = uni.get("avg_tuition_usd_per_year", 0)
        tuition_str = "Free" if tuition == 0 else f"${tuition:,.0f}"
        living = uni.get("avg_living_cost_usd_per_month", 0)
        living_str = f"${living:,.0f}" if living else "~$900"
        chances = uni.get("admission_chances", "Medium")
        cat = uni.get("category", "match")
        icon = "🟢" if cat == "safe" else "🟡" if cat == "match" else "🔴"
        msg_lines.append(
            f"| {i} | **{uni.get('name','N/A')}** | {uni.get('country','N/A')} | "
            f"{uni.get('city','N/A')} | {tuition_str} | {living_str} | {icon} {chances} |"
        )
    msg_lines.append("")

    for i, uni in enumerate(recommendations, 1):
        rank = f"QS #{uni.get('qs_world_rank')}" if uni.get("qs_world_rank") else "Unranked"
        msg_lines.append(f"**{i}. {uni.get('name')} — {uni.get('country')}** | {rank}")

        if uni.get("why_recommended"):
            msg_lines.append(uni["why_recommended"])

        if uni.get("backlog_policy"):
            msg_lines.append(f"• 📋 {uni['backlog_policy']}")

        scholarships = uni.get("scholarships") or []
        if scholarships and isinstance(scholarships[0], dict) and scholarships[0].get("url"):
            msg_lines.append("• 🏆 **Scholarships:**")
            msg_lines.append("  | Name | Basis | Amount | Deadline |")
            msg_lines.append("  |------|-------|--------|----------|")
            for s in scholarships[:3]:
                if isinstance(s, dict):
                    msg_lines.append(
                        f"  | [{s.get('name','N/A')}]({s.get('url','#')}) | "
                        f"{s.get('basis','Merit')} | "
                        f"{s.get('amount_description','N/A')} | "
                        f"{s.get('deadline','N/A')} |"
                    )
        elif uni.get("has_scholarships"):
            msg_lines.append("• 🏆 Scholarships available — see university website")

        if uni.get("website"):
            msg_lines.append(f"• 🌐 [{uni.get('name')} website]({uni['website']})")
        msg_lines.append("")

    if comparison.get("recommendation_summary"):
        msg_lines.append("**📊 Summary**")
        msg_lines.append(comparison["recommendation_summary"])

    return {
        **state,
        "recommended_universities": recommendations,
        "university_comparison": comparison,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens1 + tokens2,
        "message": "\n".join(msg_lines),
    }
