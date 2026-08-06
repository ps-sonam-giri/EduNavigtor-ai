"""
Orchestrator Agent – LangGraph workflow entry point.

Decides which agents to run based on the query, maintains workflow state,
and prevents unnecessary agent execution using conditional edges.
"""

import json
import time
import uuid
from typing import Any, Dict, List, Optional

from langgraph.graph import END, StateGraph

from agents.finance_agent import finance_agent
from agents.llm import ainvoke_llm, extract_json_from_response, llm_fast
from agents.profile_agent import profile_agent
from agents.report_agent import report_agent
from agents.scholarship_agent import scholarship_agent
from agents.state import AgentState
from agents.timeline_agent import timeline_agent
from agents.university_agent import university_agent
from prompts.orchestrator_prompts import ORCHESTRATOR_ROUTING_PROMPT


# ── Node: Orchestrator decides which agents to call ───────────────────────────

async def orchestrator_node(state: AgentState) -> AgentState:
    """
    Analyses the user query and conversation history.
    If it's a follow-up question, answers directly.
    Otherwise routes to relevant agents.
    """
    query = state.get("user_query", "")
    profile = state.get("student_profile", {})
    profile_complete = state.get("profile_complete", False)
    chat_history = state.get("chat_history", [])

    # Build conversation context for routing
    recent_history = ""
    if chat_history:
        recent = chat_history[-6:]  # last 6 messages
        recent_history = "\n".join([
            f"{m.get('role', 'user').upper()}: {m.get('content', '')[:200]}"
            if isinstance(m, dict)
            else f"{getattr(m, 'role', 'user').upper()}: {getattr(m, 'content', '')[:200]}"
            for m in recent
        ])

    routing_prompt = ORCHESTRATOR_ROUTING_PROMPT.format(
        query=query,
        profile_summary=json.dumps(profile, indent=2),
        profile_complete=profile_complete,
        agents_available=[
            "profile_agent", "university_agent", "scholarship_agent",
            "finance_agent", "timeline_agent", "report_agent",
        ],
    )

    # Add history context to routing prompt
    if recent_history:
        routing_prompt += f"\n\nRecent conversation:\n{recent_history}"

    response, tokens = await ainvoke_llm(routing_prompt, fast=True)
    routing_data = extract_json_from_response(response)

    agents_to_run: List[str] = routing_data.get("agents_to_run", _default_agents(query, profile_complete))
    reasoning: str = routing_data.get("reasoning", "Running standard workflow.")
    direct_answer: bool = routing_data.get("direct_answer", False)

    # If direct_answer mode, generate response from conversation context + web search
    if direct_answer and not agents_to_run and recent_history:
        direct_prompt = f"""You are EduPilot AI, a study abroad advisor for Indian students.
Use Google Search to find current, accurate information when needed.

Answer this question DIRECTLY and SPECIFICALLY based on the conversation history.
Use bullet points. Show tables where helpful. Reference actual numbers.

Conversation history:
{recent_history}

Student question: {query}

Rules:
- If asking about universities → show table with name, country, tuition, chances
- If asking about cost/budget → show exact USD and INR breakdown
- If asking about scholarships → list with name, amount, basis, deadline
- If asking about timeline → give month-by-month milestones
- If asking about visa → give specific steps and documents list
- Always use the student's actual profile numbers from the conversation
- Never say "as mentioned earlier" — always give the actual answer
- Use web search for current 2025-2026 data on fees, deadlines, rankings

Answer now with structured bullet points and tables:"""

        # Use web search for direct answers too
        direct_response, tokens2 = await ainvoke_llm(direct_prompt, use_search=True)
        tokens += tokens2

        return {
            **state,
            "agents_to_run": [],
            "orchestrator_reasoning": reasoning,
            "agents_executed": ["orchestrator"],
            "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
            "message": direct_response,
        }

    return {
        **state,
        "agents_to_run": agents_to_run,
        "orchestrator_reasoning": reasoning,
        "agents_executed": ["orchestrator"],
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
    }


