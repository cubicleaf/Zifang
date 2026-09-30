**Document status: Archived — 2026-09-29.** Preserved for historical reference.

# 字坊 · Full UX Audit
*April 3, 2026 · Design System + UX Copy + User Flows*

---

## Overview

This audit covers all four tabs (Browse / Drill / Forge / Workshop) using three lenses: design system consistency, UX copy quality, and user flow clarity. Findings are grouped by severity.

---

## 1. DESIGN SYSTEM AUDIT

### 1a. Naming Inconsistencies (same component, different names)

The biggest structural issue in the codebase is that the same visual pattern gets reinvented with new class names in each tab. This makes the CSS longer than it needs to be and makes future changes harder.

| Pattern | Browse | Drill | Workshop |
|---------|--------|-------|----------|
| Category filter pill | `.cat-bubble` | `.setup-cat-bubble` | `.vocab-cat-pill` |
| Toggle (select all/clear) | `.cat-toggle-btn` | `.drill-cat-toggle-btn` | n/a |
| Segment switcher | `.segment-btn` | `.mode-seg-btn` | n/a |

**Recommendation:** Pick one name per component. `.filter-pill` for all category buttons. `.segment-btn` for all segment controls. This is low-urgency but worth doing on any major refactor pass.

---

### 1b. Hardcoded Color Values (should use CSS tokens)

The `:root` block defines nice token names like `--jade-soft` and `--gold-soft`, but then the unselected state for category bubbles hardcodes the same colors at a different opacity instead of using the tokens.

**Examples of hardcoded values that should reference tokens:**
- `.cat-bubble.unselected`: uses `rgba(45, 106, 79, 0.07)` — should be a token like `--jade-ghost` or `--jade-soft` at reduced opacity
- `.cat-bubble.cat-favorites.unselected`: uses `rgba(184, 134, 11, 0.07)` — same issue for gold
- `.setup-cat-bubble.unselected` (Drill): uses `rgba(70, 130, 180, 0.06)` — this uses BLUE instead of jade for the default category unselected state. Browse uses jade, Drill uses blue. These should match.

**Note:** The Browse and Drill tabs use *different accent colors* for unselected category pills — Browse is jade-tinted, Drill is blue-tinted. This is probably unintentional and creates subtle visual incoherence.

---

### 1c. Token Usage — `--mauve` defined but underused

`--mauve: #7d5080` and `--mauve-soft` are defined in `:root` but don't appear in any visible component styles I found. Either they're used in JS-injected styles or they're vestigial. Worth auditing.

---

### 1d. Good Token Usage (worth keeping)

The shadow tokens (`--shadow-sm`, `--shadow-md`), border radius (`--radius`, `--radius-sm`), and easing (`--ease`) are consistently applied throughout. The color palette is genuinely well-constructed — rice/sand/ink/jade/vermillion reads as a coherent system. The left accent bar on `.card::before` is a nice detail.

---

## 2. UX COPY AUDIT

### 2a. Labels That Are Doing Their Job Well

These are copy decisions that work and should be preserved:

- **"✗ Struggling" / "✓ Got it"** — clear, action-oriented, emotionally appropriate for flashcard grading
- **"Writing your scene..."** — the loading state for Workshop is warm and contextual, not generic
- **"Craft Mandarin dialogues from your vocabulary"** — Forge's subtitle explains the value clearly
- **"Generate Dialogue"** with 生成 hover — the bilingual CTA pattern is distinctive and on-brand
- **"Regenerate"** on output — short, obvious
- **"Too many words selected (max 12). The dialogue would lose coherence."** — the "why" explanation is excellent
- **"Select at least one vocabulary word first."** — clear, but could be warmer (see below)
- Error messages in `friendlyGroqError()` — genuinely excellent. Specific, actionable, tells you exactly how long to wait and where to go. This is better error handling than most commercial apps.
- **"Or type your own scene"** in topic picker — clear label for the custom input

---

### 2b. Copy Issues

**Browse — Empty State:**
```
沒有啦😗
```
This works but the emoji makes it feel slightly out of character with the rest of the aesthetic. The copy is cute but gives no actionable guidance. If you search "xyz" and get this, you don't know whether to try a different search, clear filters, or if you just typed the wrong thing.

*Suggested fix:* `沒有啦 · No matches. Try a different search or clear your filters.`

---

**Drill Setup — Subtitle:**
```
Configure your session
```
This is the weakest copy in the app. It's technically accurate but dead. You're on a Chinese learning app, and the setup screen just says "Configure your session" like enterprise software.

