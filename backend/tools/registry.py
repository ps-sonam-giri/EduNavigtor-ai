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


REGISTERED_TOOLS = {
    "tavily_search": {
        "name": "tavily_search",
        "description": "Perform live web search via Tavily API for current university rankings, fees, deadlines, and scholarships.",
        "input_schema": TavilySearchInput.model_json_schema(),
        "handler": search_tavily_web,
    },
    "search_universities": {
        "name": "search_universities",
        "description": "Query verified university database for matching countries, tuition budget, CGPA requirements, and ranking.",
        "input_schema": UniversitySearchInput.model_json_schema(),
        "handler": search_universities_tool,
    },
    "search_scholarships": {
        "name": "search_scholarships",
        "description": "Search scholarships matching student CGPA eligibility, country, and merit criteria.",
        "input_schema": ScholarshipSearchInput.model_json_schema(),
        "handler": search_scholarships_tool,
    },
    "calculate_financial_breakdown": {
        "name": "calculate_financial_breakdown",
        "description": "Calculate tuition + living costs breakdown, INR currency conversion, monthly loan EMI, and ROI payback period.",
        "input_schema": FinancialBreakdownInput.model_json_schema(),
        "handler": calculate_financial_breakdown_tool,
    },
    "extract_transcript_data": {
        "name": "extract_transcript_data",
        "description": "Parse uploaded transcript or scorecard PDF to extract CGPA, IELTS, degree, and backlogs.",
        "input_schema": TranscriptExtractionInput.model_json_schema(),
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
    """Execute a tool by name with arguments and return observation result."""
    tool = REGISTERED_TOOLS.get(name)
    if not tool:
        return {"error": f"Tool '{name}' not found. Available tools: {list(REGISTERED_TOOLS.keys())}"}

    try:
        handler = tool["handler"]
        result = await handler(**args)
        return {"tool": name, "observation": result}
    except Exception as e:
        return {"tool": name, "error": f"Execution error in '{name}': {str(e)}"}
