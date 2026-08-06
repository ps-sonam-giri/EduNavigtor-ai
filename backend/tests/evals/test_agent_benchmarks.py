"""
Benchmark Evaluation Suite for EduPilot AI.
Tests end-to-end agent decision-making across realistic student scenarios.
"""

import pytest
from tools.registry import execute_tool
from agents.verifier import verifier_node
from agents.state import AgentState


BENCHMARK_SCENARIOS = [
    {
        "id": "scenario_1_low_cgpa_high_budget",
        "profile": {"cgpa": 6.2, "total_budget_usd": 60000, "preferred_countries": ["USA"]},
        "target_uni": {"name": "US Private College", "min_cgpa": 6.0, "avg_tuition_usd_per_year": 40000},
        "expected_verifier": True,
    },
    {
        "id": "scenario_2_high_cgpa_low_budget",
        "profile": {"cgpa": 9.1, "total_budget_usd": 10000, "preferred_countries": ["Germany"]},
        "target_uni": {"name": "TU Berlin", "min_cgpa": 7.5, "avg_tuition_usd_per_year": 500},
        "expected_verifier": True,
    },
    {
        "id": "scenario_3_cgpa_mismatch_failure",
        "profile": {"cgpa": 5.5, "total_budget_usd": 30000},
        "target_uni": {"name": "Top Tier Uni", "min_cgpa": 8.0, "avg_tuition_usd_per_year": 15000},
        "expected_verifier": False,
    },
]


@pytest.mark.asyncio
@pytest.mark.parametrize("scenario", BENCHMARK_SCENARIOS)
async def test_benchmark_scenarios(scenario):
    state: AgentState = {
        "student_profile": scenario["profile"],
        "recommended_universities": [scenario["target_uni"]],
        "observations": [{"observation": [{"name": scenario["target_uni"]["name"]}]}],
    }

    res = await verifier_node(state)
    assert res["verifier_passed"] == scenario["expected_verifier"]
