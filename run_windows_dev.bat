@echo off
setlocal
cd /d "%~dp0backend"
if not exist ".venv314\Scripts\python.exe" (
  echo Once setup_windows.bat dosyasini calistirin.
  pause
  exit /b 1
)
echo Gelistirme modu: http://127.0.0.1:8000
.venv314\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
