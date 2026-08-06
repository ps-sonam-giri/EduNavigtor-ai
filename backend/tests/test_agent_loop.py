"""
Unit tests for ReAct Agent Loop & Verifier Node.
"""

import pytest
from agents.verifier import verifier_node
from agents.state import AgentState


@pytest.mark.asyncio
async def test_verifier_node_cgpa_violation():
    state: AgentState = {
        "student_profile": {"cgpa": 6.5, "total_budget_usd": 30000},
        "recommended_universities": [
            {
                "name": "High Standard University",
                "min_cgpa": 8.0,
                "avg_tuition_usd_per_year": 15000,
            }
        ],
        "observations": [],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is False
    assert "CGPA Violation" in result["verifier_critique"]


@pytest.mark.asyncio
async def test_verifier_node_budget_violation():
    state: AgentState = {
        "student_profile": {"cgpa": 8.5, "total_budget_usd": 15000},
        "recommended_universities": [
            {
                "name": "Expensive University",
                "min_cgpa": 7.0,
                "avg_tuition_usd_per_year": 45000,
            }
        ],
        "observations": [],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is False
    assert "Budget Violation" in result["verifier_critique"]


@pytest.mark.asyncio
async def test_verifier_node_success():
    state: AgentState = {
        "student_profile": {"cgpa": 8.5, "total_budget_usd": 30000},
        "recommended_universities": [
            {
                "name": "TU Munich",
                "min_cgpa": 7.0,
                "avg_tuition_usd_per_year": 1000,
            }
        ],
        "observations": [{"observation": [{"name": "TU Munich"}]}],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is True


@pytest.mark.asyncio
async def test_graph_loops_back_on_verifier_failure():
    """
    A verifier failure with turns remaining should route back to agent_decide.
    """
    from agents.orchestrator import route_after_verifier

    state = {
        "verifier_passed": False,
        "turn_count": 2,
        "max_turns": 6,
    }
    assert route_after_verifier(state) == "agent_decide"


@pytest.mark.asyncio
async def test_graph_ends_at_max_turns_even_if_verifier_fails():
    from agents.orchestrator import route_after_verifier

    state = {
        "verifier_passed": False,
        "turn_count": 6,
        "max_turns": 6,
    }
    assert route_after_verifier(state) == "end"


@pytest.mark.asyncio
async def test_graph_ends_when_verifier_passes():
    from agents.orchestrator import route_after_verifier

    state = {
        "verifier_passed": True,
        "turn_count": 3,
        "max_turns": 6,
    }
    assert route_after_verifier(state) == "end"
