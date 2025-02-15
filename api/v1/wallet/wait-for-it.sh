#!/usr/bin/env bash

set -e

TIMEOUT=15
HOST=""
PORT=""
CMD=()

usage() {
  echo "Usage: $0 host:port [-t timeout] [-- command args]"
  exit 1
}

if [ "$#" -lt 1 ]; then
  usage
fi

HOST=$(echo "$1" | cut -d: -f1)
PORT=$(echo "$1" | cut -d: -f2)
shift

while [ "$#" -gt 0 ]; do
  case "$1" in
    -t)
      TIMEOUT="$2"
      shift 2
      ;;
    --)
      shift
      CMD=("$@")
      break
      ;;
    *)
      usage
      ;;
  esac
done

echo "Ожидание доступности $HOST:$PORT с таймаутом $TIMEOUT секунд..."
start_ts=$(date +%s)

while true; do
  if echo > /dev/tcp/$HOST/$PORT 2>/dev/null; then
    echo "$HOST:$PORT доступен!"
    break
  fi
  sleep 1
  current_ts=$(date +%s)
  elapsed=$(( current_ts - start_ts ))
  if [ $elapsed -ge $TIMEOUT ]; then
    echo "Таймаут: не удалось дождаться $HOST:$PORT за $TIMEOUT секунд."
    exit 1
  fi
done

if [ ${#CMD[@]} -gt 0 ]; then
  exec "${CMD[@]}"
fi
