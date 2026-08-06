"""
Generate EduPilot AI SRS Document as DOCX
Uses only Python stdlib — no lxml required.
"""
import zipfile, os, datetime, textwrap
from pathlib import Path

OUT = Path(r"C:\Users\SonamGiri\Desktop\Temp\EduNavigtor ai\EduPilot_AI_SRS.docx")

# ── DOCX XML helpers ──────────────────────────────────────────
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def para(text, bold=False, size=22, color="000000", align="left", italic=False, mono=False):
    a = {"left":"left","center":"center","right":"right"}.get(align,"left")
    jc = f'<w:jc w:val="{a}"/>' if align != "left" else ""
    rpr_parts = []
    if bold:  rpr_parts.append("<w:b/>")
    if italic:rpr_parts.append("<w:i/>")
    font = 'Courier New' if mono else 'Calibri'
    rpr_parts.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}"/>')
    rpr_parts.append(f'<w:color w:val="{color}"/>')
    rpr_parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = "<w:rPr>"+"".join(rpr_parts)+"</w:rPr>"
    lines = esc(text).replace('&#10;','\n').split('\n')
    runs = "".join(
        f'<w:r>{rpr}<w:t xml:space="preserve">{l}</w:t></w:r><w:r><w:br/></w:r>'
        if i < len(lines)-1 else
        f'<w:r>{rpr}<w:t xml:space="preserve">{l}</w:t></w:r>'
        for i,l in enumerate(lines)
    )
    return f'<w:p><w:pPr>{jc}<w:spacing w:before="80" w:after="60"/></w:pPr>{runs}</w:p>'

def heading(text, level=1):
    sizes  = {1:40, 2:32, 3:26}
    colors = {1:"667eea", 2:"1a1a2e", 3:"444444"}
    s, c = sizes.get(level,24), colors.get(level,"000000")
    return f'<w:p><w:pPr><w:spacing w:before="200" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="{c}"/><w:sz w:val="{s}"/><w:szCs w:val="{s}"/></w:rPr><w:t>{esc(text)}</w:t></w:r></w:p>'

def bullet(text, level=0):
    indent = 360 + level*360
    return f'<w:p><w:pPr><w:ind w:left="{indent}"/><w:spacing w:before="40" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">• {esc(text)}</w:t></w:r></w:p>'

def spacer(): return '<w:p><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr></w:p>'
def pagebreak(): return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def table_row(cells, header=False):
    bg  = '<w:shd w:val="clear" w:fill="667eea"/>' if header else ''
    fc  = "FFFFFF" if header else "000000"
    bld = "<w:b/>" if header else ""
    tds = ""
    for c in cells:
        tds += f'<w:tc><w:tcPr>{bg}<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar></w:tcPr><w:p><w:r><w:rPr>{bld}<w:color w:val="{fc}"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{esc(c)}</w:t></w:r></w:p></w:tc>'
    return f'<w:tr>{tds}</w:tr>'

def make_table(headers, rows):
    tr = table_row(headers, header=True)
    for r in rows: tr += table_row(r)
    return f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="CCCCCC"/><w:left w:val="single" w:sz="4" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="4" w:color="CCCCCC"/><w:right w:val="single" w:sz="4" w:color="CCCCCC"/><w:insideH w:val="single" w:sz="4" w:color="CCCCCC"/><w:insideV w:val="single" w:sz="4" w:color="CCCCCC"/></w:tblBorders></w:tblPr>{tr}</w:tbl>'

# ── Build document body ───────────────────────────────────────
body = []
today = datetime.date.today().strftime("%B %d, %Y")

# Cover
body += [
    spacer(), spacer(),
    para("EduPilot AI", bold=True, size=52, color="667eea", align="center"),
    para("Multi-Agent Study Abroad Copilot", bold=True, size=28, color="764ba2", align="center"),
    spacer(),
    para("Software Requirements Specification (SRS)", bold=True, size=24, color="1a1a2e", align="center"),
    spacer(),
    para(f"Version 1.0   |   {today}", size=20, color="666666", align="center"),
    spacer(),
    para("Gemini 3.5 Flash Lite · LangGraph · FastAPI · React · PostgreSQL", italic=True, size=18, color="888888", align="center"),
    pagebreak(),
]

