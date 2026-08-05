# EduPilot AI – Multi-Agent Study Abroad Copilot

A production-quality AI agent platform that helps Indian students plan their entire study abroad journey. Built with LangGraph, Qwen2.5 (Ollama), FastAPI, React, and PostgreSQL — **100% free and open-source, no paid APIs required**.

---

## Architecture Overview

```
Student
  │
  ▼
React Frontend (Vite + TypeScript + Tailwind)
  │
  ▼
FastAPI Backend (Python 3.12)
  │  ├── JWT Auth
  │  ├── REST API (v1)
  │  └── Background Tasks
  │
  ▼
LangGraph Orchestrator
  │
  ├── Profile Agent          → Extracts/validates student profile
  ├── Country Rec Agent      → Scores & recommends countries
  ├── University Agent       → Queries DB, ranks, explains
  ├── Scholarship Agent      → Matches scholarships by eligibility
  ├── Finance Agent          → Calculates full budget breakdown
  ├── Timeline Agent         → Builds personalised roadmap
  └── Report Agent           → Generates final report
  │
  ▼
MCP Tools
  ├── Gmail MCP              → Send reports via Gmail
  ├── Filesystem MCP         → Extract data from documents
  └── PostgreSQL MCP         → Natural language DB queries
  │
  ▼
PostgreSQL Database
  └── Universities, Scholarships, Countries, Profiles, Reports, Logs

  ↕
Ollama (Qwen2.5)             → Local LLM, no paid API
```

---

## LangGraph Agent Workflow

```
User Query
    │
    ▼
[Orchestrator] ─── analyses query ──→ decides agents_to_run list
    │
    ▼
[Profile Agent]     ← enriches/validates student profile
    │
    ▼
[Country Rec]       ← scores countries by budget, goals, post-study work
    │
    ▼
[University Agent]  ← queries PostgreSQL, ranks universities, explains why
    │
    ▼
[Scholarship Agent] ← matches scholarships, explains eligibility gaps
    │
    ▼
[Finance Agent]     ← full breakdown: tuition + living + visa + insurance
    │
    ▼
[Timeline Agent]    ← month-by-month personalised application roadmap
    │
    ▼
[Report Agent]      ← assembles final report, writes executive summary
    │
    ▼
PDF Report  →  Gmail MCP  →  Student's inbox
```

**The orchestrator is NOT a fixed sequential pipeline.** It reads the user query and dynamically decides which agents to invoke. A query like "What scholarships am I eligible for?" only runs profile + scholarship agents. A full plan request runs all 7.

---

## Tech Stack

| Layer          | Technology                     | Why                                  |
|----------------|--------------------------------|--------------------------------------|
| Frontend       | React 18, Vite, TypeScript     | Fast, type-safe SPA                  |
| UI Styling     | Tailwind CSS, Framer Motion    | Rapid, animated, accessible UI       |
| State          | Zustand, React Query           | Lightweight state + data fetching    |
| Backend        | FastAPI (Python 3.12)          | Async, fast, auto-docs               |
| Auth           | JWT (python-jose + passlib)    | Stateless, secure                    |
| ORM            | SQLAlchemy 2.0 (async)         | Type-safe async DB                   |
| Database       | PostgreSQL 16                  | Structured data with JSONB support   |
| LLM            | Ollama + Qwen2.5               | Free, local, no API key              |
| Agents         | LangGraph 0.2                  | Stateful multi-agent orchestration   |
| MCP            | Gmail, Filesystem, PostgreSQL  | Pluggable tool integrations          |
| PDF Reports    | ReportLab                      | Professional PDF generation          |
| Containers     | Docker + Docker Compose        | One-command deployment               |

---

## Database Schema

```
users
  └── student_profiles (1:1)
  └── applications    (1:N) ──→ universities
  └── reports         (1:N)
  └── agent_logs      (1:N)

countries
  └── universities    (1:N)
      └── scholarships (1:N)

scholarships (also standalone, not tied to university)
```

---

## Project Structure

```
EduPilot AI/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Pydantic settings
│   │   ├── database.py          # Async SQLAlchemy engine
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── api/v1/              # REST API routes
│   │   └── core/                # Security, deps, logging
│   ├── agents/
│   │   ├── orchestrator.py      # LangGraph workflow + entry point
│   │   ├── state.py             # Shared AgentState TypedDict
│   │   ├── llm.py               # Ollama/Qwen2.5 client
│   │   ├── profile_agent.py
│   │   ├── university_agent.py
│   │   ├── scholarship_agent.py
│   │   ├── finance_agent.py
│   │   ├── timeline_agent.py
│   │   └── report_agent.py
│   ├── prompts/                 # All LLM prompt templates
│   ├── mcp_tools/               # Gmail, Filesystem, PostgreSQL MCP
│   ├── services/                # PDF report generation
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── pages/               # All 10 pages
│       ├── components/          # Layout, shared components
│       ├── stores/              # Zustand stores
│       └── lib/                 # API client
│
├── database/
│   └── migrations/
│       ├── 001_initial_schema.sql
│       └── 002_seed_universities.sql
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
│
└── docker-compose.yml
```

