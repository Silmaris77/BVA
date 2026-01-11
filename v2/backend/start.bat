@echo off
echo ============================================================
echo BrainVentureAcademy v2.0 - Backend API
echo ============================================================
cd /d "%~dp0..\.."
echo Working directory: %CD%
echo.
echo Starting server on http://localhost:8001
echo API Docs: http://localhost:8001/docs
echo Health Check: http://localhost:8001/api/health
echo.
echo Credentials:
echo   Username: admin
echo   Password: admin123
echo ============================================================
echo.
python -m uvicorn v2.backend.main:app --host 127.0.0.1 --port 8001 --reload
pause
