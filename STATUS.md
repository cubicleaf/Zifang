---
attention: Active
state: Live
form: Website
updated: 2026-07-31
live_url: null
---

# 字坊 — STATUS

**What this file is.** A living scratchpad of *decisions* Tim has made about Zifang and *ideas* he's had but not yet acted on. Distinct from [markdowns/zifang-pending-queue.md](markdowns/zifang-pending-queue.md) (which is the feature backlog) — this file is the higher-level "where is my head on this project."

**How to use it.**
- When a decision lands, add it to **Decisions** with the date and a one-line "why."
- When an idea surfaces, drop it in **Ideas** even if half-formed. The point is to externalize it before it evaporates.
- When an idea matures into a decision, move it. When a decision is superseded, strike it through and note what replaced it.
- Reference [INTENT.md](INTENT.md) for LLM doctrine, the pending queue for backlog, [markdowns/zifang-design-system.md](markdowns/zifang-design-system.md) for architecture.

**Last updated:** 2026-07-31

## Where I left off

HSK6 enrichment is **complete and live**: all 2500 cards (IDs 5001–7500) are enriched in `data/hsk6-enriched.json`, zero R1–R10 errors, zero gaps. Uploaded to Supabase via `node upload-hsk6-enriched.js` — all 2500 upserted successfully. The live app is now serving the finished dataset.

## Back Burner

- <!-- bb:forge-validator --> Forge correctness layers (per 2026-05-26 decision): Layer 1 deterministic validator first (free, biggest mechanical-error catch), then same-model critic, then Sonnet routing

## Log

- 2026-07-31: Supabase admin-key hygiene cleanup is complete. Created an untracked project-root `.env`, moved the `service_role` credential out of `upload-*.js` and `migrate.js`, added loud missing-env failure guards to those scripts, and created `_meta/SECRETS-HYGIENE.md` so the procedure is actually documented. No public leak was found; no key rotation performed.
- 2026-07-12: The 2026-07-01 `service_role` "exposure" was investigated and is **not a public leak**: the scripts holding the admin key (`upload-*.js`, `migrate.js`) are **untracked and were never committed** to the public `cubicleaf/Zifang` repo (which tracks only `index.html`, carrying the public-by-design `anon` key). The latent risk — a stray `git add .` sweeping the secret scripts in — was closed by gitignoring `.env`/`upload-*.js`/`migrate.js`/`data/contacts.json`. The remaining work at that point was hygiene only, and it was completed on 2026-07-31.
- 2026-07-12: Investigated the 2026-07-01 `service_role` "exposure" — it is NOT public. The upload scripts and `migrate.js` that hold the admin key are untracked and were never committed (`git log --all` empty for them); the public repo tracks only `index.html`, which carries the `anon` key (public by design). Closed the latent risk by gitignoring `.env`, `upload-*.js`, `migrate.js`, and `data/contacts.json` so a stray `git add .` can't leak them. The hygiene guide now lives at `_meta/SECRETS-HYGIENE.md`.
- 2026-07-11: `tims-ux-playbook/SKILL.md` (which lived in this folder as a birthplace accident) is now DEPRECATED. The playbook's canonical home is `~/Documents/ux-playbook/` (canon/corpus split + generated skill). The local copy carries a deprecation banner; safe to archive/delete during the planned location cleanup. Zifang's own design docs (`markdowns/zifang-design-system.md` etc.) are unaffected.
- 2026-07-10: Reshaped to the two-axis STATUS format (SPEC-converged-v1 §2). Formatting migration only — `updated:` deliberately not bumped.
- 2026-07-15: Migrated the header from the retired `relationship / kind` pilot to the canonical `attention / state / form` schema. Zifang now reads as `Active / Live / Website`: a real deployed working surface, not just a prototype shorthand.

## Decisions

