@echo off
setlocal
cd /d "%~dp0backend"

if not exist ".venv314\Scripts\python.exe" (
  echo Python 3.14 sanal ortami bulunamadi.
  echo Once setup_windows.bat dosyasini calistirin.
  pause
  exit /b 1
)

echo NSosyal Baglam Python 3.14 ile baslatiliyor...
echo Tarayici adresi: http://127.0.0.1:8000
start "" http://127.0.0.1:8000
.venv314\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
