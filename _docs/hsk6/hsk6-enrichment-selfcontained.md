**Document status: Archived — 2026-09-29.** Preserved for historical reference.

# HSK6 Enrichment — Self-Contained Continuation Prompt

**You are picking this up cold. This document contains everything you need. Read it fully before writing a single line of JSON.**

Last updated: 2026-05-20  
Progress: 1,110 / 2,500 cards enriched. 2,191 card-tasks remain.

---

## What you are doing

Enriching flashcards for a live Taiwanese Mandarin flashcard app (Zifang). The app uses a Supabase backend and a vanilla JS frontend (`index.html`). HSK6 has 2,500 cards. A "skeleton" card (bare: simplified, traditional, pinyin, english) must become a full learning card with part-of-speech, a semantic note, component breakdown, and two example sentences.

Every card you submit goes live to real learners. There is no staging environment. Structural errors cause silent blank rendering in the UI. Do not guess on format — the schema is exact.

---

## File map

```
/Users/cubicleaf/Documents/Chinese shit/
├── data/
│   ├── hsk6-skeleton.json       ← 2,500 bare cards — authoritative for id, traditional, pinyin
│   └── hsk6-enriched.json       ← 1,110 enriched cards — this is what you grow
├── upload-hsk6-enriched.js      ← pushes hsk6-enriched.json to Supabase (run at session end)
└── markdowns/
    └── hsk6-enrichment-selfcontained.md  ← this file
```

The two pipeline scripts live at `/tmp/` — write them to disk at the start of each session (code below).

---

## Step 0 — Write pipeline scripts to disk

At the start of every session, run these two blocks to create the scripts. They are idempotent.

### append_hsk6.py — for new full cards (Phase 2)

```python
#!/usr/bin/env python3
"""Validate and append HSK6 enriched cards to hsk6-enriched.json.
Usage: cat cards.json | python3 /tmp/append_hsk6.py
"""
import json, sys

ENRICHED_FILE = '/Users/cubicleaf/Documents/Chinese shit/data/hsk6-enriched.json'
SKELETON_FILE = '/Users/cubicleaf/Documents/Chinese shit/data/hsk6-skeleton.json'

skel         = json.load(open(SKELETON_FILE))
simp_to_id   = {c['simplified']: c['id']         for c in skel}
simp_to_trad = {c['simplified']: c['traditional'] for c in skel}
id_to_pinyin = {c['id']:         c['pinyin']      for c in skel}

new_cards    = json.load(sys.stdin)
existing     = json.load(open(ENRICHED_FILE))
existing_ids = {c['id'] for c in existing}

errors = []
for c in new_cards:
    if simp_to_id.get(c['simplified']) is None:
        errors.append(f"  '{c['simplified']}': not found in skeleton")
if errors:
    print("UNKNOWN SIMPLIFIED CHARS:"); print('\n'.join(errors)); sys.exit(1)

for c in new_cards:
    c['id']          = simp_to_id[c['simplified']]
    c['traditional'] = simp_to_trad[c['simplified']]
    sk_py = id_to_pinyin[c['id']]
    if sk_py and sk_py != c.get('pinyin', ''):
        if c.get('pinyin'):
            print(f"  PINYIN CORRECTED: {c['simplified']} {c['pinyin']} → {sk_py}")
        c['pinyin'] = sk_py

dupes = [c for c in new_cards if c['id'] in existing_ids]
if dupes:
    print(f"WARNING: {len(dupes)} dupes skipped: {[c['simplified'] for c in dupes]}")
    new_cards = [c for c in new_cards if c['id'] not in existing_ids]

combined = sorted(existing + new_cards, key=lambda c: c['id'])
with open(ENRICHED_FILE, 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)
print(f"Total: {len(combined)} cards. Added {len(new_cards)}.")
```

### patch_hsk6.py — for fixing existing partial cards (Phases 1a and 1b)

