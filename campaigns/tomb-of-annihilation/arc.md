# Campaign Arc — tomb-of-annihilation

*Structured (imported) campaign. Full act/chapter tree lives here so it stays out of the hot path at `/dm:dnd load`. `state.md → ## Campaign Arc` holds only the current+next chapter window. Read this file when advancing chapters or answering a broad-arc question.*

*Structure note: ToA is **hub-and-spoke** — Chapters 1–2 are open exploration; Chapter 3 (Omu) is a nine-shrine hub the party can tackle in any order; Chapters 4–5 are the linear endgame. Source detail is referenced from the player's own copy of the module per chapter, not stored here.*

```yaml
type: structured
source: "Tomb of Annihilation"
structure: hub-and-spoke
current_act: 1
current_chapter: "1.1"

acts:
  - act: 1
    title: "Port Nyanzaru — The Only Safe Harbor"
    chapters:
      - id: "1.1"
        title: "Arrival & The Charge"
        location: "Port Nyanzaru"
        source_ref: "module Ch.1 (player copy)"
        key_beats:
          - "Party learns the nature of the Death Curse and accepts the charge (patron: Syndra Silvane or table's chosen hook)"
          - "Party understands they must journey into the interior to find the source"
        telegraph_scene: "A dying NPC visibly wasting from the curse; resurrection magic failing; the patron's plea."
        branching_notes: "Any patron works (Syndra Silvane is default). Hook can also be Flaming Fist contract or personal stakes if a PC was once raised."
        status: current
      - id: "1.2"
        title: "Provisioning & A Guide"
        location: "Port Nyanzaru (Grand Souk, Merchants' Ward, Temple District)"
        source_ref: "module Ch.1 (player copy)"
        key_beats:
          - "Party hires a guide (Azaka, Eku, Qawasha, etc.) — required to navigate the hexcrawl"
          - "Party provisions and may complete 1–2 city side quests for coin/allies"
        telegraph_scene: "The merchant princes' offers and the guides' auditions; rival faction agents making their pitches."
        branching_notes: "Which guide they pick seeds later loyalty/betrayal. Side quests (dinosaur race, etc.) are optional but build investment."
        status: pending

  - act: 2
    title: "The Land of Chult — The Green Hell"
    chapters:
      - id: "2.1"
        title: "Into the Jungle (Hexcrawl)"
        location: "Chult wilderness"
        source_ref: "module Ch.2 (player copy)"
        key_beats:
          - "Party survives the jungle (navigation, foraging, disease, random encounters)"
          - "Party gathers rumors/clues pointing toward Omu"
        telegraph_scene: "First brutal wilderness encounter; the canopy closing overhead; a guide's warning."
        branching_notes: "Open exploration. Key location-dungeons (Camp Vengeance, Firefinger, Mbala, Wreck of the Narwhal, Hrakhamar, Nangalore, Kir Sabal) can be visited in any order or skipped."
        status: pending
      - id: "2.2"
        title: "Finding Omu"
        location: "Orolunga / Kir Sabal / Mbala (oracle sites)"
        source_ref: "module Ch.2 (player copy)"
        key_beats:
          - "Party learns the location of the lost city of Omu (e.g. from Saja N'baza, the naga oracle at Orolunga, or Asharra at Kir Sabal)"
        telegraph_scene: "An oracle or NPC who knows the way and what it will cost — the city is hidden in a sinkhole-ringed valley."
        branching_notes: "Multiple sources can reveal Omu. Mbala's hag Nanny Pu'pu is a dangerous alternative source."
        status: pending

  - act: 3
    title: "Omu — The Forbidden City"
    chapters:
      - id: "3.1"
        title: "The Ruined City & The Nine Shrines"
        location: "Omu"
        source_ref: "module Ch.3 (player copy)"
        key_beats:
          - "Party recovers the nine puzzle cubes from the nine trickster-god shrines"
          - "Party contends with the yuan-ti patrols, the grung, and the King of Feathers (undead T-rex)"
        telegraph_scene: "The valley rim; the dead city below; the first shrine puzzle establishing the pattern."
        branching_notes: "HUB. Shrines in any order. Some cubes may be held by NPCs/monsters (Nanny Pu'pu, Withers, yuan-ti). The trickster gods bargain for aid."
        status: pending
      - id: "3.2"
        title: "The Threshold of the Tomb"
        location: "Omu — palace ruins / Fane approach"
        source_ref: "module Ch.3–4 (player copy)"
        key_beats:
          - "Party locates the entrance to the Tomb of the Nine Gods and learns the cubes are the key"
        telegraph_scene: "The puzzle-cube mechanism; signs that the yuan-ti also seek the way down."
        branching_notes: "Party may enter the Fane first (Ch.4) or find a way to the Tomb directly."
        status: pending

  - act: 4
    title: "Fane of the Night Serpent"
    chapters:
      - id: "4.1"
        title: "The Yuan-ti Temple"
        location: "Fane of the Night Serpent (beneath Omu)"
        source_ref: "module Ch.4 (player copy)"
        key_beats:
          - "Party confronts or evades the yuan-ti cult (Ras Nsi / Fenthaza)"
          - "Party secures any missing cubes and the means to open the Tomb"
        telegraph_scene: "The serpent-cult's scope; Fenthaza's offer or Ras Nsi's wrath; the captive princess Mwaxanaré thread."
        branching_notes: "Stealth, alliance with Fenthaza against Ras Nsi, or open assault all viable. Withers may appear to lead them onward."
        status: pending

  - act: 5
    title: "Tomb of the Nine Gods — The Death-Trap"
    chapters:
      - id: "5.1"
        title: "Level 1 — Rotten Halls"
        location: "Tomb of the Nine Gods, L1"
        source_ref: "module Ch.5 (player copy)"
        key_beats: ["Party enters the Tomb; first lethal traps establish the rules of the place"]
        telegraph_scene: "Withers as macabre guide; Acererak's warning handouts."
        branching_notes: "Megadungeon. Each level is a gauntlet of traps and trickster-god trials."
        status: pending
      - id: "5.2"
        title: "Level 2 — Dungeon of Deception"
        location: "Tomb L2"
        source_ref: "module Ch.5 (player copy)"
        key_beats: ["Illusion and misdirection trials"]
        telegraph_scene: ""
        branching_notes: ""
        status: pending
      - id: "5.3"
        title: "Level 3 — Vault of Reflection"
        location: "Tomb L3"
        source_ref: "module Ch.5 (player copy)"
        key_beats: ["Mirror/reflection trials; trickster-god aid in play"]
        telegraph_scene: ""
        branching_notes: ""
        status: pending
      - id: "5.4"
        title: "Level 4 — Chambers of Horror"
        location: "Tomb L4"
        source_ref: "module Ch.5 (player copy)"
        key_beats: ["Escalating horror; the Tomb's cruelty peaks before the machinery"]
        telegraph_scene: ""
        branching_notes: ""
        status: pending
      - id: "5.5"
        title: "Level 5 — Gears of Hate"
        location: "Tomb L5"
        source_ref: "module Ch.5 (player copy)"
        key_beats: ["The grinding mechanism guarding the final descent"]
        telegraph_scene: ""
        branching_notes: ""
        status: pending
      - id: "5.6"
        title: "Level 6 — Cradle of the Death God"
        location: "Tomb L6 — the Soulmonger"
        source_ref: "module Ch.5 (player copy)"
        key_beats:
          - "Party destroys the Soulmonger and ends the atropal — lifting the Death Curse"
          - "Possible confrontation with Acererak"
        telegraph_scene: "The soul-storm; the atropal in its cradle; the trapped souls visible."
        branching_notes: "Destroying the Soulmonger is the win. Acererak typically escapes to scheme again (sequel hook)."
        status: pending

outstanding_beats:
  - "Accept the charge and grasp the Death Curse (1.1)"
  - "Hire a guide and provision (1.2)"

steering_notes: >
  Open in Port Nyanzaru. Make the curse personal and visible early — show it killing
  someone, show resurrection failing. The clock is the patron's health and the world's
  death toll: dithering has a cost (faction rivals reach Omu, the patron weakens). Do not
  rush them out of the city — the side quests and guide-hiring build the investment that
  makes the jungle and Tomb land. Telegraph that the interior is lethal before they leave.

revision_log: []
```
