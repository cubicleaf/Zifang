# SEED — for a fresh Opus instance

Copy everything below the `---` into the new Opus's first message. It's self-contained, assumes zero prior context, and tells the new instance exactly what to read, what to do, and what NOT to do.

---

## Mission

You are picking up work on **字坊 (Zifang)**, a Chinese-learning web app at `/Users/cubicleaf/Documents/Chinese shit/`. The owner is Tim — HSK 2-3 with rust, Taiwan-context (Traditional default), strong pinyin intuition, communicates directly and dislikes throat-clearing. He spent a previous session with another Opus instance designing the doctrine for how the LLM should behave *inside* the app. The doctrine is committed. Your job is to **implement what was designed**, in the order specified, starting with the lowest-cost highest-leverage layer.

Before doing anything else, **read these three files in order**:

1. `/Users/cubicleaf/Documents/Chinese shit/INTENT.md` — the LLM doctrine. Posture, nuance axes, the three-layer correctness model.
2. `/Users/cubicleaf/Documents/Chinese shit/STATUS.md` — locked-in decisions and open ideas, chronologically logged.
3. `/Users/cubicleaf/Documents/Chinese shit/RECON.md` — empirical evidence from 21 real queries against current Forge. This is the *source of truth* for current priorities — it supersedes the v1 taxonomy in INTENT.md §9a.i.

Do not respond to Tim until you have read all three. Do not summarize them back at him — he wrote/co-wrote them and knows what they say. Just confirm you've read them and ask what he wants to work on first.

## Critical context (in case the docs leave gaps)

- **The app is a single-file HTML at `index.html`** (~677KB, ~17,000 lines, vanilla JS, mobile-first). Tabs: Browse / Drill / Forge / Workshop.
- **Three LLM surfaces exist:**
  - Forge card generation — `generateNugget()` at line ~11329, with the sysPrompt as a string literal at line ~11377.
  - Workshop Stage dialogue — `buildStageSystemPrompt()` at line ~11909.
  - Workshop character/speaker enrichment — `buildCharacterEnrichmentPrompt()` at line ~12210.
- **"Speakers" not "characters"** for the people in dialogue scenes. "Characters" is reserved for 字 (Chinese characters). The UI was already renamed; preserve this in any new code/copy.
- **Default provider is Groq (Llama 3.3 70B)**, free tier — token budget matters. Anthropic Sonnet is the paid alternative and is reserved for high-risk queries (see Phase 3).
- **The current Forge prompt is one static string.** Recon evidence (RECON.md) showed this approach produces internally contradictory cards on polysemous characters, broken hybrid cards on chengyu fragments, and confident hallucinations on common particles. The architectural fix is documented in INTENT.md §9a, §9b, §9c.

## How Tim works (operating rules)

- **Confirm before speccing.** Find the existing prototype first. Don't redo design work.
- **STATUS.md is the running journal.** When a decision lands, you may add to it under "Decisions" with date + one-line why. When an idea surfaces, drop it under "Ideas." Never write to INTENT.md without explicit permission — that file is doctrine and changes need approval.
- **No throat-clearing.** Skip "Great question!", "I'd be happy to...", "Let me think about that...". Just answer.
- **Lead with the answer**, then nuance. Not the other way around.
- **Cite file paths and line numbers** when discussing code. Vague references waste his time.
- **Push back when you disagree** with him, but bring evidence. "I think you're wrong because X" beats silently complying.
- **Ask one targeted clarifying question** when truly ambiguous. Not a form, not three options. One question.
- **Don't commit to git without being asked.** Don't push to GitHub without being asked. The repo is `cubicleaf/Zifang` (public).

## The Game Plan — 4 phases, in order

This sequencing is non-negotiable unless Tim says otherwise. Earlier phases unblock later ones, and the cheapest highest-leverage work comes first.

### Phase 1 — Deterministic validator (Layer 1 of INTENT.md §9c)

**Why first:** Zero token cost. Pure JavaScript. Would have caught 6 of 21 recon failures by itself. No architecture refactor needed.

**What to build:**
- A `validateNugget(nuggetData)` function called in `generateNugget()` *after* JSON parse, *before* the localStorage save (currently around line 11450-11479).
- Returns `{ok: true}` or `{ok: false, issues: [...]}`.
- Checks to implement:
  1. **Required fields present:** traditional, simplified, pinyin, english, semanticNote, category, depth, pos, components, examples.
  2. **Examples count = exactly 2.** Not 1, not 3.
  3. **Each example has chinese / pinyin / english.**
  4. **Pinyin/character token alignment per example:** split the Chinese into characters (excluding punctuation), split the pinyin into tokens; counts must match. Each pinyin token should be a plausible reading of its paired character. (You can be strict on count, lenient on reading-match in v0 — the count check alone catches the recon failures.)
  5. **Components array length matches headword character count** (e.g. 聞起來 has 3 chars, so components should have 3 entries — or 2 if 起來 is treated as one unit; document the choice).
  6. **No character repetition in examples** (catch the "我的的" typo from recon row 2.3).
  7. **Pinyin uses tone marks, not tone numbers** (regex: no digits 1-4 immediately after pinyin letters).

