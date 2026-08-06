"""
Unit tests for Tool Registry & Domain Tools.
"""

import pytest
from tools.registry import get_tool_schemas, execute_tool
from tools.finance_tools import calculate_financial_breakdown_tool


def test_tool_registry_schemas():
    schemas = get_tool_schemas()
    assert isinstance(schemas, list)
    assert len(schemas) >= 4
    tool_names = [s["name"] for s in schemas]
    assert "search_universities" in tool_names
    assert "search_scholarships" in tool_names
    assert "calculate_financial_breakdown" in tool_names
    assert "extract_transcript_data" in tool_names


@pytest.mark.asyncio
async def test_financial_breakdown_tool():
    result = await calculate_financial_breakdown_tool(
        tuition_usd_per_year=15000,
        living_cost_usd_per_month=1000,
        scholarship_deduction_usd=3000,
        duration_years=2.0,
    )

    assert result["tuition_per_year_usd"] == 15000
    assert result["living_cost_per_year_usd"] == 12000
    assert result["net_cost_year1_usd"] == 24000  # (15000+12000) - 3000
    assert result["net_cost_year1_inr"] == 24000 * 87.0
    assert "loan_roi_analysis" in result
    assert result["loan_roi_analysis"]["estimated_monthly_emi_inr"] > 0


@pytest.mark.asyncio
async def test_execute_unknown_tool():
    res = await execute_tool("non_existent_tool", {})
    assert "error" in res
    assert "not found" in res["error"]
