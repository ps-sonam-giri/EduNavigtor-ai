# EduPilot AI – Multi-Agent Study Abroad Copilot

**EduPilot AI** is an end-to-end, production-grade **Multi-Agent AI Platform & Copilot** engineered to guide Indian students through every step of their study abroad journey.

Powered by **LangGraph stateful agent orchestration**, **custom Model Context Protocol (MCP) servers**, **PostgreSQL**, **FastAPI**, **React 18**, and **AI Document Extraction Engine**, EduPilot AI transforms study abroad planning from overwhelming research into an automated, transparent, and personalized experience.

---

## 🏗️ Complete System Architecture

```
                                ┌────────────────────────────────────────────────┐
                                │    React 18 SPA (TypeScript + Tailwind CSS)    │
                                │              http://localhost:3000             │
                                └───────────────────────┬────────────────────────┘
                                                        │ REST API / JSON
                                                        ▼
                                ┌────────────────────────────────────────────────┐
                                │         FastAPI Async Backend (Python 3.12)    │
                                │              http://localhost:8000             │
                                └───────────────┬────────────────┬───────────────┘
                                                │                │
                       ┌────────────────────────┘                └────────────────────────┐
                       ▼                                                                  ▼
 ┌───────────────────────────────────────────┐                                      ┌───────────────────────────┐
 │   LangGraph Multi-Agent Orchestrator      │                                      │    MCP Servers & Tools    │
 │                                           │                                      │                           │
 │  ├── 1. Profile Agent                     │                                      │ ├── Gmail MCP (Port 8001) │
 │  ├── 2. Country Recommendation Agent      │                                      │ ├── Core Tools (Port 8003)│
 │  ├── 3. University Agent                  │                                      │ └── Filesystem PDF MCP    │
 │  ├── 4. Scholarship Agent                 │                                      │                           │
 │  ├── 5. Finance & Budget Agent            │                                      └─────────────┬─────────────┘
 │  ├── 6. Timeline Agent                    │                                                    │
 │  └── 7. Report Agent                      │                                                    │
 └─────────────┬─────────────────────────────┘                                                    │
               │                                                                                  │
               ▼                                                                                  ▼
 ┌───────────────────────────┐                                                      ┌───────────────────────────┐
 │  LLM Engine (Gemini 3.5 / │                                                      │    PostgreSQL Database    │
 │      Ollama Qwen2.5)      │                                                      │   Profiles, Universities, │
 └───────────────────────────┘                                                      │    Scholarships, Reports  │
                                                                                    └───────────────────────────┘
```

---

## 🤖 The 7 Autonomous AI Agents (LangGraph Workflow)

```
                                    User Request / Profile Input
                                                │
                                                ▼
                                   ┌───────────────────────────┐
                                   │   LangGraph Orchestrator  │
                                   └─────────────┬─────────────┘
                                                 │
      ┌──────────────────┬───────────────────────┼───────────────────────┬──────────────────┐
      ▼                  ▼                       ▼                       ▼                  ▼
┌───────────┐   ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐   ┌────────────┐
│  Profile  │   │  Country Rec    │    │  University      │    │  Scholarship    │   │  Finance   │
│   Agent   │   │     Agent       │    │     Agent        │    │     Agent       │   │   Agent    │
└─────┬─────┘   └────────┬────────┘    └────────┬─────────┘    └────────┬────────┘   └─────┬──────┘
      │                  │                      │                       │                  │
      └──────────────────┴──────────────────────┼───────────────────────┴──────────────────┘
                                                │
                                                ▼
                                   ┌───────────────────────────┐
                                   │      Timeline Agent       │
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                   ┌───────────────────────────┐
                                   │       Report Agent        │
                                   └─────────────┬─────────────┘
                                                 │
                                                 ▼
                                ┌─────────────────────────────────┐
                                │ PDF Generation & Email Dispatch │
                                │   (ReportLab & Gmail MCP 8001)  │
                                └─────────────────────────────────┘
```

### Specialized Agents:
1. **Profile Agent (`backend/agents/profile_agent.py`)**: Normalizes CGPA, test scores (IELTS/GRE), work experience, and target degree. Flaggers flag missing data before execution.
2. **Country Recommendation Agent (`backend/agents/country_rec_agent.py`)**: Scores countries (USA, UK, Canada, Germany, Australia, Ireland, etc.) based on budget fit, post-study work visa duration (PSW), PR path feasibility, and academic eligibility.
3. **University Agent (`backend/agents/university_agent.py`)**: Ranks target, moderate, and reach universities from PostgreSQL and Tavily Live Web Search while enforcing reasoning for every recommendation.
4. **Scholarship Agent (`backend/agents/scholarship_agent.py`)**: Matches institutional and government scholarships while highlighting exact eligibility gaps.
5. **Finance & Budget Agent (`backend/agents/finance_agent.py`)**: Calculates 1-year and 2-year cost breakdowns in USD ($) and INR (₹) covering tuition, living costs, visa fees, and insurance minus scholarships.
6. **Timeline Agent (`backend/agents/timeline_agent.py`)**: Builds a month-by-month application roadmap tailored to Fall/Spring intake cycles.
7. **Report Agent (`backend/agents/report_agent.py`)**: Renders comprehensive executive summary reports and compiles downloadable PDF reports via ReportLab.

