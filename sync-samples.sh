#!/bin/bash
set -e

SAMPLES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SAMPLES_DIR"

echo "Regenerating strudel.json..."
python3 "$SAMPLES_DIR/generate_strudel_json.py"

echo "Committing and pushing..."
git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "Update samples $(date '+%Y-%m-%d %H:%M:%S')"
  git push
fi

HASH=$(git rev-parse --short HEAD)
REPO_URL=$(git config --get remote.origin.url | sed -E 's#.*github.com[:/](.+)\.git#\1#')
LINE="samples('https://raw.githubusercontent.com/${REPO_URL}/main/strudel.json?v=${HASH}')"

echo "$LINE" | pbcopy
echo ""
echo "Copied to clipboard:"
echo "$LINE"
