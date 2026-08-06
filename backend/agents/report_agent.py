"""
Report Generator Agent – builds final report and context-aware chat reply.
"""

import json
from typing import Any, Dict

from agents.llm import ainvoke_llm
from agents.state import AgentState
from prompts.report_prompts import EXECUTIVE_SUMMARY_PROMPT, FINAL_RECOMMENDATION_PROMPT


async def report_agent(state: AgentState) -> AgentState:
    profile = state.get("student_profile", {})
    universities = state.get("recommended_universities", [])
    countries = state.get("recommended_countries", [])
    scholarships = state.get("matched_scholarships", [])
    finance = state.get("finance_breakdown", {})
    timeline = state.get("application_timeline", [])
    user_query = state.get("user_query", "")

    # ── Executive summary ─────────────────────────────────────────────────────
    summary_prompt = EXECUTIVE_SUMMARY_PROMPT.format(
        profile_summary=state.get("profile_summary", ""),
        top_universities=json.dumps(universities[:3], indent=2),
        top_scholarships=json.dumps(scholarships[:3], indent=2),
        finance_summary=json.dumps(
            finance.get("breakdowns", [])[:3] if finance else [], indent=2
        ),
        timeline_phases=json.dumps(
            [t.get("phase") for t in timeline[:5]], indent=2
        ),
    )
    summary_text, tokens1 = await ainvoke_llm(summary_prompt, use_search=True)

    # ── Final recommendation ──────────────────────────────────────────────────
    rec_prompt = FINAL_RECOMMENDATION_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        universities=json.dumps(universities[:5], indent=2),
        scholarships=json.dumps(scholarships[:3], indent=2),
        finance=json.dumps(finance, indent=2),
        career_goal=profile.get("career_goal", "Not specified"),
    )
    rec_text, tokens2 = await ainvoke_llm(rec_prompt, use_search=False)

    # ── Assemble report ───────────────────────────────────────────────────────
    final_report: Dict[str, Any] = {
        "executive_summary": summary_text.strip(),
        "final_recommendation": rec_text.strip(),
        "student_profile": profile,
        "profile_summary": state.get("profile_summary", ""),
        "recommended_countries": countries,
        "recommended_universities": universities,
        "university_comparison": state.get("university_comparison", {}),
        "matched_scholarships": scholarships,
        "finance_breakdown": finance,
        "application_timeline": timeline,
        "metadata": {
            "session_id": state.get("session_id"),
            "agents_executed": state.get("agents_executed", []),
        },
    }

    executed = list(state.get("agents_executed", []))
    executed.append("report_agent")

    finance_breakdowns = finance.get("breakdowns", []) if finance else []

    # ── Build dynamic message based on what agents ran ───────────────────────
    agents_ran = state.get("agents_executed", [])
    user_query = state.get("user_query", "").lower()

    # If query is specifically about universities → lead with university table
    if "university" in user_query or "universities" in user_query or "suggest" in user_query or "recommend" in user_query:
        # Build university table as primary response
        msg_lines = []

        if universities:
            msg_lines.append("**🎓 Recommended Universities**\n")
            msg_lines.append("| # | University | Location | Tuition/yr | Living/mo | Scholarships | Chances |")
            msg_lines.append("|---|-----------|----------|-----------|-----------|--------------|---------|")
            for i, uni in enumerate(universities[:6], 1):
                name = uni.get('name', 'N/A')
                country = uni.get('country', 'N/A')
                city = uni.get('city') or uni.get('location_city', '')
                location = f"{city}, {country}" if city else country
                tuition = uni.get('avg_tuition_usd_per_year', 0)
                tuition_str = f"${tuition:,.0f}" if tuition else "Free"
                living = uni.get('avg_living_cost_usd_per_month', 0)
                living_str = f"${living:,.0f}" if living else "~$900"
                has_sch = uni.get('has_scholarships') or bool(uni.get('scholarships'))
                sch_str = "✅ Yes" if has_sch else "❌ No"
                chances = uni.get('admission_chances', 'Medium')
                cat = uni.get('category', 'match')
                icon = "🟢" if cat == "safe" else "🟡" if cat == "match" else "🔴"
                msg_lines.append(f"| {i} | **{name}** | {location} | {tuition_str} | {living_str} | {sch_str} | {icon} {chances} |")
            msg_lines.append("")

            # Scholarship details per university
            for i, uni in enumerate(universities[:6], 1):
                scholarships_list = uni.get('scholarships') or []
                msg_lines.append(f"**{i}. {uni.get('name')}**")
                if uni.get('why_recommended'):
                    msg_lines.append(uni.get('why_recommended'))
                if scholarships_list:
                    msg_lines.append("• 🏆 **Scholarships:**")
                    msg_lines.append("  | Scholarship | Basis | Amount |")
                    msg_lines.append("  |-------------|-------|--------|")
                    for s in scholarships_list[:3]:
                        if isinstance(s, dict):
                            msg_lines.append(f"  | {s.get('name','N/A')} | {s.get('basis','Merit')} | {s.get('amount_description','N/A')} |")
                elif uni.get('has_scholarships'):
                    msg_lines.append("• 🏆 Scholarships available (check website)")
                if uni.get('website'):
                    msg_lines.append(f"• 🌐 {uni.get('website')}")
                if uni.get('backlog_policy'):
                    msg_lines.append(f"• 📋 Backlog policy: {uni.get('backlog_policy')}")
                msg_lines.append("")

        # Add final recommendation from report
        if rec_text.strip():
            msg_lines.append(rec_text.strip())

        msg_lines.append("\n📄 Full PDF report saved to the **Reports** section.")
        message = "\n".join(msg_lines)

    else:
        # For full plan queries — show complete summary
        message_parts = [summary_text.strip(), ""]
        if rec_text.strip():
            message_parts.append(rec_text.strip())
        if finance_breakdowns:
            message_parts.append("\n**💰 Cost Summary**")
            for b in finance_breakdowns[:3]:
                uni_name = b.get("university", "N/A")
                cost = b.get("total_year1_usd", 0)
                net = b.get("net_cost_year1_usd", cost)
                message_parts.append(f"• {uni_name}: ${cost:,.0f}/yr total | ${net:,.0f}/yr after scholarships")
        if timeline:
            message_parts.append("\n**📅 Timeline Highlights**")
            for t in timeline[:4]:
                message_parts.append(f"• Month {t.get('month_offset', 0) + 1}: {t.get('milestone', '')} [{t.get('priority', '').upper()}]")
        message_parts.append("\n📄 Full PDF report saved to the **Reports** section.")
        message = "\n".join(message_parts)

    return {
        **state,
        "final_report": final_report,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens1 + tokens2,
        "message": message,
    }