---

## 🌐 Compare Universities Worldwide Engine

The platform features an advanced **Global University Comparison Engine**:
- **Dynamic Live Web Search Fallback**: Query any university in the world (e.g. Harvard, Oxford, TUM Munich, ETH Zurich, NUS Singapore, IIT Bombay). If not pre-seeded in database, the backend queries live web data to extract QS rank, tuition, acceptance rate, CGPA, IELTS score, and scholarships.
- **Region & Country Filters**: Filter by 14+ world destinations (USA 🇺🇸, UK 🇬🇧, Canada 🇨🇦, Germany 🇩🇪, Australia 🇦🇺, Singapore 🇸🇬, Japan 🇯🇵, India 🇮🇳, Switzerland 🇨🇭, etc.).
- **Side-by-Side Table**: Compare up to 4 universities simultaneously with automatic "Best Choice" highlight badges.

---

## 📑 AI Document Extraction Engine

Located in `backend/tools/document_tools.py`, the engine processes uploaded PDFs (transcripts, test scorecards, resumes):
- **Transcripts**: Auto-detects and extracts CGPA/GPA.
- **IELTS Scorecards**: Auto-detects Listening, Reading, Writing, Speaking bands and TRF number.
- **Resumes/CV**: Structural check of Education, Work Experience, Projects, and Skills.

---

## ⚡ Model Context Protocol (MCP) Integration

EduPilot AI leverages two standalone MCP Servers:
1. **Gmail MCP Server (`http://localhost:8001`)**: Handles direct email dispatch of PDF reports to user inboxes using SMTP with a local fallback queue (`backend/reports/sent_emails/`).
2. **Core Tools MCP Server (`http://localhost:8003`)**: Exposes university search, scholarship lookup, and financial calculation tools over JSON-RPC.

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Frontend** | React 18, Vite, TypeScript | Type-safe Single Page Application |
| **Styling & UI** | Tailwind CSS, Framer Motion, Lucide Icons | Animated, responsive interface |
| **State Management** | React Query, Zustand | Async state and query caching |
| **Backend API** | FastAPI (Python 3.12) | High-performance async REST framework |
| **Agent Framework** | LangGraph 0.2 | Stateful multi-agent graph DAG |
| **LLM Provider** | Gemini 3.5 / Ollama Qwen2.5 | Multi-model LLM engine |
| **Database** | PostgreSQL 18 | Relational database for unis & profiles |
| **Protocol** | Model Context Protocol (MCP) | Modular microservice tool servers |
| **PDF Generation** | ReportLab | Executive PDF generation |

---

## 🌐 Service Ports & Endpoints

| Service | Port | Endpoint URL | Description |
| :--- | :--- | :--- | :--- |
| **Frontend Web App** | `3000` | [http://localhost:3000](http://localhost:3000) | React Frontend Application |
| **Backend API** | `8000` | [http://localhost:8000](http://localhost:8000) | FastAPI Core Backend |
| **API Docs (Swagger)** | `8000` | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive OpenAPI Documentation |
| **Gmail MCP Server** | `8001` | [http://localhost:8001](http://localhost:8001) | MCP Server for Email & Report Dispatch |
| **Core Tools MCP Server**| `8003` | [http://localhost:8003](http://localhost:8003) | MCP Server for University/Scholarship Tools |

---

## 🚀 Quick Start Instructions

### 1. One-Click Automated Start
Launch all 4 services with a single PowerShell script:
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

### 2. Manual Startup

#### Step 1: Verify PostgreSQL
Ensure PostgreSQL is running locally on port 5432 with database `edupilot_db`.

#### Step 2: Seed Database
```powershell
cd backend
.\venv\Scripts\python.exe ..\seed_universities.py
```

#### Step 3: Run Backend API
```powershell
cd backend
.\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 4: Run MCP Servers
```powershell
# Gmail MCP (Port 8001)
.\venv\Scripts\python.exe -m mcp_servers.gmail_mcp_server

# Core Tools MCP (Port 8003)
.\venv\Scripts\python.exe -m mcp_servers.core_tools_mcp_server
```

#### Step 5: Run Frontend
```powershell
cd frontend
npm run dev
```

---

## 📜 License

EduPilot AI is open-source software licensed under the **MIT License**.

