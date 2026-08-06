# EduPilot AI → L2+ Agentic Platform: Master Implementation Plan (v3 — Docker-Free, Re-Verified)

> **Status**: Re-verified against live codebase on 2026-08-06. All file paths confirmed. All false alarms from v2 corrected.

---

## System Realities (Verified)

| Item | Verified Finding |
|---|---|
| RAM | **32 GB** — plenty. Qwen 7b runs fully in RAM (~5GB). 3b is also fine but less capable |
| GPU | Intel Iris Xe (shared, ~2GB VRAM) — **CPU inference only via Ollama** |
| LLM Strategy | **Gemini Flash primary** (API key already in `.env`); **Qwen2.5:7b** as local fallback |
| `api.ts` | **EXISTS** at `frontend/src/lib/api.ts` (54 lines, partial — needs SSE + HITL methods added) |
| `docker-compose.yml` | Used for PostgreSQL + backend + frontend — **all replaced with local installs** |
| `start.ps1` | Already exists with local startup logic — needs DB setup step added |
| Gemini model name | `.env` has `gemini-3.5-flash-lite` — **this model name is invalid**. Must fix to `gemini-2.0-flash-lite` |
| `venv312` | Duplicate — safe to delete after confirming `venv` has all packages |
| MCP SDK | `mcp >= 1.0.0` in requirements.txt — **installed but never imported** |
| `report_service.py:203` | Verified syntax error — nested backslash f-string. Confirmed blocker |

---

## Qwen Model Recommendation

> [!TIP]
> **Use Qwen2.5:7b.** With 32GB RAM and CPU inference:
> - `qwen2.5:7b` ≈ 5GB RAM, 15-25 sec/response on CPU — reliable JSON output for ReAct loop
> - `qwen2.5:3b` ≈ 2GB RAM, 5-10 sec/response — faster but weaker at structured JSON action output (higher hallucination rate on schema compliance)
> - Gemini Flash will handle 90%+ of requests. Qwen is purely the offline fallback.
> - **Recommendation: pull `qwen2.5:7b`** — the 7b is worth the extra 3GB for agent reliability.

---

## What Gets Removed (Docker-Free)

| Remove | Replace With |
|---|---|
| `docker-compose.yml` | `start.ps1` (enhanced) + `setup.ps1` (new one-time setup script) |
| `docker/Dockerfile.backend` | Direct `uvicorn` in venv |
| `docker/Dockerfile.frontend` | Direct `npm run dev` |
| `docker/nginx.conf` | Vite dev server proxies `/api` to FastAPI directly |
| `backend/venv312/` | Delete — only `backend/venv/` remains |
| References to `host.docker.internal` | Replace with `localhost` everywhere |

---

## L2 Rubric Score Impact

| Rubric Area | Current | After Plan | Key Change |
|---|---|---|---|
| Idea fit | 9/10 | 10/10 | README cleanup |
| LLM & prompts | 6/10 | 9/10 | Schema validation, JSON repair loop |
| **MCP / tool architecture** | **2/15** | **13/15** | Real MCP server + SDK + list_tools trace |
| **Agentic loop** | **8/20** | **18/20** | Genuine ReAct loop with typed actions |
| Tool integrations | 5/10 | 9/10 | Grounded observations, typed errors |
| **Reflection** | **0/10** | **9/10** | Verifier node |
| Code quality | 5/10 | 8/10 | Syntax fix, no swallowed exceptions |
| Testing & reproducibility | 2/10 | 9/10 | Tests + captured trace + working setup |
| Explainability | 4/5 | 5/5 | README matches actual behavior |

---

## Proposed Changes — Ordered by Dependency

---

### Phase 0: Environment Cleanup & Build Blockers *(Day 1)*

Everything in this phase must be done before any code runs.

---

#### [DELETE] `docker-compose.yml`
Remove entirely. All services run locally.

#### [DELETE] `docker/` (folder)
`Dockerfile.backend`, `Dockerfile.frontend`, `nginx.conf` — all obsolete.

#### [DELETE] `backend/venv312/` (folder)
After confirming `backend/venv/` has all packages installed.

#### [MODIFY] [.gitignore](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/.gitignore)
Add (if missing):
```
venv/
venv312/
.venv/
__pycache__/
*.pyc
*.pyo
.env
node_modules/
dist/
.DS_Store
```