### 2026-07-31 — Supabase admin key moved into untracked `.env`
**What:** Removed the inline `service_role` credential from `migrate.js` and all `upload-*.js` scripts. Those local admin scripts now read `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from the untracked project-root `.env`, fail loudly if either is missing, and point to `_meta/SECRETS-HYGIENE.md` for the maintenance rule.
**Why:** The key was never publicly leaked, but leaving it inline in local scripts was bad hygiene and kept the project record stuck between "not urgent" and "not actually fixed."
**How to apply:** Keep the real values only in `.env`. Run the scripts from the project root. Rotate the key only if a real exposure is confirmed later.

### 2026-07-30 — Favicon built
**What:** Generated favicon.ico + 16/32/180/192/512 PNGs + site.webmanifest, saved to project root, link tags added to `index.html` `<head>`. Icon is a two-card "deck" shape in `--ink #2c2416` on `--rice #f5f0e8` — real tokens, kept light to match Zifang's actual paper-toned brand. Speech-bubble and ink-brush concepts were rejected as overclaiming capabilities Zifang doesn't have (no chat interface, no handwriting practice).
**Why:** Continuing the portfolio-wide favicon rollout (see `webdev/_docs/favicon-pipeline-STATUS.md`).
**How to apply:** Not yet committed/pushed — hard-refresh after deploy to confirm the tab icon updates.

### 2026-07-17 — Supporting Forge evidence and session seed moved under `_docs/`
**What:** Moved `RECON.md` and `SEED.md` from the project root to `_docs/`.
**Why:** RECON remains useful empirical evidence and SEED remains historical handoff context, but neither is a root-level source of truth for day-to-day Zifang work.
**How to apply:** Start with INTENT, STATUS, and the pending queue. Consult `_docs/RECON.md` when changing Forge correctness behavior; use `_docs/SEED.md` only as historical handoff material.

### 2026-07-15 — Zifang classification moved to the canonical attention/state/form schema
**What:** Replaced the old `relationship: Driving` / `kind: Prototype` header with `attention: Active`, `state: Live`, and `form: Website`.
**Why:** Zifang has a real working URL and is functioning as a live product surface. The older pilot vocabulary was mixing deployment reach and practical maturity in a way that no longer matches the canonical model.
**How to apply:** Treat Zifang as active live work unless the real commitment changes. Use `Dormant` only if known unfinished work is being neglected, not merely because the app goes quiet for a while.

### 2026-07-24 — HSK6 enrichment complete: all 2500 cards (IDs 5001–7500) done
This session (continuing directly after the 7280 checkpoint below) enriched the remaining cards 7281–7500 (11 batches of 20) in `data/hsk6-enriched.json`, adding `pos`, `semanticNote`, `components`, and `examples` for each, per the user's "run until you get stopped by the compute limit" instruction. Verified after every batch: zero R1–R10 rule violations. Final check confirmed 2500/2500 cards present, IDs 5001–7500, zero gaps, zero duplicates.
**Why:** Completes the multi-session HSK6 enrichment project started 2026-06-12.
**How to apply:** The enrichment project is fully done — `node upload-hsk6-enriched.js` was run this session, all 2500 cards upserted to Supabase, live app now serves the complete dataset. `/tmp/append_hsk6.py` will need to be rewritten again from `markdowns/hsk6-enrichment-selfcontained.md` if a similar bulk-JSON-append workflow is needed for a future dataset, since sandbox `/tmp` doesn't persist across sessions.

### 2026-07-24 — HSK6 enrichment continued to 7280 (IDs 6941–7280 complete, 340/560 cards this leg)
This session enriched cards 6941–7280 (17 batches of 20) in `data/hsk6-enriched.json`, adding `pos`, `semanticNote`, `components`, and `examples` for each. Verified after every batch: zero R1–R10 rule violations, checked programmatically batch by batch. Total 1900→2280.
**Why:** Continuing the multi-session HSK6 enrichment project toward ID 7500.
**How to apply:** 220 cards (7281–7500, ~11 batches) remain. Upload to Supabase (`node upload-hsk6-enriched.js`) was not run this session — still local-only; run it once enrichment reaches 7500 or whenever Tim wants the live app updated early.

