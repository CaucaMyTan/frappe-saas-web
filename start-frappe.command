#!/bin/zsh

DOCKER="/Users/mymac/Applications/Docker.app/Contents/Resources/bin/docker"
CONTAINER="devcontainer-frappe-1"

if [[ ! -x "$DOCKER" ]]; then
  echo "Khong tim thay Docker Desktop tai: $DOCKER"
  read -k 1 "?Nhan phim bat ky de dong..."
  exit 1
fi

open "/Users/mymac/Applications/Docker.app" >/dev/null 2>&1
echo "Dang cho Docker Desktop san sang..."
until "$DOCKER" info >/dev/null 2>&1; do
  sleep 2
done

"$DOCKER" start devcontainer-mariadb-1 devcontainer-redis-cache-1 devcontainer-redis-queue-1 "$CONTAINER" >/dev/null 2>&1

if ! "$DOCKER" exec "$CONTAINER" bash -lc 'ps -eo args | grep -q "[b]ench start"'; then
  "$DOCKER" exec -d -w /workspace/development/frappe-bench "$CONTAINER" \
    bash -lc 'bench start > logs/bench-start.log 2>&1'
fi

sleep 5
open "http://crm.localhost:8000/login"
echo "Frappe dang chay tai http://crm.localhost:8000"
echo "Tai khoan: Administrator | Mat khau: admin"
read -k 1 "?Nhan phim bat ky de dong cua so nay..."