#### [MODIFY] [backend/.env](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor ai/backend/.env)
Fix the invalid Gemini model name and standardize Ollama:
```diff
-GEMINI_MODEL=gemini-3.5-flash-lite
+GEMINI_MODEL=gemini-2.0-flash-lite

-OLLAMA_MODEL=qwen2.5
+OLLAMA_MODEL=qwen2.5:7b
```
> **Note:** `gemini-3.5-flash-lite` does not exist in the Google GenAI API. The closest valid models are `gemini-2.0-flash-lite` or `gemini-1.5-flash`. This is causing silent failures when Gemini is called.

#### [MODIFY] [backend/.env.example](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/backend/.env.example)
Mirror the same fix. Remove all MCP port entries (no longer separate servers):
```diff
-MCP_GMAIL_SERVER_PORT=8001
-MCP_FILESYSTEM_SERVER_PORT=8002
-MCP_POSTGRES_SERVER_PORT=8003
+# MCP server runs in-process — no separate port needed
```

#### [MODIFY] [backend/app/config.py](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/backend/app/config.py)
- Change default `gemini_model` from `"gemini-3.5-flash-lite"` → `"gemini-2.0-flash-lite"`.
- Remove `mcp_gmail_server_port`, `mcp_filesystem_server_port`, `mcp_postgres_server_port` fields (no longer used).
- Add `ollama_model: str = "qwen2.5:7b"`.

#### [MODIFY] [backend/services/report_service.py](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/backend/services/report_service.py) — Line 203
Fix nested f-string syntax error:
```python
# BEFORE (line 203 — causes SyntaxError in Python 3.11)
f"<b>{item.get('month_label', f'Month {item.get(\"month_offset\", 0) + 1}')}</b> – "

# AFTER
_fallback = f"Month {item.get('month_offset', 0) + 1}"
month_label = item.get('month_label', _fallback)
# then use month_label in the outer f-string
```

---

### Phase 0b: PostgreSQL Local Setup Script *(Day 1)*

Since Docker is gone, PostgreSQL must be installed and seeded locally.

#### [NEW] `setup.ps1` — One-time setup script
```powershell
# setup.ps1 — Run ONCE to set up the full local dev environment
# Prerequisites: Python 3.11+, Node.js 18+, PostgreSQL 16+, Ollama

# 1. Python venv (single venv only)
cd backend
if (!(Test-Path venv)) { python -m venv venv }
.\venv\Scripts\pip install -r requirements.txt

# 2. PostgreSQL — create DB and user
$env:PATH += ";C:\Program Files\PostgreSQL\16\bin"
psql -U postgres -c "CREATE USER edupilot WITH PASSWORD 'edupilot_pass';" 2>$null
psql -U postgres -c "CREATE DATABASE edupilot_db OWNER edupilot;" 2>$null

# 3. Run schema migrations
psql -U edupilot -d edupilot_db -f ..\database\migrations\001_initial_schema.sql
psql -U edupilot -d edupilot_db -f ..\database\migrations\002_seed_universities.sql
psql -U edupilot -d edupilot_db -f ..\database\migrations\003_top200_universities.sql

# 4. Pull Ollama model (fallback LLM)
ollama pull qwen2.5:7b

# 5. Frontend dependencies
cd ..\frontend
npm install

Write-Host "Setup complete! Run .\start.ps1 to launch."
```

#### [MODIFY] [start.ps1](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/start.ps1)
Enhance existing script to:
1. Check PostgreSQL is running (not Docker).
2. Start MCP server subprocess before FastAPI.
3. Start backend + frontend as before.
```powershell
# start.ps1 — Start all services locally (no Docker)
$env:PATH += ";C:\Program Files\nodejs;C:\Program Files\PostgreSQL\16\bin"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND = Join-Path $ROOT "backend"
$FRONTEND = Join-Path $ROOT "frontend"

# Check PostgreSQL
$pgRunning = (Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue | Where Status -eq Running)
if (-not $pgRunning) {
    Write-Host "Starting PostgreSQL..." -ForegroundColor Yellow
    Start-Service postgresql*
    Start-Sleep -Seconds 3
}

# Start MCP Server (in-process with backend — started by FastAPI lifespan)
Write-Host "Starting Backend (FastAPI + MCP)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "cd '$BACKEND'; .\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend (Vite)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "cd '$FRONTEND'; npm run dev"

Start-Sleep -Seconds 4
Write-Host "App: http://localhost:5173  |  API: http://localhost:8000  |  Docs: http://localhost:8000/docs"
Start-Process "http://localhost:5173"
```

