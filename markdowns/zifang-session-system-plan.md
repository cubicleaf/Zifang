# Zifang — Session System + Score-based Selection Plan

**Created:** 2026-04-26
**Status:** Approved, not yet built
**Replaces queue items:** #4 (Activity log + session stats) + #6 (Struggling algorithm audit) — merged into one initiative

---

## Decisions locked

- **Session definition:** any drill where ≥1 flashcard surfaces.
- **Persistence:** existing localStorage write-on-every-action pattern. Sessions stay open indefinitely (Pleco-style resume). No auto-abandon timeout.
- **Score system:** per-card integer 0-3.
  - Default: 0 (top priority)
  - "Got it" code: `score = min(score + 1, 3)`
  - "Struggle" code: `score = 0`
  - Card surfacing without a verdict: no score change.
- **Selection weights:** 0 → 4 tickets, 1 → 2 tickets, 2 → 1 ticket, 3 → 0.5 tickets. Weighted random sampling without replacement.
- **UI surfaces:** Drill completion screen + Settings → Progress section.

---

## Data layer

### New localStorage keys

**`zifang-card-scores`** — `{ [cardId]: number }`. Score range 0-3. Cards not present default to 0.

**`zifang-sessions`** — array of session objects:

```js
{
  id: 'sess_1714075200000',
  type: 'drill',
  startedAt: 1714075200000,
  endedAt: null,                    // null while in progress
  decks: ['hsk1', 'hsk2'],          // active deck filters at start
  direction: 'zh-en',
  cardCount: 20,                    // requested size
  cardIds: [1001, 1004, ...],       // every card surfaced
  events: [
    { t: 1714075203000, cardId: 1001, action: 'seen' },
    { t: 1714075208000, cardId: 1001, action: 'got' },
    { t: 1714075228000, cardId: 1004, action: 'struggle' }
  ],
  completed: false
}
```

### Existing key kept

**`zifang-card-stats`** — leave in place for now. May be referenced elsewhere. Deprecate gradually after Phase 1 ships.

---

## Selection algorithm

Replaces `getCardWeight()` and `weightedRandomSample()` at lines 8586-8624 of `index.html`.

```js
const SCORE_WEIGHTS = { 0: 4, 1: 2, 2: 1, 3: 0.5 };

function getCardWeight(cardId) {
  const scores = loadCardScores();
  const score = scores[cardId] ?? 0;
  return SCORE_WEIGHTS[score] ?? 4;
}
```

`weightedRandomSample()` body stays nearly identical — only the weight lookup changes.

---

## Score update on code

Replace `recordCardGotIt(cardId)` and `recordCardStruggle(cardId)`:

```js
function recordCardGotIt(cardId) {
  const scores = loadCardScores();
  const current = scores[cardId] ?? 0;
  scores[cardId] = Math.min(current + 1, 3);
  saveCardScores(scores);
}

function recordCardStruggle(cardId) {
  const scores = loadCardScores();
  scores[cardId] = 0;
  saveCardScores(scores);
}
```

`recordCardSeen()` becomes a no-op for scoring but still appends to the session events log.

---

## Session lifecycle

| Trigger | Action |
|---|---|
| First card surfaces in Drill tab | Create new session, push to `zifang-sessions` |
| Card surfaces (subsequent) | Append `{ action: 'seen' }` event |
| User taps "Got it" | Update score, append `{ action: 'got' }` event |
| User taps "Struggle" | Update score, append `{ action: 'struggle' }` event |
| User reaches completion screen | Set `endedAt` + `completed: true` |
| User starts new drill while session open | Prompt: "Resume (X cards left) or start new?" |

Every event write also commits to localStorage immediately (no batching).

---

## Migration

When the new system loads for the first time:

```js
function migrateCardStatsToScores() {
  if (localStorage.getItem('zifang-card-scores')) return;  // already migrated
  const oldStats = JSON.parse(localStorage.getItem('zifang-card-stats') || '{}');
  const scores = {};
  for (const [cardId, s] of Object.entries(oldStats)) {
    scores[cardId] = s.seen > 0 ? 1 : 0;
  }
  localStorage.setItem('zifang-card-scores', JSON.stringify(scores));
}
```

Cards with any drill history → score 1. Everything else → 0 (default). Loses struggle-rate fidelity; rebuilds within a few sessions.

---

## Backup integration

Two-line addition at line ~14405:

```js
cardScores:   safeJSON('zifang-card-scores')   || {},
sessions:     safeJSON('zifang-sessions')      || []
```

Plus matching imports in the restore flow.

---

## Build phases

**Phase 1 — Algorithm + score storage.**
Migration runs once. Old `getCardWeight` / `recordCardGotIt` / `recordCardStruggle` replaced. No UI change. Drill behavior should immediately feel different — struggling cards reappear faster, mastered cards back off.

**Phase 2 — Session log (silent).**
Session create/update/finalize wired into existing drill flow. Writes only — no UI surface. Verify via localStorage inspection.

**Phase 3 — Drill completion screen update.**
Add "Past sessions ›" text link in accent color below existing completion stats. Tap → opens session list modal (built in Phase 4).

**Phase 4 — Session list modal.**
Scrollable list of session rows: date/time, decks badge, score, duration. Tap row to expand inline (accordion) for per-card breakdown. Modal entrance follows standard pattern (backdrop fade, card scale 0.96→1 + translate 8px→0, 0.25s, `cubic-bezier(0.25, 0.1, 0.25, 1)`).

**Phase 5 — Settings → Progress section.**
- Lifetime totals: drills completed, cards reviewed, average score
- 7-day bar chart of cards reviewed (vanilla SVG, no library)
- "Show all sessions" link → same modal as Phase 4

**Phase 6 — Resume prompt.**
On Drill tab open with an `endedAt: null` session: modal asking "Resume previous session (X cards remaining) or start new?"

---

## Out of scope

Deferred for separate features:

- Forge / Workshop activity counters
- Trend charts beyond 7-day bar
- Custom weight tuning UI
- Per-deck stats breakdown
- Streak counter / daily goal flags

---

## Risk notes

1. Phase 1 alone is the highest-impact, lowest-effort win. Ship it standalone to feel the difference before building the UI.
2. Session list modal (Phase 4) is the most likely to balloon. Resist filter/sort/search add-ons.
3. 7-day bar chart (Phase 5) takes longer than expected. Date math, empty-day handling, axis labels.
4. Migration silently changes drill behavior. Cards drilled many times will start at score 1, not 3. First few post-migration drills will feel slightly off; recovers within a couple sessions.

---

## Files touched

- `index.html` — algorithm replacement (lines 8546-8625), session lifecycle hooks in drill flow, completion screen update, modal HTML/CSS/JS, settings panel additions
- `markdowns/zifang-pending-queue.md` — mark items 4 and 6 as merged
- `markdowns/zifang-project-knowledge.md` — update §2 pending queue, add session-system reference under §1

---

*Spec authored during 2026-04-26 design session.*
