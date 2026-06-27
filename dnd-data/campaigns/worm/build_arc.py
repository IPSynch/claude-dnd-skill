#!/usr/bin/env python3
"""Generate arc.md (structured 30-arc tree) from source-index.md + authored beats.

Chapter rows (id/title/source_ref) come from the index; arc-level key_beats,
telegraph and steering notes are authored below from canonical knowledge of the
storyline. Protagonist occupies Taylor's structural role. Re-run after the index
changes. Authored beats are summaries — no verbatim source prose.
"""
import re
import pathlib
from collections import OrderedDict

HERE = pathlib.Path(__file__).resolve().parent

# arc_num -> (arc_name, structure_summary, [key_beats], telegraph, steering)
ARCS = {
 1: ("Gestation",
     "Debut. The protagonist's first night out as a cape ends in a collision with Lung; the Undersiders intervene and extend an offer.",
     ["Protagonist debuts solo, intending to do good","Encounter with Lung escalates toward disaster",
      "The Undersiders intervene; protagonist helps take Lung down with a power-specific gambit",
      "The offer to join the Undersiders is made","Interlude: the heroes' side reacts to a new cape and a downed Lung"],
     "A patrol scene that puts the protagonist near ABB activity so stumbling onto Lung feels organic, not railroaded.",
     "Let the protagonist define WHY they accept the Undersiders' offer (undercover, lost, curious). That motive seeds the whole campaign."),
 2: ("Insinuation",
     "Settling in with the team and the protagonist's first heist: the bank job, and a brush with the Wards.",
     ["Protagonist meets the team properly; trust begins (Tattletale sees their secret)","The bank robbery job is planned and run",
      "Collision with Glory Girl / the Wards during the heist","First real taste of the patron's money and rules",
      "Interlude: a hero or rival's POV on the new villain crew"],
     "A low-stakes team scene (the lair, planning) before the job, so the heist's chaos lands against an established normal.",
     "Foreground the protagonist's double life and the strain it puts on civilian relationships from the new origin."),
 3: ("Agitation",
     "Fallout escalates. Bakuda's bombing campaign begins after Lung's removal; the ABB terrorizes the city.",
     ["Lung's absence destabilizes the ABB; Bakuda seizes power","Bombing campaign turns the city into a minefield",
      "The Undersiders are pressured to act / pick sides","A captured-or-cornered crisis raises the stakes personally",
      "Interlude: the cost of Bakuda's terror from another POV"],
     "A normal errand interrupted by a bombing, making the threat visceral and local before the team strategizes.",
     "Use civilian danger to force the protagonist between safe self-interest and doing good — the campaign's core tension."),
 4: ("Shell",
     "Regrouping and consequences; the team and the city take stock after the ABB crisis, and Coil's hand starts to show.",
     ["Aftermath and injuries force a regroup","The patron's deeper agenda begins to surface",
      "New rivalries/alliances among the city's capes shift","A personal thread for the protagonist deepens (team bond or civilian fallout)"],
     "A quieter recovery beat the DM can use to develop relationships before the next escalation.",
     "Plant Coil breadcrumbs the protagonist can choose to investigate; don't reveal him yet."),
 5: ("Hive",
     "The Undersiders take on bigger jobs; team identity solidifies and the protagonist's role within it crystallizes.",
     ["A larger, riskier operation tests the team","Internal team dynamics (Bitch's trust, Grue's leadership) come to a head",
      "The protagonist proves themselves / takes initiative","Stakes rise toward a citywide confrontation"],
     "A team-friction scene (e.g. earning Bitch's respect) that sets up cooperation under pressure.",
     "Reward the protagonist taking ownership; let leadership gravitate toward them as canon did with Taylor."),
 6: ("Tangle",
     "Schemes intertwine — Coil's plan, the gangs, and the heroes' moves collide; the protagonist learns more than is comfortable.",
     ["Multiple factions' plans are revealed to overlap","The protagonist uncovers part of the patron's true intent (e.g. Dinah)",
      "A betrayal or hard moral choice presents itself","The board is set for a citywide event"],
     "An information-gathering scene where a Thinker (Tattletale) hands the protagonist a thread they can't un-pull.",
     "Dinah's captivity is the moral lever — surface it here as a slow burn toward turning on Coil."),
 7: ("Buzz",
     "Tension peaks just before catastrophe; the city's powers are arrayed against each other when something far worse arrives.",
     ["Citywide cape conflict reaches a boiling point","Ominous signs precede an Endbringer","Alliances of convenience form under pressure",
      "The protagonist is forced into the wider cape community"],
     "A confrontation that feels like the climax — then the Endbringer alarm cuts it short, recontextualizing everything.",
     "Make the pre-Leviathan stakes feel ultimate, so Leviathan's arrival flips the whole frame."),
 8: ("Extermination",
     "Leviathan attacks Brockton Bay. The Endbringer truce: every cape, hero and villain, fights together. Many die. The city breaks.",
     ["The Endbringer truce forces heroes and villains to fight side by side","Leviathan's assault devastates the city",
      "Catastrophic losses; named capes die","The protagonist survives and is changed; their standing rises",
      "Interlude(s): the wider toll of the attack"],
     "The truce briefing — a rare scene of all factions in one room — before the water hits.",
     "This is a watershed. Let it cost something real and permanent; the post-Leviathan city is the new normal."),
 9: ("Sentinel",
     "Immediate aftermath of Leviathan. A broken city, displaced people, shifted power, and grief.",
     ["The city's survivors and factions reorganize amid ruin","Power vacuums open; who steps up matters",
      "The protagonist's choices about responsibility crystallize","Coil maneuvers in the chaos"],
     "A walk through the wreckage that makes the human cost concrete before politics resume.",
     "Use the vacuum to push the protagonist toward taking territory/responsibility — the warlord seed."),
 10: ("Parasite",
     "A focused threat amid the rubble tests the weakened city and the protagonist directly.",
     ["A new predator exploits the post-Leviathan weakness","The protagonist confronts it with limited resources",
      "Team and alliances are strained","A step toward the protagonist's growing influence"],
     "An intrusion into a place the protagonist now feels responsible for, forcing a defense.",
     "Keep escalating the protagonist's stake in the city's people, not just the team."),
 11: ("Infestation",
     "The Slaughterhouse Nine come to Brockton Bay. Horror, tests, and a list with the protagonist's name on it.",
     ["The Nine arrive and begin 'testing' the city's capes","Jack Slash marks the protagonist as interesting",
      "Impossible moral tests / forced choices","Temporary alliances against a shared nightmare",
      "Multiple interludes: the Nine's victims and members"],
     "A too-quiet scene that curdles as a Nine member reveals they've been present all along.",
     "Run the Nine as a slasher film, not a brawl. Dread, choice, and survival over win/lose."),
 12: ("Plague",
     "The Slaughterhouse Nine crisis deepens; the city fights for survival and the protagonist makes defining choices.",
     ["The Nine's campaign turns the city against itself","A defining hard choice for the protagonist",
      "Costly resistance; allies fall or are broken","The Nine are driven off / transformed at great cost"],
     "A trap sprung by Jack that forces the protagonist to choose who/what to save.",
     "Let the protagonist's defiance define them; Jack respects and remembers it."),
 13: ("Snare",
     "Reckoning with Coil. The patron's plan comes due and the protagonist must decide whether to break with him.",
     ["Coil moves to consolidate control of the city","The protagonist's knowledge of Dinah forces the issue",
      "A plan to turn on Coil takes shape","Double-games and timeline tricks complicate everything"],
     "A meeting with Coil where his politeness barely conceals ownership, making the break feel necessary.",
     "Coil's two-timelines power is the puzzle — winning requires removing his safety net, not out-fighting him."),
 14: ("Prey",
     "The Travelers and a hidden horror (Noelle) surface; a swap-and-clone crisis erupts across the city.",
     ["The Travelers' secret (Noelle) begins to unravel","Cloned/duplicated capes wreak havoc","The Coil reckoning collides with the Noelle crisis",
      "The protagonist brokers desperate cooperation","Interludes: the Travelers' tragedy"],
     "A tense Travelers contact scene that hints something is very wrong beneath their loyalty.",
     "Two crises braided together — keep the protagonist triaging, forced to prioritize."),
 15: ("Colony",
     "The clone/Echidna crisis peaks; uncomfortable truths about the heroes and Cauldron begin leaking out.",
     ["The duplication threat becomes citywide/existential","Captured capes' clones spill hidden secrets (Cauldron, the Triumvirate)",
      "An all-hands battle to contain the horror","The protagonist gains dangerous knowledge"],
     "A briefing/standoff where a clone blurts a secret no one was meant to hear.",
     "The leaked secrets (Cauldron, Alexandria) are seeds for the back half — note what the protagonist learns."),
 16: ("Monarch",
     "Resolution of the Coil/Echidna arcs and the protagonist's ascension; the team inherits the city's underworld.",
     ["Coil is dealt with; Dinah's fate is decided","Echidna crisis ends at great cost","The protagonist/Undersiders take Coil's territory and resources",
      "The protagonist steps fully into a leadership/warlord role","Interlude: the wider world reacts"],
     "The moment after victory where the spoils — and responsibility — fall to the protagonist.",
     "This is the pivot to the warlord era. Frame power as obligation, not reward."),
 17: ("Migration",
     "Consolidation and a turn outward; the protagonist as a territory-holder, and the world stage opening up.",
     ["The protagonist governs/protects territory","New external threats and politics intrude","Parallel worlds / wider scope become relevant",
      "Relationships and identity strain under the new role"],
     "A 'normal day running territory' scene that's interrupted by something from far outside the city.",
     "Begin widening the lens from Brockton Bay to the world; the local game is becoming a global one."),
 18: ("Queen",
     "A major confrontation forces the protagonist into a fateful gambit and a dramatic change of status.",
     ["A crisis bigger than the city demands a drastic play","The protagonist makes a sacrifice-level choice","Public identity / allegiance shifts hard",
      "The cost reframes who the protagonist is","Interludes: institutional fallout"],
     "An escalation the protagonist can't win clean, setting up a choice that trades safety for impact.",
     "Honor a bold, costly choice here; it should redefine the protagonist's place in the world."),
 19: ("Scourge",
     "Fallout of the gambit; new enemies, a tense regime, and the Simurgh's long shadow.",
     ["Consequences of the protagonist's choice land","An Endbringer (the Simurgh) shapes events from afar","Fragile new alliances tested",
      "Betrayals and shifting loyalties"],
     "A scene where a 'win' turns out to have been set up by the Simurgh, seeding paranoia.",
     "The Simurgh works by precognitive setup — let dread and distrust do the work."),
 20: ("Chrysalis",
     "A transitional crucible; the protagonist endures captivity/scrutiny and re-emerges transformed.",
     ["The protagonist is constrained, tested, or imprisoned","Identity and trust are stripped and rebuilt","An escape/turn re-establishes agency",
      "A new operating mode for the protagonist emerges"],
     "A confinement scene that strips the protagonist's usual tools, forcing growth.",
     "Use the constraint to evolve the protagonist's power use and resolve, not just to gate them."),
 21: ("Imago",
     "Re-emergence and reconciliation; old bonds renegotiated, a new role accepted, the world's threats converging.",
     ["The protagonist rejoins/reforms their circle on new terms","Hero/villain lines blur further toward alliance","Converging threats demand unity",
      "A fragile coalition begins to form","Interludes: the global picture"],
     "A reunion that's both warm and changed, acknowledging everything that happened.",
     "Start assembling the everyone-against-the-end coalition that the finale needs."),
 22: ("Cell",
     "Tighter focus under pressure; the protagonist operates inside a constrained, high-surveillance regime.",
     ["The protagonist works within (or against) a controlling authority","Trust is currency and in short supply","A contained mission with outsized stakes",
      "Cracks in the larger order show"],
     "A locked-down operation where every ally might be a watcher.",
     "Keep paranoia high; the institutions are not as solid as they pretend."),
 23: ("Drone",
     "Mechanisms of control and surveillance dominate; the protagonist navigates a world tightening around capes.",
     ["Surveillance/control apparatus bears down","The protagonist finds room to maneuver anyway","An ally's hidden agenda surfaces",
      "Momentum builds toward open crisis"],
     "A scene exposing how thoroughly the protagonist is watched, and one blind spot they can exploit.",
     "Reward cleverness against the system; the endgame needs the protagonist resourceful and trusted-enough."),
 24: ("Crushed",
     "A devastating reversal — an 'all is lost' beat where a major effort fails or a great cost is paid.",
     ["A central plan collapses or a key figure falls","The protagonist absorbs a genuine, earned defeat","The world lurches toward the brink",
      "The survivors are forced into the final configuration","Interludes: the toll"],
     "A confident push that the world answers with catastrophe — telegraphed, unstoppable.",
     "This is the back-half 'All Is Lost.' Make it land from the story's logic, not bad luck."),
 25: ("Scarab",
     "Picking up the pieces toward a last stand; the truth about the world's threat becomes undeniable.",
     ["The real, final threat is named and understood","Grief converts into grim resolve","Former enemies are pulled into one cause",
      "The shape of a final plan emerges"],
     "A reveal scene that reframes the entire campaign's conflict as prelude to the true threat.",
     "Pivot every faction toward the existential threat; old grudges become unaffordable."),
 26: ("Sting",
     "Assembling the weapon/plan against the unstoppable; precise, costly preparation and a first real strike.",
     ["A plan to hurt the unhurtable is devised","Rare resources/capes are gathered for a single shot","A coordinated strike is attempted",
      "Partial success at terrible cost","Interludes: the coalition's pieces"],
     "A heist-like assembly of exactly the right powers for one impossible shot.",
     "Lean into the protagonist's strategic mind; the plan should feel ingenious and fragile."),
 27: ("Extinction",
     "The threat goes fully global; the world begins to end and the coalition commits everything.",
     ["The threat turns openly apocalyptic","World-ending losses mount across many fronts","Total mobilization of every cape",
      "The protagonist becomes central to the last effort"],
     "An attack scene of overwhelming scale that ends any illusion of safety anywhere.",
     "Scale is now total. Keep the protagonist's human-level choices legible inside the apocalypse."),
 28: ("Cockroaches",
     "Survival against extinction; the stubborn, scrappy refusal to die that the title evokes.",
     ["Survivors regroup against impossible odds","The protagonist makes a desperate, defining move","Sacrifices buy the final chance",
      "The last plan is set in motion"],
     "A near-wipe the protagonist survives by sheer refusal, earning the final gambit.",
     "Honor endurance and defiance; this is the 'we don't get to quit' beat."),
 29: ("Venom",
     "The penultimate convergence; the coalition's final coordination, betrayals burned away, the last pieces placed.",
     ["The coalition makes its final, total commitment","A last betrayal or hard sacrifice is resolved","The protagonist's role in the endgame is locked",
      "Everything narrows to the final confrontation","Interludes: farewells and final POVs"],
     "A pre-battle scene of everyone choosing to stand together despite everything.",
     "Tie off relationships and threads; the finale should feel like every choice converging."),
 30: ("Speck",
     "The end. The final confrontation against the unstoppable, the protagonist's ultimate choice, and what it costs.",
     ["The final battle against the world-ending threat","The protagonist's decisive, costly contribution","The threat is ended — at enormous, personal price",
      "Aftermath: who survives, what the world becomes, what the protagonist gives up","Epilogue beats"],
     "The convergence of every cape and every plan for one last impossible push.",
     "Land the ending on the protagonist's choice and its cost. Bittersweet, earned, final."),
}