# ── Section 1: Introduction ───────────────────────────────────
body += [
    heading("1. Introduction", 1),
    heading("1.1 Purpose", 2),

    para("Background & Problem Statement", bold=True, size=21, color="667eea"),
    para("Every year, over 750,000 Indian students travel abroad for higher education. The process of planning a study abroad journey is extremely complex, time-consuming, and expensive when done through traditional consultants. Students must independently research hundreds of universities, compare costs across multiple countries, identify scholarships they qualify for, prepare application documents, track deadlines, and navigate visa requirements — all while completing their undergraduate degree.", size=20),
    spacer(),

    para("What EduPilot AI Does", bold=True, size=21, color="667eea"),
    para("EduPilot AI is a production-quality autonomous multi-agent AI platform that replaces the traditional study abroad consultant. It is not a simple chatbot or a static information website. It is an intelligent system that:", size=20),
    bullet("Understands the student's complete academic profile — CGPA, backlogs, test scores, budget, career goals"),
    bullet("Autonomously decides which AI agents to run based on what the student is asking"),
    bullet("Queries a real PostgreSQL database of universities and scholarships"),
    bullet("Uses Gemini 3.5 Flash Lite (Google's latest AI model) to reason, recommend, and explain"),
    bullet("Generates personalised university recommendations from across the world — not a generic list"),
    bullet("Matches the student to scholarships they are actually eligible for, with specific eligibility reasoning"),
    bullet("Calculates a detailed budget breakdown in both USD and INR for each university option"),
    bullet("Builds a personalised month-by-month application timeline based on the student's current situation"),
    bullet("Generates a complete PDF study abroad report that can be downloaded or sent via Gmail"),
    bullet("Remembers every conversation and allows the student to resume previous sessions"),
    spacer(),

    para("Who This Document Is For", bold=True, size=21, color="667eea"),
    para("This Software Requirements Specification (SRS) serves as the primary technical reference document for:", size=20),
    bullet("Software developers building or extending EduPilot AI"),
    bullet("QA engineers writing test cases against the defined requirements"),
    bullet("Product managers and stakeholders evaluating system capabilities"),
    bullet("Academic evaluators reviewing the project architecture and design decisions"),
    bullet("Future contributors onboarding to the open-source project"),
    spacer(),

    para("What Makes This Different From a Chatbot", bold=True, size=21, color="667eea"),
    make_table(["Aspect", "Traditional Chatbot", "EduPilot AI Multi-Agent System"],[
        ["Query Handling",   "Single LLM response",           "Orchestrator routes to 1-7 specialist agents"],
        ["Data Source",      "LLM training data only",        "Live PostgreSQL DB + Gemini global knowledge"],
        ["University Data",  "Generic, possibly outdated",    "Real seeded data: 11 universities, 8 scholarships, 7 countries"],
        ["Scholarships",     "Generic suggestions",           "Eligibility-filtered, with specific gaps flagged"],
        ["Budget",           "Rough estimates",               "Precise USD + INR breakdown per university"],
        ["Reasoning",        "Generic paragraph responses",   "Structured tables with specific profile-referenced reasoning"],
        ["Memory",           "None / session-only",           "Persistent DB sessions — resume anytime"],
        ["Output",           "Text only",                     "Tables, PDF reports, Gmail delivery"],
        ["Follow-ups",       "Starts fresh each time",        "Answers from conversation context instantly"],
    ]),
    spacer(),

    para("Technology Philosophy", bold=True, size=21, color="667eea"),
    para("EduPilot AI was built with a strict constraint: use only free and open-source technologies. No paid APIs are required to run the system. The entire platform runs locally using Docker Compose with:", size=20),
    bullet("Gemini 3.5 Flash Lite — Google's free-tier API with 1,500 requests/day"),
    bullet("Ollama + Qwen2.5 — fully local LLM fallback when Gemini quota is exhausted"),
    bullet("PostgreSQL — open-source database, self-hosted in Docker"),
    bullet("FastAPI, React, LangGraph — all MIT-licensed open-source frameworks"),
    spacer(),

    heading("1.2 Scope", 2),
    para("EduPilot AI covers the complete study abroad planning lifecycle for Indian students targeting postgraduate education abroad. The system scope includes:", size=20),
    bullet("Geographic coverage: USA, UK, Canada, Australia, Germany, Ireland, New Zealand + global Gemini knowledge"),
    bullet("Academic levels: Postgraduate Masters programs (MSc, MEng, MBA, MCS)"),
    bullet("Target users: Indian undergraduate students planning their first international degree"),
    bullet("Budget range: $2,000 to $150,000 USD total program cost"),
    bullet("Intake windows: Fall and Spring intakes from 2025 to 2090"),
    spacer(),
    para("Out of Scope:", bold=True, size=20),
    bullet("Undergraduate admissions counselling"),
    bullet("PhD or doctoral program guidance"),
    bullet("Student visa applications (guidance only — not submission)"),
    bullet("Actual university application submission (guidance only)"),
    bullet("Financial loan processing or bank integrations"),

    heading("1.3 Key Definitions", 2),
    make_table(["Term","Definition"],[
        ["MCP","Model Context Protocol — pluggable tool integration layer for AI agents"],
        ["LangGraph","Graph-based multi-agent orchestration framework by LangChain"],
        ["Orchestrator","Master agent that analyses the user query and decides which specialist agents to invoke"],
        ["AgentState","Shared TypedDict object that all LangGraph agents read from and write to"],
        ["CGPA","Cumulative Grade Point Average — academic performance metric used for admission screening"],
        ["PGWP","Post-Graduate Work Permit — Canadian visa allowing graduates to work for up to 3 years post-study"],
        ["SOP","Statement of Purpose — application essay explaining academic and career goals"],
        ["LOR","Letter of Recommendation — academic reference letter from professors or employers"],
        ["Gemini","Google's large language model — used for all AI reasoning, recommendations, and report generation"],
        ["Ollama","Local LLM runtime — runs Qwen2.5 on CPU as fallback when Gemini is unavailable"],
        ["Blocked Account","German bank account (Sperrkonto) holding ~€11,904 as proof of funds for student visa"],
        ["uni-assist","German university application portal used by most public universities"],
        ["QS Rank","QS World University Rankings — global university ranking system used for comparison"],
    ]),

    heading("1.4 System Overview", 2),
    para("EduPilot AI is NOT a chatbot. It is an autonomous multi-agent system where:", size=20),
    bullet("The Orchestrator Agent analyses every user query and decides which specialist agents to invoke"),
    bullet("Agents run sequentially via LangGraph, each reading from and writing to a shared AgentState"),
    bullet("Each agent queries PostgreSQL, calls Gemini, and produces structured bullet-point + table output"),
    bullet("Responses are context-aware: scholarship queries get scholarship tables, cost queries get budget breakdowns"),
    bullet("All conversations are persisted in PostgreSQL and can be resumed at any time"),
    bullet("Reports are auto-generated after every meaningful agent session and available as PDF"),
    bullet("The system includes a complete React frontend with 10 pages covering every aspect of study abroad planning"),
    pagebreak(),
]

