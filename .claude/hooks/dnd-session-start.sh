#!/usr/bin/env bash
# SessionStart hook — make the in-repo D&D data the skill's data root.
#
# Every web/mobile session clones this repo into a fresh, throwaway container.
# The dm skill reads its campaigns/characters/rules/statblocks from
# ~/.claude/dnd (paths.py default). This hook points that path at the repo's
# committed `dnd-data/` so a phone session is play-ready with zero manual steps.
#
# Safe and idempotent:
#   - no dnd-data/ in the repo  → no-op (e.g. running the skill from elsewhere)
#   - ~/.claude/dnd missing     → symlink it to dnd-data/
#   - already the right symlink  → leave it
#   - a real ~/.claude/dnd dir   → DON'T clobber a local install; advise env var
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
DATA="$PROJECT_DIR/dnd-data"
TARGET="$HOME/.claude/dnd"

[ -d "$DATA" ] || exit 0           # repo carries no game data — nothing to wire
mkdir -p "$HOME/.claude"

if [ -L "$TARGET" ]; then
  # already a symlink — repoint it at this repo's data (handles a moved checkout)
  ln -sfn "$DATA" "$TARGET"
  echo "[dnd] data root → $DATA" >&2
elif [ ! -e "$TARGET" ]; then
  ln -s "$DATA" "$TARGET"
  echo "[dnd] linked ~/.claude/dnd → $DATA" >&2
else
  # a real directory exists (local install with its own saves) — never clobber it
  echo "[dnd] ~/.claude/dnd is a real directory; leaving it untouched." >&2
  echo "[dnd] To use the repo's data instead, set: export DND_CAMPAIGN_ROOT=\"$DATA\"" >&2
fi
exit 0