```python
#!/usr/bin/env python3
"""Patch existing HSK6 cards — add missing pinyin, second examples, etc.
Usage: cat patches.json | python3 /tmp/patch_hsk6.py

Input: array of {"simplified": "X", "patch": {"field": value, ...}}
For examples: supply the FULL examples array (both sentences).
"""
import json, sys

ENRICHED_FILE = '/Users/cubicleaf/Documents/Chinese shit/data/hsk6-enriched.json'

patches     = json.load(sys.stdin)
enriched    = json.load(open(ENRICHED_FILE))
simp_to_idx = {c['simplified']: i for i, c in enumerate(enriched)}

errors = []; patched = []
for p in patches:
    idx = simp_to_idx.get(p['simplified'])
    if idx is None:
        errors.append(f"  '{p['simplified']}': not in hsk6-enriched.json"); continue
    for field, value in p['patch'].items():
        enriched[idx][field] = value
    patched.append(p['simplified'])

if errors: print("ERRORS (skipped):\n" + '\n'.join(errors))
with open(ENRICHED_FILE, 'w', encoding='utf-8') as f:
    json.dump(enriched, f, ensure_ascii=False, indent=2)
print(f"Patched {len(patched)} cards: {patched[:10]}{'...' if len(patched)>10 else ''}")
```

**Write them to disk:**
```bash
# Paste the append_hsk6.py block above into a file:
python3 - << 'EOF'
# (paste append_hsk6.py content here)
EOF

# Or just write them directly — they're in this document.
```

---

## Step 1 — Run status check at session start

```bash
cd "/Users/cubicleaf/Documents/Chinese shit"
python3 - << 'EOF'
import json
skel     = json.load(open('data/hsk6-skeleton.json'))
enriched = json.load(open('data/hsk6-enriched.json'))
enriched_ids = {c['id'] for c in enriched}

single_ex   = [(c['id'], c['simplified']) for c in enriched if len(c.get('examples',[])) == 1]
empty_py    = list(dict.fromkeys(
    (c['id'], c['simplified']) for c in enriched
    for ex in c.get('examples',[]) if ex.get('chinese') and not ex.get('pinyin')
))
unenriched  = [c for c in skel if c['id'] not in enriched_ids]

print(f"Enriched:  {len(enriched)}/{len(skel)}")
print(f"Phase 1a — empty pinyin in examples: {len(empty_py)} cards")
print(f"Phase 1b — single example only:      {len(single_ex)} cards")
print(f"Phase 2  — unenriched skeleton:      {len(unenriched)} cards")
if unenriched:
    print(f"           IDs {unenriched[0]['id']}–{unenriched[-1]['id']}")
EOF
```

Expected output at this document's writing date:
```
Enriched:  1110/2500
Phase 1a — empty pinyin in examples: 140 cards
Phase 1b — single example only:      661 cards
Phase 2  — unenriched skeleton:      1390 cards
           IDs 6111–7500
```

**Always complete phases in order: 1a → 1b → 2.**

---

## The three phases

---

### Phase 1a — Fill empty pinyin (140 cards, IDs 5971–6110)

These cards have 2 examples with `chinese` and `english` but `pinyin: ""`. You must generate the correct pinyin for each sentence and patch it in.

**List the cards:**
```bash
python3 - << 'EOF'
import json
enriched = json.load(open('data/hsk6-enriched.json'))
for c in enriched:
    if any(ex.get('chinese') and not ex.get('pinyin') for ex in c.get('examples',[])):
        print(c['id'], c['simplified'])
        for ex in c['examples']:
            print(f"  CH: {ex['chinese']}")
            print(f"  EN: {ex['english']}")
EOF
```

**Example of what you'll see (card ID 5971):**
```json
{
  "simplified": "进而",
  "id": 5971,
  "examples": [
    {"chinese": "他學好了中文，進而開始研究日文。", "pinyin": "", "english": "He mastered Chinese and then began studying Japanese."},
    {"chinese": "公司擴大規模，進而進軍國際市場。", "pinyin": "", "english": "The company expanded its scale and then entered the international market."}
  ]
}
```

**Submission format (patch):**
```bash
cat << 'PYEOF' | python3 /tmp/patch_hsk6.py
[
  {
    "simplified": "进而",
    "patch": {
      "examples": [
        {"chinese": "他學好了中文，進而開始研究日文。", "pinyin": "Tā xué hǎo le zhōngwén, jìn'ér kāishǐ yánjiū rìwén.", "english": "He mastered Chinese and then began studying Japanese."},
        {"chinese": "公司擴大規模，進而進軍國際市場。", "pinyin": "Gōngsī kuòdà guīmó, jìn'ér jìnjūn guójì shìchǎng.", "english": "The company expanded its scale and then entered the international market."}
      ]
    }
  }
]
PYEOF
```

**Critical:** In Phase 1a, supply both example sentences with the SAME `chinese` and `english` as they exist — do not alter them. Only add the `pinyin`.

