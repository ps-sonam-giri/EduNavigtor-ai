"""
Orchestrator Agent – ReAct Agent Loop & LangGraph State Graph.

Perceive → Decide Action → Execute Tool → Observe Result → Reflect/Verify → Finish
"""

import json
import time
import uuid
from typing import Any, Dict, List, Optional

from langgraph.graph import END, StateGraph

from agents.llm import ainvoke_llm, extract_json_from_response
from agents.state import AgentState
from agents.verifier import verifier_node
from tools.registry import execute_tool, get_tool_schemas


REACT_DECISION_PROMPT = """You are EduPilot AI, an autonomous study abroad copilot for Indian students.
Your task is to help the student by deciding the BEST tool action to execute next, OR providing the final grounded answer.

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
  "final_answer": "Complete, structured answer with tables and markdown bullet points."
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
        return {
            **state,
            "turn_count": turn_count + 1,
            "current_thought": thought,
            "pending_action": None,
            "message": final_answer or response_text,
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


def build_workflow() -> StateGraph:
    """Construct ReAct Agent Workflow StateGraph."""
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

    # Verifier -> END
    graph.add_edge("verifier", END)

    return graph.compile()


_workflow = None


def get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow


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
