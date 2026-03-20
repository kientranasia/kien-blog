#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

STATE_FILE=".last_built_commit"
HISTORY_FILE=".build-history.log"

on_error() {
  local rc=$?
  echo "[$(date -Is)] build failed rc=$rc head=$(git rev-parse HEAD 2>/dev/null || echo unknown)" >> "$HISTORY_FILE"
  exit "$rc"
}
trap on_error ERR

git fetch --quiet origin || true
git pull --quiet --ff-only || true

HEAD="$(git rev-parse HEAD)"
PREV="$(cat "$STATE_FILE" 2>/dev/null || true)"

if [[ "$HEAD" == "$PREV" ]]; then
  exit 0
fi

echo "[$(date -Is)] build start head=$HEAD prev=${PREV:-none}" >> "$HISTORY_FILE"

hugo --minify --config hugo.yaml
docker compose up -d --build --force-recreate web

echo "$HEAD" > "$STATE_FILE"
echo "[$(date -Is)] build ok head=$HEAD" >> "$HISTORY_FILE"