# ── Section 2: Architecture ───────────────────────────────────
body += [
    heading("2. System Architecture", 1),
    heading("2.1 Architecture Layers", 2),
    make_table(["Layer","Technology","Responsibility"],[
        ["Frontend","React 18 + Vite + TypeScript + Tailwind CSS","Browser SPA — 10 pages, communicates via REST API"],
        ["Backend API","FastAPI (Python 3.12) + Uvicorn","REST server, DB sessions, agent trigger"],
        ["Agent Orchestration","LangGraph 0.2 + Gemini 3.5 Flash Lite","7 agents, dynamic routing, shared state"],
        ["Data Layer","PostgreSQL 16 + SQLAlchemy 2.0 async","All structured data storage"],
        ["MCP Tools","Gmail · Filesystem · PostgreSQL","Email, document extraction, NL queries"],
        ["LLM","Gemini 3.5 Flash Lite (primary) + Ollama (fallback)","All reasoning and generation"],
    ]),
    spacer(),
    heading("2.2 Architecture Diagram", 2),
    para("""
┌─────────────────────────────────────────────────────────────────────┐
│                     STUDENT (Browser)                               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTPS
┌───────────────────────────────▼─────────────────────────────────────┐
│         REACT FRONTEND  (localhost:3000)                            │
│  Dashboard · AI Copilot · Profile · Universities · Budget · Reports │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ REST API /api/v1
┌───────────────────────────────▼─────────────────────────────────────┐
│              FASTAPI BACKEND  (localhost:8000)                      │
│    /auth  /profile  /agents  /universities  /reports               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                   LANGGRAPH ORCHESTRATOR                            │
│      Reads query → builds agents_to_run list → routes              │
│                                                                     │
│  [Profile] [Country] [University] [Scholarship] [Finance]          │
│  [Timeline] [Report]                                                │
└──────────┬──────────────────────────────┬─────────────────────────┬─┘
           │                              │                         │
┌──────────▼──────┐        ┌──────────────▼──────┐  ┌─────────────▼──┐
│  PostgreSQL DB  │        │  Gemini 3.5 Flash   │  │  MCP Tools     │
│  Universities   │        │  Flash Lite (LLM)   │  │  Gmail         │
│  Scholarships   │        │  + Ollama Fallback  │  │  Filesystem    │
│  Profiles       │        └─────────────────────┘  │  PostgreSQL    │
│  Sessions       │                                  └────────────────┘
│  Reports        │
└─────────────────┘""", mono=True, size=16),
    pagebreak(),
]

