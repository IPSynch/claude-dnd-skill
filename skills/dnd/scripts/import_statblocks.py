#!/usr/bin/env python3
"""
import_statblocks.py — import monster statblocks from a bestiary into the
campaign statblock library (the "supplemental" dataset that lookup.py and the
DM merge on top of the bundled SRD).

The bundled SRD (`data/dnd5e_srd.json`) is fixed and rebuilt from upstream SRD
repos by `build_srd.py`. This script is the path for *non-SRD* bestiaries — a
Monster Manual, Tome of Beasts, or any homebrew book — to land in the same
library so `lookup.py monster "<name>"` and combat resolution can use them.
Records are written to `data/dnd5e_supplemental.json` (or the 2024 file), which
`lookup.py` already merges *without overwriting* SRD entries.

Two halves, mirroring `import_campaign.py` + `build_supplemental.py`:

  1. READ — extract and chunk a book so the DM (Claude) can read it and parse
     each statblock into a JSON record. Text extraction is shared with
     `import_campaign.py` (PDF column-aware, MD/TXT/DOCX).

         import_statblocks.py <file> --info
         import_statblocks.py <file> --chunks
         import_statblocks.py <file> --chunk N

  2. MERGE — validate parsed records and write them into the supplemental
     library, stamped with provenance and de-duplicated against the SRD.

         import_statblocks.py --add-json '<json>'  --source-book "Tome of Beasts"
         import_statblocks.py --add-file recs.json --source-book "Tome of Beasts"

  Manage the imported bestiary:

         import_statblocks.py --list
         import_statblocks.py --remove "Clockwork Dragon"
         import_statblocks.py --remove-book "Tome of Beasts"

Record schema matches the SRD monster shape so the existing formatter / combat
math works unchanged:

    name, index, description, cr, xp, size, type, hp, hp_dice, ac, speed,
    str, dex, con, int, wis, cha, alignment, languages

Only `name` is required. `index` is derived from the name, `xp` is derived from
`cr` when absent, and ability scores default to 10. Each imported record also
carries a `_source` provenance tag (the `--source-book` label).

A note on rights: only import books you have the right to use. The SRD and
Creative-Commons bestiaries (e.g. Kobold Press's open Tome of Beasts content)
are fine to keep in a shared library; closed/copyrighted books (the WotC
Monster Manual) should stay in your own local copy and not be committed back.
"""

import argparse
import datetime
import json
import os
import sys

# Reuse the proven text extraction + chunking from the campaign importer.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import import_campaign as ic  # noqa: E402
import lookup as lk  # noqa: E402


# ─── CR → XP (standard 5e encounter table) ────────────────────────────────────
CR_XP = {
    "0": 10, "1/8": 25, "1/4": 50, "1/2": 100,
    "1": 200, "2": 450, "3": 700, "4": 1100, "5": 1800, "6": 2300,
    "7": 2900, "8": 3900, "9": 5000, "10": 5900, "11": 7200, "12": 8400,
    "13": 10000, "14": 11500, "15": 13000, "16": 15000, "17": 18000,
    "18": 20000, "19": 22000, "20": 25000, "21": 33000, "22": 41000,
    "23": 50000, "24": 62000, "25": 75000, "26": 90000, "27": 105000,
    "28": 120000, "29": 135000, "30": 155000,
}

ABILITIES = ("str", "dex", "con", "int", "wis", "cha")


def _cr_key(cr) -> str:
    """Normalise a CR value to the key form used in CR_XP ('1/4', '5', '0')."""
    if cr is None:
        return ""
    if isinstance(cr, float) and cr.is_integer():
        cr = int(cr)
    s = str(cr).strip()
    # Common decimal spellings of fractional CRs.
    return {"0.125": "1/8", "0.25": "1/4", "0.5": "1/2"}.get(s, s)