---

### Phase 1: Real MCP Server (stdio transport, in-process) *(Days 2–3)*

> This is the single highest-impact phase. Currently 2/15 on MCP rubric. Target: 13/15.
> Transport: **stdio** — MCP server runs as a subprocess launched by the FastAPI lifespan. This is simpler than HTTP transport and works perfectly for a local dev setup.

#### [NEW] `backend/mcp_server/__init__.py`

#### [NEW] `backend/mcp_server/server.py`
```python
"""
EduPilot AI — Real MCP Server
Uses the official `mcp` SDK (already in requirements.txt, never imported before).
Transport: stdio — launched as subprocess by MCPClient.
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ListToolsResult
import asyncio, json

app = Server("edupilot-tools")

TOOLS = [
    Tool(
        name="search_universities",
        description="Search universities from the database by country, CGPA, tuition budget, and course interest.",
        inputSchema={
            "type": "object",
            "properties": {
                "country": {"type": "string"},
                "max_tuition_usd": {"type": "number"},
                "min_cgpa": {"type": "number"},
                "course_interest": {"type": "string"}
            },
            "required": []
        }
    ),
    Tool(
        name="match_scholarships",
        description="Find scholarships matching student CGPA, nationality, and degree level.",
        inputSchema={...}  # full schema in implementation
    ),
    Tool(
        name="calculate_financials",
        description="Calculate Year 1 cost breakdown: tuition + living + visa + insurance - scholarships. Returns INR and USD.",
        inputSchema={...}
    ),
    Tool(
        name="extract_document",
        description="Parse a student-uploaded PDF transcript and extract CGPA, test scores, and backlogs.",
        inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}
    ),
    Tool(
        name="send_email_report",
        description="Send the generated PDF report to the student's email. REQUIRES human approval before sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "recipient": {"type": "string", "format": "email"},
                "report_id": {"type": "string"},
                "requires_approval": {"type": "boolean", "const": True}
            },
            "required": ["recipient", "report_id", "requires_approval"]
        }
    ),
]

@app.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    from mcp_server.tools import dispatch_tool
    result = await dispatch_tool(name, arguments)
    return [TextContent(type="text", text=json.dumps(result))]

async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

#### [NEW] `backend/mcp_server/tools/__init__.py`
```python
async def dispatch_tool(name: str, arguments: dict) -> dict:
    if name == "search_universities":
        from .university_tool import search_universities
        return await search_universities(**arguments)
    elif name == "match_scholarships":
        from .scholarship_tool import match_scholarships
        return await match_scholarships(**arguments)
    elif name == "calculate_financials":
        from .finance_tool import calculate_financials
        return await calculate_financials(**arguments)
    elif name == "extract_document":
        from .document_tool import extract_document
        return await extract_document(**arguments)
    elif name == "send_email_report":
        from .email_tool import send_email_report
        return await send_email_report(**arguments)
    else:
        return {"error": f"Unknown tool: {name}"}
```

#### [NEW] `backend/mcp_server/tools/university_tool.py`
- Safe parameterized SQLAlchemy query — no LLM-generated SQL.
- Returns `List[UniversityRecord]` with `source: "database"` + `retrieved_at` timestamp on every record.
- Pydantic-validates inputs before hitting DB.

#### [NEW] `backend/mcp_server/tools/scholarship_tool.py`
- Queries DB for scholarships, filters by CGPA ≥ min_cgpa, nationality match, degree match.
- Returns `List[ScholarshipMatch]` with `eligible: bool` and `reason` per item.

#### [NEW] `backend/mcp_server/tools/finance_tool.py`
- **Pure arithmetic** — no LLM.
- Year 1 cost = tuition + living cost estimate + visa fee + health insurance.
- Scholarship deduction applied.
- Loan EMI calculator: `(principal * monthly_rate) / (1 - (1+r)^-n)`.
- Returns `FinancialBreakdown` with USD and INR (at fixed exchange rate from config).

#### [NEW] `backend/mcp_server/tools/document_tool.py`
- Uses `pdfplumber` or existing `PyPDF2` to extract text from uploaded transcript.
- Regex patterns for CGPA, IELTS, TOEFL, GRE, backlog count.
- Returns `DocumentData`.

#### [NEW] `backend/mcp_server/tools/email_tool.py`
- Move Gmail send logic from `backend/mcp_tools/gmail_mcp.py`.
- Add `requires_approval` check: if `True`, return `{"status": "approval_required"}` instead of sending — the HITL gate node handles the pause.

#### [NEW] `backend/mcp_client/client.py`
```python
"""
MCP Client — launches the MCP server as a subprocess (stdio transport)
and provides get_tool_schemas() + execute_tool() to the ReAct agent.
"""
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio, json
from functools import lru_cache