ARC_NAMES = {n: v[0] for n, v in ARCS.items()}


def yaml_list(items):
    return "[" + ", ".join('"' + i.replace('"', "'") + '"' for i in items) + "]"


def main():
    rows = []
    for line in (HERE / "source-index.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([\w.\-]+)\s*\|\s*(\d+)\s*\|\s*source/([\w.\-]+)\.md\s*\|\s*(.+?)\s*\|", line)
        if m:
            rows.append((m.group(1), int(m.group(2)), m.group(3), m.group(4)))

    by_arc = OrderedDict()
    for cid, arc, sref, title in rows:
        by_arc.setdefault(arc, []).append((cid, sref, title))

    out = []
    out.append("# Campaign Arc — Worm (Parahumans)\n")
    out.append("*Structured (imported) campaign. Full 30-arc / 304-chapter tree. "
               "Read on demand when advancing chapters or answering a broad-arc question — "
               "NOT at every load (state.md carries the current window). Chapter text is the "
               "lazy `source/<id>.md` corpus (gitignored verbatim prose; rebuild with build_corpus.py).*\n")
    out.append("*Protagonist occupies Taylor's structural role; where a canonical beat hinged on "
               "bug-control specifically, re-thread it to the protagonist's power. Beats below are "
               "authored summaries of the storyline, not source prose.*\n")
    out.append("```yaml")
    out.append("type: structured")
    out.append('source: "Worm (Parahumans) by Wildbow"')
    out.append("structure: linear")
    out.append("current_act: 1")
    out.append('current_chapter: "1.1"')
    out.append("")
    out.append("acts:")
    for arc in sorted(by_arc):
        name, summary, beats, telegraph, steering = ARCS[arc]
        out.append(f"  - act: {arc}")
        out.append(f'    title: "{name}"')
        out.append(f'    summary: "{summary}"')
        out.append(f"    key_beats: {yaml_list(beats)}")
        out.append(f'    telegraph_scene: "{telegraph}"')
        out.append(f'    steering_notes: "{steering}"')
        out.append("    chapters:")
        for cid, sref, title in by_arc[arc]:
            status = "current" if cid == "1.1" else "pending"
            out.append(f'      - id: "{cid}"')
            out.append(f'        title: "{title}"')
            out.append(f'        source_ref: "source/{sref}.md"')
            out.append(f"        status: {status}")
    out.append("")
    out.append("# Outstanding beats for the CURRENT chapter only (1.1). Update at /dm:dnd save.")
    out.append(f"outstanding_beats: {yaml_list(ARCS[1][2])}")
    out.append("")
    out.append("steering_notes: >")
    out.append(f"  {ARCS[1][4]}")
    out.append("")
    out.append("revision_log: []")
    out.append("```")
    (HERE / "arc.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote arc.md: {len(by_arc)} acts, {len(rows)} chapters.")


if __name__ == "__main__":
    main()
