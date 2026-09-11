#!/usr/bin/env bash
set -euo pipefail

# Starts a fresh, local demo that uses this repository's custom Frappe, CRM,
# and Voice CRM branches. It is deliberately for local evaluation only.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Docker Desktop on some macOS installations does not add its CLI to PATH.
if ! command -v docker >/dev/null 2>&1; then
  docker_cli_dir="$HOME/Applications/Docker.app/Contents/Resources/bin"
  if [ -x "$docker_cli_dir/docker" ]; then
    export PATH="$docker_cli_dir:$PATH"
  fi
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker Desktop is required. Install and start it, then run this script again." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker Desktop is installed but is not running. Start it, then run this script again." >&2
  exit 1
fi

compose=(docker compose -f .devcontainer/docker-compose.yml)
"${compose[@]}" up -d

echo "Waiting for MariaDB..."
for _ in {1..30}; do
  if "${compose[@]}" exec -T mariadb mariadb-admin ping -h localhost -p123 --silent >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

if ! "${compose[@]}" exec -T mariadb mariadb-admin ping -h localhost -p123 --silent >/dev/null 2>&1; then
  echo "MariaDB did not become ready. Run: ${compose[*]} logs mariadb" >&2
  exit 1
fi

if [ ! -d development/frappe-bench ]; then
  echo "Creating a fresh Frappe bench with the custom applications..."
  "${compose[@]}" exec -T frappe bash -lc '
    cd /workspace/development
    python installer.py \
      --apps-json=/workspace/apps.json \
      --bench-name=frappe-bench \
      --site-name=demo.localhost \
      --frappe-repo=https://github.com/CaucaMyTan/frappe-saas-web.git \
      --frappe-branch=app-frappe \
      --admin-password=admin \
      --db-type=mariadb
  '
elif [ ! -d development/frappe-bench/sites/demo.localhost ]; then
  echo "The bench already exists; creating the demo site..."
  "${compose[@]}" exec -T frappe bash -lc '
    cd /workspace/development
    python installer.py \
      --apps-json=/workspace/apps.json \
      --bench-name=frappe-bench \
      --site-name=demo.localhost \
      --frappe-repo=https://github.com/CaucaMyTan/frappe-saas-web.git \
      --frappe-branch=app-frappe \
      --admin-password=admin \
      --db-type=mariadb
  '
else
  echo "Existing demo site found; keeping its data."
fi

if ! "${compose[@]}" exec -T frappe bash -lc 'ps -eo args | grep -q "[b]ench start"'; then
  "${compose[@]}" exec -d -w /workspace/development/frappe-bench frappe \
    bash -lc 'bench start > logs/bench-start.log 2>&1'
fi

echo
echo "Demo is starting at http://demo.localhost:8000"
echo "Login: Administrator / admin"
echo "The first setup can take several minutes while dependencies and assets build."