class MCPClient:
    def __init__(self):
        self._session: ClientSession | None = None
        self._tool_schemas: list | None = None

    async def connect(self):
        """Launch MCP server subprocess and open session."""
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "mcp_server.server"],
        )
        self._read, self._write = await stdio_client(server_params).__aenter__()
        self._session = ClientSession(self._read, self._write)
        await self._session.initialize()

    async def get_tool_schemas(self) -> list[dict]:
        """Call list_tools() — cached after first call."""
        if self._tool_schemas is None:
            result = await self._session.list_tools()
            self._tool_schemas = [t.model_dump() for t in result.tools]
        return self._tool_schemas

    async def execute_tool(self, name: str, args: dict) -> dict:
        """Call a registered tool and return structured observation."""
        result = await self._session.call_tool(name, args)
        content = result.content[0].text if result.content else "{}"
        return {
            "tool": name,
            "args": args,
            "result": json.loads(content),
            "source": "mcp",
        }

_client: MCPClient | None = None

async def get_mcp_client() -> MCPClient:
    global _client
    if _client is None:
        _client = MCPClient()
        await _client.connect()
    return _client
```

#### [DELETE] `backend/mcp_tools/postgres_mcp.py` *(after Phase 1 tools are live)*
Unsafe NL-to-SQL removed. Replaced by typed `search_universities` tool.

#### [DELETE] `backend/mcp_tools/filesystem_mcp.py` *(immediately)*
Not referenced anywhere — safe to delete now.

---

### Phase 2: ReAct Agent Loop *(Days 4–5)*

#### [NEW] `backend/agents/actions.py`
```python
from pydantic import BaseModel, field_validator
from typing import Literal, Any

class CallToolAction(BaseModel):
    action_type: Literal["call_tool"]
    tool_name: str
    tool_args: dict[str, Any]
    reasoning: str  # required chain-of-thought

    @field_validator("tool_name")
    @classmethod
    def tool_must_be_registered(cls, v):
        VALID_TOOLS = {
            "search_universities", "match_scholarships",
            "calculate_financials", "extract_document", "send_email_report"
        }
        if v not in VALID_TOOLS:
            raise ValueError(f"Unknown tool: {v}. Must be one of {VALID_TOOLS}")
        return v

class FinishAction(BaseModel):
    action_type: Literal["finish"]
    final_response: str
    reasoning: str

AgentAction = CallToolAction | FinishAction

def parse_agent_action(text: str) -> AgentAction:
    """Parse LLM output into AgentAction. Raises ValueError on failure."""
    import json, re
    # Try JSON fence first
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    raw = m.group(1) if m else re.search(r"\{.*\}", text, re.DOTALL)
    if not raw:
        raise ValueError("No JSON object found in LLM response")
    data = json.loads(raw if isinstance(raw, str) else raw.group(0))
    if data.get("action_type") == "call_tool":
        return CallToolAction(**data)
    elif data.get("action_type") == "finish":
        return FinishAction(**data)
    raise ValueError(f"Unknown action_type: {data.get('action_type')}")
