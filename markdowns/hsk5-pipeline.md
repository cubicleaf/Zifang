# HSK 5 Generation Pipeline

**Decided:** 2026-04-29. **Approach:** hybrid Python pre-fill + LLM enrichment + hand-correction.

---

## Why hybrid (and not the four alternatives I considered)

| Approach | Verdict | Reason |
|---|---|---|
| Pure LLM batching (HSK 4 style) | Rejected | LLM is wasted on mechanical fields (id, trad, simp, pinyin). Burns output budget for low value. Also LLMs hallucinate pinyin. |
| Pure Python (no LLM) | Rejected | Python can't write semanticNote, components[], examples[]. Heart of the deck is the LLM-generated content. |
| Topic-clustered batches (food, tech, abstract) | Rejected | Cool pedagogically but ID assignment becomes messy. Alphabetical = stable IDs = trivial dedup. |
| Lazy-load split file | Rejected | Violates Tim's locked single-file-HTML constraint. |
| **Hybrid (chosen)** | **Selected** | Mechanical fields done deterministically by Python (cheap, exact). Content fields done by LLM (where it adds value). Hand-correction layer at the end. |

---

## Pipeline stages

### Stage 1 — Python skeleton (deterministic, ~1 minute)

**Script:** `scripts/hsk5_skeleton.py`
**Input:** `data/hsk5-source-2012.txt` (1,300 simplified words)
**Output:** `data/hsk5-skeleton.json` (1,291 cards with mechanical fields filled)

Per card:
1. Drop the 9 NUGGETS duplicates (哎, 嗯, 不得了, 多余, 好奇, 进步, 夸张, 系统, 自由).
2. Assign id: 2401, 2402, ... 3691.
3. simplified = source word.
4. traditional = OpenCC s2twp(simp) → apply override dict → final.
5. pinyin = pypinyin Style.TONE(simp) → join syllables → apply override dict → final.
6. category = "hsk5".
7. depth = "basic".
8. Stub fields: english="", pos="", semanticNote="", components=[], examples=[].

The Python override dicts encode every Scout-A and Scout-C finding. Stage 1 alone produces a deck that's 60% finished from a data-correctness perspective.

### Stage 2 — LLM enrichment (~13 batches × ~100 cards each)

**Per batch:** Read N skeleton cards (with mechanical fields locked) + the full `hsk5-hazard-map.md` rulebook → output N enriched cards with `english`, `pos`, `semanticNote`, `components[]`, `examples[]` filled.

**Why batching:** LLM output is capped per call. ~100 fully-enriched HSK 5 cards is the realistic ceiling per pass. 1,291 / 100 ≈ 13 batches.

**Critical priming for every batch:**
- "DO NOT regenerate trad/simp/pinyin — those are pre-locked. Fill only english/pos/semanticNote/components/examples."
- "If word is in Section 5 (separable verbs), at least one example MUST show the split form."
- "If word is a measure word, semanticNote MUST list 3+ noun classes it pairs with."
- "If word is in classical/formal register list, semanticNote MUST flag the register."
- "If word is 国庆节/公元/土豆 — apply the explicit warning per Section 8."

**Failure mode to watch:** LLMs default to generic "this word means X" notes. The hazard-map priming is what prevents flat output.

### Stage 3 — Hand-correction pass (~280 cards, Tim-driven)

**Tooling:** Diff-and-flag script that surfaces every card with:
- A pinyin in the override list (verify final value)
- A traditional in the override list (verify final value)
- A separable-verb classification (verify split-example presence)
- A heteronym character (verify reading per gloss)

Tim spot-fixes these in `hsk5-staging.json` directly. Cards he approves get a `verified: true` flag.

### Stage 4 — Merge to index.html (single transactional edit)

**Only run when staging is green.** Insert the full HSK5_NUGGETS array after the HSK4_NUGGETS array in index.html. Add `'hsk5'` to category labels in `getCategoryLabel()` and `getCategoryLabelBilingual()`. Add HSK 5 pill to the three button locations (line ~7346, ~7427, ~7772). Test mobile.

---

## Realistic timeline

| Stage | Time | Sessions |
|---|---|---|
| Stage 1 (Python skeleton) | ~1 minute | 1 |
| Stage 2 (LLM enrichment) | ~13 batches × ~5 min generation | 3-4 sessions |
| Stage 3 (hand-correction) | ~2 hours of Tim spot-fixing | 1-2 sessions |
| Stage 4 (merge to index.html) | ~30 min | 1 session |
| **Total** | **~5-7 sessions** | |

This is honest scope. HSK 4's 600 cards took multiple sessions; HSK 5 doubles that and adds the override complexity.

---

## What ships in THIS session

- ✓ Stage 1 complete (skeleton with all 1,291 mechanical fields)
- ✓ ~~First Stage 2 batch~~ → realistic: first ~50-100 cards as quality sample, so Tim can spot-check the format and approve before we commit to 13 batches.
- 🛑 Remaining 12+ Stage 2 batches: future sessions.
- 🛑 Stage 3 hand-correction: future sessions.
- 🛑 Stage 4 merge: future session.

---

## Risk register

1. **OpenCC dictionary updates** could silently break overrides. Pin opencc-python-reimplemented version in requirements.
2. **pypinyin updates** could change default readings. Pin version. Consider unit test that asserts override list still matches expected wrong-default output.
3. **LLM example-sentence drift** — generated examples might not actually contain the target word. Lint with regex check after each batch.
4. **Heteronym disambiguation** — if Stage 2 LLM picks the wrong sense, the entire card is wrong. Each batch must include the Scout C disambiguation table inline.
