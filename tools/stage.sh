#!/usr/bin/env bash
# Build the publishable site into _site/ — everything a visitor should get, and
# nothing else.
#
# The repo is public, but that is not the same thing as serving the build notes
# on the production domain. Without this step the Pages artifact is the whole
# repo, and DEPLOY.md, README.md, docs/ and tools/ answer 200 on
# inheritingislam.com — including the sales one-pagers, which check.py
# deliberately never audits.
#
#     tools/stage.sh            # builds ./_site
#     tools/stage.sh /tmp/out   # builds somewhere else
#
# CI runs this exact script, so what you test locally is what ships.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/_site}"

rm -rf "$OUT"
mkdir -p "$OUT"

# Note the trailing slashes: copy the contents of ROOT, not ROOT itself.
# -a keeps dotfiles, so .nojekyll travels with it.
rsync -a "$ROOT/" "$OUT/" \
  --exclude '.git' \
  --exclude '.github' \
  --exclude '.gitignore' \
  --exclude '.DS_Store' \
  --exclude '_site' \
  --exclude '_internal' \
  --exclude '_issued' \
  --exclude 'tools' \
  --exclude 'docs' \
  --exclude 'DEPLOY.md' \
  --exclude 'README.md'

# CNAME is what tells Pages the custom domain when the artifact comes from
# Actions rather than a branch. If it goes missing the domain silently detaches.
test -s "$OUT/CNAME" || { echo "::error::CNAME missing from the staged site"; exit 1; }

echo "Staged $(find "$OUT" -type f | wc -l | tr -d ' ') files into $OUT"
