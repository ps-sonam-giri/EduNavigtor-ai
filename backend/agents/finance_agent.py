"""
Finance Agent
Calculates a detailed budget breakdown per university/country:
- Tuition
- Living cost
- Visa fee
- Health insurance
- Miscellaneous
Produces a comparison table and affordability assessment.
"""

import json
from typing import Any, Dict, List

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from prompts.finance_prompts import FINANCE_BREAKDOWN_PROMPT


async def finance_agent(state: AgentState) -> AgentState:
    """
    Produces a detailed finance_breakdown dict covering each
    recommended university/country combination.
    """
    profile = state.get("student_profile", {})
    universities = state.get("recommended_universities", [])
    countries = state.get("recommended_countries", [])
    scholarships = state.get("matched_scholarships", [])

    # Build finance context
    finance_context = _build_finance_context(universities, countries)

    prompt = FINANCE_BREAKDOWN_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        finance_context=json.dumps(finance_context, indent=2),
        scholarships=json.dumps(
            [{"name": s.get("name"), "amount_usd": s.get("amount_usd")} for s in scholarships[:5]],
            indent=2,
        ),
        budget_usd=profile.get("total_budget_usd", "Not specified"),
    )

    response_text, tokens = await ainvoke_llm(prompt, use_search=True)
    finance_data = extract_json_from_response(response_text)

    # Ensure we always have a valid structure
    if not finance_data:
        finance_data = _calculate_finance_fallback(universities, countries, profile)

    executed = list(state.get("agents_executed", []))
    executed.append("finance_agent")

    # Build message for finance-only queries
    breakdowns = finance_data.get("breakdowns", [])
    if breakdowns:
        msg_lines = ["**💰 Budget Breakdown**\n"]
        for b in breakdowns[:4]:
            msg_lines.append(f"**{b.get('university')} ({b.get('country')})**")
            msg_lines.append(f"• Tuition: ${b.get('tuition_per_year_usd', 0):,.0f}/yr")
            msg_lines.append(f"• Living cost: ${b.get('living_cost_per_year_usd', 0):,.0f}/yr")
            msg_lines.append(f"• Visa + Insurance: ${(b.get('visa_fee_usd', 0) + b.get('health_insurance_per_year_usd', 0)):,.0f}")
            msg_lines.append(f"• **Total Year 1: ${b.get('total_year1_usd', 0):,.0f}** (₹{b.get('total_year1_inr', 0):,.0f})")
            if b.get("scholarship_savings_usd"):
                msg_lines.append(f"• After scholarship: ${b.get('net_cost_year1_usd', 0):,.0f}/yr")
            affordable = b.get("affordable")
            msg_lines.append(f"• {'✅ Within budget' if affordable else '⚠️ Exceeds budget'}\n")

        if finance_data.get("loan_advice"):
            msg_lines.append(f"**📋 Loan Advice**")
            msg_lines.append(finance_data["loan_advice"])

        message = "\n".join(msg_lines)
    else:
        message = "Could not calculate budget. Please ensure your profile has a total budget set."

    return {
        **state,
        "finance_breakdown": finance_data,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
        "message": message,
    }


def _build_finance_context(
    universities: List[Dict[str, Any]],
    countries: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Build per-university finance context for the LLM prompt."""
    context = []
    country_map = {c.get("name"): c for c in countries}

    for uni in universities[:5]:
        country_data = country_map.get(uni.get("country"), {})
        tuition = uni.get("avg_tuition_usd_per_year", 0) or 0
        living_monthly = (
            uni.get("avg_living_cost_usd_per_month")
            or country_data.get("avg_living_cost_usd_per_month", 1000)
            or 1000
        )
        visa = country_data.get("visa_fee_usd", 200) or 200
        insurance = country_data.get("health_insurance_usd_per_year", 500) or 500

        context.append(
            {
                "university": uni.get("name"),
                "country": uni.get("country"),
                "tuition_per_year_usd": tuition,
                "living_cost_per_month_usd": living_monthly,
                "living_cost_per_year_usd": living_monthly * 12,
                "visa_fee_usd": visa,
                "health_insurance_per_year_usd": insurance,
                "application_fee_usd": uni.get("application_fee_usd", 75) or 75,
                "misc_per_year_usd": 2000,
                "total_year1_usd": tuition + (living_monthly * 12) + visa + insurance + 2000,
            }
        )
    return context


def _calculate_finance_fallback(
    universities: List[Dict],
    countries: List[Dict],
    profile: Dict,
) -> Dict[str, Any]:
    """
    Rule-based finance calculation as fallback when LLM fails to return JSON.
    """
    context = _build_finance_context(universities, countries)
    student_budget = profile.get("total_budget_usd") or 0

    breakdowns = []
    for item in context:
        total = item["total_year1_usd"]
        affordable = student_budget >= total if student_budget else None
        breakdowns.append(
            {
                **item,
                "affordable": affordable,
                "budget_gap_usd": max(0, total - student_budget) if student_budget else None,
            }
        )

    return {
        "breakdowns": breakdowns,
        "cheapest_option": min(context, key=lambda x: x["total_year1_usd"])
        if context
        else None,
        "student_budget_usd": student_budget,
        "currency_note": "All amounts in USD. Exchange rate: 1 USD ≈ 83 INR (verify current rate).",
    }