*Suggested fix:* `What are we drilling today?` or just remove it — the section labels (Categories, Count, Mode) are self-explanatory.

---

**Drill Complete Screen:**
```
完成！ / Session complete
```
"Session complete" as a static subtitle is flat. There's no acknowledgment of what was accomplished. The stats below (Total: 25, Vocab: 12, etc.) are already there — the subtitle doesn't need to do more work — but it's a missed opportunity for something memorable.

*Suggested fix:* Could dynamically vary this: "Not bad.", "Clean sweep.", "Keep going." based on score. Or just remove the subtitle entirely since 完成！ already lands the message.

---

**Workshop — "Use Credits to Enrich":**
This button appears in the Character Creator. "Credits" is unexplained anywhere. What is a credit? How many do I have? Where do I get more? This creates confusion and looks like a broken feature.

*Two options:*
1. If it's not functional yet: remove or hide the button
2. If it is functional: rename to "Enrich with AI" and add a tooltip or footnote explaining the credit system

---

**Workshop — Stage dot controls (度/級/人/字):**
These four glyphs control Length, HSK Level, Speakers, and Character Set. There are no English labels — the Chinese glyphs are the only indicator. For a learner at HSK 2-3, 度 (degree/length) and 級 (level) are recognizable, but a first-time user has no idea what these controls do.

Current: just the glyph and options
*Suggested fix:* Add a small English tooltip or static subtitle below each glyph. Example:
- 度 · Length
- 級 · HSK Level
- 人 · Speakers
- 字 · Script

---

**Forge — Input Placeholder:**
```
輸入漢字或詞語⋯
```
The placeholder is Chinese-only. The Forge subtitle says "any Chinese word or phrase" so this is technically consistent — but a new user who doesn't know what 輸入 means might not realize they need to type *here*. This is minor but worth flagging.

*Optional fix:* `輸入漢字或詞語 · type a word or phrase`

---

**Browse — Category Buttons Mix Languages Inconsistently:**
- Browse buttons: Chinese span + English text (e.g., `<span>詞彙</span> Vocab`)
- Drill category buttons: Chinese only (no English translation)
- Workshop vocab picker: Chinese only (no English)

This inconsistency means Browse is accessible to beginners but the other tabs assume more confidence. Given the app is a learning tool, this feels like an oversight rather than a deliberate choice.

---

**The "Custom" Button in Vocab Picker:**
The "Custom" button in Workshop's vocab picker clears the selection and focuses the search input — but from the user's perspective it's not obvious this is what it does. It looks like it would open a "custom words" view. The button label doesn't describe what it actually does.

*Suggested fix:* Rename to "Type words" or "Search" or just remove it (since the search field is already visible above it).

---

**Spicy Mode Password Screen:**
```
这个功能是锁着的
```
This uses *Simplified* Chinese (`锁`) inside an app that defaults to Traditional (`鎖`). Small inconsistency but worth noting: `這個功能是鎖著的`.

---

**Browse — "全選 All" toggle button:**
The CTA mixes scripts — `全選 All`. This pattern is used throughout the app (it's intentional and kind of charming), but it's worth flagging that it's only used in Browse and Drill toggles, not elsewhere. Decide whether it's a system-wide pattern or an exception.

---

## 3. USER FLOW AUDIT

### 3a. The Biggest Flow Problem: Workshop Cast is Buried

To add a character in Workshop:
1. User opens the Stage tab
2. User taps the **Topic pill** (场)
3. In the Topic modal, at the *bottom*, they see 人物 Cast
4. They tap the **+** button to open the Character Creator
5. They fill out 7 fields
6. They tap Save

The Cast section lives *inside the Topic modal*. These are separate concerns — a topic ("eating out") and a cast of characters should be separate choices. A new user will never discover characters exist without stumbling on them while setting a topic.

**Recommendation:** Bring Cast out of the Topic modal and make it a third pill in the Stage pills row alongside Words and Topic. Something like:
```
[词 3 words]  [场 Eating out]  [人 2 cast]
```
This surfaces the feature, clarifies the hierarchy, and lets each choice live in its own modal.

---

### 3b. Drill — "Struggling" Category UX

The "Struggling" filter button appears in the Drill setup as a peer of Vocab/Phrase/Idiom/Concept/Custom — but it's actually a different *kind* of filter (it's a cross-category behavioral flag, not a semantic category). A user who hasn't had any cards flagged will tap it and wonder why they get zero results, or not understand what it means.

