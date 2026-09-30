**Document status: Archived — 2026-09-29.** Preserved for historical reference.

# HSK6 Enrichment — Continuation Prompt
**Last updated:** 2026-05-20  
**Status:** 1,110 / 2,500 cards enriched. 2,191 card-tasks remain across three phases.

---

## What this project is

A Zifang flashcard app (index.html + Supabase backend) for learners of **Traditional Chinese as used in Taiwan**. Each deck covers a vocabulary level (HSK 1–6). The HSK6 deck has 2,500 cards. Cards are enriched from a bare skeleton (simplified, traditional, pinyin, english) into full learning cards with POS, semantic notes, components, and two example sentences.

The app is live. Every field submitted becomes immediately visible to learners. Errors are not hypothetical — they show up as blank rendering, wrong characters, or misleading definitions.

---

## Files you need

| File | Path | Purpose |
|------|------|---------|
| Skeleton | `data/hsk6-skeleton.json` | 2,500 bare cards — authoritative for `id`, `traditional`, `pinyin` |
| Enriched (working file) | `data/hsk6-enriched.json` | 1,110 enriched cards — grow this |
| Append script | `/tmp/append_hsk6.py` | Validates + appends new full cards |
| Patch script | `/tmp/patch_hsk6.py` | Patches existing cards (second examples, missing pinyin) |
| Upload script | `upload-batch02.js` | Pushes hsk6-enriched.json to Supabase (run at end of session) |

**At the start of every session, run this status check:**
```python
python3 -c "
import json
skel = json.load(open('data/hsk6-skeleton.json'))
enriched = json.load(open('data/hsk6-enriched.json'))
enriched_ids = {c['id'] for c in enriched}
single_ex = [(c['id'], c['simplified']) for c in enriched if len(c.get('examples',[])) == 1]
empty_py = [(c['id'], c['simplified']) for c in enriched
            for ex in c.get('examples',[]) if ex.get('chinese') and not ex.get('pinyin')]
unenriched = [c for c in skel if c['id'] not in enriched_ids]
print(f'Enriched: {len(enriched)}/{len(skel)}')
print(f'Phase 1a — empty pinyin in examples: {len(set(c[0] for c in empty_py))} cards')
print(f'Phase 1b — single example: {len(single_ex)} cards')
print(f'Phase 2  — unenriched: {len(unenriched)} cards (IDs {unenriched[0][\"id\"]}–{unenriched[-1][\"id\"]} if any)')
"
```

---

## Remaining work — three phases in order

### Phase 1a — Fill empty pinyin in examples (140 cards, IDs 5971–6110)

These cards have 2 examples with `chinese` and `english` fields but `pinyin` is an empty string `""`. This happened because an earlier enrichment session used a schema that dropped pinyin. The pinyin must now be generated and patched in.

**How to identify them:**
```python
python3 -c "
import json
enriched = json.load(open('data/hsk6-enriched.json'))
for c in enriched:
    for ex in c.get('examples',[]):
        if ex.get('chinese') and not ex.get('pinyin'):
            print(c['id'], c['simplified'], '|', ex['chinese'][:30])
            break
"
```

**How to submit a pinyin patch:**
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

---

### Phase 1b — Add second examples to single-example cards (661 cards, IDs 5043–5726)

These cards have exactly 1 example. A second pass was never run on the early batches. Each card needs a second example sentence added (with `chinese`, `pinyin`, and `english`).

**How to identify them:**
```python
python3 -c "
import json
enriched = json.load(open('data/hsk6-enriched.json'))
for c in enriched:
    if len(c.get('examples',[])) == 1:
        print(c['id'], c['simplified'], '|', c.get('examples',[{}])[0].get('chinese','')[:30])
"
```

**How to submit a second-example patch:**
```bash
cat << 'PYEOF' | python3 /tmp/patch_hsk6.py
[
  {
    "simplified": "阿弥陀佛",
    "patch": {
      "examples": [
        {"chinese": "...(existing example)...", "pinyin": "...", "english": "..."},
        {"chinese": "...(new second example)...", "pinyin": "...", "english": "..."}
      ]
    }
  }
]
PYEOF
```

