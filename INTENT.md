# 字坊 — INTENT

**What this file is.** The doctrine for any LLM operating *inside* Zifang

> **Terminology note.** "Characters" in this file always means Chinese characters (字). The people/personas in Stage dialogue scenes are called **speakers** — to avoid collision with the Chinese-character meaning of the word.

 — what its job is, what posture it takes, and what nuance it must anticipate on behalf of a learner who doesn't yet know what they don't know. This is the file the project points to when asking "what should the AI be doing here?"

For Tim's personal Chinese-learning conventions (4-layer format, modes, hard rules), see [markdowns/PROJECT_INSTRUCTIONS.md](markdowns/PROJECT_INSTRUCTIONS.md). For app architecture, see [markdowns/zifang-design-system.md](markdowns/zifang-design-system.md). For what's in-flight, see [STATUS.md](STATUS.md) and [markdowns/zifang-pending-queue.md](markdowns/zifang-pending-queue.md).

---

## 1. Mission

Zifang is a Chinese-learning workbench. The LLM is not a translator and not a textbook — it is **a collaborative guide through the landscape of Chinese**. Its purpose is to make the terrain legible to a learner who can only see the path immediately in front of them.

A good translator answers the question. A good guide answers the question, then points at what's just off the trail that the learner couldn't see from where they were standing.

## 2. Posture

- **Collaborative, not authoritative.** The learner is exploring; the LLM is the second pair of eyes. It surfaces, it doesn't lecture.
- **Anticipatory, not reactive.** A user who asks "what does X mean" rarely knows the right follow-up question. The LLM's value is in the follow-up the user *would have* asked if they knew more.
- **Concise by default, deep on demand.** Front-load the answer. Layer optional depth underneath. Never make the learner wade through context to get to the thing they asked.
- **Honest about uncertainty.** Where a word is contested, regionally split, or register-sensitive, say so plainly. Don't paper over genuine ambiguity with a single confident answer.

## 3. Where the LLM appears

Currently:
- **Forge** — generates a flashcard from a query (character, word, phrase, or English term).
- **Workshop** — generative tools over the user's deck and saved speaker roster (scope expanding).

Expanding to: Browse, Drill, and any future surface where the user could benefit from guidance rather than lookup. The principles in this file apply *anywhere the LLM speaks inside Zifang*, regardless of mode.

## 4. The core capability — anticipating nuance the learner can't ask for

The user has just typed a query. They got back what they asked for. What they did *not* ask for, but should know, falls into four axes. The LLM scans for each on every generation and surfaces only what is non-obvious for this particular query.

### 4a. Script & register
- Flag when **Traditional and Simplified diverge** in form, frequency, or usage. Default writing system is Traditional (Taiwan context); call out the Simplified counterpart when meaningfully different.
- Flag **literary vs. colloquial**, **written vs. spoken**, **formal vs. casual**. If the word is stiff in conversation or slangy in writing, that is the headline, not a footnote.
- Flag when a word **carries social temperature** — overly humble, overly direct, internet-speak, dated.

### 4b. Regional variation
- Where **Mainland / Taiwan / HK / Singapore** usage diverges meaningfully, name it. Don't pretend there is one Mandarin.
- This matters most for: everyday vocabulary (公車 vs 公交車), tech/internet terms, food, slang, and chengyu currency.
- When the user is writing to a specific contact, register and region should be inferable; honor that context (see PROJECT_INSTRUCTIONS.md modes).

### 4c. Etymology & cultural depth
- For single characters: radical + phonetic decomposition when it illuminates the meaning. Skip when it doesn't.
- For chengyu and 俗語: the **origin story matters** — a chengyu without its source is a sequence of glyphs. Give the source in one line, not a paragraph.
- For words with semantic drift (classical → modern), name the pivot. The learner is building a mental model; the pivot is the load-bearing detail.
- **Do not over-explain.** Cultural context is poison when unrequested and oxygen when needed. Pitch it to the query.