# ── Country recommendation (lightweight, rule-based + LLM) ───────────────────

async def country_recommendation_node(state: AgentState) -> AgentState:
    """
    Recommends countries based on budget, course, and profile.
    Uses a simple rule-based scoring + LLM explanation.
    """
    profile = state.get("student_profile", {})
    preferred = profile.get("preferred_countries", [])

    # Fetch country data
    countries = await _fetch_countries(preferred)

    # Score countries
    scored = _score_countries(countries, profile)
    top_countries = scored[:4]

    # Get LLM to explain WHY each country
    from prompts.orchestrator_prompts import COUNTRY_REASONING_PROMPT

    prompt = COUNTRY_REASONING_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        countries=json.dumps(top_countries, indent=2),
    )
    response, tokens = await ainvoke_llm(prompt)
    enriched = extract_json_from_response(response)
    recommended = enriched.get("recommended_countries", top_countries)

    executed = list(state.get("agents_executed", []))
    executed.append("country_recommendation")

    return {
        **state,
        "recommended_countries": recommended,
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
    }


def _score_countries(countries: List[Dict], profile: Dict) -> List[Dict]:
    """Rule-based country scoring."""
    budget = profile.get("total_budget_usd") or 50000
    preferred = [c.lower() for c in (profile.get("preferred_countries") or [])]
    course = (profile.get("course_interest") or "").lower()

    scored = []
    for c in countries:
        score = 0
        name = c.get("name", "").lower()
        avg_tuition = c.get("avg_tuition_usd_per_year") or 25000

        # Budget fit
        if avg_tuition <= budget * 0.6:
            score += 30
        elif avg_tuition <= budget * 0.8:
            score += 20
        elif avg_tuition <= budget:
            score += 10

        # Preferred country bonus
        if name in preferred:
            score += 25

        # Post-study work rights
        psw = c.get("post_study_work_years") or 0
        score += min(psw * 5, 20)

        # Course relevance (simplified)
        popular = [x.lower() for x in (c.get("popular_courses") or [])]
        if any(course in p for p in popular):
            score += 15

        scored.append({**c, "match_score": score})

    return sorted(scored, key=lambda x: x["match_score"], reverse=True)


async def _fetch_countries(preferred: List[str]) -> List[Dict]:
    """Fetch countries from DB."""
    try:
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.country import Country

        engine = create_async_engine(settings.database_url, echo=False)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            result = await session.execute(
                select(Country).where(Country.is_active == True).order_by(Country.name)
            )
            rows = result.scalars().all()
            await engine.dispose()
            return [
                {
                    "name": c.name,
                    "code": c.code,
                    "avg_tuition_usd_per_year": float(c.avg_tuition_usd_per_year or 0),
                    "avg_living_cost_usd_per_month": float(c.avg_living_cost_usd_per_month or 0),
                    "visa_fee_usd": float(c.visa_fee_usd or 0),
                    "health_insurance_usd_per_year": float(c.health_insurance_usd_per_year or 0),
                    "post_study_work_years": c.post_study_work_years,
                    "overview": c.overview,
                    "pros": c.pros,
                    "cons": c.cons,
                    "popular_courses": c.popular_courses,
                }
                for c in rows
            ]
    except Exception:
        return []


# ── Conditional routing functions ─────────────────────────────────────────────

def should_run_profile(state: AgentState) -> str:
    # If direct answer already set, go to END
    if state.get("message") and not state.get("agents_to_run"):
        return "end"
    agents = state.get("agents_to_run", [])
    return "profile_agent" if "profile_agent" in agents else "country_recommendation"


def should_run_university(state: AgentState) -> str:
    agents = state.get("agents_to_run", [])
    return "university_agent" if "university_agent" in agents else "scholarship_agent"


def should_run_scholarship(state: AgentState) -> str:
    agents = state.get("agents_to_run", [])
    return "scholarship_agent" if "scholarship_agent" in agents else "finance_agent"