```

#### [MODIFY] `backend/agents/state.py`
Add to `AgentState`:
```python
messages: List[Dict]          # conversation trajectory
observations: List[Dict]      # [{tool, args, result, source, retrieved_at}]
current_thought: str          # reasoning at current step
turn_count: int               # iteration counter
max_turns: int                # default 8
verifier_critique: str        # feedback from verifier
pending_approval: bool        # HITL gate flag
pending_action: Dict          # serialized action awaiting approval
```

#### [MODIFY] `backend/agents/orchestrator.py` — **Major Refactor**

Replace the entire static pipeline with three nodes:

**`agent_decide_node(state)`**
```
1. Get tool schemas from MCP client (list_tools — cached)
2. Build ReAct prompt: system role + tool schemas + observations + turn_count
3. Call ainvoke_llm()
4. Parse response → AgentAction (Pydantic)
5. On parse failure: retry once with correction prompt
6. Increment turn_count
7. Return updated state with current_thought + pending action
```

**`tool_execute_node(state)`**
```
1. Read CallToolAction from state
2. If tool == "send_email_report" and requires_approval → set pending_approval=True, return (pauses graph via LangGraph interrupt)
3. Call mcp_client.execute_tool(name, args)
4. On success: append observation to state.observations
5. On error: append error observation (never swallow — {tool, error: "...", source: "mcp"})
6. Return updated state
```

**Routing:**
```
START → agent_decide_node
agent_decide_node → call_tool → tool_execute_node  (if turn_count < max_turns)
agent_decide_node → call_tool → force_finish_node  (if turn_count >= max_turns)
agent_decide_node → finish → verifier_node
tool_execute_node → agent_decide_node
force_finish_node → END
verifier_node → approved → END
verifier_node → critique → agent_decide_node  (max 2 correction rounds)
```

**Remove entirely:**
- `should_run_profile`, `should_run_university`, `should_run_scholarship`, `should_run_finance`, `should_run_timeline`, `should_run_report`
- `orchestrator_node`
- All static conditional edges
- `profile_agent`, `country_recommendation_node`, `university_agent`, `scholarship_agent`, `finance_agent`, `timeline_agent`, `report_agent` as **LangGraph nodes** — these become tool implementations inside the MCP server

#### [MODIFY] `backend/prompts/orchestrator_prompts.py`
New ReAct system prompt template:
```python
REACT_SYSTEM_PROMPT = """
You are EduPilot AI, a study-abroad advisor for Indian students.
You operate in a Reason → Act → Observe → Repeat loop.

## Available Tools
{tool_schemas_json}

## Rules
- Output ONLY valid JSON matching one of:
  {{"action_type": "call_tool", "tool_name": "...", "tool_args": {{...}}, "reasoning": "..."}}
  {{"action_type": "finish", "final_response": "...", "reasoning": "..."}}
- Only use tool names from the Available Tools list above.
- Before finishing, verify every claim exists in your observations.
- Turn {turn_count} of {max_turns} maximum.
{verifier_critique_section}

## Student Profile
{profile_json}

## Prior Observations
{observations_json}

## User Request
{user_query}

Output your next action as JSON:
"""
```

#### [MODIFY] `backend/agents/llm.py`
- Replace `except Exception as e: return f"[LLM unavailable: {str(e)}]", 0` with:
  - Log full error via `structlog`
  - Raise typed `LLMError(message, provider)` exception
  - Caller (`agent_decide_node`) catches and appends as error observation
- Add `tenacity` retry decorator to `_invoke_gemini` (already in requirements — just not used):
  ```python
  from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
  @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), ...)
  ```

---

### Phase 3: Verifier / Reflection Node *(Day 6)*

#### [NEW] `backend/agents/verifier.py`

```python
"""
Verifier Node — grounds agent output against tool observations.
Implements the L2-required reflection/evaluation pass.
"""

async def verifier_node(state: AgentState) -> AgentState:
    observations = state.get("observations", [])
    finish_action = state.get("pending_finish_action", {})
    profile = state.get("student_profile", {})
    
    issues = []
    
    # Check 1: CGPA eligibility
    for uni in finish_action.get("universities", []):
        obs_cgpa = _find_uni_cgpa_requirement(uni["name"], observations)
        if obs_cgpa and profile.get("cgpa", 0) < obs_cgpa:
            issues.append(f"CGPA_MISMATCH: {uni['name']} requires {obs_cgpa} but student has {profile['cgpa']}")
    
    # Check 2: Budget compliance  
    cost = _find_total_cost(observations)
    budget = profile.get("total_budget_usd", float("inf"))
    if cost and cost > budget:
        issues.append(f"BUDGET_EXCEEDED: cost ${cost} > budget ${budget}")
    
    # Check 3: Fact grounding — every university/scholarship in response must be in an observation
    for name in _extract_entity_names(finish_action.get("final_response", "")):
        if not _entity_in_observations(name, observations):
            issues.append(f"UNGROUNDED_FACT: '{name}' not found in any tool observation")
    
    if not issues:
        return {**state, "verified": True}
    
    critique = "Verifier found issues:\\n" + "\\n".join(f"- {i}" for i in issues)
    return {
        **state,
        "verified": False,
        "verifier_critique": critique,
        "verifier_rounds": state.get("verifier_rounds", 0) + 1,
    }
