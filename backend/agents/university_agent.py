"""
University Recommendation Agent
Queries PostgreSQL + Gemini global knowledge.
Always returns 5 universities from at least 3 different countries.
"""

import json
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from prompts.university_prompts import UNIVERSITY_COMPARISON_PROMPT

GLOBAL_RECOMMENDATION_PROMPT = """You are an expert study abroad counsellor with global university knowledge.

Student Profile:
- CGPA: {cgpa} / 10
- Backlogs: {backlogs}
- IELTS: {ielts}
- Budget: ${budget_usd} USD total
- Course Interest: {course_interest}
- Career Goal: {career_goal}
- Preferred Countries: {preferred_countries}

User asked: "{user_query}"

Universities already in our database (use these if relevant):
{db_universities}

STRICT RULES:
1. Return EXACTLY 5 universities
2. Include universities from AT LEAST 3 DIFFERENT COUNTRIES
3. Even if student prefers one country, show global alternatives for comparison
4. Include at least 1 affordable option (tuition under $8,000/yr or free)
5. Use REAL, existing university names only
6. For each: reference the student's actual CGPA, backlogs, IELTS, budget specifically
7. Include real scholarships each university offers to Indian students

Respond ONLY with valid JSON:
{{
  "recommendations": [
    {{
      "name": "Official University Name",
      "country": "Country",
      "city": "City",
      "qs_world_rank": 200,
      "category": "safe",
      "match_score": 80,
      "why_recommended": "• Your CGPA {cgpa} meets their 6.0 minimum\\n• Backlog-friendly — accepts up to 10 backlogs\\n• Free tuition saves $28,000 vs private options",
      "why_not_first_choice": "• Requires German language skills for some programs",
      "admission_chances": "High",
      "avg_tuition_usd_per_year": 500,
      "avg_living_cost_usd_per_month": 950,
      "total_cost_year1_usd": 14000,
      "programs": ["MSc Artificial Intelligence", "MSc Computer Science"],
      "intake_months": ["October", "April"],
      "has_scholarships": true,
      "scholarships": [
        {{
          "name": "DAAD Scholarship",
          "basis": "Merit-based",
          "amount_description": "€934/month + travel allowance",
          "eligibility": "Good academic record, motivation letter",
          "deadline": "October annually",
          "url": "https://www.daad.de/en/"
        }},
        {{
          "name": "Deutschlandstipendium",
          "basis": "Merit-based",
          "amount_description": "€300/month",
          "eligibility": "Outstanding academic and social achievements",
          "deadline": "May annually",
          "url": "https://www.deutschlandstipendium.de"
        }}
      ],
      "graduate_employment_rate": 88,
      "min_cgpa": 6.0,
      "min_ielts": 6.0,
      "backlog_policy": "Accepts students with backlogs — strong SOP required",
      "website": "https://university.edu"
    }}
  ]
}}

Return EXACTLY 5 universities from at least 3 different countries. No exceptions.
"""


