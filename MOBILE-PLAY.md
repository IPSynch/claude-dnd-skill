# Playing on Mobile (Android) — Anywhere

This repo doubles as a **portable campaign store** so you can play on your phone
while travelling — no laptop required. Your campaign, characters, house/combat
rules, and statblock library all live in the repo (`dnd-data/`), so every cloud
session has them automatically.

> **Keep this repository PRIVATE.** It holds third-party module and bestiary
> text; only store material you personally own.

## How it works

1. Every web/mobile session clones this repo into a fresh container.
2. A **SessionStart hook** (`.claude/hooks/dnd-session-start.sh`) symlinks
   `~/.claude/dnd` → `dnd-data/`, so the `dm` skill finds your data with no setup.
3. You play in chat; the skill reads/writes `dnd-data/`.
4. At session end you **commit & push** so progress is saved for next time.

## First-time setup (once)

1. Make the GitHub repo **Private** (Settings → General → Danger Zone → Change visibility).
2. That's it — the data and hook are already committed.

## Each play session on your phone

1. Open the **Claude app** (or claude.ai/code in the browser) and start a session
   on this repo / its environment.
2. The hook wires the data automatically. Then just type:
   ```
   /dm:dnd load toa
   ```
   (or `/dm:dnd character new` first if you haven't made your PCs yet).
3. Play by text. The TV/audio **display companion is laptop-LAN-only** — skip it
   on mobile; the whole game runs in chat.
4. **When you finish**, save and persist:
   ```
   /dm:dnd save
   ```
   then ask me (or run) a commit & push of `dnd-data/`:
   ```
   git add dnd-data && git commit -m "session save: <date>" && git push
   ```
   Your next session — on any device — picks up exactly where you left off.

## Notes

- **Multiple campaigns / characters** all live side by side under `dnd-data/`.
- **Local laptop play still works**: if you already have a real `~/.claude/dnd`,
  the hook won't touch it — set `DND_CAMPAIGN_ROOT="$PWD/dnd-data"` to use the
  repo data there instead.
- **Don't forget to push** — unpushed saves live only in the throwaway container.