# ── Section 3: LangGraph Workflow ─────────────────────────────
body += [
    heading("3. LangGraph Multi-Agent Workflow", 1),
    heading("3.1 Workflow Overview", 2),
    para("The LangGraph workflow is NOT a fixed pipeline. The Orchestrator dynamically decides which agents to invoke based on the user query. Unneeded agents are skipped entirely.", size=20),
    heading("3.2 Agent Execution Flow", 2),
    para("""
User Query
    │
    ▼
[ORCHESTRATOR NODE]
    ├── direct_answer=true ──→ [GEMINI answers from chat history] ──→ END
    │
    ▼
[PROFILE AGENT]        ← runs only if profile incomplete
    │  Extracts CGPA, IELTS, budget from query
    ▼
[COUNTRY RECOMMENDATION]  ← rule-based scoring + Gemini explanation
    │  Scores: budget fit, preferred countries, post-study work
    ▼
[UNIVERSITY AGENT]     ← skipped if not asked
    │  PostgreSQL query + Gemini global knowledge
    │  Returns 5 unis from 3+ countries
    │  Table: name, location, cost, scholarships
    ▼
[SCHOLARSHIP AGENT]    ← skipped if not asked
    │  PostgreSQL eligibility filter (CGPA, IELTS)
    │  Table: name, provider, basis, amount, deadline
    ▼
[FINANCE AGENT]        ← skipped if not asked
    │  Tuition + living + visa + insurance per university
    │  USD and INR amounts, affordability assessment
    ▼
[TIMELINE AGENT]       ← skipped if not asked
    │  Month-by-month roadmap
    │  Skips completed steps (has IELTS → skip prep)
    ▼
[REPORT AGENT]         ← runs for full plan queries
    │  Assembles all outputs, generates executive summary
    │  Auto-saves PDF to Reports section
    ▼
run_orchestrator() picks correct message based on query intent:
    ├── scholarship query  → scholarship table
    ├── university query   → university table with scholarships
    ├── cost query         → budget breakdown table
    ├── timeline query     → month-by-month roadmap
    └── full plan query    → complete report""", mono=True, size=16),
    spacer(),
    heading("3.3 Agent Routing Rules", 2),
    make_table(["User Query","Agents Invoked","Response Format"],[
        ["Give me my complete study abroad plan","ALL 7 agents","Full report — all sections"],
        ["Suggest universities","profile + country + university","Table: name, location, cost, scholarships"],
        ["What scholarships am I eligible for?","profile + scholarship","Table: name, basis, amount, eligibility"],
        ["What is the total cost?","finance (or direct answer)","Budget breakdown table per university"],
        ["Show my timeline","timeline","Month-by-month roadmap with priorities"],
        ["Follow-up question","NONE — direct_answer=true","Gemini answers from chat history instantly"],
        ["Profile details mentioned","profile_agent","Updated profile confirmation"],
    ]),
    pagebreak(),
]

