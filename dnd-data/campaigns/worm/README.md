# Worm — D&D 5e Campaign

A `/dm:dnd` campaign that runs the **Worm** (Parahumans) storyline with a **new protagonist
replacing Taylor** (new origin, same canonical plot). The protagonist takes Taylor's structural
role: debut → Lung → the Undersiders → the full 30-arc spine.

## What's here

| File | Role |
|---|---|
| `world.md` | Brockton Bay, factions, cape classification system, threat arc (load-time core) |
| `world-nodes.md` | Quest seeds + locations (lazy reference) |
| `npcs.md` / `npcs-full.md` | Canonical cast index + full entries (DM reference, has spoilers) |
| `arc.md` | Full structured 30-arc / 304-chapter tree with per-arc beats |
| `state.md` | Live state + structured arc pointer (currently Arc 1, ch 1.1) |
| `session-log.md` | Session 0 import record |
| `source-index.md` | Chapter → source-file map |
| `build_corpus.py` | Regenerates the `source/` corpus from the Worm PDF |
| `build_arc.py` | Regenerates `arc.md` from the index + authored beats |
| `characters/` | Protagonist sheet goes here (pending) |

## Copyright note

The verbatim novel text (`source/*.md`) is **gitignored** — it is not committed. It's the full
copyrighted novel, kept locally only as the DM's lazy reference. Everything committed is original
campaign material (setting, cast, arc beats — summaries) plus the build scripts.

## Setup (regenerate the corpus on a fresh checkout)

```bash
export DND_CAMPAIGN_ROOT="<repo>/dnd-data"          # point the skill at this data root
pip install pymupdf                                  # PDF extraction
python3 dnd-data/campaigns/worm/build_corpus.py \
  --pdf "/path/to/Worm - Parahumans Novel Series by Wildbow.pdf"
python3 skills/dnd/scripts/corpus_check.py --campaign worm   # expect: lazy-corpus layout OK
```

## Play

```
/dm:dnd character new      # build the protagonist (define power, trigger/origin)
/dm:dnd load worm          # start playing at Arc 1 — Gestation
```

Powers are mapped to D&D 5e mechanics — see `world.md → Power → 5e mapping`. The protagonist's
power and origin come from the character file; canon beats that hinged on Taylor's bug-control
get re-threaded to the new power.