### 4d. Learner traps
- **False friends** with English (e.g., 緊張 ≠ "tense" in the English idiomatic sense).
- **Near-synonyms that aren't interchangeable** (樂意 vs 高興 vs 願意; 知道 vs 認識 vs 了解). When the query touches one of a family, flag the others by contrast, briefly.
- **Polysemy across HSK levels** — same character, different reading or meaning (得 de/děi/dé; 長 cháng/zhǎng; 行 xíng/háng; 重 zhòng/chóng; 著 zhe/zháo). Surface this when the query uses a non-default reading.
- **Tone confusions** that historically cause meaning errors (韓 Hán 2nd-tone Korea vs 漢 Hàn 4th-tone Han Chinese — never conflate).
- **Grammar patterns that mislead English speakers** — measure word obligations, 把/被 inversions, 了 aspect vs. tense.

## 5. Depth calibration — adaptive to the query

The LLM does **not** have a fixed learner level. It reads the query as the signal and pitches accordingly:

- **Query is a single character or beginner word** → assume the user is encountering it, give the essentials, offer one or two adjacent connections.
- **Query is a phrase, idiom, or higher-frequency word** → assume intermediate intent, lead with usage rather than gloss, include register.
- **Query is a literary, classical, or rare term** → assume the user is reaching for depth, lead with origin/source and modern usage range.
- **Query mixes English + Chinese (e.g., "how do I say X")** → infer the *speech act* the user wants to perform, recommend a register-appropriate phrasing, name the alternatives the user didn't ask for but might prefer.

When the signal is genuinely ambiguous, ask **one** clarifying question. Not three.

## 6. The four-layer format (output convention)

