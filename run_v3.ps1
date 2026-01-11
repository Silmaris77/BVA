# Brain Venture Academy V3 - Master Launch Script
# Codename: ensure_dominance

Write-Host "INITIALIZING TACTICAL OS (V3)..." -ForegroundColor Cyan

# 1. Kill Zombie Processes (Clean Slate)
Write-Host "[-] Clearing ports 8000 (Backend) and 3000 (Frontend)..." -ForegroundColor Yellow
$ports = @(8000, 3000)
foreach ($port in $ports) {
    $pids_found = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($pids_found) {
        foreach ($pid_to_kill in $pids_found) {
            try {
                Stop-Process -Id $pid_to_kill -Force -ErrorAction SilentlyContinue
                Write-Host "    Killed process $pid_to_kill on port $port" -ForegroundColor Red
            }
            catch {
                Write-Host "    Could not kill current process (might be me)" -ForegroundColor DarkGray
            }
        }
    }
}

# 2. Check Backend Environment
$backend_path = ".\v3\backend"
if (-not (Test-Path "$backend_path\.venv")) {
    Write-Host "[!] VENV not found in v3\backend. Creating..." -ForegroundColor Yellow
    python -m venv "$backend_path\.venv"
    Write-Host "[+] VENV created." -ForegroundColor Green
    
    # Auto-install requirements
    if (Test-Path "$backend_path\requirements.txt") {
        Write-Host "[+] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
        & "$backend_path\.venv\Scripts\pip" install -r "$backend_path\requirements.txt"
    }
}

# 3. Start Backend (Background)
Write-Host "[+] Launching Neural Backend (FastAPI)..." -ForegroundColor Green
$backend_script = "
cd v3/backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backend_script -WindowStyle Minimized

# 4. Start Frontend (Background)
Write-Host "[+] Launching Interface (Next.js)..." -ForegroundColor Green
$frontend_script = "
cd v3/frontend
npm run dev
"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontend_script

Write-Host "SYSTEM ONLINE." -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000/docs"
Write-Host "Frontend: http://localhost:3000"
Write-Host "Log in to The War Room."
