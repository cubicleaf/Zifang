# 字坊 Zifang — Updated Full Audit
*April 29, 2026 · Multi-agent · Compared against 2026-04-03 baseline*

---

## 0 · How this audit was done

Four sub-agents ran in parallel, each with a different mandate and assumption-set: code architecture, UX/pedagogy/anti-feature, data integrity, and first-principles novel directions. Findings were then cross-referenced for contradictions and amplifications. This isn't a single voice — it's four voices trying to break the app from different angles, then reconciled.

---

## 1 · The single most important finding

**The app has zero audio.** No `<audio>`, no `speechSynthesis`, no `AudioContext`, no `SpeechRecognition`. Every drill, every dialogue, every example sentence is silent text. Tim's stated bottleneck is the **spoken-anxiety gap** (我打字比說話好很多). The current architecture actively reinforces silent reading. Every feature shipped to date has been a beautiful answer to a question Tim isn't asking.

This is the single largest gap between what Zifang is doing and what Tim says he wants it to do for him.

---

## 2 · Stale doc claims (the audit found before it found anything else)

| Claim in `zifang-project-knowledge.md` | Reality | Status |
|---|---|---|
| `index.html` ~7,600 lines | 18,002 lines | Doc is off by 137% |
| Z-04 (Forge edit-before-save) DONE | `forgeReviewState` exists, but no clear edit UI before save | Probably partial |
| Z-07 (Save Workshop dialogues) implied done | No save button on Workshop output found | Still open |
| Session system Phases 1-6 DONE | Phase 1 (scoring) shipped solidly. Phases 4-6 (modal, settings progress, resume prompt) partial or missing | Partial |
| `markdowns/zifang-audit-checklist.md` exists (referenced in project knowledge) | File does not exist on disk | Missing reference |
| `markdowns/zifang-audit-2026-04-09.md` is "most recent audit" | File does not exist on disk | Missing reference |
| `lexicon.json` is "source of truth" | Index.html has all decks hardcoded; lexicon.json is never read by the app | Orphaned |
| Naming inconsistencies fixed | `.cat-bubble` / `.setup-cat-bubble` / `.vocab-cat-pill` all still coexist (~240 lines of CSS duplication) | Still open |

**Implication:** before the next dev session, project-knowledge.md needs a refresh pass. It's load-bearing for future Claude sessions and currently misleads them.

---

## 3 · Code architecture — top risks (delta from baseline)

**3.1 — Blur filter on tab transitions (lines 186-201).** Design system explicitly forbids `filter: blur()` on tab content because it creates a containing block that traps `position: fixed` modals. Current code animates `filter: blur(0px → 6px)` on every tab switch. Latent bug waiting for a modal to open mid-transition. Replace with opacity-only fade (already exists as `tabFadeIn`).

**3.2 — localStorage schema sprawl (19 keys, three prefix conventions).** `zf_*`, `nugget-*`, `zifang-*` all coexist. Two keys (`nugget-lexicon`, `default-model`) are written but **never exported in backups** — silent data loss risk. `zifang-card-stats` is marked deprecated but still receives dual writes on every drill (lines 9717-9739). Clean schema migration overdue.

**3.3 — State alias brittleness (lines 9636-9648).** `state.drill.cats = state.selectedCats` is a live alias — not a copy. The comment warns "DO NOT reassign... it breaks the alias and quietly de-syncs the tabs," but there's no guard rail. One careless `state.drill.cats = new Set(...)` anywhere silently breaks cross-tab consistency and you'd never know.

**3.4 — CSS naming triplication (~240 lines of duplication).** Same component, three names. Old audit flagged it. Still unfixed.

**3.5 — Inline event handlers in `hoverPinyin()` (line 9778, 117 call sites).** Violates the spirit of the documented "delegation-first" rule. Works fine, but if you ever need a global hover listener, you can't intercept these.

**Surprisingly well-built:** the score-weights / migration / weighted-sample logic is correct and elegant. Cross-tab card-delete propagation is actually solid. Color-mix pill ramp tokens are textbook clean. Hover-pinyin auto-sizing via canvas binary search is sophisticated. `friendlyGroqError()` is genuinely better than most commercial apps.

---

## 4 · UX delta vs 2026-04-03 baseline

**Closed (5):** Browse pill strip horizontal (Z-03), Drill score on completion screen (Z-X), Forge edit-before-save (`forgeReviewState` exists), color-mix tokens replacing hardcoded values (1b), `--mauve` no longer vestigial (now drives Workshop dot controls).