**Important:** When patching, you must include BOTH examples (the existing one AND the new one) — the entire `examples` array is replaced. First read the existing example from `hsk6-enriched.json` before patching.

---

### Phase 2 — Enrich skeleton cards from scratch (1,390 cards, IDs 6111–7500)

These cards are bare skeleton with no enrichment. Use the append script.

**Invocation pattern:**
```bash
cat << 'PYEOF' | python3 /tmp/append_hsk6.py
[
  {
    "simplified": "词",
    "pos": "n",
    "semanticNote": "...",
    "components": [{"char": "词", "meaning": "word; part of speech"}],
    "examples": [
      {"chinese": "...", "pinyin": "...", "english": "..."},
      {"chinese": "...", "pinyin": "...", "english": "..."}
    ]
  }
]
PYEOF
```

**Do NOT submit** `id`, `traditional`, or `pinyin` for the card itself — the script assigns them from the skeleton. (You do submit `pinyin` inside each example.)

---

## The complete card schema

```json
{
  "simplified": "进而",          // submitted — must match skeleton exactly
  // "id": DO NOT SUBMIT         // auto-assigned from skeleton
  // "traditional": DO NOT SUBMIT // auto-assigned from skeleton
  // "pinyin": DO NOT SUBMIT      // auto-assigned from skeleton (card-level)
  "pos": "conj/adv",             // submitted — see POS rules below
  "semanticNote": "...",         // submitted
  "components": [                // submitted
    {"char": "进", "meaning": "advance; enter"},
    {"char": "而", "meaning": "and; but; yet (connective particle)"}
  ],
  "examples": [                  // submitted — EXACTLY 2
    {
      "chinese": "他學好了中文，進而開始研究日文。",
      "pinyin": "Tā xué hǎo le zhōngwén, jìn'ér kāishǐ yánjiū rìwén.",
      "english": "He mastered Chinese and then began studying Japanese."
    },
    {
      "chinese": "公司擴大規模，進而進軍國際市場。",
      "pinyin": "Gōngsī kuòdà guīmó, jìn'ér jìnjūn guójì shìchǎng.",
      "english": "The company expanded its scale and then entered the international market."
    }
  ]
}
```

---

## Rules — every single one is enforced by the Verifier agent

### R1 — Example schema: EXACTLY these three keys
```json
{"chinese": "...", "pinyin": "...", "english": "..."}
```
**Never use** `sentence`, `translation`, or any other key names. The app at `index.html:9485` reads only `ex.chinese` and `ex.english`. Using the wrong keys causes silent blank rendering in the live app. This is the most impactful failure mode seen in production.

### R2 — Two examples, no exceptions
Every card must have exactly 2 example sentences. Not 1, not 3. The single-example failure across 661 cards happened because a second-pass run was skipped after the first batch — the pipeline did not validate counts at submission time.

### R3 — Pinyin in every example field
`pinyin` must be non-empty in every example. The 140 empty-pinyin cards happened because one enrichment session adopted the `sentence/translation` schema which never included a pinyin field. Even when the schema was fixed, pinyin remained empty. Always verify all three keys are populated.

### R4 — Traditional characters in all Chinese text
The `chinese` field in examples must use **Traditional Chinese characters** — the script used in Taiwan. The skeleton's `traditional` field is the canonical form for the headword. Examples should follow the same script throughout.

**Known trap:** 于 vs 於  
Use `於` (U+65BC), not `于` (U+65BC look-alike). Three cards (IDs 5735, 5861, 5922) reached production with simplified `于` slipping into traditional-script examples. Always use `於` in traditional-register text.

**Known trap:** 啓 vs 啟  
Use `啟` (U+555F). Both are valid traditional forms but `啟` is preferred in Taiwan and prevents string-match failures.

### R5 — Pinyin apostrophe rule
When a syllable beginning with **a**, **e**, or **o** follows another syllable (without a space separating them), insert an apostrophe:

| Wrong | Correct |
|-------|---------|
| cóngér | cóng'ér |
| fāngàn | fāng'àn |
| liànài | liàn'ài |
| rèài | rè'ài |
| yòuéryuán | yòu'éryuán |
| jìnér | jìn'ér |

