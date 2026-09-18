#!/bin/bash
set -e
cd "$(dirname "$0")/backend"

PY=""
if command -v python3.14 >/dev/null 2>&1; then
  PY="$(command -v python3.14)"
elif command -v python3 >/dev/null 2>&1; then
  PY="$(command -v python3)"
fi

if [ -z "$PY" ]; then
  echo "Python bulunamadı. Python 3.14 kurup tekrar deneyin."
  read -r -p "Kapatmak için Enter'a basın..." _
  exit 1
fi

VER="$($PY -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "Python $VER kullanılıyor: $PY"

"$PY" -m venv .venv314
./.venv314/bin/python -m pip install --upgrade pip
./.venv314/bin/python -m pip install -r requirements.txt
./.venv314/bin/python -m pytest -q

echo
echo "Kurulum ve testler tamamlandı. run_mac.command dosyasını açabilirsiniz."
read -r -p "Kapatmak için Enter'a basın..." _