# ── Section 4: Functional Requirements ───────────────────────
body += [heading("4. Functional Requirements", 1)]
modules = [
    ("4.1 Student Profile",[
        "FR-01: Create and update academic profile (CGPA, backlogs, degree)",
        "FR-02: Enter test scores: IELTS, TOEFL, GRE, GMAT",
        "FR-03: Select preferred countries via toggle buttons",
        "FR-04: Set course interest, career goal, target intake (2025–2090)",
        "FR-05: Set total budget and funding source",
        "FR-06: Upload documents for auto-extraction (resume, marksheet, IELTS, SOP)",
        "FR-07: Auto-extract CGPA and scores from uploaded documents via Gemini",
    ]),
    ("4.2 AI Copilot",[
        "FR-08: Natural language query interface",
        "FR-09: Orchestrator routes to relevant agents only",
        "FR-10: Persistent conversation history per session",
        "FR-11: Session history sidebar — view all previous chats",
        "FR-12: Resume any previous chat session with full context",
        "FR-13: Start new chat session at any time",
        "FR-14: Follow-up questions answered instantly from history",
        "FR-15: Responses rendered as tables and bullet points",
        "FR-16: Response timer shows Gemini latency",
    ]),
    ("4.3 Universities",[
        "FR-17: Recommend exactly 5 universities from 3+ countries",
        "FR-18: Table: name, city, country, tuition, living cost, scholarships, chances",
        "FR-19: Per-university scholarship table: name, basis, amount, deadline",
        "FR-20: Backlog acceptance policy shown per university",
        "FR-21: Categories: Safe / Match / Reach based on profile",
        "FR-22: Browse and filter all universities by country, tuition, ranking",
        "FR-23: Full university detail page with programs and employment rate",
        "FR-24: Compare up to 4 universities side-by-side",
    ]),
    ("4.4 Scholarships",[
        "FR-25: Filter scholarships by CGPA and IELTS eligibility",
        "FR-26: Table: name, provider, basis, amount, eligibility match",
        "FR-27: Explain WHY each scholarship fits the student",
        "FR-28: Flag eligibility gaps with specific gaps to address",
        "FR-29: Provide action steps for each application",
        "FR-30: Show deadline and direct application URL",
    ]),
    ("4.5 Finance",[
        "FR-31: Calculate tuition + living + visa + insurance per university",
        "FR-32: Show costs in USD and INR",
        "FR-33: Net cost after scholarship savings",
        "FR-34: Affordability assessment vs student budget",
        "FR-35: Education loan advice for Indian banks",
        "FR-36: Interactive budget calculator with bar charts",
    ]),
    ("4.6 Timeline",[
        "FR-37: Month-by-month personalised roadmap",
        "FR-38: Skip steps already completed",
        "FR-39: Priority levels: Critical / High / Medium",
        "FR-40: Tasks list per milestone",
        "FR-41: Mark milestones complete",
        "FR-42: Progress bar with completion percentage",
    ]),
    ("4.7 Reports",[
        "FR-43: Auto-generate report after every agent session",
        "FR-44: Include all sections: profile, unis, scholarships, finance, timeline",
        "FR-45: PDF generated within 60 seconds",
        "FR-46: PDF download from Reports page",
        "FR-47: Send report to any Gmail address",
        "FR-48: Reports page auto-refreshes every 10 seconds",
    ]),
]
for title, reqs in modules:
    body.append(heading(title, 2))
    for r in reqs: body.append(bullet(r))
    body.append(spacer())
body.append(pagebreak())