def should_run_finance(state: AgentState) -> str:
    agents = state.get("agents_to_run", [])
    return "finance_agent" if "finance_agent" in agents else "timeline_agent"


def should_run_timeline(state: AgentState) -> str:
    agents = state.get("agents_to_run", [])
    return "timeline_agent" if "timeline_agent" in agents else "report_agent"


def should_run_report(state: AgentState) -> str:
    agents = state.get("agents_to_run", [])
    return "report_agent" if "report_agent" in agents else END


# ── Build LangGraph workflow ──────────────────────────────────────────────────

def build_workflow() -> StateGraph:
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("profile_agent", profile_agent)
    graph.add_node("country_recommendation", country_recommendation_node)
    graph.add_node("university_agent", university_agent)
    graph.add_node("scholarship_agent", scholarship_agent)
    graph.add_node("finance_agent", finance_agent)
    graph.add_node("timeline_agent", timeline_agent)
    graph.add_node("report_agent", report_agent)

    # Entry point
    graph.set_entry_point("orchestrator")

    # Orchestrator decides which path to take
    graph.add_conditional_edges(
        "orchestrator",
        should_run_profile,
        {
            "profile_agent": "profile_agent",
            "country_recommendation": "country_recommendation",
            "end": END,
        },
    )

    # Profile → Country
    graph.add_edge("profile_agent", "country_recommendation")

    # Country → University (conditional)
    graph.add_conditional_edges(
        "country_recommendation",
        should_run_university,
        {
            "university_agent": "university_agent",
            "scholarship_agent": "scholarship_agent",
        },
    )

    # University → Scholarship (conditional)
    graph.add_conditional_edges(
        "university_agent",
        should_run_scholarship,
        {
            "scholarship_agent": "scholarship_agent",
            "finance_agent": "finance_agent",
        },
    )

    # Scholarship → Finance (conditional)
    graph.add_conditional_edges(
        "scholarship_agent",
        should_run_finance,
        {
            "finance_agent": "finance_agent",
            "timeline_agent": "timeline_agent",
        },
    )

    # Finance → Timeline (conditional)
    graph.add_conditional_edges(
        "finance_agent",
        should_run_timeline,
        {
            "timeline_agent": "timeline_agent",
            "report_agent": "report_agent",
        },
    )

    # Timeline → Report (conditional)
    graph.add_conditional_edges(
        "timeline_agent",
        should_run_report,
        {
            "report_agent": "report_agent",
            END: END,
        },
    )

    graph.add_edge("report_agent", END)

    return graph.compile()


# Compiled workflow (singleton)
_workflow = None


def get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow


# ── Public entry point ────────────────────────────────────────────────────────

