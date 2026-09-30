---
attention: Active
state: Live
form: Website
updated: 2026-09-29
live_url: null
---

# 字坊 — STATUS

**What this file is.** A living scratchpad of *decisions* Tim has made about Zifang and *ideas* he's had but not yet acted on. Distinct from [markdowns/zifang-pending-queue.md](markdowns/zifang-pending-queue.md) (which is the feature backlog) — this file is the higher-level "where is my head on this project."

**How to use it.**
- When a decision lands, add it to **Decisions** with the date and a one-line "why."
- When an idea surfaces, drop it in **Ideas** even if half-formed. The point is to externalize it before it evaporates.
- When an idea matures into a decision, move it. When a decision is superseded, strike it through and note what replaced it.
- Reference [INTENT.md](INTENT.md) for LLM doctrine, the pending queue for backlog, [markdowns/zifang-design-system.md](markdowns/zifang-design-system.md) for architecture.

**Last updated:** 2026-09-17

## Where I left off

HSK6 enrichment is **complete and live**: all 2500 cards (IDs 5001–7500) are enriched in `data/hsk6-enriched.json`, zero R1–R10 errors, zero gaps. Uploaded to Supabase via `node upload-hsk6-enriched.js` — all 2500 upserted successfully. The live app is now serving the finished dataset.

## Open

Live items from the 2026-08-02 scratchpad reconciliation, in recommended order. Full evidence
and implementation notes in [_docs/2026-08-02-scratchpad-reconciliation.md](_docs/2026-08-02-scratchpad-reconciliation.md).
Scratchpad wording is kept verbatim so the notes and this file stay greppable against each other.

- <!-- open:hidden-cards-ui --> **"best way to show hidden cards? (where does the user press to see that mode?)"** — answer today is *nowhere*. `restoreAllHiddenCards()` (`index.html:8512`) is defined once and never called; a swiped-away built-in card is unreachable from Browse, Drill, and Workshop with no path back. Data-reachability bug, not a feature. Minimum fix: a `Hidden cards: N / Restore all` row in Settings → Progress (`#settings-pane-progress`, `7343`) wired to the existing function. The browsable "hidden as a pseudo-deck pill" version is the larger design, deferrable.
- <!-- open:flashcard-settings-render --> **"fix render of the flashcard settings and the transition between tabs"** — `.settings-panel` is height-locked to `min(480px,80dvh)` with a comment that still says "the taller of the **two**" panes when there are now four (`5145-5152`), and `#settings-pane-sliders` opts out of scrolling entirely (`overflow-y: hidden`, `5213`). The 2×2 theme grid compresses with no scrollbar to recover it. Tab switching is a bare `display:none` swap (`5212`, `15206-15207`) so panes hard-cut while the tab buttons animate. Fix both in one pass; note `openSettingsKeys()` (`15095-15101`) and the reset at `15773-15775` also poke `.hidden` directly.
- <!-- open:workshop-known-words --> **"Use the known words to produce sentences in the workshop"** — the %known / %new / user-chosen mix. The only genuinely new capability in the scratchpad. Needs no new storage: derive from `loadCardScores()` (`8603-8626`). **Sample 15–45 words, do not inject the pool** — measured cost is ~90 tokens for 25 words vs ~5,000 for 1,000. Three design hazards: (a) "new" must come from cards with *no* scores entry, not score 0, which conflates unseen with repeatedly-failed; (b) known words must go in a *separate* prompt block from `VOCABULARY TO INCLUDE` (`12513`), whose "MUST appear" rule (`12549`) they should not inherit; (c) `stageState.hskLevel` defaults to 1 (`11763`) while known words will come from HSK5/6 drilling — those instructions fight. Belongs in prompt layer L2 per the 2026-05-25 layered-assembly decision, not appended to the static string.
- <!-- open:workshop-squircle-pinyin --> **"fix the pinyin protocol inside of the workshop squircle buttons"** — the four cast-row squircles (`8027-8039`) use plain `title=` attributes while the dot controls directly above them (`7925-7955`) use the full `hpShow()` body-portal tooltip, and the spicy button uses a third mechanism (`.spicy-toast`). Three tooltip systems on one screen. Check first whether `.cast-row-btn`'s squircle `clip-path` (`484`) clips an in-DOM `.hp-pinyin` the way `.dot-opt` does — that determines whether this needs the portal branch extended or just a span wrap.
- <!-- open:cheap-correctness-batch --> Cheap correctness fixes, one sitting: (1) Library **"edit mode"** button says `Edit` but only deletes — rename to `Remove` (`7495`, `13925`, `13936`); (2) **"Use Credits to Enrich"** consumes no credits and never touches Sonnet — it calls Groq with the user's free-tier key (`8140`, `16773-16781`) — rename to `Enrich with AI`; (3) Moria gate subtitle is Simplified (`8075`), contradicting the Traditional default — 这个功能是锁着的 → 這個功能是鎖著的; (4) Workshop Script dot control defaults to **Simplified** (`7955`) against the same doctrine — move `active` to the `traditional` button; (5) delete the orphaned `// inline arrays kept as offline fallback` comment (`8529`), which contradicts `15614`; (6) add an empty-Browse state — `getFiltered()` returns zero cards when nothing is selected (`9196`), which is every new user's first view.

