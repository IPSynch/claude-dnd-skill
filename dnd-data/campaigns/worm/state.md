# Campaign: worm
**Created:** 2026-06-27  **Last session:** —  **Session count:** 0  **Ruleset:** 2014

## Current Situation
- **Location:** Brockton Bay — the Docks district, night (campaign opening)
- **In-world date/time:** Spring, ~2011 (canonical opening; exact date flexible)
- **Party:** *(protagonist character file pending — to be slotted into Taylor's structural role)*
- **Party status:** *(pending character creation)*

## World State
- **In-world date:** Spring 2011, Earth Bet
- **Season:** Spring  **Weather:** Warm nights, coastal damp
- **Threat arc stage:** 1 — Now (street-level gang war in Brockton Bay)
- **Faction states:**
  - The Undersiders: small villain crew, heist-focused, hidden patron — the protagonist's entry point
  - ABB (Lung/Bakuda): aggressive, dominant through fear of Lung
  - Empire 88 (Kaiser): largest gang, white-supremacist power bloc
  - Merchants (Skidmark): disorganized drug gang
  - Protectorate/Wards (Armsmaster, Miss Militia): understaffed official heroes
  - Coil: hidden schemer; secret patron of the Undersiders (not yet known to the protagonist)

## Active Quests
*(none yet — begins at character creation / Session 1)*

## Open Threads & Rumours
- A new cape is about to debut in the Docks (the protagonist).
- Lung and the ABB are expanding their reach.

## Faction Moves
*Updated at the end of each session.*
*(none yet)*

## Recent Events
*(Session 1 pending — campaign imported from the Worm novel as a structured arc)*

## Active Combat
*(none)*

## Live State Flags
*Structured facts designed to survive context compaction. Re-read before any recap or status claim.*

**Cover:**
*(none established — protagonist's civilian identity TBD with character file)*

**Faction stances** *(toward the party)*:
*(none established — the protagonist has not yet debuted)*

**NPC dispositions:**
*(none established)*

## Campaign Arc
```yaml
# --- STRUCTURED ARC POINTER (imported from Worm) ---
type: structured
source: "Worm (Parahumans) by Wildbow"
structure: linear
arc_file: arc.md
current_act: 1
current_chapter: "1.1"
current_chapter_detail:
  id: "1.1"
  title: "Gestation 1.1"
  location: "Brockton Bay — the Docks, night"
  source_ref: "source/1.1.md"
  key_beats:
    - "Protagonist debuts solo as a cape, intending to do good"
    - "Patrol drifts into ABB/gang territory; tension builds"
  telegraph_scene: "A first-patrol scene establishing the protagonist's new power, costume, and reason for going out — drifting toward ABB activity so the Lung encounter (1.2+) feels organic."
next_chapter: "1.2"
outstanding_beats:
  - "Protagonist debuts solo, intending to do good"
  - "Encounter with Lung escalates toward disaster"
  - "The Undersiders intervene; protagonist helps take Lung down with a power-specific gambit"
  - "The offer to join the Undersiders is made"
steering_notes: >
  Arc 1 (Gestation) opens the campaign. Establish the protagonist's new origin/trigger and
  power (from the pending character file), then steer the first patrol toward Lung. The
  protagonist occupies Taylor's role — the Lung fight should end with a clever, power-specific
  gambit rather than brute force, leading into the Undersiders' offer. Let the protagonist
  decide WHY they accept; that motive seeds the whole campaign.
```

## Arc History
*(empty until the first arc completes)*

## Session Flags
- autosave: on
- roll_mode: players

## DM Notes (hidden from players)
- **Campaign concept:** Play Worm with a new protagonist replacing Taylor, new origin story, canonical storyline preserved. The protagonist takes Taylor's exact structural slot (debut → Lung → Undersiders → the full 30-arc spine).
- **Source corpus:** Full novel segmented to `source/<id>.md` (304 chapters), gitignored. Rebuild with `build_corpus.py --pdf <path>`. Read only the current chapter's file before running its scenes — never pre-load.
- **Powers:** D&D 5e mechanically; map the protagonist's cape power and all NPC capes to 5e per `world.md → Power → 5e mapping`. Keep each cape's "one thing" fixed in flavor; scale mechanics with level.
- **Re-threading:** Where canon hinged on Taylor's bug-control (e.g. the Lung win), redesign the "how" around the protagonist's power once the character file arrives.
- **Pending:** protagonist character file (powers, trigger/origin, civilian life NPCs). Until then, the campaign scaffold is complete and ready to play from `/dm:dnd load worm` + `/dm:dnd character new`.
