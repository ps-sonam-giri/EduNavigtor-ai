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

GLOBAL_RECOMMENDATION_PROMPT = """You are an expert study abroad counsellor for Indian students. Use your latest knowledge and web search to find REAL, CURRENT university information.

Student Profile:
- CGPA: {cgpa}/10 | Backlogs: {backlogs} | IELTS: {ielts}
- Budget: ${budget_usd} USD total | Course: {course_interest}
- Career Goal: {career_goal}
- Preferred Countries: {preferred_countries}

User asked: "{user_query}"

Universities from our database (reference only):
{db_universities}

REQUIREMENTS:
1. Return EXACTLY {num_universities} universities from AT LEAST {num_countries} DIFFERENT COUNTRIES
2. Use REAL, CURRENT data — use web search for latest QS rankings, tuition fees, and deadlines
3. Match universities specifically to CGPA {cgpa}, backlogs {backlogs}, budget, and career goal
4. Include at least 1 budget-friendly option (under $10,000/yr tuition)
5. For EACH university include at least 2-3 REAL scholarships with current amounts and deadlines
6. Include scholarship application URLs
7. Reference the student's actual profile numbers in why_recommended

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
      "why_recommended": "• Your CGPA {cgpa} exceeds their minimum requirement of X.X\\n• Tuition $X/yr fits your ${budget_usd} budget\\n• Strong {course_interest} program ranked top 50 globally",
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
          "eligibility": "Good academic record, motivation letter, under 32 years",
          "deadline": "October 2025",
          "url": "https://www.daad.de/en/study-and-research-in-germany/scholarships/daad-scholarships/"
        }},
        {{
          "name": "Deutschlandstipendium",
          "basis": "Merit-based",
          "amount_description": "€300/month for minimum 2 semesters",
          "eligibility": "Outstanding academic and social achievements",
          "deadline": "May 2025",
          "url": "https://www.deutschlandstipendium.de/en/"
        }}
      ],
      "graduate_employment_rate": 88,
      "website": "https://university.edu"
    }}
  ]
}}

CRITICAL: Return EXACTLY {num_universities} universities from at least {num_countries} countries.
Each university MUST have real scholarship data with URLs. Do not say "check website".
"""


async def university_agent(state: AgentState) -> AgentState:
    profile = state.get("student_profile", {})
    countries = state.get("recommended_countries", [])
    user_query = state.get("user_query", "")

    db_universities = await _fetch_candidate_universities(profile, countries)

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
    num_countries = min(requested_count, 5)  # at least spread across countries

    prompt = GLOBAL_RECOMMENDATION_PROMPT.format(
        cgpa=cgpa, backlogs=backlogs, ielts=ielts,
        budget_usd=budget, course_interest=course, career_goal=career,
        preferred_countries=json.dumps(preferred),
        db_universities=json.dumps(db_universities[:3], indent=2),
        user_query=user_query,
        num_universities=requested_count,
        num_countries=num_countries,
    )

    # Use Google Search grounding for real-time university data
    response_text, tokens1 = await ainvoke_llm(prompt, use_search=True)
    data = extract_json_from_response(response_text)
    recommendations: List[Dict[str, Any]] = data.get("recommendations", [])

    if not recommendations:
        recommendations = db_universities[:5]

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
    msg_lines = [f"**🎓 University Recommendations ({len(recommendations)} universities)**\n"]
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


async def _fetch_candidate_universities(profile, countries):
    try:
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.university import University
        from app.models.country import Country

        engine = create_async_engine(settings.database_url, echo=False)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        cgpa = profile.get("cgpa") or 0.0
        budget = profile.get("total_budget_usd") or 999999
        country_names = [c.get("name") for c in countries if c.get("name")]

        async with session_factory() as session:
            q = (
                select(University, Country.name.label("country_name"))
                .join(Country, University.country_id == Country.id)
                .where(University.is_active == True)
                .where((University.min_cgpa == None) | (University.min_cgpa <= cgpa))
                .where((University.avg_tuition_usd_per_year == None) | (University.avg_tuition_usd_per_year <= budget))
            )
            if country_names:
                q = q.where(Country.name.in_(country_names))
            q = q.order_by(University.qs_world_rank.asc().nullslast()).limit(5)
            result = await session.execute(q)
            rows = result.all()
            await engine.dispose()
            return [{"name": u.name, "country": cn, "city": u.location_city,
                     "qs_world_rank": u.qs_world_rank,
                     "avg_tuition_usd_per_year": float(u.avg_tuition_usd_per_year or 0),
                     "programs": u.programs, "has_scholarships": u.has_scholarships}
                    for u, cn in rows]
    except Exception:
        return []