---

### Phase 1b — Add second examples (661 cards, IDs 5043–5726)

These cards have exactly 1 example. You must write a second, complementary example. The second example should contrast or extend the first — not repeat the same context.

**List the cards:**
```bash
python3 - << 'EOF'
import json
enriched = json.load(open('data/hsk6-enriched.json'))
for c in enriched:
    if len(c.get('examples',[])) == 1:
        print(c['id'], c['simplified'], '|', c['examples'][0].get('chinese','')[:35])
EOF
```

**Example of what you'll see (card ID 5043):**
```json
{
  "simplified": "包庇",
  "id": 5043,
  "pos": "v",
  "examples": [
    {"chinese": "他被指控包庇下屬。", "pinyin": "Tā bèi zhǐkòng bāobì xiàshǔ.", "english": "He was accused of covering up for his subordinates."}
  ]
}
```

**Submission format — supply BOTH examples (patch replaces the entire array):**
```bash
cat << 'PYEOF' | python3 /tmp/patch_hsk6.py
[
  {
    "simplified": "包庇",
    "patch": {
      "examples": [
        {"chinese": "他被指控包庇下屬。", "pinyin": "Tā bèi zhǐkòng bāobì xiàshǔ.", "english": "He was accused of covering up for his subordinates."},
        {"chinese": "警方懷疑有官員包庇這起詐欺案，正展開調查。", "pinyin": "Jǐngfāng huáiyí yǒu guānyuán bāobì zhè qǐ zhàqī àn, zhèng zhǎnkāi diàochá.", "english": "Police suspect an official covered up this fraud case and have launched an investigation."}
      ]
    }
  }
]
PYEOF
```

---

### Phase 2 — Enrich skeleton cards from scratch (1,390 cards, IDs 6111–7500)

These are bare skeleton cards. You generate all fields.

**List what's left:**
```bash
python3 - << 'EOF'
import json
skel = json.load(open('data/hsk6-skeleton.json'))
enriched_ids = {c['id'] for c in json.load(open('data/hsk6-enriched.json'))}
remaining = [c for c in skel if c['id'] not in enriched_ids]
for c in remaining[:30]:
    print(f"{c['id']}|{c['simplified']}|{c['traditional']}|{c['pinyin']}|{c['english']}")
EOF
```

**Submission format:**
```bash
cat << 'PYEOF' | python3 /tmp/append_hsk6.py
[
  {
    "simplified": "扩散",
    "pos": "v/n",
    "semanticNote": "To spread; proliferation — used for physical diffusion (heat, gas), epidemic spread, and abstract spreading of ideas or influence. 核擴散 (nuclear proliferation) is a politically charged Taiwan-relevant term given cross-strait tensions. In medicine: 癌細胞擴散 (cancer metastasis/spread). Distinct from 傳播 (broadcast, spread via communication) — 擴散 implies physical/spatial dispersal. 擴 means expand; 散 means scatter.",
    "components": [
      {"char": "扩", "pinyin": "kuò", "meaning": "expand; enlarge"},
      {"char": "散", "pinyin": "sàn", "meaning": "scatter; disperse; come apart"}
    ],
    "examples": [
      {"chinese": "颱風帶來的豪雨迅速向山區擴散。", "pinyin": "Táifēng dài lái de háoyǔ xùnsù xiàng shānqū kuòsàn.", "english": "The torrential rain brought by the typhoon rapidly spread toward the mountain areas."},
      {"chinese": "謠言一旦在網路上擴散，就很難控制了。", "pinyin": "Yáoyán yīdàn zài wǎnglù shàng kuòsàn, jiù hěn nán kòngzhì le.", "english": "Once a rumor spreads on the internet, it's very hard to control."}
    ]
  }
]
PYEOF
```

**Do NOT include** `id`, `traditional`, or the card-level `pinyin` — the append script pulls these from the skeleton automatically and will WARN you if they differ.

---

## The exact card schema

This is what a complete, correct card looks like. Every field is required for Phase 2. For Phases 1a/1b you are only patching the `examples` field.

