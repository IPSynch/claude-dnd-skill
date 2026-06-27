# Session Log — worm

## Session 0 — Import — 2026-06-27
Source: Worm (Parahumans Novel Series) by Wildbow (PDF, 1.68M words, 6001 pages)
Imported: 30 acts, 304 chapters, ~30 named NPCs, Brockton Bay + wider Earth Bet locations.

**Concept:** D&D 5e campaign set in the *Worm* setting. A new protagonist replaces Taylor with
a completely new origin story; the canonical storyline is preserved. The protagonist occupies
Taylor's exact structural role (debut → Lung → the Undersiders → the full 30-arc spine).

**Build notes:**
- Full novel segmented into a lazy source corpus `source/<id>.md` (one file per canonical
  chapter). Verbatim prose is gitignored for copyright; regenerate with
  `python3 build_corpus.py --pdf "<path to Worm PDF>"`.
- `world.md` / `world-nodes.md` — Brockton Bay, factions, cape classification system, Three
  Truths, threat escalation across all 30 arcs.
- `npcs.md` / `npcs-full.md` — canonical cast (Undersiders, Protectorate/Wards, gang leaders,
  Coil, Travelers, Slaughterhouse Nine, Endbringers, Triumvirate, Cauldron).
- `arc.md` — full structured 30-arc / 304-chapter tree with per-arc key beats and source_refs.
- `state.md` — structured arc pointer set to Arc 1 (Gestation), chapter 1.1.

**Pending:** protagonist character file (power, trigger/origin, civilian-life NPCs). Once it
arrives: create the PC sheet, re-thread any canon beats that hinged on Taylor's specific power,
and begin play at Arc 1.

→ Next: `/dm:dnd character new` (build the protagonist), then `/dm:dnd load worm` to play.