**Still open (4):** Cast as third pill in Stage (3a — biggest discoverability hole in Workshop), Drill setup subtitle still "Configure your session" (2b), Workshop dialogues vanish on close (3g/Z-07), CSS naming unification (1a).

**Unclear (3):** Workshop dot controls English sublabels, "Use Credits to Enrich" button copy, Browse "沒有啦😗" empty state guidance.

**Net:** 5 of 12 baseline recommendations addressed in 26 days. Decent throughput. The big infrastructure work (session ledger + score system) explains where the time went.

---

## 5 · Pedagogy critique (honest)

The score system (0-3, weights 4/2/1/0.5) is **standard Anki-style spacing logic**, not dormant-knowledge framing. It treats "struggling on a word I knew in 2018" identically to "encountering a brand-new word." Pedagogically those are different animals. There is **no surface in the app** that distinguishes dormant-recognition failure from genuine-novelty failure. Tim's stated mental model — "knowledge isn't lost, it's dormant" — is not actually expressed in the data model.

The "Got it / Struggling" binary captures the SRS signal but not the **most relevant signal for a rusty learner**: how *fast* the recognition came back. A wake-up timer (ms between reveal and tap) would be a more honest metric for dormancy than a binary tag.

The HSK4 deck (600 cards added 2026-04-28) doubled the pool. For an HSK 2-3 learner trying to wake up basics, that's a strategic question — does dilution of the high-priority basics serve revival, or fight it?

---

## 6 · Data integrity verdict

| Check | Status |
|---|---|
| Deck counts (HSK 1-4 + original) | ✓ All verified, exact match to claims |
| Lexicon.json as source of truth | ✗ Orphaned. Index.html is de-facto source |
| Trad/Simp consistency | ✓ HSK 1 spot-check clean |
| Taiwan-modern overrides in HSK 4 | Needs spot-check (聯絡, 支持, 通過, 製造, 製作, 幹活兒, 乾燥, 網路, 軟體) |
| Pinyin tone marks for HSK 4 heteronyms | Needs spot-check for 期 (qí vs qī), 質 (zhí vs zhì) |
| Contacts.json compliance (no Instagram for mainland, except Moon) | ✓ Fully compliant — every mainland contact correctly segregated |
| HSK5 scout files (A/B/C/D) | ✓ Excellent diligence. 30 hand-review words, 9 NUGGETS dupes flagged for drop, ~130 grammar/register annotations needed |
| Chengyu collection | ⚠ Not directly verified this pass — schema and source citations unconfirmed |

**Bottom line:** data is ~85% clean. The single most critical hygiene step before HSK5 generation is verifying HSK4 actually applied Taiwan-modern forms for the disputed words. If HSK4 ships 制造 and HSK5 ships 製造, that's an inconsistency Tim will notice every day.

---

## 7 · Anti-features (candidates to cut or de-emphasize)

These earn an explicit defense in the next decision pass, or they should be on the chopping block:

1. **Spicy mode** — fully built Moria gate easter egg with password protection (~500 lines). Cute, but is it ever used? If not, it's pure surface area.
2. **Three Drill themes** — Night Study / Bamboo Grove / Clean Slate. Charming. Probably also unused outside the first day Tim shipped them.
3. **Workshop character roster** — extensive feature, but Cast is buried inside the Topic modal. Architecturally substantial; experientially invisible. Either surface it (third pill in Stage) or simplify it dramatically.
4. **The dual-write to `zifang-card-stats`** — pure overhead now that scores drive selection. Lift the legacy writes; keep reads only as a final migration safety net for one more cycle, then delete.
5. **Forge tab as a major surface** — ~3,000 lines of code. If telemetry showed Tim uses it once a month, the value-to-maintenance ratio is upside-down.

The point of an anti-feature audit isn't to delete things. It's to ask: which of these would I miss if a fire deleted them? Anything that wouldn't earn a rebuild deserves at minimum a demotion.

---

## 8 · Three new directions worth pursuing (filtered from seven generated)

**A. Living Lexicon — drill what you actually use.** Tim corresponds with real humans whose vocabulary differs (Echo vs Jerry vs Moon). Hanban's HSK 4 list doesn't know any of those people. A "paste a conversation, extract Chinese tokens, dedupe against your lexicon, ask if you want to save the new ones" pipeline would convert the app from a generic HSK trainer into a personal corpus tool. Per-contact decks ("words Echo uses") flow from this. Pre-conversation reply-prep mode flows from this. This is the version of Zifang that nobody else ships for you.

