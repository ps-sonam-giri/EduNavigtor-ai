# EduPilot AI – Complete Project Manual & Technical Guide

---

## 1. Executive Summary

**EduPilot AI** is a production-grade, state-of-the-art **Multi-Agent AI Copilot** engineered to guide Indian students through their end-to-end study abroad journey.

Unlike conventional static portals or basic chatbot wrappers, EduPilot AI combines **LangGraph stateful multi-agent orchestration**, **custom Model Context Protocol (MCP) servers**, a **PostgreSQL relational database**, and an **AI document verification engine** to deliver personalized, verifiable, and transparent study abroad plans.

---

## 2. System Architecture & High-Level Flow

```
                      ┌────────────────────────────────────────────────┐
                      │    React 18 SPA (TypeScript + Tailwind CSS)    │
                      │               http://localhost:3000            │
                      └───────────────────────┬────────────────────────┘
                                              │ REST API / HTTP
                                              ▼
                      ┌────────────────────────────────────────────────┐
                      │          FastAPI Async Backend (Python)        │
                      │               http://localhost:8000            │
                      └───────────────┬────────────────┬───────────────┘
                                      │                │
             ┌────────────────────────┘                └────────────────────────┐
             ▼                                                                  ▼
┌───────────────────────────┐                                      ┌───────────────────────────┐
│   LangGraph Multi-Agent   │                                      │    MCP Servers & Tools    │
│       Orchestrator        │                                      │                           │
│  ├── Profile Agent        │                                      │ ├── Gmail MCP (Port 8001) │
│  ├── Country Rec Agent    │                                      │ ├── Core Tools (Port 8003)│
│  ├── University Agent     │                                      │ └── Filesystem PDF MCP    │
│  ├── Scholarship Agent    │                                      │                           │
│  ├── Finance Agent        │                                      └─────────────┬─────────────┘
│  ├── Timeline Agent       │                                                    │
│  └── Report Agent         │                                                    │
└────────────┬──────────────┘                                                    │
             │                                                                   │
             ▼                                                                   ▼
┌───────────────────────────┐                                      ┌───────────────────────────┐
│  LLM Engine (Gemini /     │                                      │    PostgreSQL Database    │
│      Ollama Qwen2.5)      │                                      │   Profiles, Universities, │
└───────────────────────────┘                                      │    Scholarships, Reports  │
                                                                   └───────────────────────────┘
```

---

## 3. The 7 Autonomous AI Agents (LangGraph Orchestrator)

The platform is powered by **7 specialized AI agents** orchestrated statefully via **LangGraph 0.2**:

### 1. Profile Agent (`profile_agent.py`)
- **Purpose**: Validates, normalizes, and enriches the student's profile (CGPA, IELTS/GRE scores, work experience, budget, target degree).
- **Function**: Ensures missing or edge-case input data is flagged before running heavy analysis.

### 2. Country Recommendation Agent (`country_rec_agent.py`)
- **Purpose**: Evaluates and scores destination countries (USA, UK, Canada, Germany, Australia, Ireland, etc.).
- **Evaluation Criteria**: Financial budget fit, post-study work visa duration (PSW), PR path feasibility, and academic match.

### 3. University Agent (`university_agent.py`)
- **Purpose**: Queries the PostgreSQL database to match, rank, and categorize universities into 3 tiers:
  - 🟢 **Target / Safe**: High admission probability.
  - 🟡 **Moderate Match**: Balanced academic and financial fit.
  - 🔴 **Reach**: Competitive / Ivy-league tier.
- **Reasoning Enforced**: Explains *why* each university was selected based on the student's exact CGPA and test scores.

### 4. Scholarship Agent (`scholarship_agent.py`)
- **Purpose**: Matches government, institutional, and private scholarships.
- **Gap Analysis**: Explicitly highlights eligibility gaps (e.g. *"Your CGPA of 7.2 is below the minimum 7.5 requirement for DAAD"*) and provides action steps to qualify.

### 5. Finance & Budget Agent (`finance_agent.py`)
- **Purpose**: Computes full 1-year and 2-year cost estimates in both USD ($) and INR (₹).
- **Breakdown**: Tuition fees + living expenses + visa fees + health insurance − matched scholarship deductions.

### 6. Timeline Agent (`timeline_agent.py`)
- **Purpose**: Builds a month-by-month application roadmap tailored to the student's target intake (e.g., Fall 2026 / Spring 2027).
- **Dynamic Milestones**: Skips completed steps (e.g., skips IELTS preparation if the student already holds a 7.5 band score).

