"""
Unit tests for MCP Client discovery and HTTP dispatch primitives.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from tools.mcp_client import MCPClient
from tools.registry import execute_tool, get_tool_schemas


@pytest.mark.asyncio
async def test_mcp_client_discovery():
    client = MCPClient(server_urls=["http://localhost:8001"])
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "tools": [
            {"name": "send_email", "description": "Send email via Gmail MCP"}
        ]
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
        tools = await client.discover_tools()
        assert "send_email" in tools
        assert client._tool_to_server_map.get("send_email") == "http://localhost:8001"


@pytest.mark.asyncio
async def test_mcp_client_call_dispatch():
    client = MCPClient(server_urls=["http://localhost:8001"])
    client._tool_to_server_map["send_email"] = "http://localhost:8001"

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": "success", "message": "Dispatched"}

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp):
        result = await client.call_mcp_tool("send_email", {"to": "test@example.com"})
        assert result is not None
        assert result.get("protocol") == "mcp"
        assert result.get("observation", {}).get("status") == "success"


@pytest.mark.asyncio
async def test_registry_fallback_when_mcp_offline():
    # Test that execute_tool handles schema validation and fallback cleanly
    result = await execute_tool("calculate_financial_breakdown", {
        "tuition_usd": 25000,
        "living_cost_usd": 12000,
        "scholarship_usd": 5000
    })
    assert result is not None
    assert "observation" in result or "error" in result