## Back Burner

- <!-- bb:forge-validator --> Forge correctness layers (per 2026-05-26 decision): Layer 1 deterministic validator first (free, biggest mechanical-error catch), then same-model critic, then Sonnet routing. **Blocker found 2026-08-02:** Layer 3 cannot fire as specified — `const provider = groqKey ? 'groq' : 'anthropic'` (`index.html:10444`) makes Groq win unconditionally whenever a Groq key exists, so a user with both keys can never reach Sonnet. Fix that line before building routing logic.
- <!-- bb:moria --> **"get moria sorted"** — ambiguous ask, low stakes, behind the spicy password gate. Two divergent assets exist: `moria.html` (standalone, viewBox 500×680, 111 drawing elements, Tengwar arch text) and the inline gate injected at `index.html:16918` (viewBox 200×230, 19 elements). Likely means port the good art in, or delete the standalone so it stops implying unfinished work. `moria/` also holds 10 reference screenshots from 2026-04-01, so a third reading is "finish the art from those." Needs Tim to say which.

## Log

- 2026-09-29: Cleared the root of two one-off HTML prototypes, a pre-HSK4 HTML snapshot, and two loose screenshots. They are preserved under `_docs/prototypes/`, `_docs/snapshots/`, and `_docs/captures/`, with a root `README.md` explaining the live app, operational scripts, and reference folders. `moria.html` and its companion `moria/` remain together at the root because that is a separate active surface. No files were deleted; `old images/` was untouched.


- 2026-09-17: Shipped the offline card cache (IndexedDB) and the `.offline-notice` strip; see Decisions.
  Also corrected the stale `// inline arrays kept as offline fallback` comment on the `ALL_CARDS`
  declaration (one of the `open:cheap-correctness-batch` items). **Line numbers cited elsewhere in this
  file and in `_docs/2026-08-02-scratchpad-reconciliation.md` are now shifted** — the patch inserted
  +48 lines at old-3501 (CSS), +5 at old-7265 (markup), +82 at old-8330 (JS), and +15 across the
  boot block at old-15611. Net +150. For any reference above old-3501 the number is unchanged; above
  old-8330 add ~135; above old-15611 add ~150. Staged locally, **not deployed**.

- 2026-08-02: Reconciled Tim's out-of-repo scratchpad (13 bullets) against the code at `e7a034c`. Decomposed to 20 atomic line-items: 5 Done, 1 Done differently, 5 Premise false, 9 Not started. Report at [_docs/2026-08-02-scratchpad-reconciliation.md](_docs/2026-08-02-scratchpad-reconciliation.md). Live items moved to **Open** above in the scratchpad's own vocabulary so the two are greppable against each other. Two kills recorded under Decisions ("decks in github", "expand decks using llama") plus one skip (SVG FC theme swatches). Three incidental defects found that were not in the scratchpad: no offline fallback (Back Burner), Sonnet routing unreachable (Back Burner), Workshop script default is Simplified against project doctrine (Open, cheap batch). Verified by extracting `drillFontSize`/`calcPinyinFontSize`/the score model verbatim and running them over all 3,791 HSK5+HSK6 cards — longest headword is 4 chars, so the drill font ladder's 5/7/8+ branches never fire on shipped decks, and `calcPinyinFontSize` clamps on ordinary 1-char cards instead. No app code changed this session.

