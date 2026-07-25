#!/bin/bash
# Requires: brew install fswatch

SAMPLES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FSWATCH=$(command -v fswatch || echo "/opt/homebrew/bin/fswatch")

echo "Watching $SAMPLES_DIR for changes... (ctrl+C to stop)"

"$FSWATCH" -o -l 2 "$SAMPLES_DIR" \
  --exclude '\.git' \
  --exclude 'strudel\.json' \
| while read -r _; do
    echo "Change detected, syncing..."
    "$SAMPLES_DIR/sync-samples.sh"
done