---

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.ai) installed locally OR included via Docker

### 1. Clone and configure
```bash
cd backend
cp .env.example .env
# Edit .env if needed (defaults work out of the box)
```

### 2. Pull the Qwen2.5 model
```bash
ollama pull qwen2.5
```

### 3. Start all services
```bash
docker-compose up -d
```

### 4. Run database migrations
```bash
# Migrations auto-run on first PostgreSQL container start
# Or manually:
docker exec -it edupilot_postgres psql -U edupilot -d edupilot_db -f /docker-entrypoint-initdb.d/001_initial_schema.sql
docker exec -it edupilot_postgres psql -U edupilot -d edupilot_db -f /docker-entrypoint-initdb.d/002_seed_universities.sql
```

### 5. Open the app
| Service  | URL                            |
|----------|-------------------------------|
| Frontend | http://localhost:3000          |
| Backend API | http://localhost:8000       |
| API Docs | http://localhost:8000/docs     |

---

## Running Without Docker (Development)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # Edit with your DB settings
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                    # Runs on http://localhost:3000
```

### PostgreSQL (Local)
```sql
CREATE USER edupilot WITH PASSWORD 'edupilot_pass';
CREATE DATABASE edupilot_db OWNER edupilot;
\c edupilot_db
\i database/migrations/001_initial_schema.sql
\i database/migrations/002_seed_universities.sql
```

---

## MCP Configuration

### Gmail MCP
1. Create OAuth2 credentials in Google Cloud Console
2. Add to `backend/.env`:
   ```
   GMAIL_CLIENT_ID=your-client-id
   GMAIL_CLIENT_SECRET=your-client-secret
   ```
3. Run the OAuth flow to get `gmail_credentials.json`

### PostgreSQL MCP
Starts automatically — the agents use direct async SQLAlchemy as primary path with MCP as a secondary NL query layer.

### Filesystem MCP
Install `pypdf` for PDF extraction:
```bash
pip install pypdf
```

---

## API Reference

| Method | Endpoint                          | Description                     |
|--------|-----------------------------------|---------------------------------|
| POST   | /api/v1/auth/register             | Create account                  |
| POST   | /api/v1/auth/login                | Login, get JWT tokens            |
| GET    | /api/v1/auth/me                   | Current user info                |
| GET    | /api/v1/profile                   | Get student profile              |
| POST   | /api/v1/profile                   | Create profile                   |
| PUT    | /api/v1/profile                   | Update profile                   |
| POST   | /api/v1/profile/upload-document   | Upload & extract document        |
| POST   | /api/v1/agents/run                | Run multi-agent workflow         |
| POST   | /api/v1/agents/chat               | Conversational agent interface   |
| GET    | /api/v1/agents/logs               | Agent execution logs             |
| GET    | /api/v1/universities              | List universities (with filters) |
| GET    | /api/v1/universities/:id          | University detail                |
| GET    | /api/v1/universities/scholarships/list | List scholarships           |
| GET    | /api/v1/universities/countries/list   | List destination countries  |
| POST   | /api/v1/reports/generate          | Generate full report             |
| GET    | /api/v1/reports                   | List user reports                |
| GET    | /api/v1/reports/:id/download      | Download PDF                     |
| POST   | /api/v1/reports/email             | Send report via Gmail            |

---

## How the AI Reasoning Works

Every recommendation includes explicit reasoning. The LLM is instructed to:

- **University recommendations**: Reference the student's specific CGPA, IELTS, budget, and career goal in every explanation.
- **Scholarship matching**: Flag any eligibility gap (e.g., "Your CGPA of 7.2 is below the minimum 7.5") and provide action steps.
- **Finance breakdown**: Calculate in both USD and INR with scholarship deductions.
- **Timeline**: Generate month-by-month milestones only relevant to this student (skip steps already done).
- **Final recommendation**: Give a single top recommendation and explain why NOT to choose alternatives.

The orchestrator prompt enforces: *"Never produce recommendations without reasoning."*

---

## Scalability Plan

| Concern          | Current                      | Future                                   |
|------------------|------------------------------|------------------------------------------|
| LLM              | Local Qwen2.5                | Swap to Llama 3 70B or Claude via bedrock|
| Database         | Single PostgreSQL             | Read replicas + PgBouncer                |
| Agent parallelism| Sequential LangGraph          | Parallel node execution with async fan-out|
| Caching          | None                         | Redis for session state and LLM responses|
| Auth             | JWT only                     | OAuth (Google, LinkedIn)                 |
| Universities DB  | Seeded static data           | Web scraping pipeline + admin CMS        |
| Deployment       | Docker Compose               | Kubernetes with HPA                      |
| Observability    | Structlog                    | OpenTelemetry + Grafana                  |

---

## Environment Variables Reference

See `backend/.env.example` for all available configuration options.

---

*Built with LangGraph + Qwen2.5 + FastAPI + React. No paid APIs. Fully local.*
