@echo off
chcp 65001 >nul
REM SaijinOS Morning Startup (ASCII Safe Version)
REM Double-click to run

echo.
echo ====================================================
echo     SaijinOS Morning Startup
echo ====================================================
echo.

echo [INFO] Checking persona memory log...
if exist "F:\saijin\personas\import\構文人\project_memory_log.yaml" (
    echo [OK] Persona memory log found
) else (
    echo [WARN] Persona memory log not found
)

echo.
echo [INFO] Project Information:
echo   Project: SaijinOS AI Integration System
echo   Version: v0.1.0
echo   Team: 7-Persona Development Team
echo   Date: %date%

echo.
echo [INFO] Activating Python virtual environment...
call "F:\saijinos\.venv\Scripts\Activate.ps1" >nul 2>&1

echo [INFO] Changing to project directory...
cd /d "F:\sajinos_final"

echo.
echo [INFO] Important files check:
if exist "README.md" (echo [OK] README.md) else (echo [WARN] README.md missing)
if exist "HANDOVER.md" (echo [OK] HANDOVER.md) else (echo [WARN] HANDOVER.md missing)
if exist "src\saijinos_real_ai.py" (echo [OK] saijinos_real_ai.py) else (echo [WARN] saijinos_real_ai.py missing)
if exist "Dockerfile" (echo [OK] Dockerfile) else (echo [WARN] Dockerfile missing)

echo.
echo [INFO] Quick Commands for today:
echo   API Server: python src\saijinos_real_ai.py
echo   Health Check: http://localhost:8000/health
echo   API Docs: http://localhost:8000/docs
echo   Docker: docker-compose up -d

echo.
echo [INFO] Today's recommended tasks:
echo   1. System monitoring startup
echo   2. API server stabilization  
echo   3. Web UI development
echo   4. Mobile integration prep

echo.
echo ====================================================
echo [SUCCESS] SaijinOS Morning Startup Complete!
echo [INFO] Ready for development. Have a great day!
echo ====================================================
echo.

echo Press any key to continue...
pause >nul