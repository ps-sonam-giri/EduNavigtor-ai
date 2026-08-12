"""
EduPilot AI Tool Registry.
Registers typed tools and dispatches execution.
"""

from typing import Any, Dict, List
from tools.university_tools import search_universities_tool, UniversitySearchInput
from tools.scholarship_tools import search_scholarships_tool, ScholarshipSearchInput
from tools.finance_tools import calculate_financial_breakdown_tool, FinancialBreakdownInput
from tools.document_tools import extract_transcript_data_tool, TranscriptExtractionInput
from tools.tavily_tools import search_tavily_web, TavilySearchInput


from tools.mcp_client import mcp_client


REGISTERED_TOOLS = {
    "tavily_search": {
        "name": "tavily_search",
        "description": "Perform live web search via Tavily API for current university rankings, fees, deadlines, and scholarships.",
        "input_schema": TavilySearchInput.model_json_schema(),
        "model_cls": TavilySearchInput,
        "handler": search_tavily_web,
    },
    "search_universities": {
        "name": "search_universities",
        "description": "Query verified university database for matching countries, tuition budget, CGPA requirements, and ranking.",
        "input_schema": UniversitySearchInput.model_json_schema(),
        "model_cls": UniversitySearchInput,
        "handler": search_universities_tool,
    },
    "search_scholarships": {
        "name": "search_scholarships",
        "description": "Search scholarships matching student CGPA eligibility, country, and merit criteria.",
        "input_schema": ScholarshipSearchInput.model_json_schema(),
        "model_cls": ScholarshipSearchInput,
        "handler": search_scholarships_tool,
    },
    "calculate_financial_breakdown": {
        "name": "calculate_financial_breakdown",
        "description": "Calculate tuition + living costs breakdown, INR currency conversion, monthly loan EMI, and ROI payback period.",
        "input_schema": FinancialBreakdownInput.model_json_schema(),
        "model_cls": FinancialBreakdownInput,
        "handler": calculate_financial_breakdown_tool,
    },
    "extract_transcript_data": {
        "name": "extract_transcript_data",
        "description": "Parse uploaded transcript or scorecard PDF to extract CGPA, IELTS, degree, and backlogs.",
        "input_schema": TranscriptExtractionInput.model_json_schema(),
        "model_cls": TranscriptExtractionInput,
        "handler": extract_transcript_data_tool,
    },
}


def get_tool_schemas() -> List[Dict[str, Any]]:
    """Return JSON schemas for all registered tools."""
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["input_schema"],
        }
        for tool in REGISTERED_TOOLS.values()
    ]


async def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool by name with arguments.
    First attempts execution via MCP server protocol (/tools/call).
    Falls back gracefully to direct typed local handler if MCP server is offline.
    """
    tool = REGISTERED_TOOLS.get(name)
    if not tool:
        return {"error": f"Tool '{name}' not found. Available tools: {list(REGISTERED_TOOLS.keys())}"}

    # Input Schema Validation
    validated_args = args
    if tool.get("model_cls"):
        try:
            model_cls = tool["model_cls"]
            validated_obj = model_cls(**args)
            validated_args = validated_obj.model_dump()
        except Exception as ve:
            return {"tool": name, "error": f"Invalid arguments for '{name}': {str(ve)}"}

    # 1. Primary path: MCP Server Protocol Invocation over HTTP
    mcp_result = await mcp_client.call_mcp_tool(name, validated_args)
    if mcp_result is not None:
        return mcp_result

    # 2. Fallback path: Direct local function handler
    try:
        handler = tool["handler"]
        result = await handler(**validated_args)
        return {"tool": name, "observation": result, "protocol": "local_fallback"}
    except Exception as e:
        return {"tool": name, "error": f"Execution error in '{name}': {str(e)}", "protocol": "local_fallback"}