- 2026-07-31: Migrated Zifang's Groq default off the deprecated `llama-3.3-70b-versatile` model and onto `openai/gpt-oss-120b`. Centralized the Groq model ID in `index.html`, updated all Groq request paths to use it, and refreshed stale Llama-specific UI copy so the key/model settings match the current setup before a new API key is entered.
- 2026-07-31: Began the runtime terminology cleanup away from legacy `nugget` wording. Safe pass completed in `index.html`: core Forge/runtime identifiers now use `card` language (`generateCard`, `validateGeneratedCard`, `ALL_CARDS`, `pendingCard`, `userCards`, etc.). Verified with a JS syntax check on the extracted inline script. Remaining `nugget` strings are intentionally limited to persistence-sensitive localStorage/cache/theme/auth keys and compatibility comments around them.
- 2026-07-31: Supabase admin-key hygiene cleanup is complete. Created an untracked project-root `.env`, moved the `service_role` credential out of `upload-*.js` and `migrate.js`, added loud missing-env failure guards to those scripts, and created `_meta/SECRETS-HYGIENE.md` so the procedure is actually documented. No public leak was found; no key rotation performed.
- 2026-07-12: The 2026-07-01 `service_role` "exposure" was investigated and is **not a public leak**: the scripts holding the admin key (`upload-*.js`, `migrate.js`) are **untracked and were never committed** to the public `cubicleaf/Zifang` repo (which tracks only `index.html`, carrying the public-by-design `anon` key). The latent risk — a stray `git add .` sweeping the secret scripts in — was closed by gitignoring `.env`/`upload-*.js`/`migrate.js`/`data/contacts.json`. The remaining work at that point was hygiene only, and it was completed on 2026-07-31.
- 2026-07-12: Investigated the 2026-07-01 `service_role` "exposure" — it is NOT public. The upload scripts and `migrate.js` that hold the admin key are untracked and were never committed (`git log --all` empty for them); the public repo tracks only `index.html`, which carries the `anon` key (public by design). Closed the latent risk by gitignoring `.env`, `upload-*.js`, `migrate.js`, and `data/contacts.json` so a stray `git add .` can't leak them. The hygiene guide now lives at `_meta/SECRETS-HYGIENE.md`.
- 2026-07-11: `tims-ux-playbook/SKILL.md` (which lived in this folder as a birthplace accident) is now DEPRECATED. The playbook's canonical home is `~/Documents/ux-playbook/` (canon/corpus split + generated skill). The local copy carries a deprecation banner; safe to archive/delete during the planned location cleanup. Zifang's own design docs (`markdowns/zifang-design-system.md` etc.) are unaffected.
- 2026-07-10: Reshaped to the two-axis STATUS format (SPEC-converged-v1 §2). Formatting migration only — `updated:` deliberately not bumped.
- 2026-07-15: Migrated the header from the retired `relationship / kind` pilot to the canonical `attention / state / form` schema. Zifang now reads as `Active / Live / Website`: a real deployed working surface, not just a prototype shorthand.

## Decisions

### 2026-09-17 — Offline fallback shipped as an IndexedDB cache, not localStorage
**What:** `fetchCards()` results are now cached to IndexedDB (`zifang-cache` / `kv` / `remote-cards-v1`)
on every successful load, and restored when Supabase is unreachable *or* returns an empty set. A quiet
`.offline-notice` strip under the header reports the degraded state. Closes the old
`bb:offline-fallback` item.

**Why:** The Supabase project was paused on 2026-08-07 for free-tier inactivity, and
`zifang.vercel.app` served **0 cards for ~6 weeks** — confirmed live on 2026-09-17
(`ALL_CARDS = 0`, `_remoteCards = 0`; `fkgjduganefwmakxxnqt.supabase.co` did not resolve in DNS
even against 8.8.8.8). The failure was silent to the user: the catch block logged "falling back to
inline data" for inline arrays that had been removed. A `state: Live` project had no degraded mode.

