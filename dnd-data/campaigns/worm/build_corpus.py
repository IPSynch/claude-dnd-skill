#!/usr/bin/env python3
"""
build_corpus.py — regenerate the Worm lazy-source corpus from the source PDF.

The verbatim novel text is NOT committed to git (copyright). This script
rebuilds the per-chapter source corpus locally from your own copy of the PDF so
the campaign is fully playable. Point --pdf at the extracted PDF and run it.

    python3 build_corpus.py --pdf "/path/to/Worm - Parahumans Novel Series by Wildbow.pdf"

It slices the book by its table-of-contents chapter boundaries into
source/<id>.md (one file per canonical chapter) and writes source-index.md.
Chapter ids match the arc.chapter scheme used in arc.md (e.g. 1.1, 1.i, 3.5).

Requires: pymupdf  (pip install pymupdf)
"""
import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def slug_id(title: str, fallback_arc: int) -> str:
    """Derive an arc.chapter id from a TOC title."""
    t = title.strip()
    # Standard chapter: "Gestation 1.1", "Insinuation 2.10"
    m = re.match(r"^[A-Za-z].*?\s+(\d+)\.(\d+)\s*$", t)
    if m:
        return f"{m.group(1)}.{m.group(2)}"
    # Bonus half-interlude: "Interlude 3½ (Bonus)" -> 3.5
    if "½" in t:
        m = re.search(r"(\d+)", t)
        if m:
            return f"{m.group(1)}.5"
    # Interlude with a number: "Interlude 1", "Interlude 11 (Donations ...)"
    m = re.match(r"^Interlude\s+(\d+)", t)
    if m:
        base = f"{m.group(1)}.i"
        # capture a trailing letter/part to disambiguate multi-part interludes
        extra = re.search(r"Interlude\s+\d+\s*([A-Za-z])\b", t)
        return base + (extra.group(1).lower() if extra else "")
    # Endbringer / named interludes and anything else: slugify
    s = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return f"{fallback_arc}-{s}" if s else f"{fallback_arc}-x"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="path to the Worm PDF")
    ap.add_argument("--out", default=str(HERE), help="campaign dir (default: this dir)")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: pymupdf not installed. Run: pip install pymupdf", file=sys.stderr)
        return 2

    pdf = pathlib.Path(args.pdf).expanduser()
    if not pdf.exists():
        print(f"ERROR: PDF not found: {pdf}", file=sys.stderr)
        return 2

    out = pathlib.Path(args.out).resolve()
    source_dir = out / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf))
    toc = doc.get_toc()  # [level, title, page] (1-based pages)
    if not toc:
        print("ERROR: PDF has no table of contents to segment by.", file=sys.stderr)
        return 2

    # Build (id, title, start_page0, end_page0, arc) for each chapter.
    entries = []
    seen = {}
    for i, (_lvl, title, page) in enumerate(toc):
        start0 = max(0, page - 1)
        end0 = (toc[i + 1][2] - 1) if i + 1 < len(toc) else doc.page_count
        m = re.match(r"^[A-Za-z].*?\s+(\d+)\.\d+", title) or re.match(r"^Interlude\s+(\d+)", title)
        arc = int(m.group(1)) if m else (entries[-1][4] if entries else 0)
        cid = slug_id(title, arc)
        # de-dup ids just in case
        if cid in seen:
            seen[cid] += 1
            cid = f"{cid}-{seen[cid]}"
        else:
            seen[cid] = 0
        entries.append((cid, title.strip(), start0, end0, arc))

    index_rows = []
    for cid, title, start0, end0, arc in entries:
        text = []
        for p in range(start0, min(end0, doc.page_count)):
            text.append(doc.load_page(p).get_text())
        body = "\n".join(text).strip()
        (source_dir / f"{cid}.md").write_text(
            f"# {title}\n\n_Arc {arc} · source pages {start0 + 1}-{end0}_\n\n{body}\n",
            encoding="utf-8",
        )
        scope = title
        index_rows.append((cid, arc, scope))

    # source-index.md
    lines = [
        "# Worm — Source Corpus Index",
        "",
        f"Source: Worm (Parahumans) by Wildbow — {len(entries)} chapters across "
        f"{max(a for _, a, _ in index_rows)} arcs.",
        "",
        "Verbatim prose is gitignored; regenerate with `build_corpus.py`.",
        "",
        "| Chapter | Arc | Source file | Scope |",
        "|---|---|---|---|",
    ]
    for cid, arc, scope in index_rows:
        lines.append(f"| {cid} | {arc} | source/{cid}.md | {scope} |")
    (out / "source-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {len(entries)} chapter files to {source_dir}")
    print(f"Wrote {out / 'source-index.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
