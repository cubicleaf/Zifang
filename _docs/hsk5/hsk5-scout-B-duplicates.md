# HSK 5 vs Existing Decks — Duplicate Audit (Scout B)

Source list: `data/hsk5-source-2012.txt` (1,300 simplified words)
Existing decks audited (extracted from `index.html`):

| Deck | Category tag | Records found | ID range |
|---|---|---|---|
| HSK 1 | `hsk1` | 150 | 1001–1150 |
| HSK 2 | `hsk2` | 151 | 1201–1351 |
| HSK 3 | `hsk3` | 301 | 1401–1701 |
| HSK 4 | `hsk4` | 600 | 1801–2400 |
| Original NUGGETS — `vocab` | `vocab` | 42 | 1–~140 |
| Original NUGGETS — `phrase` | `phrase` | 32 | (mixed) |
| Original NUGGETS — `particle` | `particle` | 31 | (mixed) |
| Original NUGGETS — `idiom` | `idiom` | 34 | (mixed) |
| Original NUGGETS — `concept` | `concept` | 16 | (mixed) |
| Original NUGGETS — `connector` | `connector` | 9 | (mixed) |

(Counts match the HSK build documentation. Strict regex extraction handled both single-quote and double-quote card formats and escaped apostrophes inside `english`/`semanticNote`.)

---

## 1. Hard duplicates (exact simplified form match)

Cross-referencing all 1,300 HSK 5 simplified words against every card across HSK 1, HSK 2, HSK 3, HSK 4, and original NUGGETS, **9 hard duplicates** were found. **Zero** of them collide with HSK 1–4. All 9 collide with the original NUGGETS deck.

| # | Simplified | Existing Deck | Existing ID | Existing Pinyin | Existing English | Existing POS / Depth | Notes |
|---|---|---|---|---|---|---|---|
| 1 | 哎 | NUGGETS `particle` | 145 | āi | hey / alas | particle / basic | Standard interjection. HSK 5 lists it for the same use. |
| 2 | 嗯 | NUGGETS `particle` | 134 | ng / ǹg | mm-hmm, uh-huh | particle / basic | Standard acknowledgment sound. Same sense as HSK 5. |
| 3 | 不得了 | NUGGETS `vocab` | 57 | bùdéliǎo | extremely, terribly, dreadfully, awfully | adv / intermediate | Same intensifier/exclamation sense. |
| 4 | 多余 | NUGGETS `vocab` | 34 | duōyú | superfluous | adj / basic | Same standard meaning. |
| 5 | 好奇 | NUGGETS `vocab` | 80 | hàoqí | curious, curiosity, inquisitive | adj / intermediate | Same standard meaning. |
| 6 | 进步 | NUGGETS `vocab` | 53 | jìnbù | progression, progress, advancement | noun / basic | Same standard meaning. |
| 7 | 夸张 | NUGGETS `vocab` | 77 | kuāzhāng | exaggeration, exaggerated, to boast | adj / basic | Same standard meaning. |
| 8 | 系统 | NUGGETS `vocab` | 33 | xìtǒng | system | noun / basic | Same standard meaning. |
| 9 | 自由 | NUGGETS `vocab` | 56 | zìyóu | freedom, liberty, free | noun / intermediate | Same standard meaning. |

### Cross-checks performed (and what they returned)

- **Simplified-vs-simplified across all 1,300 HSK 5 words:** 9 hits (above).
- **HSK 5 word against existing card's *traditional* form (in case HSK 5 source slipped in a traditional form somewhere):** 0 hits.
- **HSK 5 word against HSK 1 / 2 / 3 / 4 explicitly:** 0 hits.

### Single-character HSK 5 entries that already exist as standalone cards

Of HSK 5's 188 single-character entries, only **2** already exist as standalone cards in any existing deck:

- 哎 (NUGGETS particle, id 145)
- 嗯 (NUGGETS particle, id 134)

The remaining 186 single-char HSK 5 words are net-new at the standalone level (some appear as components of compound words in existing decks but never as their own card — those do **not** count as duplicates).

---

## 2. Soft duplicates / new sense at HSK 5