```

---

### Phase 4: Shared Report Data Contract *(Day 6)*

#### [NEW] `backend/schemas/report_schema.py`
```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ObservationRecord(BaseModel):
    tool: str
    args: dict
    result: dict
    source: str = "mcp"
    retrieved_at: datetime

class ReportContent(BaseModel):
    profile: dict
    recommended_countries: List[dict] = []
    recommended_universities: List[dict] = []
    matched_scholarships: List[dict] = []
    finance_breakdown: dict = {}
    application_timeline: List[dict] = []
    final_recommendation: str = ""
    observations: List[ObservationRecord] = []
    verified: bool = False
    generated_at: datetime = datetime.utcnow()
```

#### [MODIFY] `backend/services/report_service.py`
- Import `ReportContent` and validate before PDF generation.
- Read all fields from `ReportContent` model — no more dual-key aliasing.
- Fix the syntax error on line 203 (Phase 0 action repeated here as dependency).

---

### Phase 5: API Routes — SSE Streaming & HITL *(Day 7)*

#### [MODIFY] `backend/app/api/v1/agents.py`
Add two new endpoints:

**`POST /api/v1/agents/stream`** (SSE):
```python
from fastapi.responses import StreamingResponse
import asyncio

@router.post("/stream")
async def stream_agent(request: AgentRunRequest):
    async def event_generator():
        # Run LangGraph workflow with event callbacks
        async for event in run_workflow_with_events(request):
            yield f"data: {json.dumps(event)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

SSE event types emitted:
```json
{"type": "thought", "content": "I need to check universities first"}
{"type": "tool_call", "tool": "search_universities", "args": {...}}
{"type": "observation", "tool": "search_universities", "result": {...}, "source": "mcp"}
{"type": "verifier", "status": "pass"}
{"type": "hitl_required", "action": "send_email_report", "session_id": "..."}
{"type": "finish", "response": "..."}
```

**`POST /api/v1/agents/approve`** (HITL):
```python
@router.post("/approve")
async def approve_action(session_id: str, approved: bool):
    # Resume LangGraph from HITL interrupt
    ...
```

**Fix `_persist_logs`**:
- Log per-tool status from actual observation: `{"tool": name, "status": "success"|"error", "duration_ms": ...}`
- Never write blanket `status="success"` for every executed node.

---

### Phase 6: Frontend Updates *(Day 8)*

#### [MODIFY] `frontend/src/lib/api.ts`
Extend the existing 54-line file with SSE streaming and HITL:
```typescript
// Add to existing api.ts

// ── Agent Streaming ────────────────────────────────────────────────────────
export function streamAgentEvents(
  query: string,
  sessionId: string | undefined,
  onEvent: (event: AgentEvent) => void
): EventSource {
  const url = `/api/v1/agents/stream`
  // POST-based SSE via fetch (EventSource only supports GET)
  const controller = new AbortController()
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, session_id: sessionId }),
    signal: controller.signal,
  }).then(async res => {
    const reader = res.body!.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const lines = decoder.decode(value).split('\n')
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try { onEvent(JSON.parse(line.slice(6))) } catch {}
        }
      }
    }
  })
  return controller as any  // return controller so caller can abort
}

// ── HITL Approval ─────────────────────────────────────────────────────────
export const approveAction = (sessionId: string, approved: boolean) =>
  api.post('/agents/approve', { session_id: sessionId, approved })
```

#### [MODIFY] `frontend/src/pages/ChatPage.tsx`
- Replace direct `agentApi.chat()` calls with `streamAgentEvents()`.
- Render live **Thought Trajectory Accordion**:
  ```
  🤔 Thinking...  [reasoning text]
  🔧 Tool: search_universities  {country: "Canada", max_tuition_usd: 30000}
  📊 Observation: 4 universities found
  ✅ Verifier: All facts grounded
  💬 Final Answer: [response]
  ```

#### [NEW] `frontend/src/components/ApprovalModal.tsx`
- Shown when `event.type === "hitl_required"`.
- Displays: recipient email, report preview.
- Approve / Reject buttons call `approveAction(sessionId, true/false)`.

---

### Phase 7: Security *(Day 9)*

#### [DELETE] `backend/mcp_tools/postgres_mcp.py`
- All DB access now goes through typed MCP server tools — NL-to-SQL is gone.