**How to apply:** The old Back Burner note proposed localStorage and said it would "close it cheaply."
**That premise was wrong** — HSK5 (1.80 MB) + HSK6 (3.37 MB) is ~5.2 MB of JSON, over the ~5 MB
localStorage ceiling, so a localStorage cache would have thrown `QuotaExceededError` on write.
IndexedDB has no practical limit and is already async. Verified by writing and restoring all 3,791
cards with Supabase down. **This does not un-pause Supabase** — free-tier projects re-pause after
7 days of inactivity, so the cache is the safety net, not the fix.


### 2026-08-02 — Killed: "decks in github instead of the html", "expand decks using llama", SVG FC theme swatches
**What:** Three scratchpad items retired rather than built.
(1) **"figure out if there's a benefit in putting the decks in github instead of the html"** — the premise is already false. Decks left the HTML: `_remoteCards = await fetchCards()` from Supabase (`index.html:15611`, `8341-8342`), and `15614` states plainly that inline arrays were removed. Supabase gives row-level column selection a static GitHub JSON file cannot; a static file means fetching all 3,791 cards on every load; and the 2026-07-31 gitignore work deliberately kept `data/` write scripts untracked, which moving decks into the repo would reopen.
(2) **"add an option to expand decks using llama? (llama find similar words from deck's title)"** — highest hallucination surface in the app against the weakest input signal. `_docs/RECON.md` found confident hallucination to be the #2 failure mode of exactly this model on exactly this kind of open-ended generation, and `validateGeneratedCard()` is wired to Forge's single-card path, not to any bulk path. Deck titles (自創, 句型) also say nothing about contents. The model reference is stale besides — Groq moved to `openai/gpt-oss-120b` on 2026-07-31.
(3) **"(also svg of FC themes)"** — skipped. The current div-based swatches (`7377-7386`) are legible; hand-drawn SVG minicards would add a permanent sync obligation against the `THEMES` object (`14985`) for a cosmetic gain.
**Why:** Each was a reasonable thought when written and each has been overtaken — by a completed migration, by empirical evidence about model reliability, or by cost/benefit that does not clear.
**How to apply:** Do not resurface these as open work. If deck expansion is ever revisited, build only the bounded version: seed from the deck's *existing* cards (`components[]` + `semanticNote` are far richer than a two-character title), cap at 5 suggestions, route each through `generateCard()` so the validator runs, and require per-word confirmation. Never bulk-insert.

### 2026-08-02 — Drill character sizing is adequate; the real gap is pinyin sizing
**What:** **"make variable size for the Chinese characters in Flashcards"** resolved as Done differently rather than built. Three mechanisms already adapt headword size: a stepped ladder at `index.html:9997-10004` (≥8 → 2.2rem, =7 → 2.4rem, ≥5 → 2.6rem, else 3.0rem base at `2197`), `smartWrapDrillChar()` (`9833-9871`), and CSS `word-break: break-all` (`2204`). Running the ladder verbatim over all 3,791 shipped HSK5+HSK6 cards showed the longest headword is 4 characters — the 5/7/8+ branches never execute on shipped content. Meanwhile `calcPinyinFontSize()` (`9874-9890`) clamps to `[0.62, 1.1]` and hits the floor on ordinary single-character cards with long syllables (莊 zhuāng, 窗 chuāng) while a 2-char card sits at 0.94.
**Why:** Building continuous character sizing would produce no visible change on the decks that ship. The visible inconsistency is on the pinyin line, not the character line.
**How to apply:** If this is picked up, do the two small things instead: widen the `calcPinyinFontSize` floor at `9887` (0.62 → ~0.78, or make the clamp relative to character count), and add `maxlength="12"` to `#forge-word-input` (`7662`), which currently has none and is the only path that can reach the dormant ladder branches. Changing the clamp touches every card back in Drill plus the Settings demo card (`7391-7397`) — check the 1-char and 8-char extremes together.