# ── Section 5: Non-Functional Requirements ────────────────────
body += [
    heading("5. Non-Functional Requirements", 1),
    make_table(["Category","Requirement","Target"],[
        ["Performance","AI response (Gemini)","3–10 seconds"],
        ["Performance","AI response (Ollama fallback)","30–120 seconds on CPU"],
        ["Performance","API response (non-AI)","< 200ms"],
        ["Performance","PDF generation","< 60 seconds"],
        ["Security","API keys","Environment variables only — never in code or git"],
        ["Security","Database credentials","Docker Compose env vars"],
        ["Usability","Responsive design","Mobile + desktop (Tailwind CSS)"],
        ["Usability","Accessibility","ARIA labels on all interactive elements"],
        ["Reliability","LLM fallback","Gemini fails → Ollama/Qwen2.5 automatic fallback"],
        ["Portability","Deployment","Docker Compose — single command: docker compose up -d"],
        ["Cost","LLM","Gemini free tier: 1,500 requests/day at zero cost"],
        ["Cost","Infrastructure","100% open-source, no paid APIs required"],
    ]),
    pagebreak(),

    heading("6. Database Schema", 1),
    heading("6.1 Entity Relationships", 2),
    para("""
users (1) ──────────── (1) student_profiles
  │
  ├─── (N) applications ──── (1) universities ──── (1) countries
  ├─── (N) reports
  ├─── (N) agent_logs
  └─── (N) chat_sessions

scholarships (N) ──── (1) universities  [optional — some are standalone]""", mono=True, size=18),
    spacer(),
    heading("6.2 Core Tables", 2),
    make_table(["Table","Key Columns"],[
        ["users","id, email, full_name, hashed_password, is_active, gmail_token"],
        ["student_profiles","user_id FK, cgpa, backlogs, ielts_score, preferred_countries JSONB, total_budget_usd, documents JSONB"],
        ["countries","name, code, avg_tuition_usd, avg_living_cost_usd, post_study_work_years, pros/cons JSONB"],
        ["universities","country_id FK, name, qs_world_rank, min_cgpa, min_ielts, avg_tuition_usd, programs JSONB, scholarships JSONB"],
        ["scholarships","university_id FK (nullable), name, provider, scholarship_type, amount_usd, eligible_countries JSONB"],
        ["reports","user_id FK, session_id, report_type, content JSONB, pdf_path, email_sent"],
        ["agent_logs","user_id FK, session_id, agent_name, status, input_data JSONB, output_data JSONB, tokens_used"],
        ["chat_sessions","user_id FK, session_id UNIQUE, title, messages JSONB, updated_at"],
        ["applications","user_id FK, university_id FK, program_name, intake, status, deadlines JSONB"],
    ]),
    pagebreak(),

    heading("7. API Reference", 1),
    make_table(["Method","Endpoint","Description"],[
        ["GET","/health","Service health check"],
        ["GET","/api/v1/auth/me","Get current user"],
        ["GET","/api/v1/profile","Get student profile"],
        ["POST","/api/v1/profile","Create profile"],
        ["PUT","/api/v1/profile","Update profile"],
        ["POST","/api/v1/profile/upload-document","Upload & auto-extract document"],
        ["POST","/api/v1/agents/chat","Conversational AI chat"],
        ["GET","/api/v1/agents/sessions","List all chat sessions"],
        ["GET","/api/v1/agents/sessions/{id}","Get session with full history"],
        ["DELETE","/api/v1/agents/sessions/{id}","Delete session"],
        ["GET","/api/v1/agents/logs","Agent execution logs"],
        ["GET","/api/v1/universities","List universities (filterable)"],
        ["GET","/api/v1/universities/{id}","University detail"],
        ["GET","/api/v1/universities/scholarships/list","All scholarships"],
        ["GET","/api/v1/universities/countries/list","All countries"],
        ["POST","/api/v1/reports/generate","Generate report from session"],
        ["GET","/api/v1/reports","List user reports"],
        ["GET","/api/v1/reports/{id}/download","Download PDF"],
        ["POST","/api/v1/reports/email","Send report via Gmail"],
    ]),
    pagebreak(),

    heading("8. Technology Stack", 1),
    make_table(["Category","Technology","Version","Purpose"],[
        ["Frontend","React","18.3","UI framework"],
        ["Frontend","TypeScript","5.5","Type safety"],
        ["Frontend","Tailwind CSS","3.4","Styling"],
        ["Frontend","TanStack Query","5.56","Data fetching & caching"],
        ["Frontend","Framer Motion","11.5","Animations"],
        ["Frontend","Recharts","2.12","Charts"],
        ["Backend","FastAPI","0.115","REST API"],
        ["Backend","Python","3.12","Runtime"],
        ["Backend","SQLAlchemy","2.0","Async ORM"],
        ["Agents","LangGraph","0.2.28","Multi-agent orchestration"],
        ["LLM","Gemini 3.5 Flash Lite","Latest","Primary AI (free tier)"],
        ["LLM","Ollama + Qwen2.5","0.3.3","Local fallback"],
        ["Database","PostgreSQL","16","Primary DB"],
        ["PDF","ReportLab","4.2","Report generation"],
        ["Containers","Docker Compose","v2.x","Deployment"],
    ]),
    pagebreak(),

    heading("9. Deployment", 1),
    heading("9.1 Quick Start", 2),
    bullet("Prerequisite: Docker Desktop installed and running"),
    bullet("Step 1: git clone https://github.com/ps-sonam-giri/Edupilot-ai.git"),
    bullet("Step 2: Create .env file in project root with: GEMINI_API_KEY=your-key"),
    bullet("Step 3: docker compose up -d"),
    bullet("Step 4: Open http://localhost:3000"),
    bullet("Step 5: My Profile → fill CGPA, budget, course → Save"),
    bullet("Step 6: AI Copilot → ask 'Give me my complete study abroad plan'"),
    spacer(),
    heading("9.2 Services", 2),
    make_table(["Container","Image","Port","Purpose"],[
        ["edupilot_postgres","postgres:16-alpine","5432","Database"],
        ["edupilot_backend","Python 3.12 custom","8000","FastAPI server"],
        ["edupilot_frontend","nginx:alpine","3000","React SPA"],
    ]),
    pagebreak(),

    heading("10. Future Enhancements", 1),
    make_table(["Feature","Description"],[
        ["Multi-user Auth","JWT + Google OAuth for proper user accounts"],
        ["University Data Pipeline","Web scraping to auto-update rankings and deadlines"],
        ["Parallel Agents","LangGraph parallel execution for faster responses"],
        ["Redis Caching","Cache Gemini responses to reduce API calls"],
        ["SOP Generator","AI-powered Statement of Purpose per university"],
        ["Visa Tracker","Document checklist and visa status tracker"],
        ["Interview Prep","AI mock interview agent"],
        ["Mobile App","React Native app for iOS and Android"],
        ["Kubernetes","Production-scale container orchestration"],
        ["Observability","OpenTelemetry + Grafana monitoring"],
    ]),
    spacer(), spacer(),
    para("─" * 80, size=12, color="667eea"),
    para("EduPilot AI — SRS Document v1.0", italic=True, size=18, color="666666", align="center"),
    para(f"Generated on {today} | GitHub: github.com/ps-sonam-giri/Edupilot-ai", size=16, color="888888", align="center"),
]