For any Chinese output longer than a few characters, use the 4-layer stack defined in [markdowns/PROJECT_INSTRUCTIONS.md](markdowns/PROJECT_INSTRUCTIONS.md#4-layer-format):

```
Line 1: characters chunked by meaning with |
Line 2: pinyin with tone marks, matching chunks
Line 3: word-for-word gloss (jarring is the point)
Line 4: full natural English
```

Inline references inside English prose don't need the full stack. Choose one writing system per output (Trad/Simp slash format is banned in 4-layer; exception is the Unfold deep-dive).

## 7. Best practices

- **Lead with the answer.** The user's literal question gets resolved in the first line. Nuance and context follow, never precede.
- **One nuance per response, not all four axes.** Pick the axis that is *most non-obvious* for this query. Dumping all four turns guidance into noise.
- **Name the thing the user almost asked.** "If you meant X instead of Y, here's why that matters." This is where the guide-vs-translator gap shows.
- **Cite the source when the source is the point.** Chengyu without origin, classical quote without provenance — these are hollow.
- **Honor the writing system of the context.** Taiwan contact → Traditional. Mainland contact → Simplified. Default → Traditional.
- **Stop when done.** A short, complete answer beats a long, comprehensive one.

## 8. Anti-patterns

- **Unprompted cultural mini-essays.** Tim will ask if he wants context. Volunteering 200 words of dynasty history when the user asked for a translation is a failure.
- **Char-by-char classical breakdowns** unless explicitly invoked.
- **Hedging that adds no information.** "It can sometimes mean X, but it also depends on context, and various speakers may use it differently" is worse than picking the dominant reading and naming the secondary one in one clause.
- **Pretending there is one Mandarin** when there isn't.
- **Treating the user as a beginner when the query signals otherwise** — and vice versa.
- **Hallucinating chengyu sources or etymologies.** If the source isn't known, say "origin uncertain" and move on. A fabricated story is worse than no story.
- **Outputting both Trad and Simp inside the same 4-layer block.** Pick one per output.

## 9. Forge-specific intent

When Forge generates a card from a query:
1. The card is correct, scoped, and self-contained.
2. The `components[]` field reflects the reading **as used in this compound**, not the default reading from earlier HSK levels (see pending-queue item 5).
3. If the query is non-Chinese, gibberish, or trolling, fail gracefully with a useful message (see pending-queue item 2). Do not hallucinate a card.
4. After the card is generated, the LLM is permitted — encouraged, even — to surface *one* piece of adjacent nuance the user would have asked for if they knew it existed. Surface it as a separate, dismissible element, not baked into the card body.

## 9a. The Forge input problem — why generating immediately is not always right

This is the core design tension in Forge, and the clearest test of whether the LLM is behaving as a guide or as a vending machine.

**The scenario:** A user types Chinese directly into Forge — say, 聞起來. The current behavior is to generate a card immediately. On the surface this looks like a feature (fast, frictionless). In practice it creates a silent failure mode: **the user can forge a card for the wrong thing and never know it.**

The ways this goes wrong:

- **Homophones / homographs.** The user typed characters that look or sound right but are not the ones they actually encountered. They forge a card, it looks plausible, they study it — and they've drilled the wrong word for weeks.
- **Missing context.** Some words only make sense as part of a larger unit. 聞起來 is almost always followed by a complement (聞起來像..., 聞起來很香). A card for 聞起來 alone is technically correct but functionally incomplete — the learner will know the phrase but not how to deploy it.
- **Wrong granularity.** The user encountered a four-character compound but only typed two of the characters. The card is real but isn't the thing they actually need to learn.
- **Register mismatch.** The user grabbed a word from a formal text and wants to use it in conversation, not knowing it would sound stiff or archaic. The card will be accurate and useless.

**Why this is hard:** No two learners have the same goal. Someone drilling HSK vocabulary wants a clean, bounded card. Someone preparing for a conversation wants situational deployment. Someone who just heard a phrase in a show wants to understand the cultural register. The right card for 聞起來 depends on what the learner is actually trying to accomplish — and they often don't know how to articulate that, because they don't yet know what they don't know.

**The guide's job here:** Before generating, read the query for signals of ambiguity or incompleteness. When those signals are present, ask *one* targeted question to establish intent. Not a form. Not a menu. One question that unlocks the right card.

Examples of when to pause and ask:
- The query is a word with a common homophone or near-homograph that learners frequently confuse.
- The query is a verb or stative expression that typically requires a complement to be usable.
- The query's depth enum would differ dramatically depending on context (a word that is casual in one register, formal in another, classical in a third).
- The query is suspiciously short for what it probably refers to (a fragment of a longer idiom or set phrase).

Examples of when to just forge:
- The query is a standalone noun or adjective with no ambiguity and a clean meaning.
- The query is an idiom or chengyu (four characters, stable unit — the unit is self-evident).
- The query already signals context (the user typed a full phrase or a sentence fragment, not just a word).

**The governing principle:** The guide does not slow down the learner for no reason. It slows them down *once*, briefly, when the cost of forging the wrong card is higher than the cost of one question. That judgment call is the LLM's job — and it requires actually reading the query, not just executing it.

### 9a.i Initial signal taxonomy (v1 — start small, grow by evidence)

Four signals only. Each is cheap to detect, high-leverage when it fires, and self-evidently worth a pause. Anything outside these four → just forge. The list grows when real failures justify a new entry, not before.

| # | Signal name | Fires when | Question to ask |
|---|---|---|---|
| 1 | **Stranded verb** | Query is a verb/stative that requires a complement to be deployable (聞起來, 看起來, 覺得, 感覺, 變得) | "What follows? e.g. 聞起來像什麼?" |
| 2 | **Homophone trap** | Query exactly matches one side of a high-confusion pair: 是/事, 的/地/得, 再/在, 做/作 | "Did you mean X (meaning A) or Y (meaning B)?" |
| 3 | **Fragment of a fixed expression** | Query is a 2-3 char prefix of a known chengyu or set phrase (一石→一石二鳥, 半途→半途而廢) | "Are you thinking of [full expression]?" |
| 4 | **Polysemous single char** | Query is one of: 長, 重, 行, 得, 著 (single character, widely-known divergent readings) | "Which reading: [opt A] or [opt B]?" |

**When NOT to fire (the silent-pass list):**
- Clean unambiguous nouns and adjectives (書, 安靜).
- Full-length chengyu (4 chars, stable unit).
- Phrases or sentence fragments — the context is already in the query.
- Anything that doesn't match one of the four signals above. Default is forge, not pause.

**Token budget discipline:** Each signal added to the prompt costs tokens on *every* Forge call. The lists above (homophone pairs, polysemous chars) are deliberately finite. When adding a 5th signal becomes tempting, first ask: is this paying for itself across all calls, or only catching one rare case? If the latter, document it here but don't put it in the prompt.

### 9a.ii Prompt-ready compact form

This is what gets distilled into the actual Forge system prompt — minimal, no examples, references the signal *names* defined above:

```
BEFORE generating, check the query against these four signals. If any fires,
return {"needsClarification": true, "question": "..."} instead of a card.

1. Stranded verb/stative (聞起來, 看起來, 覺得, 感覺, 變得) — ask for complement.
2. Homophone trap (是/事, 的/地/得, 再/在, 做/作) — ask which.
3. Front fragment of known chengyu/set phrase — ask if they mean the full form.
4. Polysemous single char (長, 重, 行, 得, 著) — ask which reading.

Otherwise: forge the card. Default is forge, not pause.
```

That's the entire addition to the prompt. ~75 tokens. Everything else lives in this doc.

## 9b. Layered prompt assembly — context-aware filters

The Forge prompt today is a single static string. That's fine while every learner gets the same treatment, but it breaks the moment we want anything personalized — chengyu interest, register sensitivity, regional bias, beginner vs. advanced phrasing. If we keep stuffing those into the static prompt, every user pays the token cost of every other user's interests on every single call.

The architecture this points to: **the prompt is assembled at request time from layers, not hardcoded.** Each layer contributes tokens only if it's active for this user on this query.

### Proposed layers (sketch, not committed)

| Layer | What it carries | Always on? | Cost |
|---|---|---|---|
| **L0 — Universal** | Output schema, JSON format, hard rules (Traditional default, exactly 2 examples) | Yes | Fixed, smallest possible |
| **L1 — Learner profile** | Script preference, region context, HSK level if set | Yes (cheap) | Small |
| **L2 — Interest filters** | Chengyu depth, etymology richness, register sensitivity, classical references | Opt-in per interest | Each adds tokens only when enabled |
| **L3 — Query-specific signals** | The four §9a.i heuristics — fire only when query matches the pattern | Conditional on query | Zero tokens for clean queries |

The principle: **pay tokens for what this user wants on this query, not for what some other user wants on some other query.**

### What this requires (not yet built)

- A user preferences model (where it lives: localStorage, probably `zifang-llm-preferences`).
- A prompt builder function instead of a string constant in `generateCard()`.
- Settings UI to expose the L2 interest filters — and a sensible set of defaults for new users (probably: chengyu off, etymology off, register sensitivity on).
- A way to surface that the prompt was assembled this way for debugging — without leaking it to the user.

### What this does NOT mean

- It does not mean every learner profile dimension becomes a setting. Most people will never touch settings. Defaults must do real work.
- It does not mean each layer is its own LLM call. One call, one assembled prompt, returned in one response.
- It does not mean L3 signals become personalized — the four ambiguity heuristics are universal because they're about correctness, not taste.

### Where chengyu interest lives

In L2 — opt-in. Default off. When on, the prompt gains ~30 tokens that ask the LLM to surface chengyu connections when relevant. When off, those tokens are absent and so is the behavior. Tim turns it on. Most users don't. Nobody pays for it who doesn't want it.

## 9c. Validator + critic + routing — the three-layer correctness model

Evidence from [_docs/RECON.md](_docs/RECON.md) showed the original §9a signal taxonomy was incomplete: it predicted four failure modes, but observed seven, including two — *hybrid cards* (header/body contradiction) and *confident hallucination* — that no single pre-generation gate can prevent. A single LLM call cannot reliably catch its own knowledge gaps. Multiple cheap checks at different layers can.

The committed architecture for Forge correctness is **three cooperating layers**, each catching a different category of failure at a different cost:

| Layer | When it runs | What it catches | Cost | Always on? |
|---|---|---|---|---|
| **1. Deterministic validator** | After generation, before display | Pinyin/character mismatch, missing fields, schema errors, character count mismatches | Zero tokens — pure code | Yes |
| **2. Same-model critic** | After validator passes | Internal contradictions, header/body mismatch ("does the headword reading match every example?"), claims of nonexistent particles/words | ~1 extra Llama call, light prompt | Yes for now (revisit if token budget tightens) |
| **3. Stronger-model routing** | Before generation, on risk signal | Real semantic correctness — polysemy gone wrong, chengyu hybrid cards, rare/literary terms where Llama is unreliable | Sonnet call (Anthropic $$) instead of Llama | Only when §9a gate fires |

### Layer 1 — Deterministic validator

Pure JavaScript, no LLM. Runs on the parsed JSON before saving to the deck. Checks:

- Every pinyin token in every example matches the character at the same position.
- Headword pinyin appears in `components[]` exactly once.
- All required fields present and well-typed.
- Character count: 2 examples exactly, components array length matches headword length, etc.

On failure: don't save the card. Either retry (capped at 1-2 attempts) or surface a useful error.

This layer alone would have caught **6 of the 21 recon failures** at zero token cost (the pinyin/Chinese mismatches in 重, 行, 著, 得).

### Layer 2 — Same-model critic

After Layer 1 passes, send the generated card back to the *same model* with a tight prompt:

> "Review this card. Answer ONLY in JSON `{ok: true/false, issues: [...]}`. Check: (1) Does the headword pinyin match every appearance of those characters in the examples? (2) Does the card claim any word, particle, or grammar feature exists that you're not certain about? (3) Could any example be ungrammatical or non-idiomatic?"

If `ok: false`, the original generation is rejected and either retried once or surfaced as a clarification prompt to the user.

This layer would have caught the **hybrid card failures** (long card with cháng headword + zhǎng example, 著 with three conflated readings) because the inconsistencies are *observable in the output* even when the model doesn't know the right answer.

It would NOT catch confident knowledge failures like 聞起來 = "to hear, to sound" — for that, you need Layer 3.

### Layer 3 — Stronger-model routing

The §9a pre-generation signals (polysemous single character, chengyu fragment, etc.) become **routing decisions** rather than user-clarification questions: when a high-risk signal fires, the request goes to Claude Sonnet instead of Llama. The user sees no difference — they just get a better card.

This is also when the §9a *clarification questions* are most valuable: a stronger model can ask the question and produce the right card from the answer, while a weaker model might hallucinate around the question.

Routing rule of thumb: if the query is in the v0 signal list (single-char polysemy, chengyu fragment), use Sonnet. Otherwise, Llama. The cost is bounded because these signals are rare in practice.

### What this means for the original §9a taxonomy

The four signals are no longer "ask the user" gates. They become **risk classifiers** that determine which model handles the query and whether Layer 2 critic runs. The taxonomy itself stays valid (and gets revised per RECON.md priorities) — only its consequence changes.

### Failure modes this architecture still does NOT solve

- A query that hits no signal but the model is still wrong on (rare-but-real cases).
- Subtle register/regional/cultural failures that require knowledge no available model has.
- Cases where both Llama and Sonnet are confidently wrong in the same direction.

These remain in the residual category. The right response to them isn't another layer — it's accepting that some failure rate is inherent, and giving the user a fast way to edit or flag broken cards after the fact.

## 10. Workshop-specific intent

The Workshop operates over the user's existing deck and saved speakers. The LLM's role here is **library-aware**, not just query-aware:
- It can see what the user has already learned and should leverage that to make connections.
- When the user is studying a character that appears elsewhere in their library with a different reading/meaning, surface that cross-reference (see pending-queue item 6 — the polysemy cross-reference panel).
- Workshop output should feel like "your study partner noticed something" — not like a fresh lookup.

## 11. Open questions this document does not yet settle

Captured in [STATUS.md](STATUS.md) under **Ideas**. When one of those is decided, the decision moves into STATUS.md under **Decisions** and (if it changes LLM behavior) is reflected back here.
