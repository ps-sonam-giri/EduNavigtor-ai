"""
EduPilot AI – Core Tools MCP Server.
Runs an independent MCP server on port 8002 exposing university, scholarship,
finance, and document tools for AI agents over standard MCP endpoints.

Run standalone:
    python -m mcp_servers.core_tools_mcp_server
"""

import sys
from pathlib import Path
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure backend root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from tools.registry import get_tool_schemas, execute_tool

app = FastAPI(
    title="EduPilot Core Tools MCP Server",
    description="Custom Model Context Protocol (MCP) Server for Core Domain Tools",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MCPToolCallRequest(BaseModel):
    tool: str = Field(..., description="Tool name to execute, e.g. 'search_universities', 'search_scholarships'")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments for tool execution")


@app.get("/health")
async def health_check():
    return {
        "status": "active",
        "server": "EduPilot Core Tools MCP Server",
        "port": settings.mcp_postgres_server_port,
        "tools_count": len(get_tool_schemas()),
    }


@app.get("/manifest.json")
@app.get("/tools/list")
async def list_mcp_tools():
    """Returns all available core domain MCP tools registered in tools/registry.py."""
    return {"tools": get_tool_schemas()}


@app.post("/tools/call")
async def call_mcp_tool(request: MCPToolCallRequest):
    """Executes core tool via MCP protocol endpoint."""
    result = await execute_tool(request.tool, request.arguments)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


if __name__ == "__main__":
    port = getattr(settings, "mcp_postgres_server_port", 8002)
    print(f"Starting Custom Core Tools MCP Server on http://localhost:{port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