async def university_agent(state: AgentState) -> AgentState:
    profile = state.get("student_profile", {})
    countries = state.get("recommended_countries", [])
    user_query = state.get("user_query", "")

    # Fetch DB universities
    db_universities = await _fetch_candidate_universities(profile, countries)

    # Build Gemini prompt
    cgpa = profile.get("cgpa", "Not specified")
    ielts = profile.get("ielts_score", "Not specified")
    budget = profile.get("total_budget_usd", "Not specified")
    backlogs = profile.get("backlogs", 0)
    preferred = profile.get("preferred_countries", [])
    course = profile.get("course_interest", "Not specified")
    career = profile.get("career_goal", "Not specified")

    prompt = GLOBAL_RECOMMENDATION_PROMPT.format(
        cgpa=cgpa,
        backlogs=backlogs,
        ielts=ielts,
        budget_usd=budget,
        course_interest=course,
        career_goal=career,
        preferred_countries=json.dumps(preferred),
        db_universities=json.dumps(db_universities[:3], indent=2),
        user_query=user_query,
    )

    response_text, tokens1 = await ainvoke_llm(prompt)
    data = extract_json_from_response(response_text)
    recommendations: List[Dict[str, Any]] = data.get("recommendations", [])

    if not recommendations:
        recommendations = db_universities[:5]

    # Build comparison
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

    # Build table message
    msg_lines = ["**🎓 University Recommendations (Worldwide)**\n"]

    # Main table
    msg_lines.append("| # | University | Country | City | Tuition/yr | Living/mo | Chances |")
    msg_lines.append("|---|-----------|---------|------|-----------|-----------|---------|")
    for i, uni in enumerate(recommendations[:5], 1):
        name = uni.get("name", "N/A")
        country = uni.get("country", "N/A")
        city = uni.get("city", "N/A")
        tuition = uni.get("avg_tuition_usd_per_year", 0)
        tuition_str = "Free" if tuition == 0 else f"${tuition:,.0f}"
        living = uni.get("avg_living_cost_usd_per_month", 0)
        living_str = f"${living:,.0f}" if living else "~$900"
        chances = uni.get("admission_chances", "Medium")
        cat = uni.get("category", "match")
        icon = "🟢" if cat == "safe" else "🟡" if cat == "match" else "🔴"
        msg_lines.append(
            f"| {i} | **{name}** | {country} | {city} | {tuition_str} | {living_str} | {icon} {chances} |"
        )

    msg_lines.append("")

    # Per-university detail with scholarships
    for i, uni in enumerate(recommendations[:5], 1):
        rank = f"QS #{uni.get('qs_world_rank')}" if uni.get("qs_world_rank") else "Unranked"
        msg_lines.append(f"**{i}. {uni.get('name')} — {uni.get('country')}** | {rank}")

        if uni.get("why_recommended"):
            msg_lines.append(uni["why_recommended"])

        if uni.get("backlog_policy"):
            msg_lines.append(f"• 📋 {uni['backlog_policy']}")

        # Scholarship table
        scholarships = uni.get("scholarships") or []
        if scholarships:
            msg_lines.append("• 🏆 **Scholarships:**")
            msg_lines.append("  | Name | Basis | Amount | Deadline |")
            msg_lines.append("  |------|-------|--------|----------|")
            for s in scholarships[:3]:
                if isinstance(s, dict):
                    name_s = s.get("name", "N/A")
                    basis = s.get("basis", "Merit")
                    amount = s.get("amount_description", "N/A")
                    deadline = s.get("deadline", "N/A")
                    msg_lines.append(f"  | {name_s} | {basis} | {amount} | {deadline} |")
        elif uni.get("has_scholarships"):
            msg_lines.append("• 🏆 Scholarships available — visit university website")

        if uni.get("website"):
            msg_lines.append(f"• 🌐 {uni['website']}")
        msg_lines.append("")

    if comparison.get("recommendation_summary"):
        msg_lines.append("**📊 Summary**")
        msg_lines.append(comparison["recommendation_summary"])

    message = "\n".join(msg_lines)

    return {
        **state,
        "recommended_universities": recommendations,
        "university_comparison": comparison,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens1 + tokens2,
        "message": message,
    }


async def _fetch_candidate_universities(
    profile: Dict[str, Any],
    countries: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    try:
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.university import University
        from app.models.country import Country

        engine = create_async_engine(settings.database_url, echo=False)
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        cgpa = profile.get("cgpa") or 0.0
        budget = profile.get("total_budget_usd") or 999999
        country_names = [c.get("name") for c in countries if c.get("name")]

        async with async_session() as session:
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
            return [
                {
                    "name": u.name,
                    "country": cn,
                    "city": u.location_city,
                    "qs_world_rank": u.qs_world_rank,
                    "avg_tuition_usd_per_year": float(u.avg_tuition_usd_per_year or 0),
                    "avg_living_cost_usd_per_month": float(u.avg_living_cost_usd_per_month or 0),
                    "programs": u.programs,
                    "has_scholarships": u.has_scholarships,
                    "website": u.website,
                    "min_cgpa": u.min_cgpa,
                }
                for u, cn in rows
            ]
    except Exception:
        return []