11 HSK5 cards reached production with missing apostrophes. The model that generated them never inserted apostrophes — it was a systematic LLM artifact. The Verifier must check every pinyin string character by character.

**Exception:** Some multi-character words use a space instead of apostrophe (skeleton is authoritative for card-level pinyin — e.g., `téng ài`, `wò shǒu`). For example-level pinyin you write yourself, use apostrophes per the above rule.

### R6 — Heteronym format
When a word has two valid readings, format as: `tǔ, tù` (comma-space, both readings, matching skeleton's format). Never use slash: `tǔ/tù` is wrong.

### R7 — POS taxonomy (canonical short-form, no spaces)
Use only these base tokens: `v`, `n`, `adj`, `adv`, `conj`, `prep`, `pron`, `mw`, `particle`, `idiom`, `phrase`, `chengyu`, `interjection`, `num`

Combined POS: use slash, no spaces: `v/n`, `adj/adv`, `n/mw`  
Never use: `verb`, `noun`, `adjective`, `adverb`, `conjunction`, `preposition`, `pronoun`, `measure word`, `verb / noun`, `noun, verb`, or any variant with spaces around the slash.

### R8 — Taiwan register in examples
Examples must reflect life in Taiwan, not mainland China. Refer to:

**Institutions:** 全民健保 (NHI), 健保卡 (NHI card), 學測/GSAT, 指考, 高鐵 (HSR), 捷運/MRT, 台積電 (TSMC), 故宮博物院, 中央氣象局, 行政院, 勞動部  
**Culture:** 廟會, 夜市, 滷肉飯, 珍珠奶茶, 雞排, 虱目魚, 控肉飯, 刈包, 米粉  
**Geography:** 阿里山, 花蓮, 墾丁, 台南, 九份, 日月潭, 玉山  
**System:** 注音符號 (Bopomofo, not pinyin as primary), 身分證 (not 身份证), 健保 (not 医保)

Do NOT use: 普通话, 高考, 地铁 (use 捷運), 人民币, 北京, 上海 as default settings.

### R9 — semanticNote quality
The note should:
- Explain **what makes this word distinctive** — not just restate the definition
- Cover usage register (formal/colloquial/written), collocations, and nuance
- Note Taiwan-specific context where relevant (political sensitivity, local institutions, cultural connotations)
- Flag heteronyms, false friends, or common learner errors
- Be 80–200 words

Do NOT write: "This word means X. It is used in Y situations." That's a definition, not a semantic note.

### R10 — Components
Each component must have `char` (single character or morpheme) and `meaning` (a brief gloss in English — what that character contributes to the word's meaning). Do not include `pinyin` in components. 2–4 components is typical; single-character words have 1.

---

## Multi-agent architecture (recommended)

Run three agents per batch:

### Agent 1 — Generator
Receives: a list of simplified characters to enrich (or existing partial cards to complete)  
Produces: raw JSON cards matching the schema  
Batch size: 20–30 cards per run

### Agent 2 — Verifier
Receives: Agent 1's JSON output  
Task: Check every card against Rules R1–R10. For each card, output PASS or a specific list of failures. Do not guess — check mechanically.

**Verifier checklist (apply to every card):**
```
R1  □ examples use ONLY keys: chinese, pinyin, english (no sentence, no translation)
R2  □ examples array has exactly 2 items
R3  □ pinyin is non-empty in both examples
R4  □ chinese field uses Traditional characters; no 于 (use 於); no 啓 (use 啟)
R5  □ apostrophes present before a/e/o syllables (scan each pinyin string)
R6  □ heteronym pinyin uses "tǔ, tù" format (comma-space), not slash
R7  □ pos uses only canonical short-form tokens, no spaces around slash
R8  □ examples reference Taiwan context (not mainland-default institutions/geography)
R9  □ semanticNote is substantive (not a restatement of the definition); 80+ words
R10 □ components array is non-empty; each item has char + meaning (no pinyin key)
```

Output format:
```
PASS: 进而, 进攻, 进化
FAIL:
  进展 — R3: pinyin empty in example 2; R5: "jìnér" missing apostrophe → "jìn'ér"
  近来 — R8: example references 北京 — use Taiwan context instead
```

### Agent 3 — Corrector
Receives: Generator's JSON + Verifier's FAIL list  
Task: Fix every flagged issue. Re-submit to Verifier. Only cards with PASS on all rules are sent to the pipeline.

**Why a Corrector instead of regenerating:** Regeneration risks introducing new errors. The Corrector makes targeted surgical fixes — it knows exactly what's wrong (from the Verifier) and can address each issue without touching what's already correct.

---

## What went wrong in previous sessions — and why

### 1. Schema split (silent, catastrophic)
**What:** IDs 5971–6110 use `sentence`/`translation` keys instead of `chinese`/`english`.  
**Why:** A session changed the prompt template and used different key names. The pipeline script did not validate example keys, so invalid cards passed through silently.  
**Impact:** 140 cards render completely blank in the live app right now.  
**Fix:** Phase 1a above. Going forward: Verifier R1 catches this before submission.

### 2. Missing apostrophes in pinyin (systematic LLM artifact)
**What:** 11 HSK5 cards have pinyin like `cóngér`, `fāngàn` instead of `cóng'ér`, `fāng'àn`.  
**Why:** The model that generated those cards never inserted apostrophes before a/e/o syllables. It wasn't told to. The rule was absent from the prompt.  
**Impact:** Pinyin is technically wrong — learners mispronounce or misparse syllable boundaries.  
**Fix:** R5 in every prompt and Verifier checklist.

### 3. 661 single-example cards
**What:** Cards IDs 5043–5726 have only 1 example each.  
**Why:** The second-example pass was simply never run on the early batches. The enrichment pipeline accepted 1-example cards without complaint.  
**Fix:** Phase 1b above. Going forward: Verifier R2 rejects any card with ≠ 2 examples.

### 4. 于 contamination in traditional-script examples
**What:** Three cards used mainland `于` instead of Taiwan `於` in both the `traditional` field and example sentences.  
**Why:** LLMs default to mainland Chinese norms when not explicitly instructed. 于 and 於 are homophones and the model chose the simplified-friendly form.  
**Fix:** R4 in every prompt and Verifier.

### 5. POS taxonomy fragmentation (126+ distinct forms)
**What:** POS values varied wildly — `verb`, `v`, `verb / noun`, `v/n`, `noun,verb`, `adjective/verb`, etc. — across decks.  
**Why:** Each enrichment session used its own prompt with its own POS examples. No canonical list was enforced.  
**Impact:** The app likely can't display POS consistently; any POS-based filtering is broken.  
**Fix:** R7. This has been retrospectively normalized across HSK1–5 in Supabase.

### 6. Sense-priority drift (medium priority, 5 confirmed cards)
**What:** The `english` field promotes a modern/figurative sense at the expense of the HSK-source primary sense.  
**Why:** LLMs tend toward contemporary usage. The model wasn't told to anchor to the HSK source definition.  
**Impact:** Misleads HSK exam students who need the tested sense.  
**Cards:** 5271 澄清, 5121 辩证, 5361 大不了, 5631 稿件 — surgical `english` field edits needed.

---

## Uploading to Supabase

After each enrichment session, push the updated file:
```bash
cd "/Users/cubicleaf/Documents/Chinese shit"
node upload-batch02.js
```

The upload script reads `data/hsk6-enriched-batch-02.json`. **After consolidating to `hsk6-enriched.json`, you should update `upload-batch02.js` to point to `data/hsk6-enriched.json` instead**, or create a new `upload-hsk6-enriched.js`.

The upload uses `resolution=merge-duplicates` — safe to rerun at any time.

---

## Batch size guidance

- **Phase 1a (pinyin patches):** 20–40 cards per batch — fast, mechanical
- **Phase 1b (second examples):** 15–25 cards per batch — read existing example first, write complementary second
- **Phase 2 (full enrichment):** 20–30 cards per batch — full cognitive load

Start each session by running the status check script above to confirm where you are.