```json
{
  "simplified": "扩散",

  // DO NOT SUBMIT THESE — auto-filled from skeleton:
  // "id": 6111,
  // "traditional": "擴散",
  // "pinyin": "kuòsàn",

  "pos": "v/n",

  "semanticNote": "To spread; proliferation — used for physical diffusion (heat, gas), epidemic spread, and abstract spreading of ideas or influence. 核擴散 (nuclear proliferation) is a politically charged Taiwan-relevant term given cross-strait tensions. In medicine: 癌細胞擴散 (cancer metastasis/spread). Distinct from 傳播 (broadcast, spread via communication) — 擴散 implies physical/spatial dispersal.",

  "components": [
    {"char": "扩", "pinyin": "kuò", "meaning": "expand; enlarge"},
    {"char": "散", "pinyin": "sàn", "meaning": "scatter; disperse; come apart"}
  ],

  "examples": [
    {
      "chinese": "颱風帶來的豪雨迅速向山區擴散。",
      "pinyin": "Táifēng dài lái de háoyǔ xùnsù xiàng shānqū kuòsàn.",
      "english": "The torrential rain brought by the typhoon rapidly spread toward the mountain areas."
    },
    {
      "chinese": "謠言一旦在網路上擴散，就很難控制了。",
      "pinyin": "Yáoyán yīdàn zài wǎnglù shàng kuòsàn, jiù hěn nán kòngzhì le.",
      "english": "Once a rumor spreads on the internet, it's very hard to control."
    }
  ]
}
```

---

## Rules — all enforced by the Verifier

These are not suggestions. Every card that fails any rule must be corrected before it touches the file.

---

### R1 — Example keys: EXACTLY `chinese`, `pinyin`, `english`

```json
// CORRECT
{"chinese": "...", "pinyin": "...", "english": "..."}

// WRONG — these key names break the live app silently
{"sentence": "...", "translation": "..."}
{"text": "...", "romanization": "...", "meaning": "..."}
```

**Why this matters:** The app at `index.html:9485` reads only `ex.chinese` and `ex.english`. Any other key names render as blank. This is the failure that caused 140 production cards to show nothing to users. The pipeline script does NOT check key names — the Verifier must.

---

### R2 — Exactly 2 examples per card

Not 1. Not 3. Exactly 2.

**Why this happened:** 661 cards were generated with 1 example and a second pass was never run. The pipeline accepted partial cards. The Verifier must reject any card where `examples.length !== 2`.

---

### R3 — `pinyin` non-empty in both examples

```json
// WRONG
{"chinese": "他學好了中文。", "pinyin": "", "english": "He mastered Chinese."}

// CORRECT
{"chinese": "他學好了中文。", "pinyin": "Tā xué hǎo le zhōngwén.", "english": "He mastered Chinese."}
```

**Why this happened:** One batch used the `sentence`/`translation` schema, which never included a pinyin key. When that schema was later corrected to `chinese`/`english`, the pinyin field was added as an empty string. 140 cards are still in this state.

---

### R4 — Traditional Chinese characters throughout

The `chinese` field in examples must use Traditional script — the standard in Taiwan.

**Specific traps:**

| Wrong (simplified/wrong variant) | Correct (Taiwan Traditional) |
|----------------------------------|-------------------------------|
| 于 (U+4E8E) | 於 (U+65BC) |
| 啓 (U+5553) | 啟 (U+555F) |
| 爱 | 愛 |
| 国 | 國 |
| 时 | 時 |

The 于/於 distinction is the most common failure — three production cards reached Supabase with 于 in the traditional field and all example sentences. When writing example sentences, never use mainland-simplified 于; always use 於.

---

### R5 — Apostrophes before a/e/o syllables

When a syllable beginning with **a**, **e**, or **o** follows another syllable without a separating space, insert an apostrophe before it.

```
WRONG       CORRECT
cóngér      cóng'ér       (从而)
fāngàn      fāng'àn       (方案)
liànài      liàn'ài       (恋爱)
rèài        rè'ài         (热爱)
yòuéryuán  yòu'éryuán    (幼儿园)
jìnér       jìn'ér        (进而)
píngān      píng'ān       (平安)
```

**Why this happened:** A model generating an entire batch never inserted apostrophes — it was a systematic artifact, not a one-off mistake. 11 HSK5 cards reached production this way. The Verifier must scan every pinyin character-by-character for this pattern: if a vowel (a, e, o) follows a consonant that begins a new syllable, there must be either a space or an apostrophe.

**Quick test:** Search each pinyin string for the regex `[āáǎàaēéěèeōóǒòo][āáǎàaēéěèeōóǒòo]` — two consecutive vowel-starting syllables without separation is always wrong.

---

