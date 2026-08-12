"""
Unit tests for Verifier Node claim auditing and reflection loop.
"""

import pytest
from agents.verifier import verifier_node
from agents.state import AgentState


@pytest.mark.asyncio
async def test_verifier_flags_budget_violation_in_text():
    state: AgentState = {
        "user_query": "Find universities in USA",
        "student_profile": {"total_budget_usd": 25000, "cgpa": 8.0},
        "recommended_universities": [
            {"name": "Expensive University", "avg_tuition_usd_per_year": 45000, "min_cgpa": 7.0}
        ],
        "message": "We recommend Expensive University which costs $45,000 per year.",
        "observations": [],
        "agents_executed": [],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is False
    assert "Budget Violation" in result["verifier_critique"] or "Message Claim Violation" in result["verifier_critique"]


@pytest.mark.asyncio
async def test_verifier_flags_missing_citations_when_search_used():
    state: AgentState = {
        "user_query": "What are current TU Munich fees?",
        "student_profile": {"total_budget_usd": 30000, "cgpa": 8.5},
        "message": "TU Munich tuition is free for international students in most engineering programs but semester fee is 150 euros.",
        "observations": [
            {"tool": "tavily_search", "observation": {"results": [{"title": "TUM Fees", "url": "https://tum.de/fees"}]}}
        ],
        "agents_executed": [],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is False
    assert "Citation Requirement" in result["verifier_critique"]


@pytest.mark.asyncio
async def test_verifier_passes_valid_state_and_citations():
    state: AgentState = {
        "user_query": "What are current TU Munich fees?",
        "student_profile": {"total_budget_usd": 30000, "cgpa": 8.5},
        "recommended_universities": [
            {"name": "Technical University of Munich", "avg_tuition_usd_per_year": 600, "min_cgpa": 8.0}
        ],
        "message": "Technical University of Munich has low fees. [Source: TUM](https://tum.de/fees)",
        "observations": [
            {"tool": "tavily_search", "observation": {"results": [{"title": "Technical University of Munich", "url": "https://tum.de/fees"}]}}
        ],
        "agents_executed": [],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is True


@pytest.mark.asyncio
async def test_verifier_flags_unselected_country_in_executive_brief():
    state: AgentState = {
        "user_query": "suggest me some japanese universities",
        "student_profile": {"preferred_countries": ["Australia"], "cgpa": 5.6},
        "message": "🎯 Executive Brief\nStudying in Japan is great. While your student profile primarily notes Australia and a 5.6 CGPA...",
        "observations": [],
        "agents_executed": [],
    }

    result = await verifier_node(state)
    assert result["verifier_passed"] is False
    assert "Unselected Country Mention" in result["verifier_critique"]