A "soft duplicate" would mean: same simplified form already exists, but the HSK 5 entry intends a meaningfully different sense, POS, or pronunciation (the way HSK 4 introduced 得 (děi, modal) on top of HSK 2's 得 (de, particle), or the way the brief raised 得 (dé, verb) as a possible HSK 5 case).

I went through each of the 9 hard duplicates and compared the existing card's `english` + `semanticNote` + `pos` against what HSK 5 standard usage targets for that word. **None of the 9 show a meaningfully different sense at HSK 5.** Each existing card already covers the meaning HSK 5 students will encounter:

- 哎 — HSK 5 uses it as the same calling-attention / sighing interjection. Existing note already says "Dual purpose: calling attention OR sighing." Covered.
- 嗯 — HSK 5 uses it as the same acknowledgment particle. Covered.
- 不得了 — HSK 5 uses the same intensifier sense. Covered.
- 多余 / 好奇 / 进步 / 夸张 / 系统 / 自由 — HSK 5 standard senses match the existing definitions exactly. No POS shift, no second pronunciation, no register change.

**No soft duplicates identified. No 得-style new-sense cases were found in the HSK 5 list against existing decks.**

(For full transparency: I scanned the HSK 5 source for the obvious historic-overload candidates that might come back at a higher level — 得, 着, 了, 过, 把, 地, 还 — and **none of them appear as standalone single-character entries in the HSK 5 source list**. So there is no recurring particle-vs-modal-vs-verb collision to design around for HSK 5.)

---

## 3. Decision matrix

For each hard duplicate, recommendation:

| # | Simplified | Existing card | Recommendation | Reasoning |
|---|---|---|---|---|
| 1 | 哎 | id 145 (particle) | **DROP from HSK 5 generation** | Existing card already covers the exact sense HSK 5 introduces. Generating a near-identical card adds noise. |
| 2 | 嗯 | id 134 (particle) | **DROP from HSK 5 generation** | Same as above. Nothing new at HSK 5. |
| 3 | 不得了 | id 57 (vocab) | **DROP, optionally NOTE-EXPAND** | Sense identical. Optional: tag id 57 with `alsoIn:["hsk5"]` so the HSK 5 deck surface still shows it. |
| 4 | 多余 | id 34 (vocab) | **DROP, optionally NOTE-EXPAND** | Same as above. |
| 5 | 好奇 | id 80 (vocab) | **DROP, optionally NOTE-EXPAND** | Same as above. |
| 6 | 进步 | id 53 (vocab) | **DROP, optionally NOTE-EXPAND** | Same as above. |
| 7 | 夸张 | id 77 (vocab) | **DROP, optionally NOTE-EXPAND** | Same as above. |
| 8 | 系统 | id 33 (vocab) | **DROP, optionally NOTE-EXPAND** | Same as above. |
| 9 | 自由 | id 56 (vocab) | **DROP, optionally NOTE-EXPAND** | Same as above. |

**KEEP-SEPARATE: 0 cards.**
**DROP (skip during HSK 5 generation): 9 cards.**
**NOTE-EXPAND (recommended treatment): all 9.** Add an `alsoIn:["hsk5"]` (or equivalent) tag to the existing NUGGETS cards so HSK 5 deck queries still surface them, without minting duplicate IDs in the 25xx range.

---

## 4. Summary numbers for the synthesizer

- HSK 5 source size: **1,300** words
- Hard duplicates with HSK 1: **0**
- Hard duplicates with HSK 2: **0**
- Hard duplicates with HSK 3: **0**
- Hard duplicates with HSK 4: **0**
- Hard duplicates with original NUGGETS (vocab/phrase/idiom/particle/concept/connector): **9**
- Soft duplicates / new-sense candidates: **0**
- Net-new cards to generate for HSK 5 if we DROP the 9 dupes: **1,291**
- Net-new cards if we KEEP every HSK 5 entry (parallel to HSK 4's "intentional duplicates" approach): **1,300** with 9 cross-deck pointers to existing NUGGETS cards.

### Comparison to the HSK 4 build

The HSK 4 build documented 12 intentional duplicates (2 with HSK 2, 10 with NUGGETS). HSK 5 lands at **9 with NUGGETS, 0 with HSK 1–4** — a slightly cleaner overlap profile. The 0-overlap with HSK 1–4 is the headline finding: HSK 5 vocabulary is genuinely additive over the standardized 1–4 deck.

### Risk callouts for downstream scouts / synthesizer

- Because all 9 collisions are with the *original* NUGGETS deck (not HSK 1–4), the dedup decision is a curatorial one about the NUGGETS deck's identity, not an HSK-progression-pedagogy one. If NUGGETS is meant to stay "pre-HSK / vibes deck", keeping the existing cards and skipping HSK 5 versions is cleaner.
- The HSK 5 source list contains **no** standalone entries for 得 / 着 / 了 / 过 / 把 / 地 / 还, so the HSK 4-style "modal vs particle" overload risk does not recur at HSK 5.
- One pinyin sanity check worth flagging: existing id 57 stores `búdéliǎo` (with `bú`), which is the spelled-out tone-sandhi form. Standard dictionary spelling is `bùdéliǎo`. Not a duplicate issue, but a normalization issue if the HSK 5 generator pulls dictionary pinyin and the deduper compares strings.

---

## 5. Method notes (so this is reproducible)

1. Extracted every card record from `index.html` with a Python regex tolerant of both `'`-quoted and `"`-quoted JS object literals, and of escaped quotes inside `english` / `semanticNote` (this matters: a naive regex misses ~30 cards including id 1032 没 because of `didn\'t`).
2. Wrote `(id, simplified, traditional, pinyin, english, category)` rows to a TSV.
3. Loaded the 1,300 HSK 5 simplified words from `data/hsk5-source-2012.txt`.
4. For each HSK 5 word, looked up `by_simplified` and `by_traditional` against the full card set.
5. For each hard hit, pulled the existing card's full sense fields (`english`, `pos`, `depth`, `semanticNote`) and compared against the standard HSK 5 sense to determine soft-dupe status.

Final counts (all 4 HSK decks): 150 / 151 / 301 / 600 = exactly the documented totals, confirming the extraction was complete.