**Recommendation:** Visually separate it from the content categories. It could sit below the category row with a small label: "or drill by history" / or just appear dimmed until there are cards in it.

---

### 3c. Missing: Score/Progress Feedback in Drill

The completion screen shows total cards and mode, but not the score. The grading buttons (✗ Struggling / ✓ Got it) accept input but the results aren't reflected in the complete screen. A user who graded every card "Got it" gets the same screen as one who graded everything "Struggling."

This is the core of Z-02 (struggling pile), but even before implementing cross-session memory, showing the session score (e.g., "22/25 got it") would close the feedback loop.

---

### 3d. Browse — Category Filter Consumes too Much Vertical Space (Z-03)

Current layout: 2-column bubble grid, ~3 rows = roughly 120-140px used just for category filtering before you see any cards. On a 480px-wide phone, that's 20%+ of the screen gone to navigation chrome before content starts.

This is the confirmed Z-03 fix. The horizontal pill strip would cut this to ~44px (one row). Easy win.

---

### 3e. Forge — No Edit Before Save (Z-04)

The Forge generates a card and the only options are to save it as-is or discard. AI output is occasionally wrong — wrong tones, questionable example sentences, cultural errors. With no edit step, bad cards enter the deck permanently.

This is Z-04. It's a critical flow gap given the app's learning purpose.

---

### 3f. Custom Cards — No Backup (Z-05)

If localStorage is cleared, all Forge-created cards are gone. There's no export, no cloud backup, no warning. For a deck that a user has been building over weeks, this is a real risk.

---

### 3g. Workshop Dialogues — Generated and Gone (Z-07)

After Workshop generates a dialogue, there's no save button. Interesting output is immediately at risk of being lost. This gap is more visible to users than the custom card backup issue because the loss is *immediate* (close the tab, done) vs. eventual (localStorage clearing).

---

## 4. PRIORITIZED RECOMMENDATIONS

### Tier 1 — High Impact, Relatively Easy

1. **Add Cast as a third pill in Stage (Z-06 variant)** — surfaces hidden feature, fixes the buried flow. Probably 30-40 lines of JS + a small CSS addition.

2. **Drill setup subtitle: replace "Configure your session"** — one-line copy change, zero code change.

3. **Completion screen: show session score** — "22/25 got it" would make the whole Drill loop feel rewarding. Needs ~10 lines of JS to track grades during session.

4. **Workshop dot controls: add English sublabels** — simple HTML change, zero JS.

5. **Browse → horizontal pill strip (Z-03)** — recovers ~100px of screen real estate. CSS-only or near-CSS.

### Tier 2 — Medium Impact, More Work

6. **Z-04: Forge edit-before-save** — prevents bad AI cards from entering the deck. Core data quality fix.

7. **Z-07: Save Workshop dialogues** — localStorage + simple list view. Users who generate anything good currently lose it.

8. **"Use Credits to Enrich" — fix or remove** — either explain the credit system clearly or pull the button until it's ready.

### Tier 3 — Polish + Architecture

9. **Unify category pill naming** (`.cat-bubble` / `.setup-cat-bubble` / `.vocab-cat-pill` → one class) — CSS cleanup, no user-facing change.

10. **Token-ify unselected state colors** — define `--jade-ghost`, use it consistently across Browse + Drill.

11. **Z-05: Export custom cards to JSON** — important for data resilience, low urgency until deck grows.

12. **Z-02: Struggling pile cross-session tracking** — high value eventually, but needs localStorage schema design first.

---

## 5. THINGS THAT ARE WORKING WELL (DON'T TOUCH)

- The overall visual language — rice/sand/ink/jade is distinctive and feels handmade
- The hover-pinyin system — elegant, unobtrusive, consistent
- Error messages in `friendlyGroqError()` — among the best copy in the app
- The flip card animation and progress dots in Drill
- Character Creator field design (Name/Role/Want/Fear/Quirk) — surprisingly thoughtful character design tool
- The left accent bar on Browse cards (`::before`)
- Bilingual section labels (Chinese + English with hover pinyin) throughout
- The 造人 Character Creator title — genuinely fun
- Stage topic presets ("Surprise me", "Eating out", etc.) — right level of specificity
- The paper texture overlay — subtle but contributes to the handcrafted feel

---

*Audit complete. Next step: pick a Tier 1 item and build it.*
