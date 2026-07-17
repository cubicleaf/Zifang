#!/usr/bin/env python3
"""
HSK 6 deck skeleton generator.

Reads:  data/hsk6-source-with-defs.txt    (2,499 entries, TSV: simp \t trad \t numbered \t toned \t english)
        data/hsk6-staging-batch-01.json   (100 already-enriched cards — merged in by simplified match)
Writes: data/hsk6-skeleton.json           (~2,499 cards)

Source file already provides simplified, traditional, pinyin (toned), english — so this script is mostly
mechanical. Stage 2 (LLM enrichment) still needs to fill: pos, semanticNote, components, examples.

IDs start at 5001. (HSK 5 occupies 2401–3691; old HSK 6 batch sits at 4001–4100 and is overlaid here
by simplified-form lookup so prior enrichment work isn't lost.)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "hsk6-source-with-defs.txt"
PRIOR = ROOT / "data" / "hsk6-staging-batch-01.json"
OUT = ROOT / "data" / "hsk6-skeleton.json"

START_ID = 5001

def main():
    if not SRC.exists():
        sys.exit(f"Source file missing: {SRC}")

    # Load prior enriched cards keyed by simplified, so we can overlay them
    prior_by_simp = {}
    if PRIOR.exists():
        for c in json.loads(PRIOR.read_text(encoding="utf-8")):
            prior_by_simp[c["simplified"]] = c

    cards = []
    seen = set()
    skipped_dupes = 0

    with SRC.open(encoding="utf-8-sig") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip("\n").strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 5:
                print(f"  warn line {lineno}: only {len(parts)} fields — {parts}", file=sys.stderr)
                continue
            simp, trad, _numbered, toned, english = parts[:5]
            simp, trad, toned, english = simp.strip(), trad.strip(), toned.strip(), english.strip()

            if simp in seen:
                skipped_dupes += 1
                continue
            seen.add(simp)

            card_id = START_ID + len(cards)
            prior = prior_by_simp.get(simp)

            card = {
                "id":           card_id,
                "traditional":  trad or simp,
                "simplified":   simp,
                "pinyin":       toned,
                "english":      english,
                "category":     "hsk6",
                "depth":        "basic",
                "pos":          (prior or {}).get("pos", ""),
                "semanticNote": (prior or {}).get("semanticNote", ""),
                "components":   (prior or {}).get("components", []),
                "examples":     (prior or {}).get("examples", []),
            }
            cards.append(card)

    OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")

    enriched_count = sum(1 for c in cards if c["semanticNote"])
    print(f"Wrote {len(cards)} cards to {OUT.name}")
    print(f"  ID range: {cards[0]['id']}–{cards[-1]['id']}")
    print(f"  Already enriched (carried over from prior batch): {enriched_count}")
    if skipped_dupes:
        print(f"  Skipped {skipped_dupes} duplicate simplified entries")

if __name__ == "__main__":
    main()