#### [MODIFY] `backend/agents/university_agent.py` (if retained as helper)
- Remove the `GLOBAL_RECOMMENDATION_PROMPT` instruction to use "global knowledge" for real universities.
- LLM may only report universities that appear in `search_universities` tool observations.
- All university fields must have `source: "database"` tag.

#### [MODIFY] `backend/app/api/v1/reports.py`
- Replace direct `GmailMCPClient()` call with a call that goes through the HITL gate first.
- Validate report data against `ReportContent` Pydantic schema before PDF generation.

---

### Phase 8: Test Suite *(Days 10–11)*

#### [NEW] `backend/tests/conftest.py`
- Pytest fixtures: mock DB session, mock MCP client, sample student profiles.

#### [NEW] `backend/tests/test_syntax.py`
```python
def test_backend_compiles():
    import compileall, sys
    result = compileall.compile_dir("backend", quiet=True)
    assert result == 1  # 1 = success
```

#### [NEW] `backend/tests/test_mcp_server.py`
```python
async def test_list_tools_returns_5_tools(): ...
async def test_search_universities_with_valid_params(): ...
async def test_search_universities_empty_db_returns_empty_list(): ...
async def test_match_scholarships_cgpa_filter(): ...
async def test_calculate_financials_is_deterministic(): ...
async def test_unknown_tool_returns_error_dict(): ...
```

#### [NEW] `backend/tests/test_agent_loop.py`
```python
async def test_react_loop_calls_tool_then_finishes(): ...
async def test_max_iterations_exits_gracefully(): ...
async def test_malformed_action_json_retried_once(): ...
async def test_unknown_tool_becomes_error_observation(): ...
async def test_verifier_catches_cgpa_mismatch(): ...
async def test_verifier_correction_triggers_replan(): ...
async def test_hitl_pauses_before_email_send(): ...
```

#### [NEW] `backend/tests/test_report_service.py`
```python
def test_report_content_schema_validates(): ...
def test_pdf_generates_without_syntax_error(): ...
def test_pdf_all_sections_present(): ...
```

#### [NEW] `backend/tests/evals/student_scenarios.py`
4 benchmark cases with mock LLM, real tool logic:
1. **Low CGPA (5.8)** + high budget → verifier rejects CGPA 7.5 universities, re-plans to lower-threshold ones.
2. **High backlogs + low budget** → agent calls `match_scholarships` before `calculate_financials`.
3. **Empty DB result** → agent observes empty list, doesn't hallucinate, calls different tool.
4. **Cost hallucination** → verifier flags ungrounded number → agent corrects using `calculate_financials` observation.

---

## Evidence / Trace Capture (Required for Grading)

| Trace | Where to Save | What it Proves |
|---|---|---|
| `list_tools()` output | `traces/mcp_list_tools.json` | Real MCP discovery works |
| Full SSE session | `traces/react_session_01.jsonl` | ReAct loop with tool calls + observations |
| Verifier correction | `traces/verifier_correction_01.jsonl` | Reflection changes the answer |
| HITL approval | `traces/hitl_email_approval.jsonl` | Human-in-the-loop works |
| PDF smoke test | `traces/pdf_smoke_test_output.pdf` | All 5 sections render |

---

## Verification Commands

```bash
# 1. Syntax check
python -m compileall -q backend

# 2. All tests
cd backend && .\venv\Scripts\pytest tests/ -v --tb=short

# 3. Eval benchmarks
.\venv\Scripts\pytest tests/evals/ -v

# 4. Frontend type check
cd frontend && npx tsc --noEmit

# 5. MCP server smoke test
cd backend && .\venv\Scripts\python -m mcp_server.server --help
```

---

## Execution Summary

```
Phase 0   Phase 0b  Phase 1   Phase 2   Phase 3   Phase 4   Phase 5   Phase 6   Phase 7   Phase 8
─────────────────────────────────────────────────────────────────────────────────────────────────
Env Fix   DB Setup  MCP       ReAct     Verifier  Report    API+SSE   Frontend  Security  Tests
+ Model   + Scripts Server    Loop      Node      Schema    Streaming UI Polish  Hardening + Evals
Day 1     Day 1     Day 2-3   Day 4-5   Day 6     Day 6     Day 7     Day 8     Day 9     Day 10-11
```

**Total: ~11 days of focused work. No Docker anywhere in the pipeline.**