async def run_orchestrator(
    query: str,
    session_id: str,
    student_profile: Optional[Any],
    user_id: str,
    db: Any,
    chat_history: Optional[List] = None,
) -> Dict[str, Any]:
    """
    Main entry point called by the FastAPI route.
    Returns the final AgentState as a plain dict.
    """
    # Convert SQLAlchemy model to dict if needed
    profile_data: Dict = {}
    if student_profile:
        for col in [
            "cgpa", "cgpa_scale", "backlogs", "degree", "specialization",
            "ielts_score", "toefl_score", "gre_score", "gmat_score",
            "preferred_countries", "course_interest", "career_goal",
            "target_intake", "total_budget_usd", "financial_background",
            "work_experience_years",
        ]:
            val = getattr(student_profile, col, None)
            if val is not None:
                profile_data[col] = val

    initial_state: AgentState = {
        "user_query": query,
        "session_id": session_id,
        "user_id": user_id,
        "chat_history": [
            {"role": getattr(m, "role", m.get("role", "user") if isinstance(m, dict) else "user"),
             "content": getattr(m, "content", m.get("content", "") if isinstance(m, dict) else "")}
            for m in (chat_history or [])
        ],
        "student_profile": profile_data,
        "agents_to_run": [],
        "agents_executed": [],
        "errors": [],
        "total_tokens_used": 0,
    }

    workflow = get_workflow()
    start = time.time()
    final_state: AgentState = await workflow.ainvoke(initial_state)
    elapsed_ms = (time.time() - start) * 1000

    # Pick the most relevant message based on query intent
    query_lower = query.lower()
    message = final_state.get("message", "")

    # If a specific agent ran for a specific query, use its message directly
    agents_ran = final_state.get("agents_executed", [])

    # Priority: pick message from the most specific agent for the query
    if any(w in query_lower for w in ["scholarship", "funding", "grant", "eligible for"]):
        # scholarship query → use scholarship agent message if available
        if "scholarship_agent" in agents_ran:
            # Re-build scholarship message from state
            matched = final_state.get("matched_scholarships", [])
            if matched:
                msg_lines = ["**🏆 Scholarships You Are Eligible For**\n"]
                msg_lines.append("| Scholarship | Provider | Basis | Amount | Eligibility |")
                msg_lines.append("|-------------|----------|-------|--------|-------------|")
                for s in matched[:6]:
                    n = s.get("name", "N/A")
                    p = s.get("provider", "N/A")
                    basis = s.get("scholarship_basis", "Merit-based")
                    amt = s.get("amount_description", "N/A")
                    match = s.get("eligibility_match", "Medium")
                    icon = "🟢" if match == "High" else "🟡" if match == "Medium" else "🔴"
                    msg_lines.append(f"| **{n}** | {p} | {basis} | {amt} | {icon} {match} |")
                msg_lines.append("")
                for s in matched[:5]:
                    msg_lines.append(f"**{s.get('name')}**")
                    msg_lines.append(f"• Provider: {s.get('provider', 'N/A')}")
                    msg_lines.append(f"• Basis: **{s.get('scholarship_basis', 'Merit-based')}**")
                    msg_lines.append(f"• Amount: {s.get('amount_description', 'N/A')}")
                    criteria = s.get("eligibility_criteria", "")
                    if criteria:
                        msg_lines.append(f"• Eligibility: {criteria}")
                    if s.get("why_good_fit"):
                        msg_lines.append(s["why_good_fit"])
                    if s.get("gap_to_address"):
                        msg_lines.append(f"⚠️ {s['gap_to_address']}")
                    if s.get("deadline"):
                        msg_lines.append(f"• Deadline: **{s['deadline']}**")
                    if s.get("application_url"):
                        msg_lines.append(f"• Apply: {s['application_url']}")
                    msg_lines.append("")
                total = final_state.get("matched_scholarships_meta", {}).get("total_savings", 0)
                if total:
                    msg_lines.append(f"**💰 Total potential savings: ${total:,.0f}**")
                message = "\n".join(msg_lines)

    elif any(w in query_lower for w in ["university", "universities", "college", "suggest", "recommend", "where should"]):
        if "university_agent" in agents_ran:
            unis = final_state.get("recommended_universities", [])
            if unis and "| # | University" in (final_state.get("message") or ""):
                message = final_state.get("message", message)

    elif any(w in query_lower for w in ["cost", "budget", "fee", "afford", "how much", "price", "expense"]):
        if "finance_agent" in agents_ran:
            breakdowns = (final_state.get("finance_breakdown") or {}).get("breakdowns", [])
            if breakdowns:
                msg_lines = ["**💰 Budget Breakdown**\n"]
                msg_lines.append("| University | Country | Tuition/yr | Living/yr | Total Year 1 | After Scholarship |")
                msg_lines.append("|-----------|---------|-----------|-----------|-------------|------------------|")
                for b in breakdowns[:5]:
                    msg_lines.append(
                        f"| {b.get('university','N/A')} | {b.get('country','N/A')} | "
                        f"${b.get('tuition_per_year_usd',0):,.0f} | "
                        f"${b.get('living_cost_per_year_usd',0):,.0f} | "
                        f"${b.get('total_year1_usd',0):,.0f} | "
                        f"${b.get('net_cost_year1_usd', b.get('total_year1_usd',0)):,.0f} |"
                    )
                msg_lines.append("")
                fin = final_state.get("finance_breakdown", {})
                if fin.get("loan_advice"):
                    msg_lines.append("**📋 Loan Advice**")
                    msg_lines.append(fin["loan_advice"])
                message = "\n".join(msg_lines)

    elif any(w in query_lower for w in ["timeline", "roadmap", "plan", "when", "schedule", "step"]):
        if "timeline_agent" in agents_ran:
            tl = final_state.get("application_timeline", [])
            if tl:
                msg_lines = ["**📅 Your Application Timeline**\n"]
                phase = None
                for item in tl[:10]:
                    if item.get("phase") != phase:
                        phase = item.get("phase")
                        msg_lines.append(f"\n**{phase}**")
                    p = item.get("priority", "medium")
                    icon = "🔴" if p == "critical" else "🟡" if p == "high" else "🟢"
                    msg_lines.append(f"• {icon} Month {item.get('month_offset',0)+1}: **{item.get('milestone','')}**")
                    msg_lines.append(f"  {item.get('description','')}")
                message = "\n".join(msg_lines)

    # Persist agent logs to DB
    await _persist_logs(final_state, user_id, session_id, db)

    return {
        "output": {
            "message": final_state.get("message", ""),
            "final_report": final_state.get("final_report", {}),
            "recommended_universities": final_state.get("recommended_universities", []),
            "recommended_countries": final_state.get("recommended_countries", []),
            "matched_scholarships": final_state.get("matched_scholarships", []),
            "finance_breakdown": final_state.get("finance_breakdown", {}),
            "application_timeline": final_state.get("application_timeline", []),
        },
        "agents_executed": final_state.get("agents_executed", []),
        "reasoning": final_state.get("orchestrator_reasoning", ""),
        "tokens_used": final_state.get("total_tokens_used", 0),
        "execution_time_ms": elapsed_ms,
    }


