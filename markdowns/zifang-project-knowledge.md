# Zifang — Project Knowledge

**Last updated:** 2026-07-01 (HSK6 enrichment milestone — 1,900 cards done, IDs 5001–6900 complete)

---

## 1. THE APP

**Name:** 語言寶庫 · Tim's Nugget Explorer (project name: "zifang")
**File:** `index.html` (root of Chinese shit folder)
**Deployed at:** zifang.netlify.app (via GitHub, Netlify)
**Size:** ~7,600 lines, single-file HTML app
**Tech:** Vanilla JS, CSS custom properties, Google Fonts. No frameworks.

### 4 Tabs

**瀏覽 Browse** — Explore the nugget library. Search across pinyin, Chinese, and English. Category filters (Favorites, Vocab, Expression, Idiom, Concept, Custom). Card view and list view toggle. Hover-pinyin tooltips. Expandable card details with examples, components, related words, semantic notes.

**練習 Drill** — Flashcard study sessions. Configurable: category selection, card count, Chinese→English or English→Chinese modes. Flip-card animation. Progress dots. Keyboard shortcuts (arrow keys). Completion screen with stats. Touch swipe navigation on mobile.

**鍛造 Forge** — AI-powered nugget creation. Enter any Chinese word/phrase, get a fully enriched card (traditional/simplified, pinyin, English, category, depth, components, examples, related words, semantic notes). Two API options: Groq (free, Meta's Llama) and Anthropic (Claude Sonnet, premium). Keys stored in localStorage.

**工坊 Workshop** — AI-generated contextual dialogues. Topic selection (preset or custom), character roster management, dialogue generation via Groq API. Designed around HSK-level constraints per the HSK Framework Report.

### Design System
- Ink & paper aesthetic: rice (#f5f0e8), sand, ink color palette
- Context-dependent accent colors: jade (Browse), vermillion (Drill), copper (Forge), gold (Workshop)
- Paper texture overlay (SVG fractal noise)
- 3 themes: Night Study (dark), Bamboo Grove (sage/jade), Clean Slate (minimalist white)
- Mobile-first: 480px max-width, touch-friendly

### Deck Architecture: Hardcoded (HSK 1–4) + Supabase (HSK 5–6)

HSK 1–4 and the original nugget decks are hardcoded arrays in `index.html`. HSK 5 and HSK 6 are fetched live from Supabase on load via `fetchCards()` (see `// ========== SUPABASE ==========` block, ~line 8272). The app paginates in batches of 1,000 rows since Supabase caps single queries there.

**Supabase project:** `fkgjduganefwmakxxnqt.supabase.co`
**Tables:** `decks` (one row per category, holds UUID), `cards` (all HSK5/6 cards, keyed by `deck_id`)
**anon key** (read-only, safe for client): in `index.html` Supabase init block
**service key** (write access): in `upload-hsk6.js` and `upload-batch02.js` — do NOT expose client-side

### Hardcoded Decks (index.html)

**HSK 1 deck:** 150 words (category: `hsk1`). IDs 1001–1150.
**HSK 2 deck:** 151 words (category: `hsk2`). IDs 1201–1351. Aligned to Hanban September 2012 official vocabulary list (source: `glxxyz/hskhsk.com` GitHub repo, file `HSK Official 2012 L2.txt`). Verified 2026-04-13.
**HSK 3 deck:** 301 words (category: `hsk3`). IDs 1401–1701.
**HSK 4 deck:** 600 words (category: `hsk4`). IDs 1801–2400. Built 2026-04-28 from `HSK Official 2012 L4.txt`. Trad-first with Taiwan-modern overrides (台 not 臺, 聯絡 not 聯繫, 支持 rolled back from OpenCC's 支援, 通過 rolled back from 透過). Pinyin auto-generated via pypinyin then hand-corrected for ~25 light-tone/heteronym cases. Two intentional duplicates with HSK 2 (得 děi modal vs HSK 2 particle de; 等 etc./until vs HSK 2 wait) — different senses, separate cards. Ten intentional duplicates with original NUGGETS deck (交流, 關鍵, 內容, 功夫, 堅持, 開心, 整理, 生活, 錯誤, 隨便) — kept for Hanban faithfulness.
**Original deck:** 164 words across vocab/phrase/idiom/concept.

### Supabase Decks (fetched at runtime)

**HSK 5 deck:** 1,291 cards (category: `hsk5`). IDs 2401–3691. Source: `HSK Official 2012 L5.txt`. Skeleton generated via `scripts/hsk5_skeleton.py`. In Supabase as of 2026-05. ~30 cards enriched (early sample batch only) — enrichment pipeline not yet started in earnest. See `markdowns/hsk5-pipeline.md` for full pipeline spec.

**HSK 6 deck:** 2,500 cards (category: `hsk6`). IDs 5001–7500. Source: `data/hsk6-source-with-defs.txt` (from `glxxyz/hskhsk.com`, `HSK Official With Definitions 2012 L6.txt`). Skeleton at `data/hsk6-skeleton.json`.

**HSK 6 enrichment status (as of 2026-07-01):**
| Range | Status |
|---|---|
| 5001–5010 | ✅ Enriched (batch-01, `data/hsk6-enriched-batch-01.json`) |
| 5011–6010 | ✅ Enriched (batch-02, `data/hsk6-enriched-batch-02.json`) |
| 6011–6900 | ✅ Enriched (consolidated into `data/hsk6-enriched.json`, via `/tmp/patch_hsk6.py` batches) |
| 6901–7500 | ⬜ Skeleton only (600 cards remaining) |

**Total enriched: 1,900 / 2,500 cards** — last Supabase sync not yet re-run this session (see STATUS.md 2026-07-01 entry for the hardcoded service_role key flag before next `node upload-hsk6-enriched.js` run).

### HSK 6 Enrichment Format

Each enriched card requires these fields (beyond the skeleton's trad/simp/pinyin/english):

```json
{
  "id": 5011,
  "traditional": "案例",
  "simplified": "案例",
  "pinyin": "ànlì",
  "english": "case; example case",
  "category": "hsk6",
  "depth": "basic",
  "pos": "n",
  "semanticNote": "Taiwan-focused register/usage note...",
  "components": [{ "char": "案", "pinyin": "àn", "meaning": "case; record" }],
  "examples": [
    { "sentence": "Traditional character example sentence.", "translation": "English translation." }
  ]
}
```

Key conventions:
- `semanticNote`: Taiwan-focused — register (formal/casual), Taiwan pronunciation preferences, heteronym alerts, comparisons to similar words, cultural context, set phrases
- `examples`: Always use **traditional characters**. Exactly 2 per card. Must contain the target word.
- IDs **must be looked up from the skeleton** (`data/hsk6-skeleton.json`) before writing — never guess from position. Use the `simp_to_id` lookup.

### HSK 6 Upload Scripts

**`upload-hsk6.js`** — Deletes all HSK6 cards from Supabase and re-uploads the full skeleton. Use to reset to skeleton state.

**`upload-batch02.js`** — Upserts `data/hsk6-enriched-batch-02.json` (1,000 cards) to Supabase using `resolution=merge-duplicates`. Batch-01 has no dedicated script — upload inline.

**Bug fixed 2026-05-17:** Both scripts had a `...options` spread that overwrote the merged `headers` object (stripping the API key whenever `options.headers` was passed). Fixed by destructuring `{ headers: extraHeaders, ...rest } = options`.

**Validation helper:** `/tmp/append_batch.py` — reads new cards from stdin JSON, validates IDs against skeleton (`simp_to_id` lookup), sorts, and appends to batch-02. Exits with error on any ID mismatch.

### Architecture Rules (for dev sessions)
- Single-file HTML — all CSS, JS, and HTML in one file
- Mobile-first: test against iPhone 13 Mini viewport
- Long-press (500ms) for pinyin on mobile, hover on desktop — NEVER use inline `ontouchstart` handlers
- Use `e.target.closest()` for click delegation (NOT `e.target.classList.contains()`)
- `box-decoration-break: clone` for tight-wrapping inline text backgrounds
- Canvas-based binary search for pinyin-to-character width matching (`matchPinyinWidth`)
- When removing HTML elements, ALWAYS check for JS `getElementById` references that will cause cascade failures

### HSK Framework (planning doc: HSK_Framework_Report_Nuggets_Stage.md)
Workshop uses HSK levels (1-6) to constrain generated dialogue: vocabulary scope, grammar patterns, sentence complexity, topic coherence, and register. Replaces the old formality/register dropdowns with a single HSK level picker.

### HSK Preset Deck Rules (established 2026-04-13)
- **Source of truth:** Hanban September 2012 official vocabulary lists (`glxxyz/hskhsk.com` GitHub repo)
- **Pill label format:** `HSK 1`, `HSK 2`, etc. — uppercase HSK, space before number, no parentheses (the pill shape itself is the container). Applied in both `getCategoryLabel()` and `getCategoryLabelBilingual()`.
- **Each card must have:** exact pinyin with tone marks, exactly 2 example sentences, each example MUST contain the target word/phrase itself.
- **Hanban alignment:** use the exact word forms from the Hanban file (e.g., 男 not 男人, 女 not 女人, 对 appears once covering both meanings).
- **Apply this format to all future HSK preset decks (HSK 3, 4, 5, 6).**

### Terminology (updated 2026-04-13)
- **"Decks" not "categories."** The word "category" is being phased out entirely. Use "deck" everywhere in UI text, code comments, and documentation. The underlying `category` field in data structures remains for backwards compatibility, but user-facing language is always "deck."

### Deck System Design (locked 2026-04-13)

**Deck scope rule:** User-created deck assignment is **exclusive** — a card assigned to a user deck ONLY appears under that deck's filter. Not under Custom, not under Vocab/Phrase/etc. This is intentional: user decks are curated sets, not just extra tags.

**Exception — built-in pack membership:** A built-in card (HSK1, HSK2, Vocab, etc.) that is added to a user deck still also appears in its original pack filter. The exclusive rule applies to user-deck slots, not to co-existence with built-in packs.

**Built-in cards in user decks:** Any card (forged OR built-in preset) can be added to a user-created deck. This requires a separate membership overlay in localStorage (`zifang-deck-memberships`) rather than modifying the hardcoded card arrays. Format: `{ [cardId]: userDeckId }` (one-to-one: each card can be in at most one user deck).

**Custom = the default catch-all:** "Custom" is the permanent home for all forged cards that haven't been assigned to a named user deck. It is NOT a user-created deck — it's a system deck. Cards land in Custom on forge by default. Custom should be a visible, selectable option in all deck assignment UIs, not just an invisible fallback.

**User deck slot rule:** Each card has at most one user-deck assignment. Moving a card from deck A to deck B replaces the assignment — it doesn't create a copy. A card cannot be in two user-created decks simultaneously.

### Forge Flow (locked 2026-04-13)

**Current flow (what exists):**
1. User forges a card → card auto-saved to Custom immediately
2. Category sheet opens → user can assign to a named user deck
3. Status message says "saved to Custom & vocab" — confusing if user then reassigns

**Target flow (approved design):**
1. User forges a card → card auto-saved to Custom (as fallback, no change here)
2. Category sheet opens → **Custom is now a visible squircle option** (first in the row, vermillion, always present), plus any named user decks
3. User can: tap a named deck (moves card from Custom to that deck), tap Custom explicitly (confirms it stays in Custom), or dismiss the sheet (card stays in Custom, no assignment change)
4. Status message after category assignment reflects the actual destination: "Saved to [deck name]" or "Saved to Custom" — not the misleading "Custom & vocab" message

**Why Custom must be explicit:** Tim confirmed this — users need a clear "just put it in Custom" option. Currently the sheet only shows user-created decks and a + button. Closing without selecting anything implicitly keeps it in Custom, but that's invisible and confusing. Making Custom a tappable first option eliminates the ambiguity.

### Move to Deck — Entry Points (deferred, 2026-04-13)
Decision deferred to a future session. Known entry points to consider:
- Expanded card view in Browse (most natural placement)
- Delete modal "Move to another deck" button (currently placeholder/disabled)
- Long-press / swipe gesture on card in Browse
- Packs panel bulk management screen
Current state: "Move to another deck" button exists in delete modal but is disabled with no logic. Will be wired when the full deck-move feature is built.

### Card UI (updated 2026-04-13)
- **No bottom divider line.** The `.detail-divider` element was removed from expanded card details. Card content ends right after the last example sentence.
- **Notch design:** The last example sentence box has an inverted quarter-circle cutout (30x30px) in its bottom-right corner, created via `::after` pseudo-element with `border-top-left-radius: 30px` and `background: var(--rice-light)`. The action icon sits inside this scooped-out area.
- **Action icons:** Delete (trashcan SVG, custom cards only) and Hide (eye-slash SVG, preset cards only) are bare icon buttons — no border, no background, no text label. Positioned absolutely inside the last `.example-item` at `bottom: 0; right: 0`, offset 2px each for visual balance.
- **Delete confirmation:** Opens a centered modal (`.delete-modal-backdrop` / `.delete-modal-card`) with danger triangle icon, "Delete this card?" title, and three buttons: "Delete card" (vermillion), "Move to another deck" (dashed, disabled/placeholder), "Cancel". Backdrop click also closes.
- **Hide action:** Single-tap, no confirmation needed (reversible via Settings).
- **Icon size:** 14x14px SVG inside a 22x22px button area.

### Score-based Drill Selection + Session Log (added 2026-04-26)

**Selection driver:** `zifang-card-scores` localStorage key. Each card has an integer score 0-3:
- 0 = unseen OR last action was 'struggle' → top priority
- 1 = seen + got it once
- 2 = got it twice
- 3 = mastered (capped — see less often)

"Got it" → `score = min(score + 1, 3)`. "Struggle" → `score = 0`. Card surfacing without a verdict does NOT change the score. Migration on first load: cards with `seen > 0` in legacy `zifang-card-stats` start at score 1; everything else 0.

**Selection weights** (raffle-ticket model): score 0 → 4 tickets, 1 → 2, 2 → 1, 3 → 0.5. Implemented in `getCardWeight()` (index.html ~line 8550). `weightedRandomSample()` body unchanged.

**Session ledger:** `zifang-sessions` localStorage key. Array of session objects with `id`, `startedAt`, `endedAt`, `decks`, `direction`, `cardCount`, `cardIds`, `events` (per-card seen/got/struggle log), `completed`, `abandoned`. Hard cap 500 sessions (oldest dropped). State variable `state.drill.currentSessionId` tracks the active session in memory.

**Session lifecycle:**
- Start: `sessionStart()` called inside `startDrillSession()` after pool generation
- Update: every "got it" / "struggle" tap appends a `sessionAppendEvent()` call
- End on completion screen: `sessionFinalize(id, { completed: true })`
- No auto-abandon. Sessions stay open indefinitely (Pleco-style resume)
- Resume prompt fires when user clicks Start with an open session in the ledger

**UI surfaces:**
- Drill completion screen has a "Past sessions ›" text link (id `complete-history-btn`)
- Sessions modal (`#sessions-modal-backdrop`) lists all sessions, tap-to-expand for per-card breakdown
- Settings → Progress pane (third tab) shows lifetime totals, 7-day SVG bar chart, "Show all sessions" link

**Backup format updated to v1.1** — adds `cardScores` and `sessions` keys to the JSON export at `exportZifangBackup()`.

**Spec doc:** `markdowns/zifang-session-system-plan.md`.

### Cross-Tab State Consistency (established 2026-04-13)
- **Principle:** All 4 tabs must reflect state changes in real-time without page refresh. Deleting, hiding, or adding a card in one tab must immediately propagate to all others.
- **Implementation:** `_finishDeleteCard()` and `_finishHideCard()` both update Browse, Drill (remove from active pool, adjust index, clear gotIt/seen sets, end session if pool empties), and Workshop (re-render user category pills + vocab picker).
- **Drill pool integrity:** When a card is deleted/hidden mid-session, it is spliced from `state.drill.pool`, the index is clamped, and `saveDrillSession()` persists the change. If the pool hits zero, the session ends gracefully.
- **This principle applies to ALL future state-changing operations.** Any function that modifies the card set must propagate to every tab.

---

## 2. PENDING QUEUE

*Last updated: 2026-04-09*

Each item below is a discrete session task. Tackle one at a time.

**1 · Forge card edit-before-save** — after generation, show the card in an editable review state before committing it to the deck.

**2 · Export custom cards to JSON** — download all user-created (Custom) cards as a JSON backup that lives outside localStorage.

**3 · Workshop character roster UX review** — UX pass on the Workshop tab's character list; scope TBD.

**4 · Activity log + session stats** — track every user action (taps, flips, correct/incorrect, time spent, cards reviewed) and store alongside other localStorage data. Tapping a session entry surfaces stats. Stretch: chart progress over time. Data should be exportable with the rest.

**5 · "Understanding Zifang" onboarding section** — in-app explainer covering: what each tab does, how Forge works, what the struggling system tracks, how to use settings, and what all the icons mean. Could live as a help modal or a dedicated panel.

**6 · Struggling algorithm audit** — document exactly how the struggling system works: what triggers a card to enter struggling, what the score range is, how many correct/incorrect passes move the score up or down, what the ranking terminology is. Also evaluate whether a "true random" mode (ignoring card score) is worth adding as a toggle.

**7 · ~~Forge input robustness~~** — DONE (2026-04-10). Implemented: Chinese/English detection via Unicode ranges, client-side gibberish filter, English→Chinese translation review panel (LLM-powered suggestions), manual Chinese input fallback, and category assignment bottom sheet (replaces auto-save-to-Custom). New localStorage key: `zifang-user-categories` stores user-created categories with auto-assigned colors.

**8 · ~~Card and deck deletion~~** — PARTIALLY DONE (2026-04-13). Individual card deletion: implemented with modal confirmation (danger triangle, "Delete card" / "Move to another deck" / "Cancel"). Cross-tab state propagation: delete and hide now update Browse, Drill (pool splice + index clamp), and Workshop. Deck deletion: already existed (`executeDeleteCategory`). Remaining: "Move to another deck" button is placeholder/disabled — needs deck picker UI when move-to-deck feature lands (deferred, see Deck System Design spec above).

**9 · Forge flow + deck system overhaul** — DESIGNED (2026-04-13), not yet built. Two parts:
  - **Part A · Custom squircle in category sheet:** Add a permanent "Custom" squircle button (vermillion, first in row) to the forge category sheet (`renderCategorySquircles`). Tapping it confirms the card stays in Custom and closes the sheet. Fix the success status message to say "Saved to Custom" or "Saved to [deck]" instead of the misleading "Custom & vocab."
  - **Part B · Built-in cards in user decks + deck membership overlay:** New localStorage key `zifang-deck-memberships` (format: `{ [cardId]: userDeckId }`). Overlay applied in `getBrowseFiltered()` and `getDrillFiltered()`. UI entry points for adding a built-in card to a user deck: deferred (see "Move to Deck — Entry Points" in spec above). Data layer can be built first, UI wired later.

---

## 3. DEV SESSION CHECKLIST

- [ ] Single-file HTML — everything in one file
- [ ] Mobile-first: iPhone 13 Mini viewport
- [ ] Use `e.target.closest()` for click delegation
- [ ] Check for JS `getElementById` references before removing HTML elements
- [ ] Test all 4 tabs after changes

---

## Related Docs

- `markdowns/zifang-design-system.md` — Full component inventory, token list, UX specifications
- `markdowns/zifang-audit-checklist.md` — Periodic audit procedure
- `markdowns/zifang-audit-2026-04-09.md` — Most recent audit
- `markdowns/HSK_Framework_Report_Nuggets_Stage.md` — Workshop HSK constraints
- `markdowns/spicy-mode-upgrade-proposal.md` — Workshop explicit dialogue generation proposal
