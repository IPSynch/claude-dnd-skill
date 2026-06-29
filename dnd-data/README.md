# dnd-data — in-repo data root for the dm skill

This directory is the **data root** for the D&D skill when the repo is used as a
playable, portable campaign store (so you can play from any device — phone
included — without your laptop). It mirrors the layout the skill expects under
`~/.claude/dnd/`:

```
dnd-data/
├── campaigns/<name>/   ← state, world, npcs, arc, source corpus, supplements, saves
├── characters/         ← global character roster
├── rules/              ← global DM rules (read every load, all campaigns)
└── monster-manual/     ← statblock library (lazy reference, all campaigns)
```

A **SessionStart hook** (`.claude/hooks/dnd-session-start.sh`) symlinks
`~/.claude/dnd` → here on every session, so the skill finds it automatically.
Override per-machine with `DND_CAMPAIGN_ROOT="…/dnd-data"` if you prefer not to
symlink (e.g. on a local install that already has its own `~/.claude/dnd`).

**Persistence:** play writes into this directory. Commit & push at session end
(see `MOBILE-PLAY.md`) so your progress is waiting on the next device.

> Contains third-party module/bestiary text — **keep this repository private** and
> only store material you personally own.