async def _persist_logs(state: AgentState, user_id: str, session_id: str, db: Any):
    """Save each agent's execution as an AgentLog record."""
    try:
        import uuid as uuid_mod
        from app.models.agent_log import AgentLog

        for agent_name in state.get("agents_executed", []):
            log = AgentLog(
                id=uuid_mod.uuid4(),
                user_id=uuid_mod.UUID(user_id),
                session_id=session_id,
                agent_name=agent_name,
                status="success",
                input_data={"query": state.get("user_query", "")},
                output_data=state.get("final_report", {}),
                reasoning=state.get("orchestrator_reasoning", ""),
                tokens_used=state.get("total_tokens_used", 0) // max(len(state.get("agents_executed", [1])), 1),
            )
            db.add(log)
        await db.commit()
    except Exception:
        pass  # Non-critical


def _default_agents(query: str, profile_complete: bool) -> List[str]:
    """Fallback agent list when LLM routing fails."""
    query_lower = query.lower()
    agents = ["profile_agent"]
    agents.append("country_recommendation")
    if any(w in query_lower for w in ["university", "college", "school", "recommend", "where"]):
        agents.append("university_agent")
    if any(w in query_lower for w in ["scholarship", "funding", "grant", "award"]):
        agents.append("scholarship_agent")
    if any(w in query_lower for w in ["cost", "budget", "fee", "money", "finance", "afford"]):
        agents.append("finance_agent")
    if any(w in query_lower for w in ["timeline", "plan", "when", "schedule", "roadmap"]):
        agents.append("timeline_agent")
    if any(w in query_lower for w in ["report", "summary", "complete", "full"]):
        agents.append("report_agent")
    if not any(a in agents for a in ["university_agent", "scholarship_agent"]) and profile_complete:
        agents += ["university_agent", "scholarship_agent", "finance_agent", "timeline_agent", "report_agent"]
    return agents
