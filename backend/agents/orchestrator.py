"""
Orchestrator Agent – ReAct Agent Loop & LangGraph State Graph.

Perceive → Decide Action → Execute Tool → Observe Result → Reflect/Verify → Finish
"""

import json
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from langgraph.graph import END, StateGraph

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from agents.verifier import verifier_node
from tools.registry import execute_tool, get_tool_schemas


REACT_DECISION_PROMPT = """You are EduPilot AI, a state-of-the-art autonomous study abroad copilot.
Your task is to help the student by deciding the BEST tool action to execute next, OR providing a beautifully formatted, executive-level final answer.

Student Profile:
{profile_summary}

User Question: "{user_query}"

Available Tools:
{tool_schemas}

Accumulated Observations / History:
{observations_summary}

{critique_context}

RULES FOR DECISION-MAKING:
1. If you need data (universities, scholarships, financial calculations, document parsing), choose a TOOL ACTION.
2. If you have gathered all necessary observations to answer the query completely, choose "finish".
3. Always base your final answer strictly on returned tool observations. Do not invent unverified facts.
4. If PREVIOUS VERIFIER CRITIQUE is present in context, you MUST either call a tool to fix the flagged issue, or finish with a corrected final_answer that resolves every flagged violation.
5. ANSWER FORMATTING REQUIREMENTS (CRITICAL FOR USER READABILITY):
   - Start with a clear Executive Summary block (e.g., 🎯 **Executive Brief**).
   - Use Markdown Tables with clean column headers for multi-item comparisons (universities, fees, scholarships).
   - Use section headers (### 🎓 Top Universities, ### 🏆 Scholarship Matches, ### 💰 Financial Breakdown, ### 📌 Action Plan).
   - Include color/emoji indicators (🟢 Safe, 🟡 Target, 🔴 Reach).
   - Include direct clickable links (`[Website](URL)` or `[Apply Link](URL)`).
   - Conclude with a 💡 **Next Steps / Action Items** list.

Respond ONLY with a valid JSON object matching ONE of these formats:

Format A (Call a Tool):
{{
  "thought": "Reasoning about what tool to call next...",
  "action": "tool_name",
  "action_input": {{ "arg1": "val1" }}
}}

Format B (Finish & Output Final Answer):
{{
  "thought": "Reasoning about why we have sufficient data...",
  "action": "finish",
  "final_answer": "Beautifully formatted executive answer with tables, structured bullet points, and actionable next steps."
}}
"""


async def agent_decide_node(state: AgentState) -> AgentState:
    """
    ReAct Agent Reasoning Step.
    Analyses accumulated observations and decides next Tool Action or Finish.
    """
    query = state.get("user_query", "")
    profile = state.get("student_profile", {})
    observations = state.get("observations", [])
    critique = state.get("verifier_critique", "")
    turn_count = state.get("turn_count", 0)

    # Format observations summary
    obs_summary = "\n".join([
        f"Step {i+1} [{obs.get('tool', 'Tool')}]: {json.dumps(obs.get('observation', obs.get('error', '')), indent=2)[:500]}"
        for i, obs in enumerate(observations)
    ]) if observations else "None yet."

    critique_context = f"PREVIOUS VERIFIER CRITIQUE (Fix these errors):\n{critique}" if critique and not state.get("verifier_passed", True) else ""

    prompt = REACT_DECISION_PROMPT.format(
        user_query=query,
        profile_summary=json.dumps(profile, indent=2),
        tool_schemas=json.dumps(get_tool_schemas(), indent=2),
        observations_summary=obs_summary,
        critique_context=critique_context,
    )

    response_text, tokens = await ainvoke_llm(prompt, fast=(turn_count > 0))
    decision = extract_json_from_response(response_text)

    thought = decision.get("thought", "Deciding next step.")
    action = decision.get("action", "finish")
    action_input = decision.get("action_input", {})
    final_answer = decision.get("final_answer", "")

    executed = list(state.get("agents_executed", []))
    executed.append(f"agent_turn_{turn_count+1}")

    if action == "finish" or not action:
        raw_msg = final_answer or response_text

        # Compute RAG Evaluation Metrics (Answer Relevancy & Faithfulness)
        from app.core.rag_evaluator import evaluate_answer_relevancy_and_faithfulness
        eval_metrics = evaluate_answer_relevancy_and_faithfulness(
            user_query=state.get("user_query", ""),
            ai_response=raw_msg,
            search_context=[str(o) for o in state.get("observations", [])]
        )

        rel_pct = int(eval_metrics["answer_relevancy"] * 100)
        faith_pct = int(eval_metrics["faithfulness"] * 100)

        eval_footer = (
            f"\n\n---\n"
            f"> 🛡️ **AI Copilot Evaluation Metrics**:\n"
            f"> - **🎯 Answer Relevancy**: **{rel_pct}%** ({eval_metrics['evaluation']['relevancy_rating']})\n"
            f"> - **🟢 Faithfulness (Grounding)**: **{faith_pct}%** ({eval_metrics['evaluation']['faithfulness_rating']})"
        )

        final_msg_with_eval = raw_msg + eval_footer

        return {
            **state,
            "turn_count": turn_count + 1,
            "current_thought": thought,
            "pending_action": None,
            "message": final_msg_with_eval,
            "agents_executed": executed,
            "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
        }

    return {
        **state,
        "turn_count": turn_count + 1,
        "current_thought": thought,
        "pending_action": {"tool": action, "args": action_input},
        "agents_executed": executed,
        "total_tokens_used": state.get("total_tokens_used", 0) + tokens,
    }