### R6 — Heteronym pinyin format

When a word has two valid readings, the skeleton uses `reading1, reading2` (comma-space). Match it exactly.

```
WRONG       CORRECT
tǔ/tù       tǔ, tù
xuè/xiě     xuè, xiě
```

The `semanticNote` should explain which reading applies in which context.

---

### R7 — POS: short-form tokens, slash-separated, no spaces

**Canonical tokens:** `v` `n` `adj` `adv` `conj` `prep` `pron` `mw` `particle` `idiom` `phrase` `chengyu` `interjection` `num`

**Compound POS:** slash only, no spaces: `v/n`, `adj/adv`, `n/mw`

```
WRONG                  CORRECT
verb                   v
noun                   n
adjective              adj
verb / noun            v/n
noun, verb             n/v
adjective/adverb       adj/adv
measure word           mw
verb phrase            phrase
```

**Why this happened:** Each enrichment session used its own prompt with different POS examples. No canonical list was enforced. This resulted in 126+ distinct POS forms across the database. Retrospective normalization has been applied to HSK1–5. Do not reintroduce long-form POS.

---

### R8 — Taiwan register in examples

Examples must reflect life in Taiwan, not mainland China. The learner is studying for Taiwan context.

**Use these:**
- Healthcare: 全民健保 (NHI), 健保卡, 掛號, 診所, 衛福部
- Education: 學測/GSAT, 指考, 大學聯考, 台大, 成大, 師大
- Transport: 高鐵 (HSR), 捷運/MRT, 公車, 機車 (not 摩托車)
- Food: 滷肉飯, 珍珠奶茶, 夜市, 廟口小吃, 雞排, 控肉飯, 刈包
- Places: 阿里山, 花蓮, 墾丁, 台南, 九份, 日月潭, 玉山
- Institutions: 台積電 (TSMC), 故宮博物院, 行政院, 總統府, 中央氣象局
- Culture: 廟會, 媽祖, 農曆, 元宵節 with 湯圓, 中秋節 with 月餅

**Avoid mainland defaults:**
- 地铁 → 捷運 (MRT)
- 普通话 → 國語 or 中文
- 高考 → 學測
- 人民币 → 台幣/新台幣
- 北京/上海 as generic city → 台北/台南/高雄

---

### R9 — semanticNote quality

The note must explain **what makes this word distinctive** — not restate the definition.

**Bad (restatement):**
> "擴散 means to spread or diffuse. It is used when something spreads from one place to another."

**Good (substantive):**
> "To spread; proliferation — covers physical diffusion (heat, gas, radiation), epidemic spread, and abstract spreading of ideas. 核擴散 (nuclear proliferation) carries political weight in the Taiwan context given cross-strait tensions. Distinct from 傳播 (disseminate via media/communication) — 擴散 implies physical spatial dispersal without a sender. In medicine: 癌細胞擴散 (cancer metastasis). The 擴 component means expand; 散 means scatter — together they convey 'expand by scattering.'"

**Checklist for a good semanticNote:**
- [ ] Distinguishes this word from close synonyms
- [ ] Notes register (formal, colloquial, written)
- [ ] Covers Taiwan-specific usage where applicable
- [ ] Flags heteronyms, false friends, or learner traps
- [ ] Mentions key collocations
- [ ] 80–200 words

---

### R10 — Components format

Each entry: `{"char": "X", "pinyin": "...", "meaning": "..."}` — all three keys, always.

```json
// CORRECT
"components": [
  {"char": "扩", "pinyin": "kuò", "meaning": "expand; enlarge"},
  {"char": "散", "pinyin": "sàn", "meaning": "scatter; disperse"}
]

// WRONG — missing pinyin
"components": [
  {"char": "扩", "meaning": "expand"}
]

// WRONG — wrong key name
"components": [
  {"character": "扩", "reading": "kuò", "gloss": "expand"}
]
```

---

## Multi-agent architecture

Run three agents per batch. Do not submit to the pipeline until the Verifier passes everything.

---

### Agent 1 — Generator

**Input:** a list of simplified characters (with their skeleton data) to enrich  
**Output:** raw JSON cards, unvalidated  
**Batch size:** 20–30 cards for Phase 2; 30–50 for Phases 1a/1b (those are simpler)

Provide the Generator with:
1. The skeleton entry for each card (id, simplified, traditional, pinyin, english)
2. This prompt's R1–R10 rules
3. The Taiwan register guidance from R8

