"""
EduPilot AI – Model Context Protocol (MCP) Client Module.

Provides discovery and JSON-RPC/HTTP execution primitives to invoke tools
registered on external or local MCP servers over standard endpoints.
"""

from typing import Any, Dict, List, Optional
import httpx
import structlog
from app.config import settings

logger = structlog.get_logger(__name__)

# List of target MCP server base URLs
DEFAULT_MCP_SERVERS = [
    f"http://localhost:{getattr(settings, 'mcp_gmail_server_port', 8001)}",
    f"http://localhost:{getattr(settings, 'mcp_postgres_server_port', 8003)}",
]


class MCPClient:
    """Client for discovering and executing tools on MCP servers via standard protocol endpoints."""

    def __init__(self, server_urls: Optional[List[str]] = None):
        self.server_urls = server_urls or DEFAULT_MCP_SERVERS
        self._tool_to_server_map: Dict[str, str] = {}

    async def discover_tools(self) -> Dict[str, Dict[str, Any]]:
        """
        Discover tools across all active MCP servers.
        Returns a dictionary of tool_name -> tool_definition.
        """
        discovered_tools: Dict[str, Dict[str, Any]] = {}
        self._tool_to_server_map.clear()

        async with httpx.AsyncClient(timeout=3.0) as client:
            for server_url in self.server_urls:
                try:
                    resp = await client.get(f"{server_url}/tools/list")
                    if resp.status_code == 200:
                        data = resp.json()
                        tools = data.get("tools", [])
                        for t in tools:
                            name = t.get("name")
                            if name:
                                discovered_tools[name] = t
                                self._tool_to_server_map[name] = server_url
                                logger.info("Discovered MCP tool", tool=name, server=server_url)
                except Exception as e:
                    logger.debug("MCP server unreachable during discovery", server=server_url, error=str(e))

        return discovered_tools

    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executes a tool on its discovered MCP server over standard /tools/call endpoint.
        Returns the response dict or None if MCP server call fails/unreachable.
        """
        server_url = self._tool_to_server_map.get(tool_name)

        # If not yet mapped, attempt discovery
        if not server_url:
            await self.discover_tools()
            server_url = self._tool_to_server_map.get(tool_name)

        if not server_url:
            logger.warning("Tool not found on any active MCP server", tool=tool_name)
            return None

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                payload = {"tool": tool_name, "arguments": arguments}
                logger.info("Dispatching tool execution over MCP protocol", tool=tool_name, server=server_url)
                resp = await client.post(f"{server_url}/tools/call", json=payload)
                if resp.status_code == 200:
                    res_json = resp.json()
                    return {"tool": tool_name, "observation": res_json, "protocol": "mcp"}
                else:
                    logger.warning("MCP server call non-200", tool=tool_name, status=resp.status_code, text=resp.text[:200])
                    return {"tool": tool_name, "error": f"MCP HTTP {resp.status_code}: {resp.text[:200]}", "protocol": "mcp"}
        except Exception as e:
            logger.warning("Failed to execute tool via MCP endpoint", tool=tool_name, error=str(e))
            return None


# Global singleton instance
mcp_client = MCPClient()