async def tool_execute_node(state: AgentState) -> AgentState:
    """
    Executes the selected Tool Action and appends observation to state.
    """
    pending = state.get("pending_action")
    if not pending or not pending.get("tool"):
        return state

    tool_name = pending["tool"]
    tool_args = pending.get("args", {})

    # Execute tool
    result = await execute_tool(tool_name, tool_args)

    observations = list(state.get("observations", []))
    observations.append(result)

    # Extract structured results into state domains if applicable
    obs_data = result.get("observation", [])
    updated_state = {**state, "observations": observations, "pending_action": None}

    if tool_name == "search_universities" and isinstance(obs_data, list):
        updated_state["recommended_universities"] = obs_data
    elif tool_name == "search_scholarships" and isinstance(obs_data, list):
        updated_state["matched_scholarships"] = obs_data
    elif tool_name == "calculate_financial_breakdown" and isinstance(obs_data, dict):
        updated_state["finance_breakdown"] = obs_data

    return updated_state


def route_next_step(state: AgentState) -> str:
    """Routing function for LangGraph conditional edge."""
    turn_count = state.get("turn_count", 0)
    max_turns = state.get("max_turns", 6)

    pending = state.get("pending_action")

    if pending and pending.get("tool") and turn_count < max_turns:
        return "tool_execute"

    return "verifier"


def route_after_verifier(state: AgentState) -> str:
    """Routing function for the conditional edge out of the verifier."""
    turn_count = state.get("turn_count", 0)
    max_turns = state.get("max_turns", 6)
    verifier_passed = state.get("verifier_passed", True)

    if not verifier_passed and turn_count < max_turns:
        return "agent_decide"
    return "end"


def build_workflow() -> StateGraph:
    """Construct ReAct Agent Workflow StateGraph with Verifier Self-Correction Loop."""
    graph = StateGraph(AgentState)

    # Add Nodes
    graph.add_node("agent_decide", agent_decide_node)
    graph.add_node("tool_execute", tool_execute_node)
    graph.add_node("verifier", verifier_node)

    # Entry point
    graph.set_entry_point("agent_decide")

    # Conditional Routing from Decide Node
    graph.add_conditional_edges(
        "agent_decide",
        route_next_step,
        {
            "tool_execute": "tool_execute",
            "verifier": "verifier",
        },
    )

    # Loop back from Tool Execution to Agent Decision
    graph.add_edge("tool_execute", "agent_decide")

    # Verifier -> Conditionally loop back to agent_decide if verification failed, or END if passed/max turns
    graph.add_conditional_edges(
        "verifier",
        route_after_verifier,
        {
            "agent_decide": "agent_decide",
            "end": END,
        },
    )

    return graph.compile()


_workflow = None


def get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow


def _check_past_intake(target_intake: Optional[str], query: str) -> Tuple[bool, str]:
    import re
    q = (query or "").lower()
    t = (target_intake or "").lower()
    combined = f"{t} {q}"

    # Match past years like 2025, 2024, 2023...
    years = re.findall(r'\b(20\d\d)\b', combined)
    for y in years:
        if int(y) < 2026:
            return True, f"{target_intake if target_intake and y in target_intake else y}"

    # Match terms before August 2026
    if "2026" in combined:
        if any(term in combined for term in [
            "spring 2026", "jan 2026", "january 2026", "winter 2026",
            "summer 2026", "may 2026", "june 2026", "july 2026"
        ]):
            return True, f"{target_intake or 'Spring / Summer 2026'}"

    return False, ""


