#!/bin/bash
set -e
cd "$(dirname "$0")/backend"

if [ ! -x ".venv314/bin/python" ]; then
  echo "Sanal ortam bulunamadı. Önce setup_mac.command dosyasını çalıştırın."
  read -r -p "Kapatmak için Enter'a basın..." _
  exit 1
fi

PORT=8000
URL="http://127.0.0.1:${PORT}"
echo "NSosyal Bağlam başlatılıyor..."
echo "Adres: $URL"
(sleep 1.5; open "$URL") >/dev/null 2>&1 &
exec ./.venv314/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT"
