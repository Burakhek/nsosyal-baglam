@echo off
setlocal
cd /d "%~dp0backend"

echo [1/4] Python 3.14 kontrol ediliyor...
py -3.14 --version >nul 2>&1
if errorlevel 1 (
  echo.
  echo HATA: Python 3.14 bulunamadi.
  echo Once Python 3.14 kurulu oldugundan emin olun.
  pause
  exit /b 1
)
py -3.14 --version

echo [2/4] Python 3.14 sanal ortami hazirlaniyor...
if not exist ".venv314\Scripts\python.exe" (
  py -3.14 -m venv .venv314
)

echo [3/4] pip guncelleniyor...
.venv314\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto :fail

echo [4/4] Proje paketleri kuruluyor...
.venv314\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo.
echo KURULUM TAMAMLANDI.
echo Sonraki adim: run_windows.bat dosyasini calistirin.
pause
exit /b 0

:fail
echo.
echo KURULUM BASARISIZ. Yukaridaki hata metnini kopyalayip paylasin.
pause
exit /b 1