---

### Agent 2 — Verifier

**Input:** Agent 1's JSON output  
**Output:** PASS/FAIL per card, with specific rule violations listed

**Verifier checklist — apply to every card, every time:**

```
For each card in the batch:

R1  □ examples array exists
R1  □ every example has EXACTLY these keys: chinese, pinyin, english
R1  □ NO key named: sentence, translation, text, romanization, meaning, or anything else
R2  □ examples.length === 2 (not 1, not 3)
R3  □ example[0].pinyin is non-empty string
R3  □ example[1].pinyin is non-empty string
R4  □ example[0].chinese uses Traditional characters
R4  □ example[1].chinese uses Traditional characters
R4  □ neither example contains 于 (U+4E8E) — must be 於 (U+65BC)
R4  □ neither example contains 啓 (U+5553) — must be 啟 (U+555F)
R5  □ scan each pinyin string: no two vowel-starting syllables adjacent without apostrophe or space
    (regex: look for patterns like ér, àn, ài, ān, ōu where first char has no apostrophe before it)
R6  □ if card has multiple readings: pinyin uses "x, y" format (comma-space), not "x/y"
R7  □ pos contains only canonical tokens: v n adj adv conj prep pron mw particle idiom phrase chengyu interjection num
R7  □ pos uses slash only (no spaces around slash, no comma separator)
R7  □ pos contains no long-form token: not verb, noun, adjective, adverb, conjunction, preposition, pronoun, "measure word"
R8  □ at least one example references Taiwan context (not defaulting to 北京/上海/地铁/高考/普通话)
R9  □ semanticNote.length > 80 characters
R9  □ semanticNote does not merely restate the english definition
R10 □ components is non-empty array
R10 □ every component has char, pinyin, AND meaning keys
```

**Verifier output format:**
```
PASS: 扩散, 扩张, 喇叭, 来历

FAIL:
  蜡烛 — R3: example[1].pinyin is empty
  来临 — R5: "lái'lín" — no apostrophe needed here (lín does not start with a/e/o); but "jìnér" → "jìn'ér" in example[0]
  老练 — R7: pos is "adjective" — must be "adj"
  乐器 — R8: both examples reference 北京音樂廳 — replace with Taiwan venue (e.g. 國家音樂廳)
  老化 — R9: semanticNote is 22 chars — too short, must be substantive
```

---

### Agent 3 — Corrector

**Input:** Agent 1's full JSON + Agent 2's FAIL list  
**Output:** corrected JSON for the failed cards

The Corrector makes **targeted surgical fixes** to flagged issues only — it does not regenerate the entire card. This preserves correct content while fixing specific failures.

After correction, pass only the corrected cards back to the Verifier. Iterate until all cards pass.

**Why a Corrector rather than regenerating:** Regeneration risks introducing new errors in content that was already correct. A targeted fix addresses exactly what the Verifier flagged without touching anything else.

---

## Uploading to Supabase

After each enrichment session:

```bash
cd "/Users/cubicleaf/Documents/Chinese shit"
node upload-hsk6-enriched.js
```

This script reads `data/hsk6-enriched.json` and upserts to Supabase with `resolution=merge-duplicates`. Safe to rerun at any time. Run it after every session.

---

## What went wrong in previous sessions — root causes

Understanding these failures is how you avoid repeating them.

### Failure 1 — Schema split (140 cards, currently blank in the app)

**What happened:** IDs 5971–6110 use `sentence`/`translation` keys instead of `chinese`/`english`.  
**Root cause:** A mid-project session changed the prompt template without checking what key names the app expected. The pipeline script validated simplified chars and pinyin but never checked example key names. Cards passed the pipeline and were uploaded.  
**Impact:** 140 cards render completely blank in the live app right now. The schema fix (renaming the keys) has been applied to the local file — but `pinyin` was never generated for this batch because the old schema didn't include it. Phase 1a fixes the pinyin.  
**Prevention:** R1. Verifier rejects any example without exactly `{chinese, pinyin, english}`.

### Failure 2 — Missing apostrophes (11 HSK5 cards in production)

**What happened:** `cóngér` instead of `cóng'ér`, `fāngàn` instead of `fāng'àn`, etc.  
**Root cause:** The model generating that batch simply never inserted apostrophes. The rule was not in the prompt, and neither the pipeline script nor any downstream process checked for it. Systematic — every eligible word in that batch was wrong.  
**Impact:** Pinyin is technically incorrect; syllable boundaries are ambiguous.  
**Prevention:** R5. Verifier scans every pinyin string.

