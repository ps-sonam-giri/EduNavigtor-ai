# EduPilot AI – Start without Docker
# Run this script to start the entire application

$env:PATH += ";C:\Program Files\nodejs;C:\Program Files\PostgreSQL\18\bin"

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND  = Join-Path $ROOT "backend"
$FRONTEND = Join-Path $ROOT "frontend"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   EduPilot AI - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Start Backend ─────────────────────────────────────────────
Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$BACKEND'; `$env:PATH += ';C:\Program Files\nodejs;C:\Program Files\PostgreSQL\18\bin'; Write-Host 'Backend starting on http://localhost:8000' -ForegroundColor Green; .\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 2

# ── Start Gmail MCP Server ────────────────────────────────────
Write-Host "Starting Gmail MCP Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$BACKEND'; Write-Host 'Gmail MCP Server starting on http://localhost:8001' -ForegroundColor Green; .\venv\Scripts\python.exe -m mcp_servers.gmail_mcp_server"

Start-Sleep -Seconds 2

# ── Start Frontend ────────────────────────────────────────────
Write-Host "Starting Frontend (React)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$FRONTEND'; `$env:PATH += ';C:\Program Files\nodejs'; Write-Host 'Frontend starting on http://localhost:3000' -ForegroundColor Green; npm run dev"

Start-Sleep -Seconds 4

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   EduPilot AI is starting up!" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "   App:       http://localhost:3000" -ForegroundColor Yellow
Write-Host "   API:       http://localhost:8000" -ForegroundColor Yellow
Write-Host "   Gmail MCP: http://localhost:8001" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"