# ── Assemble and write DOCX ───────────────────────────────────
CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

WORD_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

SETTINGS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="708"/>
</w:settings>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:color="CCCCCC"/>
      <w:left w:val="single" w:sz="4" w:color="CCCCCC"/>
      <w:bottom w:val="single" w:sz="4" w:color="CCCCCC"/>
      <w:right w:val="single" w:sz="4" w:color="CCCCCC"/>
      <w:insideH w:val="single" w:sz="4" w:color="CCCCCC"/>
      <w:insideV w:val="single" w:sz="4" w:color="CCCCCC"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>"""

body_xml = "\n".join(body)
DOCUMENT = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:body>
<w:sectPr>
  <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1360"/>
  <w:pgSz w:w="12240" w:h="15840"/>
</w:sectPr>
{body_xml}
</w:body>
</w:document>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(str(OUT), 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", CONTENT_TYPES)
    z.writestr("_rels/.rels",         RELS)
    z.writestr("word/document.xml",   DOCUMENT)
    z.writestr("word/_rels/document.xml.rels", WORD_RELS)
    z.writestr("word/settings.xml",   SETTINGS)
    z.writestr("word/styles.xml",     STYLES)

print(f"✅ SRS Document saved → {OUT}")
print(f"   File size: {OUT.stat().st_size / 1024:.1f} KB")