**B. Dormant-mode toggle inside existing Drill.** Don't rebuild Drill. Add a toggle: "Rust mode." When on, the grading buttons disappear. The metric becomes wake-up time (ms between flip and tap). The UI is identical otherwise. Ship as a behind-the-scenes data layer first, then expose. Two parallel scores per card: "freshness" (current 0-3) and "warmth" (rolling-average wake-up time). This is the pedagogically honest expression of "knowledge isn't lost, it's dormant."

**C. Audio, even crudely.** A single tap-to-speak button on Drill cards using browser `speechSynthesis` with a Mandarin voice is a one-day feature that addresses the #1 stated bottleneck. Don't try to grade pronunciation — that tech isn't there yet for tones. Just **let Tim hear the words**. This alone moves the needle on speaking by closing the recognition-to-production loop. Skip "AI judges your pronunciation 73%" — that's theater.

Skipped from the seven: persona-as-app rewrite (interesting but high-cliché-risk and depends on A landing first), framework migration (constraint still serving him, don't pre-migrate), full audio shadowing pipeline (half the features fail in practice on tone recognition), four-tab-to-one-tab radical reduction (too violent for a still-evolving app), explicit Taiwan/Taigi separation tier (different project pretending to be a feature).

---

## 9 · Five most surprising findings

1. **Project knowledge says `index.html` is 7,600 lines. It's 18,002.** Doc has been load-bearing for sessions and lying for weeks.
2. **The session system is more sophisticated than its own documentation.** Score weights, ledger, weighted sampling all shipped post-design-system-doc. The app's actual capability exceeds its written spec.
3. **Lexicon.json is orphaned.** It's labeled "source of truth" in instructions but the app never reads it.
4. **Forge edit-before-save shipped quietly with no UI fanfare** — there's a `forgeReviewState` object and review panel hiding in the code, but the audit doc still flags Z-04 as critical-pending.
5. **Workshop dialogues are ephemeral by design.** No save button. No archive. Generated and gone. This contradicts the data-preservation ethos baked into every other surface (export backups, score persistence, session ledgers).

---

## 10 · Prioritized recommendations

### Tier 1 — fix before next feature ships
1. Update `zifang-project-knowledge.md` to reflect actual line count, actual feature state, and the missing audit/checklist file references. The current doc misleads every session.
2. Add basic `speechSynthesis` audio playback to Drill cards. One-day feature. Single biggest move-the-needle change available.
3. Verify HSK 4 Taiwan-modern overrides for the disputed forms (網路/軟體/聯絡/支持/通過/製造/幹活兒/乾燥) before any HSK 5 generation. Inconsistency between decks is the worst possible outcome.
4. Stop dual-writing to `zifang-card-stats`. Read-only the legacy key, plan its deletion.
5. Replace `filter: blur()` tab transition with opacity-only fade.

### Tier 2 — quality-of-life and integrity
6. Surface Cast as third pill in Workshop's Stage row (3a still open from 2026-04-03).
7. Implement Workshop dialogue save (Z-07, still missing).
8. Add `nugget-lexicon` and `default-model` to backup export (silent data loss risk).
9. Unify CSS naming: `.cat-bubble` / `.setup-cat-bubble` / `.vocab-cat-pill` → one class with modifiers.
10. Either deprecate `lexicon.json` or rename to `user-vocabulary-tracker.json` and document.

### Tier 3 — strategic / new directions
11. Ship "Rust mode" toggle in Drill (wake-up timer, no grading buttons). Phase 1 = data layer only.
12. Build conversation-paste prototype for Living Lexicon. Crude version: textarea + token extractor + "save these new ones?" sheet.
13. Onboarding section ("Understanding Zifang") — pending queue item #5, still open. Becomes more important as feature surface grows.

---

## 11 · Things working well — explicitly preserve

- The ink-on-rice-paper aesthetic (rice / sand / ink / jade / vermillion) — distinctive and culturally coherent
- Color-mix pill ramp tokens — clean, dynamic, properly tokenized
- Hover-pinyin with canvas-based width binary search — genuinely sophisticated
- `friendlyGroqError()` — better than most commercial error handling
- Cross-tab state propagation principle (delete in one tab, gone everywhere) — well-executed
- HSK5 scout files (A/B/C/D) — exemplary content-prep diligence
- Score-based selection algorithm — pedagogically standard but correctly implemented
- Tim's choice of single-file vanilla JS — the constraint is still earning its keep

---

*Audit complete. Sub-agents: code-architecture, ux-pedagogy, data-integrity, novel-directions. Next step: Tim picks one Tier 1 item to ship.*