def _normalise_record(rec: dict, source_book: str) -> tuple[dict, list]:
    """Coerce one parsed statblock into the SRD monster shape.

    Returns (record, warnings). Raises ValueError if it can't be used at all.
    """
    if not isinstance(rec, dict):
        raise ValueError("record is not a JSON object")
    name = str(rec.get("name", "")).strip()
    if not name:
        raise ValueError("record is missing a 'name'")

    warnings = []
    out = dict(rec)  # keep any extra keys (legendary actions, traits, etc.)
    out["name"] = name
    out["index"] = lk._norm(name)

    # CR + XP. Store CR in its canonical key form; derive XP from the table
    # when the book didn't give an explicit value.
    cr_key = _cr_key(rec.get("cr"))
    if cr_key:
        # Integer CRs are stored as ints in the SRD; keep fractions as strings.
        out["cr"] = int(cr_key) if cr_key.isdigit() else cr_key
        if not rec.get("xp"):
            if cr_key in CR_XP:
                out["xp"] = CR_XP[cr_key]
            else:
                warnings.append(f"{name}: unknown CR {cr_key!r}; no XP derived")
    else:
        warnings.append(f"{name}: no CR given")

    # Ability scores — default missing ones to 10 so combat math never divides
    # by a None.
    missing_abilities = []
    for ab in ABILITIES:
        if rec.get(ab) is None:
            out[ab] = 10
            missing_abilities.append(ab.upper())
        else:
            try:
                out[ab] = int(rec[ab])
            except (TypeError, ValueError):
                out[ab] = 10
                missing_abilities.append(ab.upper())
    if missing_abilities:
        warnings.append(f"{name}: defaulted ability scores {','.join(missing_abilities)} to 10")

    for field in ("hp", "ac"):
        if rec.get(field) is None:
            warnings.append(f"{name}: no {field.upper()} given")
        else:
            try:
                out[field] = int(rec[field])
            except (TypeError, ValueError):
                pass  # leave non-integer (e.g. "11 (natural armor)") as-is

    out["_source"] = source_book
    return out, warnings


# ─── Supplemental file I/O ─────────────────────────────────────────────────────

def _supp_path(ruleset: str) -> str:
    return lk._supp_path_for(ruleset)


def _load_supp(ruleset: str) -> dict:
    path = _supp_path(ruleset)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"_meta": {"description": "Supplemental entries for non-SRD content used in active campaigns",
                      "sources": []}}


def _save_supp(ruleset: str, data: dict) -> None:
    path = _supp_path(ruleset)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _srd_monster_names(ruleset: str) -> set:
    """Normalised names already present in the bundled SRD (do not shadow them)."""
    path = lk._srd_path_for(ruleset)
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        srd = json.load(f)
    return {lk._norm(r.get("name", "")) for r in srd.get("monsters", [])}


# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_add(records: list, source_book: str, ruleset: str) -> int:
    if not source_book:
        print("Error: --source-book is required when adding statblocks "
              "(provenance label, e.g. \"Tome of Beasts\").", file=sys.stderr)
        return 1

    supp = _load_supp(ruleset)
    monsters = supp.setdefault("monsters", [])
    by_name = {lk._norm(m.get("name", "")): i for i, m in enumerate(monsters)}
    srd_names = _srd_monster_names(ruleset)

    added = updated = skipped = 0
    all_warnings = []
    for raw in records:
        try:
            rec, warns = _normalise_record(raw, source_book)
        except ValueError as e:
            print(f"  skip: {e}", file=sys.stderr)
            skipped += 1
            continue
        all_warnings.extend(warns)
        key = rec["index"]

        if key in srd_names:
            print(f"  skip: {rec['name']!r} already in the bundled SRD "
                  f"(supplemental entries never override SRD, so it would be dead weight)",
                  file=sys.stderr)
            skipped += 1
            continue

        if key in by_name:
            monsters[by_name[key]] = rec
            updated += 1
        else:
            by_name[key] = len(monsters)
            monsters.append(rec)
            added += 1

    # Record provenance + import date on the file metadata.
    meta = supp.setdefault("_meta", {})
    sources = meta.setdefault("sources", [])
    if source_book not in sources:
        sources.append(source_book)
    meta["last_statblock_import"] = {
        "book": source_book,
        "date": datetime.date.today().isoformat(),
        "added": added, "updated": updated,
    }

    _save_supp(ruleset, supp)

    for w in all_warnings:
        print(f"  warning: {w}", file=sys.stderr)
    print(f"Imported from {source_book!r} into {ruleset} library: "
          f"{added} added, {updated} updated, {skipped} skipped.")
    print(f"Library now holds {len(monsters)} supplemental statblock(s) at {_supp_path(ruleset)}")
    return 0


def cmd_list(ruleset: str) -> int:
    supp = _load_supp(ruleset)
    monsters = supp.get("monsters", [])
    if not monsters:
        print(f"No supplemental statblocks in the {ruleset} library yet.")
        return 0
    # Group by source book for a readable inventory.
    by_book: dict = {}
    for m in monsters:
        by_book.setdefault(m.get("_source", "(unknown source)"), []).append(m)
    print(f"Supplemental statblocks in the {ruleset} library ({len(monsters)} total):\n")
    for book in sorted(by_book):
        rows = sorted(by_book[book], key=lambda m: m.get("name", ""))
        print(f"  {book}  ({len(rows)})")
        for m in rows:
            print(f"    - {m.get('name','?'):<28} CR {str(m.get('cr','?')):<4} "
                  f"{m.get('size','')} {m.get('type','')}".rstrip())
        print()
    return 0