### 2026-07-23 — HSK6 enrichment continued to 6940 (IDs 6901–6940 complete, 40/560 cards this leg)
This session enriched cards 6901–6940 (2 batches of 20) in `data/hsk6-enriched.json`, adding `pos`, `semanticNote`, `components`, and `examples` for each. Verified before/after: 1900→1940 total cards, zero R1–R10 rule violations on both batches (checked programmatically).
**Why:** Continuing the multi-session HSK6 enrichment project toward ID 7500.
**How to apply:** `/tmp/append_hsk6.py` and `/tmp/patch_hsk6.py` from prior sessions were gone (sandbox `/tmp` doesn't persist across sessions) — rewrote `append_hsk6.py` from the spec in `markdowns/hsk6-enrichment-selfcontained.md`, with one addition: it now also sets `category: "hsk6"` and `depth: "basic"` on each new card and pulls `english` from the skeleton, matching the actual schema found in existing cards (which the enrichment doc's schema section doesn't mention). Next session should rewrite the script the same way before continuing.

### 2026-07-01 — HSK6 enrichment continued to 6900 (IDs 6841–6900 complete, 60/600 cards this leg)
This session enriched cards 6841–6900 (3 batches of 20) in `data/hsk6-enriched.json`, adding `pos`, `semanticNote`, `components`, and `examples` for each. Verified before/after: 1840→1900 total cards, max ID 6840→6900, zero errors from `/tmp/patch_hsk6.py`.
**Why:** Continuing the multi-session HSK6 enrichment project toward ID 7500.
**How to apply:** 600 cards (6901–7500, ~30 batches) remain. Same judgment call as the 6500 session: kept skeleton's non-Taiwan-standard `traditional` field values untouched (e.g. 委托, 为难, 违背, 蔚蓝 stay as-is in the base record), but used Taiwan-standard forms (委託, 為難, 違背, 蔚藍) inside `components`/`examples`. At the time, `upload-hsk6-enriched.js` still held a plaintext `service_role` key and was flagged for cleanup. That hygiene fix was completed on 2026-07-31; the script was local/untracked, not a public repo leak.

### 2026-06-12 — HSK6 flashcard enrichment reached 6500 (IDs 5001–6500 complete, 1500/1500 cards)
This session enriched cards 6381–6500 (6 batches of 20) in `data/hsk6-enriched.json`, adding `pos`, `semanticNote`, `components`, and `examples` (Traditional Chinese, Taiwan-standard register) for each. Verified: 1500 total cards, IDs 5001–6500 present, no duplicates, no gaps.
**Why:** Continuing the multi-session HSK6 enrichment project (learner is Taiwan-based; all examples use 臺灣/軟體/員警-style Taiwan standard vocab, not Mainland forms).
**How to apply:** The skeleton (`hsk6-skeleton.json`) covers IDs up to 7500, so 6501–7500 (1000 cards, 50 batches of 20) remain to enrich next session. Continue using `/tmp/patch_hsk6.py` with the same patch-JSON workflow. Notable judgment calls made this session: kept skeleton's non-Taiwan-standard `traditional` field values (e.g. 屏幕, 啓, 爲, 锲而不舍→鍥而不捨) untouched, but used Taiwan-standard forms (螢幕, 啟, 為, 鍥而不捨) inside `components`/`examples`, flagging the discrepancy in `semanticNote` where relevant.

### 2026-05-25 — INTENT.md as the LLM doctrine doc
Created [INTENT.md](INTENT.md) at the project root. It defines what any LLM operating inside Zifang is supposed to do, its posture (collaborative guide, not translator), and the four nuance axes it must scan for (script+register, regional variation, etymology+cultural depth, learner traps).
**Why:** The LLM was doing useful work but the *intent* behind that work was undocumented — meaning every new surface or agent had to re-derive its posture from scratch. Project needed a single doctrine file to anchor it.

### 2026-05-25 — LLM depth is adaptive to the query
The LLM does not target a fixed learner level. It reads the query as the signal — single character vs. phrase vs. literary term vs. English-to-Chinese speech act — and calibrates depth accordingly.
**Why:** A fixed level (beginner, intermediate) would either patronize advanced queries or overshoot beginner ones. The query itself is the richest signal available; use it.

### 2026-05-26 — Forge correctness = three-layer validator + critic + routing
Committed architecture for Forge output correctness: (1) deterministic JS validator runs on every generation (catches pinyin/character mismatches, schema errors — zero token cost), (2) same-model critic runs after validator passes (catches internal contradictions like header/body reading mismatches — one extra Llama call), (3) §9a signal gates *route* high-risk queries to Claude Sonnet instead of Llama (catches semantic knowledge failures Llama can't catch in itself — Anthropic $$ only when needed).
**Why:** [_docs/RECON.md](_docs/RECON.md) evidence showed the original four pre-gen signals were incomplete — two major failure modes (hybrid cards, confident hallucination) can't be caught by a single LLM call no matter how good the prompt is. Cheap layered checks catch most of what one call can't.
**How to apply:** Documented in INTENT.md §9c. Implementation order: Layer 1 first (free, biggest mechanical-error catch), Layer 2 second (low cost, catches hybrid cards), Layer 3 last (requires routing logic + Anthropic key handling). The original §9a taxonomy is repurposed from "ask the user" gates to "route to Sonnet" classifiers.

### 2026-05-27 — Clarification UI added to Forge
When the model returns `needsClarification` JSON, Forge now shows the question + clickable reading/option chips in the status area instead of a parse error. User's selection routes back into `generateNugget()` with the chosen context as a clarification parameter. Button state managed across the retry cycle via `_forgeInRetry` flag to prevent flicker.
**Why:** Required JS infrastructure for the clarification gate to be usable. Without it, any `needsClarification` response silently failed.

### 2026-05-27 — Forge sysPrompt rewritten
Replaced static string with structured prompt: pre-flight clarification gate (polysemous single chars 長/重/行/得/著 + chengyu fragments → `needsClarification` JSON), 5 hard consistency rules (in-compound readings, one-to-one pinyin/char alignment, space-separated syllables, no invented particles, contradiction check), depth calibration by query type. Token cost ~839 vs ~400 previously — accepted for correctness gains confirmed by recon.
**Why:** Original prompt produced hybrid cards, wrong readings, hallucinated particles, and inconsistent pinyin. RECON evidence (21 queries) drove the rewrite.

### 2026-05-27 — Pre-flight gate moved to user message
The polysemy + chengyu fragment pre-flight check is now prepended to every user message, not just the system prompt.
**Why:** Llama follows user-turn instructions more reliably than instructions buried 500+ tokens into a system prompt. Gate was misfiring for 行 and 著 under the old architecture. ~25 extra tokens per call, worth it for gate reliability.

### 2026-05-27 — Phase 1 validator implemented
`validateNugget()` runs on every Forge generation before saving. Seven checks: required fields present, exactly 2 examples, each example has all three fields, pinyin token count matches character count (one space-separated syllable per character), components length = headword length, particle repetition typos, tone mark enforcement. On failure: one automatic retry with the specific issues injected into the user context; graceful error to user if retry also fails. Retry suppresses button flicker via `_forgeInRetry` flag.
**Why:** RECON showed 6/21 failures were catchable by pure JS at zero token cost. Validator is the scalable backstop for structural errors the prompt can't reliably prevent.

### 2026-05-26 — Recon evidence supersedes original §9a signal priorities
The four signals in INTENT.md §9a.i (stranded verbs, homophones, chengyu fragments, polysemous chars) were partly wrong. Recon priorities (revised): polysemy+hybrid cards #1, confident hallucination #2, chengyu fragment recognition #3, pinyin/Chinese consistency #4, in-compound 得 reading #5. Stranded verbs and homophones drop to #6 and #7.
**Why:** Empirical evidence from running 21 real queries through current Forge ([_docs/RECON.md](_docs/RECON.md)) revealed two failure categories (hybrid cards, confident hallucination) that weren't in the original taxonomy, and showed two of the original four signals are less harmful in practice than predicted.
**How to apply:** When implementing v0 of the pre-generation gates, use the revised priorities. INTENT.md §9a.i remains as written for now but should be updated to reflect evidence before any implementation.

### 2026-05-25 — Forge prompt becomes layered/assembled, not static
The Forge prompt will move from a single static string to a runtime-assembled stack of layers (L0 universal / L1 profile / L2 interests / L3 query-signals). Each layer contributes tokens only if active for this user on this query.
**Why:** Personalization without bloat. Tim cares deeply about chengyu; most users won't. A static prompt forces every user to pay for every other user's interests. Layered assembly means a user pays only for what they want on the query they're making.
**How to apply:** Future Forge work should not add to the static string. New behaviors get a layer assignment first, then live there. Documented in INTENT.md §9b.

### 2026-05-25 — "Speakers" is the term for Stage dialogue personas
The people/personas saved in Workshop's Stage tool are called **speakers**, not "characters." "Characters" is reserved for Chinese characters (字).
**Why:** Collision — "character" already means 字 everywhere else in the project. "Speakers" is already used internally (`stageState.speakers`) and is unambiguous.

### 2026-05-25 — LLM scope covers all surfaces where it speaks
INTENT.md applies anywhere the LLM appears in Zifang, not just Forge. Today that's primarily Forge & Workshop; the doctrine is written to extend cleanly into Browse, Drill, and future surfaces.
**Why:** Tim said this scope explicitly. Avoids the doctrine fragmenting per-surface as the app grows.

### (Pre-existing — captured here for completeness)
- **Default writing system: Traditional** (Taiwan context). Simplified only for mainland contacts. Source: [markdowns/PROJECT_INSTRUCTIONS.md](markdowns/PROJECT_INSTRUCTIONS.md).
- **4-layer format** is the canonical Chinese-output convention. Source: same file.
- **Single-file HTML app, mobile-first (iPhone 13 Mini), vanilla JS.** Source: [markdowns/zifang-design-system.md](markdowns/zifang-design-system.md).
- **Zifang lives at `~/Documents/Chinese shit/`** — not under `webdev/`. Old portfolio path is wrong; canonical fix pending Step 0 of Portfolio Manager spec.

---

## Ideas (not yet acted on)

### Forge pre-generation intent check — start with highest-leverage heuristics only
The system could get infinitely complex. Decision: don't try to catch everything. Pick the 3-4 signals that cover the most common real-world mistakes, implement those, and document everything else as the list grows. Complexity accumulates in the doc, not in the prompt.
**Why:** Diminishing returns kick in fast. Four well-chosen heuristics probably cover 80% of real cases. The remaining 20% is edge territory that can be added incrementally.

**Initial heuristic candidates (ranked by leverage):**
1. **Bare verb/stative requiring a complement** — 聞起來, 看起來, 覺得, 感覺. Nearly useless as standalone cards because they're never said alone. Ask: "What follows — what does it smell/look/feel like?"
2. **Known homophone trap** — a finite enumerable list of pairs learners most commonly confuse: 是/事, 的/地/得, 再/在, 做/作. Ask: "Which one?" with both options shown.
3. **Fragment of a fixed expression** — 2-3 chars that are the front half of a common chengyu or set phrase (一石 → 一石二鳥, 半途 → 半途而廢). Detectable against a fixed-expression list. Ask: "Are you thinking of [full phrase]?"
4. **Single character with divergent readings** — 長, 重, 行, 得, 著. Query alone gives no signal which reading the user encountered. Ask: "Which reading — [cháng/zhǎng], [zhòng/chóng]...?"

**Status:** Not yet implemented. Design next step: turn these four into a concrete taxonomy (signal → detection method → example query → question to ask), then distill into prompt language. See INTENT.md §9a for the governing principle.

### Forge pre-generation intent check — the guide should sometimes ask before forging
When a user types Chinese directly into Forge, the current behavior is immediate card generation. But this is a silent failure mode: they can forge a card for a homophone, a fragment of a longer set phrase, a register-mismatched word, or an expression that requires a complement — and never know it. The guide's job is to read the query for ambiguity signals and ask *one* targeted question when the cost of forging the wrong card is higher than the cost of one pause. No question when the query is clean; one question when it isn't. The judgment call is the LLM's, not a rules-engine's.
**Why it's hard:** Goals are individualized. HSK driller, conversational speaker, correspondence writer — the right card is different for each. The more context the AI has about what the learner is trying to accomplish, the better. But that context has to be gathered lightly, not via a form.
**Status:** Not yet acted on. Documented in INTENT.md §9a. Needs prompt design + a UI slot for the pre-generation exchange before the card is committed.

### LLM surfaces "one piece of adjacent nuance" alongside Forge cards
INTENT.md §9 floats this: after Forge generates a card, surface one — and only one — non-obvious thing the user would have asked for if they knew. As a dismissible side element, not baked into the card body. Needs a UI slot and a heuristic for which axis to pick.
**Open question:** Does this become annoying after the user has seen it 50 times for the same axis? Probably needs per-user dampening — don't keep surfacing "this is also used in Taiwan" if Tim already knows.

### Polysemy cross-reference panel
Already in the pending queue (item 6) but worth flagging here too because it's the clearest expression of "library-aware Workshop" from INTENT.md §10. Tap any character in a card's components and see every other card in the library that uses it, with reading/meaning differences called out.
**Status:** Backburner. Design when it surfaces naturally.

### "Understanding Zifang" onboarding tied to INTENT
Pending queue item 4 mentions an in-app explainer. Worth considering whether the *user-facing* explanation of what Zifang does should mirror INTENT.md's framing — "this is your guide through the landscape of Chinese, not a translator" — so the user's mental model matches the LLM's posture.
**Status:** Unstarted.

### Adaptive depth needs a feedback loop
INTENT.md commits to adaptive-to-query depth, but the LLM has no signal for whether it pitched right. Possible: a quick thumb-up/down on the response, or just "more / less" buttons. Without a loop, "adaptive" is theoretical.
**Status:** Idea only.

### Forge input validation strategy
Pending queue item 2 already captures the symptom (Forge breaks on English/gibberish/trolling). Worth treating as a sub-problem of INTENT §9.3 (fail gracefully) and designing the failure UX before the validation logic.

### How does the LLM know the user's contact context inside Forge?
PROJECT_INSTRUCTIONS.md has "writing system by contact" rules tied to `data/contacts.json`. INTENT.md says the LLM should honor that context. But Forge currently runs without contact context — it's a standalone query. Open: does Forge gain a "for whom?" optional input? Or is contact context only for correspondence-mode tools outside the app?
**Status:** Unsettled.

### Where does INTENT.md live as runtime context?
INTENT.md is human-readable doctrine. For it to actually shape LLM behavior in Forge/Workshop, some of it has to be in the system prompt the app sends. Open: is INTENT.md the *source* that gets distilled into a system prompt, or is it the prompt itself? Probably the former — needs a distillation step.
**Status:** Unsettled.

---

## Recently moved / superseded

*(Empty — nothing yet.)*
