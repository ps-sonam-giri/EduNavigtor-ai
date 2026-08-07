# EduPilot AI – Multi-Agent Study Abroad Copilot

A production-quality AI agent platform that helps Indian students plan their entire study abroad journey. Built with LangGraph, Gemini 3.5 / Qwen2.5, FastAPI, React, and PostgreSQL — **100% free and open-source, with MCP integrations**.

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
  └── Report Agent           → Generates final report & PDF
  │
  ▼
MCP Servers & Tools
  ├── Gmail MCP Server (Port 8001)  → Dispatches PDF reports & emails via Gmail SMTP/API
  ├── Core Tools MCP (Port 8003)    → Exposes university & scholarship DB tools
  └── Filesystem MCP                 → Extract data from uploaded documents (PDF/SOP)
  │
  ▼
PostgreSQL Database
  └── Universities, Scholarships, Countries, Profiles, Reports, Logs
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
PDF Report  →  Gmail MCP (Port 8001)  →  Student's inbox
```

**Dynamic Orchestration**: The orchestrator is NOT a fixed sequential pipeline. It reads user requests and dynamically routes to the appropriate agents. A query like *"What scholarships am I eligible for?"* only runs Profile + Scholarship agents, whereas full planning triggers all 7 agents.

---

## Tech Stack

| Layer          | Technology                     | Description                          |
|----------------|--------------------------------|--------------------------------------|
| Frontend       | React 18, Vite, TypeScript     | Fast, type-safe SPA                  |
| UI Styling     | Tailwind CSS, Framer Motion    | Rapid, animated, accessible UI       |
| State          | Zustand, React Query           | Lightweight state + data fetching    |
| Backend        | FastAPI (Python 3.12)          | Async REST API & OpenAPI docs        |
| Auth           | JWT (python-jose + passlib)    | Stateless secure authentication      |
| ORM            | SQLAlchemy 2.0 (async)         | Type-safe async ORM                  |
| Database       | PostgreSQL 16                  | Structured data with JSONB support   |
| LLM            | Gemini 3.5 / Ollama Qwen2.5    | Multi-provider LLM support           |
| Agents         | LangGraph 0.2                  | Stateful multi-agent orchestration   |
| MCP            | Custom Gmail & Core Tools MCP  | Standalone MCP servers (8001 & 8003) |
| PDF Reports    | ReportLab                      | Executive PDF generation             |

---

## Service Endpoints

| Service | Port | Local URL | Description |
| :--- | :--- | :--- | :--- |
| **Frontend App** | `3000` | [http://localhost:3000](http://localhost:3000) | React UI Application |
| **Backend API** | `8000` | [http://localhost:8000](http://localhost:8000) | FastAPI Core Backend |
| **API Docs** | `8000` | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive OpenAPI Docs |
| **Gmail MCP Server** | `8001` | [http://localhost:8001](http://localhost:8001) | MCP Server for Gmail Dispatch |
| **Core Tools MCP** | `8003` | [http://localhost:8003](http://localhost:8003) | MCP Server for Domain Tools |

---

## Quick Start (Without Docker)

Run the full application stack with a single command on PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

This automatically launches:
1. FastAPI Backend (`http://localhost:8000`)
2. Gmail MCP Server (`http://localhost:8001`)
3. React Frontend (`http://localhost:3000`)

---

## Email Configuration & MCP Setup

### Gmail MCP Server (`backend/mcp_servers/gmail_mcp_server.py`)
To send emails directly to user inboxes via Gmail SMTP, configure `backend/.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your_16_character_app_password
SMTP_SENDER=your-email@gmail.com
```

> **Note**: Generate a 16-character App Password at [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) with 2-Step Verification enabled.

### Development Fallback Mode
If SMTP credentials are not configured or rejected by Google, the system automatically routes emails to the local development inbox at:
`backend/reports/sent_emails/`

---

## License & Attribution

Built with LangGraph + FastAPI + React + Model Context Protocol (MCP).
Open-source under the MIT License.