def cmd_remove(name: str, ruleset: str) -> int:
    supp = _load_supp(ruleset)
    monsters = supp.get("monsters", [])
    key = lk._norm(name)
    kept = [m for m in monsters if lk._norm(m.get("name", "")) != key]
    removed = len(monsters) - len(kept)
    if not removed:
        print(f"No supplemental statblock named {name!r} found in the {ruleset} library.")
        return 1
    supp["monsters"] = kept
    _save_supp(ruleset, supp)
    print(f"Removed {removed} statblock(s) named {name!r} from the {ruleset} library.")
    return 0


def cmd_remove_book(book: str, ruleset: str) -> int:
    supp = _load_supp(ruleset)
    monsters = supp.get("monsters", [])
    kept = [m for m in monsters if m.get("_source", "") != book]
    removed = len(monsters) - len(kept)
    if not removed:
        print(f"No statblocks from {book!r} found in the {ruleset} library.")
        return 1
    supp["monsters"] = kept
    sources = supp.get("_meta", {}).get("sources", [])
    if book in sources:
        sources.remove(book)
    _save_supp(ruleset, supp)
    print(f"Removed {removed} statblock(s) from {book!r} in the {ruleset} library.")
    return 0


def _parse_records(payload: str) -> list:
    """Accept a single object, a list, or {"monsters": [...]}."""
    data = json.loads(payload)
    if isinstance(data, dict):
        if "monsters" in data and isinstance(data["monsters"], list):
            return data["monsters"]
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("JSON must be an object, a list, or {\"monsters\": [...]}")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Import monster statblocks from a bestiary into the statblock library.")
    p.add_argument("filepath", nargs="?", help="Bestiary source file (PDF/MD/TXT/DOCX) for --info/--chunk")
    # Read modes (delegate to import_campaign extraction)
    p.add_argument("--info", action="store_true", help="Print file info + chunk count")
    p.add_argument("--chunks", action="store_true", help="Print total chunk count")
    p.add_argument("--chunk", type=int, default=None, metavar="N",
                   help="Print chunk N (0-indexed, ~4000 words) for statblock parsing")
    # Merge modes
    p.add_argument("--add-json", metavar="JSON", help="Merge monster record(s) given as JSON")
    p.add_argument("--add-file", metavar="PATH", help="Merge monster record(s) from a JSON file")
    p.add_argument("--source-book", metavar="NAME", help="Provenance label for added records")
    # Manage
    p.add_argument("--list", action="store_true", help="List imported supplemental statblocks")
    p.add_argument("--remove", metavar="NAME", help="Remove a statblock by name")
    p.add_argument("--remove-book", metavar="BOOK", help="Remove all statblocks from a source book")
    p.add_argument("--ruleset", choices=["2014", "2024"], default="2014",
                   help="Which library to target (default 2014)")
    args = p.parse_args()

    rs = args.ruleset

    # Manage / merge modes (no source file needed)
    if args.list:
        sys.exit(cmd_list(rs))
    if args.remove:
        sys.exit(cmd_remove(args.remove, rs))
    if args.remove_book:
        sys.exit(cmd_remove_book(args.remove_book, rs))
    if args.add_json or args.add_file:
        try:
            payload = args.add_json
            if args.add_file:
                with open(args.add_file, encoding="utf-8") as f:
                    payload = f.read()
            records = _parse_records(payload)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(f"Error reading records: {e}", file=sys.stderr)
            sys.exit(1)
        sys.exit(cmd_add(records, args.source_book, rs))

    # Read modes — require a file
    if not args.filepath:
        p.error("a source file is required for --info/--chunks/--chunk "
                "(or use --add-json/--add-file/--list/--remove)")
    if not os.path.exists(args.filepath):
        print(f"Error: file not found: {args.filepath}", file=sys.stderr)
        sys.exit(1)
    try:
        text = ic.extract(args.filepath)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    if not text.strip():
        print("Warning: extracted text is empty. File may be image-only PDF.", file=sys.stderr)
        sys.exit(1)

    if args.info:
        print(ic.file_info(args.filepath, text))
        print("\nNext: read each chunk, parse statblocks into JSON records, then")
        print("  import_statblocks.py --add-json '<json>' --source-book \"<book>\"")
    elif args.chunks:
        print(ic.total_chunks(text))
    elif args.chunk is not None:
        chunk = ic.chunk_text(text, args.chunk)
        if not chunk:
            print(f"Error: chunk {args.chunk} out of range (max: {ic.total_chunks(text) - 1})",
                  file=sys.stderr)
            sys.exit(1)
        print(chunk)
    else:
        print(text)


if __name__ == "__main__":
    main()