### 2026-07-31 — Favicon replaced with the real Drill tab icon, in the real Drill blue
**What:** The favicon originally shipped as an invented "two overlapping rounded-rect cards" abstraction, ink on rice. Replaced with the actual Drill tab SVG path from `index.html` (the two-layer document/badge icon at line ~7438, rendered with `fill="currentColor"`), recolored to the genuine Drill accent `#4682b4` (from the `accents` map at line ~9286, not a guessed blue). Shell converted from a circle to the portfolio-wide squircle. Went through several size iterations by direct feedback; the earlier percentage-of-percentage math compounded a bug (each new "+X%" was computed from an already-overwritten, re-extracted file instead of the true original, and briefly produced a badly oversized render bleeding past the shell). Corrected by working from confirmed-good pixel widths and verifying every step by direct pixel measurement rather than trusting formulas. Final: icon is 334px wide on a 512px canvas (65.2%), confirmed to sit fully inside the shell's 488px (95.3%) bounds.
**Why:** Tim wanted the favicon to match the app's real Drill tab exactly rather than an approximation, and asked me to find the actual SVG in the codebase rather than reinvent it.
**How to apply:** Files at repo root (favicon.ico, 16/32/180/192/512 PNGs), no HTML changes needed — link tags already wired. If Drill's accent color or icon ever changes in-app, the favicon should be regenerated to match, not treated as independently locked.

### 2026-07-31 — Groq default moved from deprecated Llama 3.3 to GPT-OSS 120B
**What:** Replaced Zifang's hard-coded Groq model target `llama-3.3-70b-versatile` with a single `GROQ_DEFAULT_MODEL` constant set to `openai/gpt-oss-120b`, and updated the settings/help copy so the app no longer describes the Groq path as specifically Llama-based.
**Why:** Groq has deprecated Llama 3.3 70B Versatile and will stop serving it on 2026-08-16 for free and developer-tier usage. Leaving the old model string scattered through the app would create a silent break.
**How to apply:** Keep Groq as the free default unless there is a reason to optimize differently later. If Zifang switches again, change the centralized Groq constant first and verify all browser-direct Groq paths still inherit it.

### 2026-07-31 — Runtime terminology starts moving from `nugget` to `card`
**What:** Renamed the safe in-memory/runtime layer in `index.html` away from `nugget` language: Forge now calls `generateCard()` / `validateGeneratedCard()`, the merged library is `ALL_CARDS`, and pending/generated/user-created card objects now use `card`-based variable names.
**Why:** `nugget` was a historical scope artifact from an earlier, smaller version of Zifang. In the current app it obscures what the system actually manipulates: cards inside decks inside a larger library.
**How to apply:** Keep using `card` for single study items, `deck` for groupings, and `library`/`cards` for collections. Do not blindly rename persistence keys (`user-nuggets`, `nugget-lexicon`, etc.) without an explicit compatibility/migration pass.

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
When the model returns `needsClarification` JSON, Forge now shows the question + clickable reading/option chips in the status area instead of a parse error. User's selection routes back into `generateCard()` with the chosen context as a clarification parameter. Button state managed across the retry cycle via `_forgeInRetry` flag to prevent flicker.
**Why:** Required JS infrastructure for the clarification gate to be usable. Without it, any `needsClarification` response silently failed.

### 2026-05-27 — Forge sysPrompt rewritten
Replaced static string with structured prompt: pre-flight clarification gate (polysemous single chars 長/重/行/得/著 + chengyu fragments → `needsClarification` JSON), 5 hard consistency rules (in-compound readings, one-to-one pinyin/char alignment, space-separated syllables, no invented particles, contradiction check), depth calibration by query type. Token cost ~839 vs ~400 previously — accepted for correctness gains confirmed by recon.
**Why:** Original prompt produced hybrid cards, wrong readings, hallucinated particles, and inconsistent pinyin. RECON evidence (21 queries) drove the rewrite.

### 2026-05-27 — Pre-flight gate moved to user message
The polysemy + chengyu fragment pre-flight check is now prepended to every user message, not just the system prompt.
**Why:** Llama follows user-turn instructions more reliably than instructions buried 500+ tokens into a system prompt. Gate was misfiring for 行 and 著 under the old architecture. ~25 extra tokens per call, worth it for gate reliability.

### 2026-05-27 — Phase 1 validator implemented
`validateGeneratedCard()` runs on every Forge generation before saving. Seven checks: required fields present, exactly 2 examples, each example has all three fields, pinyin token count matches character count (one space-separated syllable per character), components length = headword length, particle repetition typos, tone mark enforcement. On failure: one automatic retry with the specific issues injected into the user context; graceful error to user if retry also fails. Retry suppresses button flicker via `_forgeInRetry` flag.
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