async def run_orchestrator(
    query: str,
    session_id: str,
    student_profile: Optional[Any],
    user_id: str,
    db: Any,
    chat_history: Optional[List] = None,
) -> Dict[str, Any]:
    """
    Main entry point invoked by FastAPI endpoints.
    """
    profile_data: Dict = {}
    if student_profile:
        if isinstance(student_profile, dict):
            profile_data = dict(student_profile)
        else:
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

    # Direct DB fallback check if profile_data is empty
    if not profile_data and db and user_id:
        try:
            import uuid
            from sqlalchemy import select
            from app.models.student_profile import StudentProfile
            p_res = await db.execute(select(StudentProfile).where(StudentProfile.user_id == uuid.UUID(str(user_id))))
            db_prof = p_res.scalar_one_or_none()
            if db_prof:
                for col in [
                    "cgpa", "cgpa_scale", "backlogs", "degree", "specialization",
                    "ielts_score", "toefl_score", "gre_score", "gmat_score",
                    "preferred_countries", "course_interest", "career_goal",
                    "target_intake", "total_budget_usd", "financial_background",
                    "work_experience_years",
                ]:
                    val = getattr(db_prof, col, None)
                    if val is not None:
                        profile_data[col] = val
        except Exception:
            pass

    # Check if profile has ANY user-configured fields
    has_info = any([
        profile_data.get("cgpa") is not None,
        profile_data.get("degree") is not None and str(profile_data.get("degree")).strip() != "",
        profile_data.get("specialization") is not None and str(profile_data.get("specialization")).strip() != "",
        profile_data.get("course_interest") is not None and str(profile_data.get("course_interest")).strip() != "",
        profile_data.get("target_intake") is not None and str(profile_data.get("target_intake")).strip() != "",
        profile_data.get("ielts_score") is not None,
        profile_data.get("total_budget_usd") is not None,
        profile_data.get("preferred_countries") is not None and len(profile_data.get("preferred_countries")) > 0,
    ])

    if not has_info:
        notice_message = (
            "⚠️ **Profile Setup Required**\n\n"
            "You haven't set up your student profile yet!\n\n"
            "Please first set up your academic profile (CGPA, degree, target countries, and budget) so AI Copilot can personalize university recommendations, tuition estimates, and scholarship matches.\n\n"
            "👉 Please go to [My Profile](/profile) to set up your profile now."
        )
        return {
            "session_id": session_id,
            "output": {"message": notice_message},
            "reasoning": "Student profile missing or empty.",
            "agents_executed": ["profile_checker"],
            "tokens_used": 0,
            "verification": {"status": "profile_required"},
        }

    # Check if target intake is in the past (2025 or before August 2026)
    is_past, detected_term = _check_past_intake(profile_data.get("target_intake"), query)
    if is_past:
        past_message = (
            "⏰ **You are late to apply!**\n\n"
            f"The target intake term specified (**{detected_term}**) has already passed or application deadlines closed prior to August 2026.\n\n"
            "Universities for 2025 and early-2026 intakes have already completed admissions, visa processing, and course orientation.\n\n"
            "💡 **Recommended Action:**\n"
            "• Please target **Fall 2026 (September 2026)** or **Spring 2027 (January 2027)** for open application windows.\n"
            "• Update your intake choice in **[My Profile](/profile)** or **[Timeline](/timeline)** to Fall 2026 / Spring 2027 to discover active university admissions."
        )
        return {
            "session_id": session_id,
            "output": {"message": past_message},
            "reasoning": "Target intake date is in the past (before August 2026).",
            "agents_executed": ["intake_checker"],
            "tokens_used": 0,
            "verification": {"status": "past_intake_late"},
        }

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
        "turn_count": 0,
        "max_turns": 6,
        "observations": [],
        "agents_executed": [],
        "errors": [],
        "total_tokens_used": 0,
    }

    workflow = get_workflow()
    start = time.time()
    final_state: AgentState = await workflow.ainvoke(initial_state)
    elapsed_ms = (time.time() - start) * 1000

    # Log to DB
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
        "verifier_passed": final_state.get("verifier_passed", True),
        "verifier_critique": final_state.get("verifier_critique", ""),
        "reasoning": final_state.get("current_thought", ""),
        "tokens_used": final_state.get("total_tokens_used", 0),
        "execution_time_ms": elapsed_ms,
    }


async def _persist_logs(state: AgentState, user_id: str, session_id: str, db: Any):
    """Persist execution log record."""
    try:
        import uuid as uuid_mod
        from app.models.agent_log import AgentLog

        log = AgentLog(
            id=uuid_mod.uuid4(),
            user_id=uuid_mod.UUID(user_id),
            session_id=session_id,
            agent_name="react_orchestrator",
            status="success" if state.get("verifier_passed", True) else "flagged",
            input_data={"query": state.get("user_query", "")},
            output_data={"message": state.get("message", "")[:500]},
            reasoning=state.get("current_thought", ""),
            tokens_used=state.get("total_tokens_used", 0),
        )
        db.add(log)
        await db.commit()
    except Exception:
        pass