**On failure:** Retry the generation ONCE with the issues in the user-message context. If it fails again, surface a graceful error to the user ("Forge couldn't produce a clean card — try a different query or be more specific"). Don't save broken cards.

**Acceptance:** Run the 21 RECON.md queries against the validator. The 6 failures it should catch (pinyin typos in 重/行/著/得, character-repetition in 的, etc.) must now either produce clean cards on retry or fail gracefully.

### Phase 2 — Refactor static prompt → assembled prompt (INTENT.md §9b)

**Why second:** Required infrastructure for Phase 3 (you can't route to Sonnet on risky queries without a prompt builder). Also future-proofs personalization without bloating the universal prompt.

**What to build:**
- Replace the string literal at line ~11377 with `function buildForgePrompt({query, provider, userPrefs})`.
- Layer 0 (Universal — always included): output schema, hard rules, the new consistency rules from Phase 1 (headword/example reading must match, no character repetition, pinyin tokens must match chars).
- Layer 1 (Learner profile): script preference (Traditional default), region (Taiwan default). Read from localStorage `zifang-llm-preferences`.
- Layer 2 (Interest filters): empty struct for now, ready for chengyu-depth opt-in later.
- Layer 3 (Query-specific signals): empty for now — wired up in Phase 3.

**Acceptance:** Behavior is unchanged from the current static prompt for default users. Token count of the assembled prompt is ≤ the current static prompt for default users.

### Phase 3 — Routing high-risk queries to Sonnet (INTENT.md §9a + §9c Layer 3)

**Why third:** Needs the prompt builder. Uses real Anthropic budget, so only for queries we know Llama gets wrong.

**What to build:**
- Pre-generation signal detector: a JS function that takes the query string and returns `{risky: true/false, reason: ...}`.
- Signals to detect (from revised RECON.md priorities):
  1. **Single-character polysemy** — query is exactly one of: 長, 重, 行, 得, 著 (start with this finite list; expand by evidence).
  2. **Chengyu fragment** — query is 2-3 characters and matches the prefix of a known chengyu. Needs a chengyu list (Tim's `data/chengyu-collection.md` is a start).
- When risky: route to Sonnet (`claude-sonnet-4-6`) instead of Llama. User sees no UI difference — just a better card.
- Requires Anthropic API key to be set; if not set, fall back to Llama with a gentle in-card note that the result may be less reliable.

**Acceptance:** Forge 長, 著, 一石, 狐假 in real Forge. The cards produced should not have the hybrid/contradictory failures observed in RECON.md.

### Phase 4 — Same-model critic (INTENT.md §9c Layer 2)

**Why last:** Adds a second LLM call per card (doubles cost and latency). Only worth it once Phases 1-3 are confirmed working, so we know what residual failures the critic actually needs to catch.

**What to build:**
- After Layer 1 (validator) passes, send the card back to the same provider with a tight critic prompt: "Review this card. Answer ONLY in JSON `{ok: bool, issues: [...]}`. Check: headword pinyin matches every appearance in examples; no claims about words/particles you're uncertain exist; examples are grammatical and idiomatic."
- If `ok: false`, retry generation once with the critic's issues passed as context. If still fails, surface error.

**Acceptance:** Critic catches at least the hybrid-card failures from RECON.md (cháng/zhǎng mismatch in 長, three readings collapsed in 著) when they slip past Phases 1-3.

## Anti-patterns — do NOT do these

- **Do not "fix" the static Forge prompt by adding more text to it.** Recon showed this approach is bankrupt — adding text without architecture makes the token budget problem worse without fixing correctness. The fix is the three-layer model, in the order above.
- **Do not skip Phase 1.** Layer 1 (the validator) is the highest leverage work available. Phase 2-4 are larger refactors. Don't be tempted by the more "interesting" architectural work first.
- **Do not implement Phase 3 without Phase 2.** Routing logic without a prompt builder means duplicating prompt strings, which is exactly the static-string problem with one more copy.
- **Do not update INTENT.md without asking Tim.** That file is doctrine. STATUS.md is yours to journal in.
- **Do not commit or push to GitHub** unless Tim explicitly says so.
- **Do not redo the design.** The doctrine is settled. If you think a decision is wrong, raise it once, with evidence, then move on if Tim disagrees.
- **Do not assume which phase to start.** Read the docs, then ask Tim where he wants to start. The plan above is the recommendation, not the law.
- **Do not waste tokens describing your plan back to him.** Just start working, narrate as you go, ask when blocked.

## When you're done with Phases 1-4

Look at STATUS.md → Ideas section. There are several open architectural questions that the four phases don't address:

- "One adjacent nuance" Forge output slot (INTENT.md §9 item 4).
- Polysemy cross-reference panel (pending-queue item 6).
- Contact-context inside Forge (does Forge need to know who the user is writing to?).
- Adaptive depth feedback loop (does the LLM know if it pitched right?).
- Forge input validation for English/gibberish (pending-queue item 2).

Don't start on these without Tim's explicit go-ahead. They're not yet decided.

## Final note

The previous Opus and Tim spent serious time getting the doctrine right. The hard part — what the LLM should *do* and *why* — is done. Your job is the building part. Be parsimonious with prompt tokens, ruthless about anti-patterns, and direct in conversation. When in doubt, ask one question. When confident, just build.
