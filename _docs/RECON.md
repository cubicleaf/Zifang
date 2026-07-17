# 字坊 — RECON

**What this file is.** Empirical baseline of how Forge behaves *today* against the four ambiguity signals defined in [INTENT.md §9a.i](../INTENT.md). Each query was theorized to expose a gap. This doc records what actually happened.

**Methodology.** Each query is typed directly into Forge with default settings (Llama via Groq, Traditional default). The resulting card is captured. We note whether the current behavior matches the predicted failure mode, partially handles it, or unexpectedly handles it well.

**Why this matters.** Theory says these four signals are the highest-leverage heuristics. Evidence either confirms that or redirects the priority. Without recon, we'd be implementing fixes for failure modes that may not actually fail in practice.

Run date: _____ Provider: Llama 3.3 70B via Groq

---

## Signal 1 — Stranded verb / stative requiring a complement

**Prediction:** The prompt makes Forge generate a card with examples (which will naturally include the complement structure since you can't write a 2-sentence example without one). But `semanticNote` will probably treat the word as standalone — it won't *flag* that the word is incomplete without a complement. The card is technically correct but pedagogically misleading: the user learns the phrase but not that it's an obligatorily-bound construction.

**What to look for in each card:**
- Does `semanticNote` explicitly say "this needs a complement / is rarely used alone"?
- Do the 2 examples both use the complement structure? (They almost certainly will.)
- Does the card feel like a standalone unit or a fragment?

| # | Query | Card output (summary) | Flagged need for complement? | Verdict |
|---|---|---|---|---|
| 1.1 | 聞起來 | english="to hear, to sound" — **WRONG MEANING**. 聞 picked as "to hear, to listen" (standalone reading) instead of "to smell" (in-compound reading). Examples: "This news sounds very interesting" — incorrect; should be 聽起來 for that. semanticNote talks about "how something sounds or is perceived" — confident hallucination. | No — never says the word needs a complement. | **CRITICAL FAILURE**: not just stranded, the card is factually wrong. Combines Signal 1 (stranded) + Signal 4 (polysemous 聞) + unexpected Signal 5 (confident hallucination). |
| 1.2 | 看起來 | english="to seem, to appear" ✓ correct. Examples use complement structure. Components break out 看/起/來 separately. | No — semanticNote says "often followed by a clause" (soft mention, not flagged as obligatory). | OK card. Soft miss on stranded-verb flagging. |
| 1.3 | 覺得 | english="to feel, to think" ✓ correct. Examples good. semanticNote covers register (casual, softening). | No — but 覺得 takes a clause naturally, examples show this. Component for 得 wrongly glossed as "particle indicating completion of an action" (it's part of the verb juéde, not a particle). | OK card with a component error. Stranded-verb signal didn't surface in this query. |
| 1.4 | 變得 | english="to become, to turn into" ✓ correct. Examples good. semanticNote compares to 變化 — nice synonym call-out. | No. Component for 得 wrongly glossed as "to obtain, to get" (wrong reading dé instead of structural de). | OK card with a component error (same family as 1.3). Stranded-verb signal not surfaced. |

**Observed pattern:** _____

---

## Signal 2 — Homophone / homograph trap

**Prediction:** Forge will pick the dominant meaning and generate a card with no acknowledgement of the alternate. For 是/事 it will pick 是 (to be). For 的/地/得 it'll pick 的 (possessive). The user gets one card, never learns there was a fork in the road.

**What to look for:**
- Does the card pick the dominant meaning silently?
- Does `semanticNote` mention the homophone/homograph partner at all?
- If the user typed the "wrong" one (e.g. they meant 事 but typed 是), does the card mislead?

| # | Query | Card output (which meaning was picked) | Mentions alternate? | Verdict |
|---|---|---|---|---|
| 2.1 | 是 | "to be, yes, is" ✓ correct dominant pick. semanticNote covers copula usage well. | No mention of 事. | Predicted behavior — silent pick. |
| 2.2 | 事 | "matter, thing, affair" ✓ correct. semanticNote talks about formality. | No mention of 是. | Predicted behavior — silent pick. |
| 2.3 | 的 | "possessive particle, modifier" ✓ correct. **BUT examples have typo "我的的" / "她的的" — character repeated. semanticNote hallucinates particles "的了" and "的嗎" which don't exist.** | No mention of 地 or 得. | **FAILURE**: typo in examples + hallucinated particles. Three-de problem entirely missed. |
| 2.4 | 得 | dé "to obtain, to get" picked. The structural-particle de (most common usage) and the modal děi (must) are NOT mentioned. Pinyin/Chinese mismatch in example ("wǒ dé le xīn gōng zuò" but Chinese has 得到了 with 到). | No mention of 的 or 地. | **FAILURE**: picked the least-common reading; missed both polysemy and homophone family. |
| 2.5 | 再 | "again, once more" ✓ correct. Includes nice 又 disambiguation in semanticNote. | No mention of 在. | Predicted behavior — silent pick, but bonus 又 contrast surfaced. |
| 2.6 | 在 | "at, in, on, to be" ✓ correct. semanticNote slightly misleading (claims 在 is more formal/literary, actually it's everyday). | No mention of 再. | Mild semanticNote drift. |
| 2.7 | 做 | "to do, to make" ✓ correct. 制作/創造 disambiguation included. | **No mention of 作.** | Predicted behavior. |
| 2.8 | 作 | "to do, to make" ✓ correct. **DID mention 做 ("slightly more formal tone than the similar character 做").** | Yes — 做 mentioned by name. | **Partial pass**: asymmetric awareness — model knows 作 is the formal variant of 做, but not the reverse. |

**Observed pattern:** _____

---

## Signal 3 — Fragment of a fixed expression

**Prediction:** This is the most uncertain. Llama may or may not recognize a 2-character fragment of a famous chengyu. If it does, it might generate the card for the fragment with no mention of the longer phrase, or it might generate the card for the longer phrase silently, or it might do something weird. This signal has the highest variance.

**What to look for:**
- Does the card forge the *fragment* (the 2 chars literally) or the *full expression*?
- Does `semanticNote` mention the parent chengyu / set phrase?
- If it forges the fragment, is the card useful in its own right or just confusing?

| # | Query | Card output (fragment or full?) | Mentions parent expression? | Verdict |
|---|---|---|---|---|
| 3.1 | 一石 | headword 一石 / english "one stone" / pos "phrase" — but **both examples use 一石二鳥**. semanticNote mentions the chengyu by name. | Yes (semanticNote names 一石二鳥) but card is for the fragment. | **HYBRID FAILURE**: card claims to teach 一石 but actually teaches 一石二鳥 through examples. Pedagogically broken. |
| 3.2 | 半途 | headword 半途 / english "halfway, en route" — examples are about being interrupted midway (compatible with 半途而廢 but not exclusively). semanticNote doesn't name the chengyu but describes the meaning. | Indirectly — no chengyu named, but the framing leans toward the 半途而廢 sense. | Mixed: 半途 IS a real standalone word, so this is less broken than 3.1, but still leaks the chengyu meaning without disambiguation. |
| 3.3 | 畫蛇 | headword 畫蛇 / english "to draw a snake" / pos "idiom" — but **both examples use 畫蛇添足** and semanticNote describes the chengyu meaning ("trying to do something, but ends up making it worse"). | Yes (semanticNote describes 畫蛇添足's meaning) but card headword is the fragment. | **HYBRID FAILURE**: same as 3.1. Card teaches 畫蛇添足 via examples but headword/meaning is 畫蛇. |
| 3.4 | 狐假 | headword 狐假 / english "to feign, to pretend" / pos "verb" — but **both examples use 狐假虎威**. semanticNote describes the chengyu's meaning. | Yes by description, no by name. | **HYBRID FAILURE**: 狐假 alone has no meaning in Mandarin. Card invents one. |

**Observed pattern:** _____

---

## Signal 4 — Polysemous single character with divergent readings

**Prediction:** Forge will pick the dominant reading (cháng for 長, zhòng for 重, xíng for 行, de for 得, zhe for 著) and generate a card for that reading. `components[]` will have the picked reading. The other reading(s) will not be mentioned. This is the failure mode that prompted pending-queue item 5 (the HSK 5 components rule).

**What to look for:**
- Which reading does the card pick?
- Does the card mention the alternate reading(s) at all?
- Does `semanticNote` flag the polysemy?

| # | Query | Reading picked | Mentions alternates? | Verdict |
|---|---|---|---|---|
| 4.1 | 長 | cháng "long, length, grow" picked. **But example 2 "他長得很高" is zhǎng (to grow tall) — pinyin even says "zhǎng de" — silently uses the other reading without flagging.** | zhǎng appears in example pinyin only; never named or explained. | **HYBRID FAILURE**: headword is one reading, example uses the other. Learner gets contradictory data within one card. |
| 4.2 | 重 | zhòng "heavy, serious, important" picked. **No mention of chóng (repeat, as in 重新/重複).** Example 1 has typo "zhēn" instead of "hěn" in pinyin. Example 2 "這個問題很重" not idiomatic (would be 嚴重). | No. | **FAILURE**: polysemy missed entirely; pinyin typo in example. |
| 4.3 | 行 | xíng "to walk, to go, to do" picked. **No mention of háng (row, line, profession — 銀行, 行業).** Example "我每天早上都會去行走" is non-idiomatic Mandarin. Pinyin "dū" wrong for 都 (should be dōu). | No. | **FAILURE**: polysemy missed; example phrasing awkward; pinyin error. |
| 4.4 | 得 | Already covered in 2.4 — picked dé reading; missed de (structural particle, most common) and děi (modal). | No. | (See 2.4) **FAILURE**: picked the least-common of three readings. |
| 4.5 | 著 | english "to wear, to put on" / pinyin "zhe" — **conflates three different readings**: zhe (aspect marker), zhuó (wear), zhù (famous/prominent). Example 1: 她著了一件紅色的衣服 — ungrammatical (should be 穿了 chuān-le). Example 2: 著名 with pinyin "zhe míng" — should be "zhù míng". | No — actively confused by them. | **WORST POLYSEMY FAILURE**: three readings collapsed into one card with internally contradictory data. Card is broken. |

**Observed pattern:** _____

---

## Synthesis (evidence-based, 2026-05-26)

### Which signal showed the largest gap between predicted and observed behavior?

**Signal 3 (chengyu fragments) — worst of the four.** Theory predicted three possible outcomes (forge fragment cleanly, silently substitute full chengyu, or do something weird). Reality: **all four queries produced "hybrid failures"** — cards with the *fragment as headword* and *chengyu examples in the body*. The model recognizes the chengyu connection but mishandles the unit boundary. Pedagogically these cards are broken: they claim to teach the fragment but actually drill the full chengyu through examples. The headword (e.g. 狐假) often has no standalone meaning in Mandarin — the card invents one.

**Signal 4 (polysemous single characters) — equally bad, possibly worse in scale.** Every single one of the five queries missed at least one major reading. The 著 card collapsed three different readings (zhe aspect marker, zhuó "wear", zhù "famous") into one internally contradictory card. The 長 card had the *headword* reading as cháng but *one example* silently uses zhǎng. These are not subtle nuance failures — these are cards that contradict themselves.

### Which signal turned out to be less of a problem than predicted?

**Signal 1 (stranded verbs) — 3 of 4 came back acceptable.** 看起來, 覺得, and 變得 all produced usable cards with correct meanings and natural-looking examples. The one catastrophic failure (聞起來) wasn't really a stranded-verb problem — it was a polysemy problem (聞 picked as "to hear" instead of "to smell"). The stranded-verb heuristic as originally designed (ask "what does it smell like?") wouldn't have caught 聞起來's actual failure mode anyway.

**Signal 2 (homophone trap) — mostly predicted "silent pick" behavior, which is less harmful than expected.** The user typed what they typed; a silent dominant-meaning pick is reasonable when the typed character is unambiguous. The 的 failure was really a hallucination problem (made-up particles, typos in examples), not a homophone problem. The 作 case was a partial pass — the model spontaneously contrasted with 做.

### Surprises — failure modes we did NOT predict

**1. Confident hallucination as a category of its own.** This wasn't on our list of signals. Multiple cards produced fluent, detailed-sounding `semanticNote` content that was factually wrong:
- 的 card: hallucinated "的了" and "的嗎" as Chinese particles (they don't exist as units).
- 聞起來 card: confidently defined as "to hear, to sound" with examples that would mislead any learner.
- 著 card: collapsed three readings into one with internally contradictory pinyin and Chinese.

The card schema has *no slot for uncertainty*. Every card looks equally authoritative. This is a higher-order problem than any of the four signals: even when the four signals are working, the model can still produce confident hallucinations on adjacent failure modes.

**2. Hybrid cards (header/body mismatch).** Both Signal 3 (chengyu fragments) and Signal 4 (polysemy) produced cards where the **headword/meaning** says one thing and the **examples** say another. This pattern wasn't in our heuristic design. It's not a single signal — it's a *consistency* failure that crosses signals.

**3. Pinyin/Chinese inconsistency in examples.** Multiple cards had pinyin that doesn't match the Chinese characters in the same example (重 had "zhēn" instead of "hěn"; 著 had "zhe míng" for 著名 which should be "zhù míng"; 行 had "dū" for 都 instead of "dōu"). This is a data quality failure independent of any semantic signal.

**4. 得 family components consistently mishandled.** Across multiple cards (覺得, 變得), the 得 character in the `components[]` array was glossed with wrong readings/meanings. This is the in-compound-reading-must-match-context problem from pending-queue item 5, surfacing in real time.

### Priority ranking after evidence (revised v1)

1. **Polysemy + hybrid card failures** — Cards that contradict themselves are the worst possible output. A learner who studies them internalizes wrong information confidently. THE highest priority.
2. **Confident hallucination** — Closely related to #1 but distinct. The model produces fluent wrong content with zero uncertainty markers. The card schema needs a way to express "I'm not fully confident about this" — or the prompt needs to refuse rather than hallucinate.
3. **Chengyu fragment recognition** — The model already recognizes fragments belong to chengyu. It just needs to be told to *ask* "do you mean [full]?" instead of forging the broken hybrid.
4. **Pinyin/Chinese consistency** — Mechanical validation step. Should be a hard rule + a post-generation check, not a heuristic.
5. **Components in-compound reading** — Already in pending-queue item 5. Recon confirms it's a real recurring problem.
6. **Stranded verbs (formerly Signal 1)** — Lower priority than initially weighted. 3 of 4 cases were fine. The one failure was a polysemy issue.
7. **Homophone disambiguation (formerly Signal 2)** — Lowest priority. Silent dominant-meaning pick is acceptable for many cases. The failures within this signal (的) were really hallucinations, not homophone issues.

### Heuristics to DROP from the v0 prompt

- **Stranded-verb-complement check** — Mostly handled by current prompt's example requirement. Doesn't address the actual failure mode (which was polysemy).
- **Homophone-pair disambiguation** — Acceptable as-is; rare to cause real harm when the user typed the character themselves. Revisit later.

### Heuristics to ESCALATE / REFINE for the v0 prompt

- **Single-character polysemy gate** — If the query is a single character known to have widely divergent readings (長, 重, 行, 得, 著, 著名 cases), return needsClarification. The current prompt picks one reading silently and frequently picks the wrong one for the context the user intends.
- **Chengyu fragment recognition** — If the query is a 2-character fragment of a known chengyu, return needsClarification asking if they mean the full form. The model already recognizes the connection; just route the recognition to a question instead of a broken card.
- **Headword/example consistency rule (NEW, not in original four)** — Add a hard rule to the prompt: the pinyin/reading of the headword character(s) MUST match the pinyin used for those same characters in every example. No silent reading-switches mid-card.
- **Pinyin/Chinese consistency rule (NEW)** — Every pinyin token in an example must correspond to the character at the same position in the Chinese. Add as a hard rule + consider a post-generation validation pass.
- **Hallucination guard (NEW, hardest)** — When the model would describe a feature, particle, or near-synonym, it must be one that actually exists. Hard to enforce in a prompt; may need a different mechanism (smaller, more focused generation prompts per field; or a confidence-flag field in the schema).

### What this means for the architecture decision in INTENT.md §9b

The layered-prompt architecture still holds. But the **L3 query-specific signals** layer should be re-scoped:
- Drop the original 4 signals as written
- Replace with: polysemy gate (single-char divergent readings), chengyu-fragment gate, and consistency rules (which are L0 universal, not L3 conditional)

The "ask one targeted question" framing from INTENT.md §9a is still right. The *questions* are different than we predicted. Update INTENT.md §9a.i to reflect what evidence says.
