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
    "cd '$BACKEND'; `$env:PATH += ';C:\Program Files\nodejs;C:\Program Files\PostgreSQL\18\bin'; Write-Host 'Backend starting on http://localhost:8000' -ForegroundColor Green; .\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 3

# ── Start Frontend ────────────────────────────────────────────
Write-Host "Starting Frontend (React)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$FRONTEND'; `$env:PATH += ';C:\Program Files\nodejs'; Write-Host 'Frontend starting on http://localhost:3000' -ForegroundColor Green; npm run dev"

Start-Sleep -Seconds 4

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   EduPilot AI is starting up!" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "   App:      http://localhost:3000" -ForegroundColor Yellow
Write-Host "   API:      http://localhost:8000" -ForegroundColor Yellow
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"