### 7. Report Agent (`report_agent.py`)
- **Purpose**: Assembles outputs from all agents into a unified structured report.
- **PDF Engine**: Uses ReportLab to render executive PDF reports complete with tables, badges, and breakdown charts.

---

## 4. Document Verification & Extraction Engine

Located in [`backend/tools/document_tools.py`](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/backend/tools/document_tools.py), the platform includes an automated AI document verification engine:

```
Uploaded Document ──► Text Extraction (PyPDF / OCR) ──► Structural Rule Matcher ──► Profile Auto-Update
```

| Document Type | Verification Checks | Extracted Insights |
| :--- | :--- | :--- |
| **Resume / CV** | Structural detection of Education, Experience, Skills, and Projects sections. | Section completeness score & confidence level. |
| **Marksheet / Transcript** | Checks academic markers (Semester, Subject, Credits, Grade, University Name). | **CGPA / GPA** value auto-populated into profile. |
| **IELTS / Scorecard** | Checks test scorecard markers (Listening, Reading, Writing, Speaking, TRF Number). | **Overall IELTS Band Score** auto-populated into profile. |
| **SOP** | Statement of Purpose intent keywords & word count analysis (flags < 150 words). | Word count & motivation alignment score. |

---

## 5. Model Context Protocol (MCP) Integration

EduPilot AI incorporates **Model Context Protocol (MCP)** to allow AI agents to securely interact with external tools:

### Gmail MCP Server (`backend/mcp_servers/gmail_mcp_server.py`)
- **Port**: `8001`
- **Exposed Tools**: `send_email`, `draft_email`, `search_emails`, `send_report`.
- **Dual Delivery Pipeline**:
  1. **Live SMTP / Gmail API**: Dispatches PDF reports directly to the student's inbox using Google App Passwords (`smtp.gmail.com:465`).
  2. **Local Dev Inbox Fallback**: If SMTP credentials are not configured or rejected by Google, emails are automatically formatted as HTML files and saved locally under `backend/reports/sent_emails/`.

### Core Tools MCP Server (`backend/mcp_servers/core_tools_mcp_server.py`)
- **Port**: `8003`
- **Exposed Tools**: University search, scholarship lookup, finance breakdown, and document parsing tools exposed over standardized MCP endpoints.

---

## 6. Service Map & Endpoints

| Service | Port | Endpoint / URL | Description |
| :--- | :--- | :--- | :--- |
| **React Frontend** | `3000` | [http://localhost:3000](http://localhost:3000) | Web Dashboard & Interactive Pages |
| **FastAPI Backend** | `8000` | [http://localhost:8000](http://localhost:8000) | Core REST API Server |
| **API Documentation** | `8000` | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger / OpenAPI Docs |
| **Gmail MCP Server** | `8001` | [http://localhost:8001](http://localhost:8001) | Custom MCP Email Server |
| **Core Tools MCP** | `8003` | [http://localhost:8003](http://localhost:8003) | Custom MCP Core Domain Server |

### Core REST API Routes

```http
POST   /api/v1/auth/register            # Create new user account
POST   /api/v1/auth/login               # Authenticate & get JWT tokens
GET    /api/v1/profile                  # Retrieve current student profile
POST   /api/v1/profile                  # Create student profile
PUT    /api/v1/profile                  # Update student profile
POST   /api/v1/profile/upload-document  # Upload document with AI verification
DELETE /api/v1/profile                  # Delete student profile
POST   /api/v1/agents/run               # Execute multi-agent LangGraph workflow
POST   /api/v1/agents/chat              # Conversational agent interface
GET    /api/v1/universities             # Search & filter university database
GET    /api/v1/reports                  # List user generated reports
GET    /api/v1/reports/:id/download     # Download report PDF
POST   /api/v1/reports/email/send       # Dispatch report email via Gmail MCP
DELETE /api/v1/reports/:id              # Delete report
```

---

## 7. Operations & Quick Start

### Starting the Full Stack Locally

Run the master start script in PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

This launches all 3 required server processes simultaneously:
1. **Backend FastAPI** on Port `8000`
2. **Gmail MCP Server** on Port `8001`
3. **React Frontend (Vite)** on Port `3000`

---

## 8. Deployment Setup

### Frontend Deployment (Vercel)
- **Root Directory**: `frontend`
- **Framework**: `Vite`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Configuration**: Uses [`vercel.json`](file:///c:/Users/SonamGiri/Desktop/Temp/EduNavigtor%20ai/vercel.json) for static build routing.

---

*Manual maintained for EduPilot AI codebase.*