### Failure 3 — 661 single-example cards

**What happened:** Cards IDs 5043–5726 have only 1 example each.  
**Root cause:** The first-pass enrichment generated 1 example per card. A second-pass run was planned but never executed. The pipeline accepted 1-example cards without complaint.  
**Prevention:** R2. Verifier rejects any card where `examples.length !== 2`.

### Failure 4 — 于 contamination (3 cards in production)

**What happened:** IDs 5735, 5861, 5922 — traditional field and example sentences contain simplified `于` instead of Traditional `於`.  
**Root cause:** LLMs default to mainland norms. 于 and 於 are homophones. Without explicit instruction to use 於, the model chose the simplified-adjacent form.  
**Prevention:** R4. Verifier checks for U+4E8E (于) in every Chinese field.

### Failure 5 — POS fragmentation (normalized, but do not reintroduce)

**What happened:** 126+ distinct POS forms — `verb`, `v`, `verb / noun`, `v/n`, `noun,verb`, etc. — accumulated across enrichment sessions.  
**Root cause:** No canonical list was enforced. Each session's prompt used its own examples.  
**Impact:** App cannot filter or display POS consistently. This has been normalized for HSK1–5.  
**Prevention:** R7. Verifier rejects any long-form or improperly formatted POS token.

### Failure 6 — Sense-priority drift (5 confirmed HSK6 cards, not yet fixed)

**What happened:** The `english` field promotes a modern or figurative sense, dropping the HSK-source primary sense.  
**Root cause:** LLMs favor contemporary usage. Without an anchor to the HSK definition, the model chose the more salient modern meaning.  
**Affected cards:** IDs 5271 (澄清), 5121 (辩证), 5361 (大不了), 5631 (稿件), 5741 (寒暄). These need surgical `english` field edits — the definition should lead with what the HSK source says.  
**Prevention:** When enriching, always read the skeleton's `english` field first. The enriched `english` field should preserve the HSK sense as primary and can extend or clarify, but must not drop it.

---

## Quick reference — correct vs incorrect

```json
// ✓ CORRECT CARD
{
  "simplified": "包庇",
  "pos": "v",
  "semanticNote": "To shield from punishment; to cover up for someone — implies willful protection of wrongdoing. 包庇犯人 (shelter a criminal), 包庇下屬 (cover up for a subordinate). Carries a strongly negative connotation of complicity. Distinct from 保護 (protect, neutral) and 庇護 (shelter, can be neutral or positive — 庇護所 is a shelter/refuge). In Taiwanese political discourse, 包庇 appears frequently in corruption investigations involving 官商勾結 (collusion between officials and business).",
  "components": [
    {"char": "包", "pinyin": "bāo", "meaning": "wrap; include; cover"},
    {"char": "庇", "pinyin": "bì", "meaning": "shelter; shield; protect (from above)"}
  ],
  "examples": [
    {"chinese": "他被指控包庇下屬。", "pinyin": "Tā bèi zhǐkòng bāobì xiàshǔ.", "english": "He was accused of covering up for his subordinates."},
    {"chinese": "警方懷疑有官員包庇這起詐欺案，正展開調查。", "pinyin": "Jǐngfāng huáiyí yǒu guānyuán bāobì zhè qǐ zhàqī àn, zhèng zhǎnkāi diàochá.", "english": "Police suspect an official covered up this fraud case and have launched an investigation."}
  ]
}

// ✗ WRONG — fails R1 (schema), R2 (1 example), R7 (long-form POS), R9 (short note)
{
  "simplified": "包庇",
  "pos": "verb",
  "semanticNote": "Means to cover up for someone.",
  "components": [{"char": "包", "meaning": "wrap"}, {"char": "庇", "meaning": "shelter"}],
  "examples": [
    {"sentence": "他包庇了罪犯。", "translation": "He sheltered the criminal."}
  ]
}
```

---

## Session wrap-up checklist

Before ending any session:

```
□ All submitted cards passed Verifier (all R1–R10)
□ patch_hsk6.py / append_hsk6.py ran without errors
□ `node upload-hsk6-enriched.js` ran successfully
□ Status check script shows correct counts (run again to confirm)
□ Note the last card ID processed and the phase for next session's handoff
```
