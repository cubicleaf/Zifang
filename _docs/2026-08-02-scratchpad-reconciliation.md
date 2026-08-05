# Scratchpad reconciliation — 2026-08-02

**What this is.** Tim's out-of-repo scratch notes (13 bullets), decomposed into 20 atomic
line-items and reconciled against `index.html` at commit `e7a034c`. Every verdict carries a
locator. Where a claim was testable, it was tested with a script rather than reasoned about.

**Headline:** 11 of 20 line-items (55%) were already resolved or rest on a premise that is no
longer true. Only 9 are live, and of those, 2 should be killed outright. The notes did not go
stale because the ideas were bad — they went stale because this project has no return path
from finished work back to the place the ideas were written down.

---

## 1 · Verdict table

| # | Atomic line-item | Verdict | Locator | Confidence |
|---|---|---|---|---|
| 1a | Variable font size for Chinese characters on Drill cards | **Done differently** | `index.html:9997-10004`, `9833-9871`, `2197-2207` | Certain |
| 2a | Hover-pinyin protocol on the Workshop cast squircle buttons | **Not started** | `index.html:8027-8039` | Certain |
| 3a | "Use Credits to Enrich" button functions | **Done** | `index.html:8140`, `16749-16800` | Certain |
| 3b | Button consumes credits / uses the paid model | **Premise false** | `index.html:16780` vs `7732-7740` | Certain |
| 4a | Default state of the 3 deck carousels is nothing selected | **Done** | `index.html:8402-8407` | Certain |
| 4b | Nothing-selected renders all cards in all 3 carousels | **Premise false** | `index.html:9196` | Certain |
| 5a | What "Edit" mode in the Library does | **Premise false** | `index.html:13930-13938`, `13948-13970` | Certain |
| 6a | The decks live inside `index.html` | **Premise false** | `index.html:15611-15614`, `8329-8345` | Certain |
| 6b | Benefit to serving decks from GitHub | **Not started** — recommend kill | see §3.6 | Likely |
| 7a | Merge the two expand/collapse buttons into one dynamic button | **Done** | `index.html:8261-8268`, `14073-14081` | Certain |
| 8a | Fix render of the flashcard (theme) settings pane | **Not started** | `index.html:5141-5152`, `5211-5213` | Likely |
| 8b | Transition between settings tabs | **Not started** | `index.html:5212`, `15206-15207` | Certain |
| 8c | SVG for the FC theme swatches | **Not started** | `index.html:7377-7386`, `5487-5510` | Certain |
| 9a | UI to view / restore hidden cards | **Not started** — orphaned function | `index.html:8512-8515` | Certain |
| 10a | Delete modal activating in the Workshop | **Done** | `index.html:8193-8198` | Certain |
| 11a | Expand decks with the LLM from the deck title | **Not started** | no match in `index.html` | Certain |
| 12a | Get Moria sorted | **Not started** — ambiguous ask | `index.html:16918`, `moria.html` | Likely |
| 13a | A "known words" array updated after each Flashcard run | **Premise false** | `index.html:8603-8626` | Certain |
| 13b | Workshop mixes %known + %new + user-chosen words | **Not started** | `index.html:12513-12545` | Certain |
| 13c | HSK level is followed in Workshop dialogue | **Done** | `index.html:12233-12237`, `12525-12543` | Certain |

**Tally:** Done 5 · Done differently 1 · Premise false 5 · Not started 9.

---

## 2 · A note on evidence quality

`git log -S` was the technique I expected to carry this audit. It did not, and you should know
why, because it changes what evidence is available to you in future.

This repo has **10 commits**, and `2ee853b "Initial commit — Zifang app"` (2026-05-25) contains
essentially the entire application. `git log -S"expand-collapse-btn"`, `-S"Use Credits to
Enrich"`, `-S"hpShow"`, `-S"carousel"`, `-S"moria"` all return exactly that one commit. The
history cannot tell you when a feature landed, because everything landed at once.

What substituted for it: **in-code comments that document their own bug fix**. `index.html:8193-8197`
is a five-line comment explaining precisely why the delete modal was moved. That comment is the
only surviving record of the fix — it is in no commit message and in no `STATUS.md` entry. Two
of the six items I could confirm as Done were confirmed this way.

**Consequence for you:** in a single-file app with a shallow history, comments are your commit
log. That is fragile but it is what you have, so the practical move is to keep writing them and
to mirror the load-bearing ones into `STATUS.md`.

---

## 3 · Per-item detail

### 1a · Variable size for Chinese characters in Flashcards — Done differently

**Status.** Three mechanisms already adapt headword size on Drill cards, none of them the
continuous "variable size" the note imagines:

1. A **stepped ladder** at `index.html:9997-10004` (front) and `10083-10089` (back):
   ≥8 chars → 2.2rem, =7 → 2.4rem, ≥5 → 2.6rem, else the 3.0rem base (`2197-2199`; 2.8rem at
   the mobile breakpoint, `5704-5706`).
2. `smartWrapDrillChar()` at `9833-9871` — inserts a line break at punctuation near the
   midpoint for 6+ char headwords, or splits at the midpoint for 8+.
3. CSS `word-break: break-all` on `.drill-char` (`2204`) as the final backstop.

**Test run.** I extracted the ladder verbatim and ran it over the two shipped datasets
(`data/hsk5-enriched.json`, `data/hsk6-enriched.json`), 3,791 cards total:

```
hsk5-enriched — 1291 cards   headword length -> count: {"1":186,"2":1066,"3":37,"4":2}
hsk6-enriched — 2500 cards   headword length -> count: {"1":169,"2":2169,"3":46,"4":116}
```

**The longest headword in either deck is 4 characters.** The ladder's 5 / 7 / 8+ branches never
execute on shipped content. Neither does `smartWrapDrillChar()`, which returns `null` below 6
characters (`9836`). All three mechanisms are dormant on the decks that ship.

Where sizing *does* misbehave is the **pinyin**, not the characters. `calcPinyinFontSize()`
(`9874-9890`) clamps to `[0.62, 1.1]`, and the clamp fires on entirely ordinary single-character
cards:

```
n=1 "zì"      -> 1.10rem   <-- CLAMPED at ceiling
n=1 "zhuāng"  -> 0.62rem   <-- CLAMPED at floor
n=2 "zì fāng" -> 0.94rem
n=8 "lù yáo zhī mǎ lì rì jiǔ jiàn rén xīn" -> 0.77rem
```

A one-character card with a six-letter syllable (莊 zhuāng, 窗 chuāng, 雙 shuāng) hits the floor
and renders its pinyin at 0.62rem — noticeably smaller than a 2-char card at 0.94rem. That is
the visible inconsistency, and it is on the *other* line.

**Assessment.** The idea as written is already satisfied for shipped decks and would produce no
visible change. The real exposure is Forge: `#forge-word-input` (`7662`) has **no `maxlength`**,
so a user can forge a 12-character headword, and that path *does* reach the dormant branches.
[Likely] that is what prompted the note.

**Recommendation — scope reduction.** Don't build continuous sizing. Do two smaller things:
- Widen the `calcPinyinFontSize` clamp floor from 0.62 to ~0.78, or better, make the clamp
  relative to character count rather than absolute. One-line change at `9887`.
- Add `maxlength="12"` to `#forge-word-input` (`7662`) so the dormant branches stay dormant.

**Breakage risk.** Changing the clamp floor affects every card back in Drill and the Settings
demo card (`7391-7397`). Low risk, but it is a visual change across the whole app, so eyeball
the 1-char and 8-char extremes together before committing.

---

### 2a · Pinyin protocol on the Workshop squircle buttons — Not started

**Status.** The four cast-row squircles — `#vocab-picker-trigger`, `#topic-pill-trigger`,
`#char-roster-btn`, `#spicy-btn` (`index.html:8027-8039`) — are icon-only and carry plain HTML
`title=` attributes. They do not use `hover-pinyin` / `hpShow()` at all.

Directly above them on the same screen, the dot controls 度 / 級 / 人 / 字 (`7925-7955`) *do*
use the full treatment: `<span class="hover-pinyin" onmouseenter="hpShow(this)">` with a
body-portal tooltip rendering Chinese + pinyin + English (`hpShow`, `9-40` lines from its
definition).

So one Workshop screen runs **three different tooltip systems**:

| Element | Mechanism | Locator |
|---|---|---|
| Dot controls (度級人字) | `hpShow()` body-portal tooltip, Chinese + pinyin + English | `7925-7955` |
| 3 cast squircles | Native browser `title=` | `8027-8035` |
| Spicy squircle | Bespoke `.spicy-toast` span | `8038-8041` |

**Assessment.** This is worth fixing and it is cheap. It is also the item most visible to you
personally, since Workshop is where you spend time. The pattern to copy already exists and is
battle-tested — `hpShow()` already handles the awkward cases (`.dot-opt` clip-path escape,
per-frame position tracking through row-expand animations).

**Implementation path.** Wrap each squircle's SVG in the `hover-pinyin` span and add `data-en`:

- 選詞 `xuǎncí` / Select Words → `#vocab-picker-trigger`
- 場景 `chǎngjǐng` / Topic → `#topic-pill-trigger`
- 人物 `rénwù` / Cast → `#char-roster-btn` (this Chinese already exists at `8049`, reuse it)
- 辣 `là` / Spicy → `#spicy-btn`

**Unforeseen consequences to check:**
- `hpShow()` branches on `el.closest('.dot-opt')` for the body-portal path. `.cast-row-btn` is
  not `.dot-opt`, so it falls through to the default in-DOM path. Check whether `.cast-row-btn`'s
  squircle `clip-path` (`484`) clips the in-DOM `.hp-pinyin` the same way it clips dot-opts — if
  it does, you need to extend the portal branch, not just add the span.
- Retiring `.spicy-toast` removes the "Make it spicy" reveal. Confirm you actually want that
  gone; it is doing slightly different work (it announces a *mode*, not a *label*).
- Keep the `title=` attributes for keyboard/screen-reader users. Hover tooltips are not
  accessible on their own.

---

### 3a / 3b · "Use Credits to Enrich" — Done, but mislabelled

**3a — the button works. Done.** `#char-enrich-btn` at `index.html:8140`, handler at
`16749-16800`. It builds a prompt via `buildCharacterEnrichmentPrompt()` (`12432`), POSTs to
Groq, parses the JSON, and persists `data.enriched` onto the saved speaker (`16794-16800`).
Failure paths are handled: missing name (`16752`), missing key with an inline
"Add one in Settings →" link (`16758-16765`).

**3b — "Credits" is wrong. Premise false.** Two ways:

1. It calls **Groq**, not Anthropic: `fetch('https://api.groq.com/...')` with
   `model: GROQ_DEFAULT_MODEL` (`16773-16781`), which is `openai/gpt-oss-120b` (`10431`). Groq's
   free tier costs nothing. No credits are consumed.
2. The paid Sonnet path is a **separate, unrelated flow** — the Forge modal at `7732-7740`
   ("Enrich with Sonnet — Use Claude Sonnet for higher quality enrichment") plus the Anthropic
   key field at `7319-7323`. The speaker-enrichment button never touches it.

The label was [Likely] copied from the Sonnet modal. Also note the button also **sits in the
Speaker Creator modal, not the cast section** — the note's location is off by one modal.

**Recommendation.** Rename to `Enrich with AI` or `Auto-fill profile`. One-word fix at `8140`.
Do not wire it to Sonnet — see the routing conflict in §5.

---

### 4a / 4b · The three carousels — one Done, one premise false

**4a — default is nothing selected. Done.** `loadSelectedCats()` (`8402-8407`) returns
`new Set()` with the comment `// first visit — all off`.

Stronger than that: all three surfaces share **one** Set by aliasing, not by syncing.
`state.drill.cats` is aliased to `state.selectedCats` (`8556-8560`) and
`stageState.vocabCatFilters` is aliased to the same object (`11778`), with an explicit
"DO NOT reassign" warning at `8584`. It is structurally impossible for the three to disagree.

**4b — nothing-selected does NOT render everything. Premise false, and the code does the
opposite.** `getFiltered()` ends with `if (!isSpecialMatch && !isCatMatch) return false;`
(`9196`). With `selectedCats` empty, neither can be true, so **every card is filtered out**.

Combined with 4a, a brand-new user's first view of Browse is empty. `loadLoadedPacks()`
(`8414-8425`) seeds only favorites / struggling / custom for new users — all three of which are
empty on day one.

**Assessment.** This is a genuine first-run problem, and it is the more interesting half of the
note. But it is not obviously a bug: the Library-panel opt-in model (`8422`, `8456`) is a
deliberate decision — you chose not to dump 3,791 cards on a new user.

**Recommendation.** Do not change the filter to "empty means all" — that would make the Library
opt-in model pointless and would render thousands of cards on first paint. Instead add an
**empty state**: when `getFiltered()` returns 0 *and* `selectedCats.size === 0`, show a single
line pointing at the Library button. Cheap, and it fixes the actual felt problem without
touching filter semantics.

**Breakage risk.** None if you add an empty state. High if you invert the filter — `getFiltered()`
is called by Browse render, drill pool construction, and the Workshop vocab picker
(`11843-11856`), so inverting it changes drill pool sizes and Workshop vocab counts too.

---

### 5a · What "Edit" mode in the Library does — Premise false

**Answer: it is not an edit mode. It is a delete mode, and nothing in it edits anything.**

The Library is the packs panel (`#packs-btn` `7481`, `#packs-panel` `7494`). `#packs-edit-btn`
(`7495`) is labelled "Edit". Its handler (`13930-13938`):

```js
const isNowActive = panel.classList.toggle('delete-mode');
_pendingDeletePackId = null;
btn.textContent = isNowActive ? 'Done' : 'Edit';
```

It toggles one CSS class named `delete-mode` and flips its own label to "Done". What that class
turns on:

- A trash-can icon appears on every forged deck (`13899-13901`).
- Tapping a deck arms a **two-tap confirmation** — the label becomes `確認? Delete?` (`13902-13904`),
  and the second tap commits.
- For **built-in** packs, commit calls `executeHideBuiltinPack()` (`13953`) — hidden, recoverable
  in principle.
- For **forged** decks, commit hard-deletes (`13962-13970`) — not recoverable.

Closing the panel resets the mode and clears any armed confirmation (`13922-13926`).

**Assessment.** The button lies. A user who taps "Edit" expecting to rename a deck finds only a
way to destroy one. The two-tap confirmation is good design; the label undermines it by not
warning that destruction is the only thing on offer.

**Recommendation.** Rename to `Remove` (label) / `Done` (active state). One-line change at
`7495` plus the two `textContent` assignments at `13925` and `13936`.

**Unforeseen consequence:** `.packs-edit-btn.active` is styled vermillion (`304`) — already the
danger colour. The CSS has been telling the truth the whole time; only the word is wrong.

---

### 6a / 6b · Decks in GitHub instead of the HTML — Premise false, then kill

**6a — the decks are not in the HTML. Premise false.**

```js
let ALL_CARDS = []; // populated from Supabase — inline arrays kept as offline fallback
```
— `index.html:8529`

and the actual load path:

```js
try { _remoteCards = await fetchCards(); }
catch (err) {
  console.warn('[字坊] Supabase fetch failed, falling back to inline data:', err);
  _remoteCards = []; // inline arrays removed — Supabase is the only source
}
```
— `index.html:15611-15614`

Cards are fetched from Supabase (`_sb.from('cards').select(...)`, `8341-8342`). The migration
already happened. The note is asking whether to move something that has already moved.

**Note the contradiction between those two comments.** `8529` says inline arrays are kept as an
offline fallback. `15614` says they were removed. `15614` is correct — `8529` is orphaned and
should be deleted. See §5 for the availability consequence, which is serious.

**6b — is there a benefit to GitHub-hosted deck JSON? Not started. Recommend kill.**

The case against, given where the project actually is:

- The data is already out of the HTML. The stated motivation is satisfied.
- Supabase gives you row-level querying (`8341-8342` selects 10 named columns), which a static
  JSON file on GitHub Pages does not. You would fetch all 3,791 cards on every page load.
- The upload tooling already exists and works (`upload-hsk6-enriched.js`, and the 2026-07-24
  STATUS entry confirms all 2500 cards upserted successfully).
- The `.gitignore` work on 2026-07-31 deliberately kept `data/` write scripts untracked. Moving
  decks into the repo re-opens the surface you just closed.

The one real argument *for* it — offline availability — is better solved by caching the Supabase
response in `localStorage` or a service worker, which costs far less than a second source of
truth. See §5.

**Verdict: kill.** Record it as decided so it stops resurfacing.

---

### 7a · Merge expand and collapse into one dynamic button — Done

There is one button, not two: `#expand-collapse-btn` (`index.html:8261`), holding two SVGs
(`#expand-icon` at `8262`, `#collapse-icon` at `8265` with `style="display:none"`). The handler
(`14073-14081`) toggles `_allExpanded`, swaps which icon is visible, and updates `aria-label`
between "Expand all cards" and "Collapse all cards".

`git log -S"expand-collapse-btn"` returns only the initial commit, so there is no history
showing a two-button predecessor — but the merged state is what ships today, which is what the
note asked for.

**Nothing to do.**

---

### 8a / 8b / 8c · Flashcard settings render, tab transition, theme SVG

**8a — the theme pane cannot scroll. Not started.** [Likely]

`.settings-panel` has a **fixed** height with a comment that is now wrong:

```css
/* Fixed height — tabs must NEVER change the modal size.
   Sized to the keys pane (the taller of the two).
   Theme pane has breathing room; keys pane overflows if needed. */
height: min(480px, 80dvh);
overflow: hidden;
```
— `index.html:5145-5152`

"the taller of the **two**" — there are **four** panes: keys, sliders, progress, backup
(`7279-7288`). The comment is stale by two panes, which is a reliable sign the sizing was never
revisited after the panel grew.

Then the theme pane specifically opts *out* of scrolling:

```css
.settings-pane { padding: 1.25rem; overflow-y: auto; flex: 1; }
#settings-pane-sliders:not(.hidden) { display: flex; flex-direction: column; overflow-y: hidden; }
```
— `5211-5213`

So: fixed 480px panel, `overflow:hidden` on the container, `overflow-y:hidden` on the pane, and
inside it a 2×2 CSS grid (`.theme-carousel`, `5464-5471` — note it is a grid, not a carousel,
despite the name) whose chips are `flex:1; min-height:0` (`5487-5490`). On a short viewport
the swatches compress toward zero height with no scrollbar to recover them. **That is the
render bug.** I have not measured it in a browser, hence [Likely] rather than [Certain] — what
would settle it is opening Settings → theme tab at 375×667 and screenshotting.

**8b — there is no transition. Not started. [Certain]**
`.settings-pane.hidden { display: none; }` (`5212`), and the switch is
`forEach(p => p.classList.add('hidden'))` then `remove('hidden')` on the target (`15206-15207`).
`display` is not animatable, so panes hard-cut. The tab *buttons* animate
(`transition: opacity 0.2s, border-color 0.2s`, `5199`) — the buttons move smoothly and the
content teleports, which is exactly the kind of mismatch that reads as "broken" rather than
"unanimated."

**8c — theme swatches are divs, not SVG. Not started. [Certain]**
Each chip is a `<span class="mini-char">字</span>` plus two `<div>` rules (`7378-7386`), styled
at `5502-5512`. Four themes in the HTML (`default`, `night-study`, `bamboo-grove`, `clean-slate`)
matching exactly four in the `THEMES` object (`14985-15033`) — so this is not a count mismatch,
it is a fidelity complaint: the div mock does not look like the card it previews.

**Assessment.** 8a is a real defect and worth fixing. 8b is polish. 8c is the least valuable of
the three — an SVG mini-card would look better but the current divs are legible, and each theme
would need its own hand-tuned SVG that then has to be kept in sync with `THEMES` by hand. That
is a new synchronisation obligation for a cosmetic gain.

**Recommendation.** Fix 8a. Do 8b at the same time since you are already in that CSS. **Skip 8c**
unless the swatches start actively misleading you about what a theme looks like.

**Implementation path for 8a:** delete the `overflow-y: hidden` override at `5213` and let the
pane scroll like the other three. Then fix the stale comment at `5147`. If the grid still
compresses, give `.theme-chip-swatch` a `min-height` in the 44–56px range instead of `min-height: 0`
(`5490`).

**For 8b:** swap the `display:none` toggle for an opacity/visibility pair so it can transition —
but be careful, `.settings-pane` uses `flex: 1` and `#settings-pane-sliders` overrides `display`
to `flex`, so a naive `display` → `opacity` swap will leave all four panes stacked in the flex
column. You need `position: absolute` on the panes plus a positioned parent, or a height-locked
wrapper.

**Breakage risk:** `openSettingsKeys()` (`15095-15101`) and the reset at `15773-15775` both
manipulate `.hidden` directly. Any change to how panes hide must update all three call sites, or
Settings will open showing two panes at once.

---

### 9a · Where does the user press to see hidden cards? — Not started

**Answer: nowhere. There is no such control, and the function that would power it is orphaned.**

The hiding machinery is complete:
- `HIDDEN_CARD_IDS_KEY = 'zf_hidden_nuggets'` (`8504`)
- `loadHiddenCards()` / `saveHiddenCards()` (`8505-8511`)
- `state.hiddenCards` (`8551`)
- `executeHideCard(nid, cardEl)` called on swipe (`9583`)
- Filtered out of Browse (`9145`), drill pool (`9247`), and Workshop vocab (`11826`)

And the restore function exists:

```js
function restoreAllHiddenCards() {
  state.hiddenCards.clear();
  saveHiddenCards();
  ...
}
```
— `index.html:8512-8515`

`grep -c "restoreAllHiddenCards" index.html` returns **1** — the definition. **It is never
called from anywhere.** There is no button, no menu item, no settings row.

**Assessment. This is the highest-stakes live item, and it is not a feature request — it is a
data-reachability bug.** A user swipes a built-in card away and it is gone from Browse, from
drills, and from Workshop vocab, permanently, with no path back short of clearing
`localStorage`. The drill filter carves out one narrow exception (`9247` keeps hidden cards that
are also in `struggling`), which means the current escape hatch is "hope you had already
struggled on it."

Note the asymmetry with the Library: hidden *packs* are recoverable via the packs panel
(`13982` — `state.loadedPacks.add(id); // restore`). Hidden *cards* are not. Same gesture, two
different recoverability guarantees.

**Recommendation — smallest thing that closes the hole.** Add a row to Settings → Progress
(`#settings-pane-progress`, `7343`) reading `Hidden cards: N` with a `Restore all` button wired
to the existing `restoreAllHiddenCards()`. That is one HTML row and one `addEventListener`. It
does not answer the note's design question ("best way to show hidden cards?") but it removes the
data-loss risk today, and you can design the browsable version later.

**The fuller version, if you want it:** add `hidden` as a pseudo-deck pill alongside `favorites`
and `struggling` in the category row. Those two are already special-cased throughout
`getFiltered()` (`9173-9175`), so the pattern exists — but it is a wider change, touching the
filter, all three carousels, and the packs panel.

**Unforeseen consequences:**
- `restoreAllHiddenCards()` calls `saveHiddenCards()` but I did not verify it triggers a
  re-render. Check whether `renderBrowse()` needs calling after it, or the count will change
  while the card list does not.
- The key is `zf_hidden_nuggets` — legacy `nugget` naming. The 2026-07-31 decision explicitly
  says **do not** rename persistence keys without a migration pass. Leave it.

---

### 10a · Delete modal activating in the Workshop — Done

Fixed, and the fix documents itself:

```html
<!-- Delete Confirmation Modal —
     MUST live at top level (sibling of all .tab-content divs), never nested
     inside any single tab. Previously nested inside #stage-content, which
     meant Workshop's display:none hid the modal when delete was triggered
     from Browse/Drill/Forge. -->
```
— `index.html:8193-8197`

The modal now sits at `8198`, after `#stage-content` closes at `8191`. `openDeleteModal()`
(`13612-13621`) adds `.open` to a body-level element, so tab state cannot hide it.

The note's phrasing ("delete appears in the workshop") and the comment's phrasing ("Workshop's
`display:none` hid the modal") describe the same root cause from opposite ends — a modal
DOM-nested inside the Workshop tab both fails to show when you are elsewhere *and* shows up in
the Workshop when you switch there.

**Nothing to do.** This is the clearest case in the whole set of a note going stale because it
was finished.

---

### 11a · Expand decks with the LLM from the deck title — Not started

No implementation. Zero matches for `expandDeck`, `similar words`, `suggestWords`, `generateDeck`
in `index.html`.

**Assessment.** This is the item I would push back on hardest.

The idea is "give the LLM a deck title, get similar words back." But the note's own parenthetical
gives the mechanism away — *"llama find similar words from deck's title"* — and title-similarity
is a weak signal. A deck called 自創 ("Custom") or 句型 ("Patterns") has a title that says nothing
about its contents. Your own `_docs/RECON.md` evidence, summarised in `STATUS.md` under the
2026-05-26 decision, found **confident hallucination** to be the #2 failure mode of exactly this
model on exactly this kind of open-ended generation. Bulk-generating unvalidated vocabulary is
the highest-hallucination-surface feature you could add, and the validator that would catch it
(`validateGeneratedCard()`, per the 2026-05-27 decision) is wired to Forge's single-card path,
not to a bulk path.

Also note the note itself says "using llama?" — Zifang moved off Llama on 2026-07-31
(`GROQ_DEFAULT_MODEL = 'openai/gpt-oss-120b'`, `10431`). The note predates that decision.

**Recommendation — heavy scope reduction, or kill.** If you build it:
- Seed from the deck's **existing cards**, not its title. You have `components[]` and
  `semanticNote` on every enriched card — far richer signal than a two-character deck name.
- Cap at 5 suggestions, and route each through the existing Forge single-card path so
  `validateGeneratedCard()` runs on every one.
- Require per-word confirmation before saving. Never bulk-insert.

That version hangs off `generateCard()` (`10436+`) and reuses the Forge review UI. If that
sounds like more work than the feature is worth to you, that is the correct read, and killing it
is the right call.

---

### 12a · Get moria sorted — Not started, and the ask is ambiguous

**What Moria actually is:** the password gate for spicy mode. `#spicy-pw-backdrop` (`8071-8082`)
contains `#moria-gate-svg` (`8073`), the heading "Speak friend and enter.", and a subtitle.

**What I found:** there are **two divergent Moria assets** and the in-app one is the lesser.

| | `moria.html` | inline in `index.html` |
|---|---|---|
| Location | project root, standalone | injected at `16918` |
| viewBox | 500 × 680 | 200 × 230 |
| Drawing elements | 111 | 19 |
| Features | Tengwar arch text on curved paths, dual glow filters, corner scroll ornaments | pillars, two arch strokes, one star polygon |

[Likely] "get moria sorted" means: port the good standalone art into the app, or delete the
standalone file so it stops implying unfinished work. I cannot verify which from the code —
what would settle it is you telling me. There is also a third reading (the `moria/` folder holds
10 reference screenshots and a HEIC from 2026-04-01, so it may mean "finish the art from those
references").

**Separate, verifiable defect found here.** The subtitle reads:

```html
<p class="moria-subtitle">这个功能是锁着的</p>
```
— `index.html:8075`

That is **Simplified** Chinese. `INTENT.md` §7 says "Default → Traditional", and `STATUS.md`
records "Default writing system: Traditional (Taiwan context)" as a pre-existing decision. The
Traditional form is 這個功能是鎖著的. This is a one-line fix regardless of what you decide about
the art.

**Assessment.** Purely cosmetic, behind a password gate you already know the answer to. Low
stakes. But it is cheap, and it is the kind of item that will sit on a list forever precisely
because it is never urgent. Either do it in ten minutes or kill it.

---

### 13a / 13b / 13c · Known words → Workshop sentences

**13c — HSK level is already followed. Done.** The Workshop system prompt has a dedicated
section:

```
═══ HSK LEVEL COMPLIANCE ═══
The user specifies an HSK level (1-6). ALL surrounding vocabulary and grammar (everything
EXCEPT the user's chosen target vocabulary) MUST stay within that level.
```
— `index.html:12233-12235`

plus per-level constraint blocks (`getHskLevelConstraints()`, `12379-12428`, six labelled
levels), injection into the user prompt at `12525-12535` (label, vocab, grammar, register,
complexity), and a restatement at `12543`. This is thorough. The note's final sentence asks for
something that exists.

**13a — "another array of known words" already exists in substance. Premise false.**

```js
// Each card has an integer score 0-3:
//   0 = unseen OR last action was 'struggle' (top priority)
//   1 = seen and got-it once
//   2 = got-it twice
//   3 = mastered (capped — see less often)
const CARD_SCORES_KEY = 'zifang-card-scores';
```
— `index.html:8603-8611`

Scores update on every drill verdict (`recordCardGotIt`, `8655+`; struggle resets to 0), not
only at the end of a run. A migration from the older `card-stats` already ran (`8629-8639`).
Note the deliberate design decision at `8646-8648`: `recordCardSeen()` "does NOT change the
score. Surfacing on screen is not a verdict." That is a *better* model than the note's proposal,
which would mark a word known after a completed run regardless of how it went.

So "known words" needs no new array and no new persistence — it is a one-line derivation:

```js
const knownIds = Object.entries(loadCardScores()).filter(([, s]) => s >= 2).map(([id]) => id);
```

I confirmed no such helper exists yet: `knownWords`, `getKnownWords`, `unseenPool`, `newWords`
all return **0** occurrences in `index.html`. `loadCardScores(` appears 4 times, `SCORE_WEIGHTS`
twice.

**13b — the %known / %new mix. Not started. This is the only genuinely new capability in the
whole note set.**

Currently `vocabList` in the Workshop prompt comes solely from `stageState.selectedVocab`
(user-picked), injected at `12513-12515`. There is no known/new blending.

**Test run — what does injecting known words actually cost?** I measured token cost against the
real HSK6 deck:

```
KNOWN-WORD INJECTION COST (per Workshop generate call)
  10 known words ->     49 tokens
  50 known words ->    243 tokens
 250 known words ->  1,245 tokens
1000 known words ->  5,003 tokens

MIX FEASIBILITY (user picks 5 target words)
70/30 of 20: 14 known +  6 new + 5 user = 25 words, ~90 tokens added
50/50 of 40: 20 known + 20 new + 5 user = 45 words, ~191 tokens added
```

**The conclusion that matters: sample, do not dump.** Handing the model your whole known-word
pool costs thousands of tokens per generation and would swamp the prompt. A *sampled* mix of
15–45 words costs 50–190 tokens — negligible against a system prompt that already runs into the
thousands. Sampling is not a compromise here; it is strictly better, because a 25-word list is
also an instruction the model can actually honour, and a 1,000-word list is not.

**The design problem the note does not address: "new" relative to what?** Score 0 means "unseen
OR last action was struggle" (`8605`) — those are two very different populations collapsed into
one value. Pulling "new words" from score 0 will hand you words you have repeatedly failed,
labelled as new. You need either a separate unseen check or to draw "new" from cards with no
entry in the scores object at all.

**And a live conflict with 13c.** `stageState.hskLevel` defaults to **1** (`11763`). If your
known words come from drilling HSK 5 and 6 but the level control sits at 1, the prompt
simultaneously tells the model "stay inside HSK 1 scaffolding" (`12543`) and hands it HSK 6
vocabulary as known. HSK 1 is roughly 150 words; the HSK 6 deck alone is 2,500 cards. Those
instructions fight, and 13c's compliance section will lose.

**Recommendation — build it, scoped like this:**
1. `getKnownWords(floor = 2, hskCeiling)` — derive from `loadCardScores()`, filter by the
   card's `category` against the current `stageState.hskLevel`. No new storage.
2. Sample 10–20 known + 5–10 new, do not inject the pool.
3. Draw "new" from cards with **no scores entry**, not from score 0.
4. Add the mix ratio as a fourth dot control next to 度/級/人/字 (`7925-7955`) — the pattern is
   there and `setupDotControl()` (`16475`) already generalises.
5. Inject as a *third* labelled block in the prompt, distinct from `VOCABULARY TO INCLUDE`
   (`12513`). Known words are permission, not obligation. The current block says every listed
   word "MUST appear" (`12549`) — do not let known words inherit that.

**Unforeseen consequences:**
- Point 5 is the one that will bite. If known words land in the existing `VOCABULARY TO INCLUDE`
  block, the model is instructed to force all 25 into one short dialogue. At `length: short` the
  target is a few hundred characters — it cannot fit, and it will either pad or drop your actual
  target words.
- The HSK level default of 1 should probably move to whatever level the user's loaded packs
  suggest, or the mix will misbehave for everyone who has not touched the 級 control.
- Prompt length is already substantial. Measure the assembled prompt before and after; the
  2026-05-25 layered-assembly decision (`INTENT.md` §9b) says new behaviours get a layer
  assignment rather than being appended to a static string. This feature is exactly the kind of
  thing that decision was written to govern — it belongs in L2 (opt-in), not L0.

---

## 4 · Recommended order

Ordered by stakes, not by how interesting each is to build.

**1. 9a — hidden-cards restore (Settings → Progress row).**
First because it is the only item where the current behaviour loses user data with no path
back. It is also nearly free: the function exists, it just needs a caller. Ship the minimal
"Hidden cards: N / Restore all" row now; design the browsable version later or never.

**2. 8a — theme pane scrolling (+ 8b while you are in that CSS).**
Second because it is a real defect on a surface whose entire job is looking good, and because
the stale "taller of the two" comment tells you nobody has looked at this since the panel grew
to four panes. Doing 8b in the same pass is efficient; doing it separately means touching the
same three call sites twice.

**3. 13b — known/new vocabulary mix in Workshop.**
Third because it is the only item that adds capability rather than repairing something. It goes
after the repairs because it is also the only one with real design risk (the HSK-level conflict,
the "new relative to what" question, the must-appear inheritance problem). Do it deliberately,
not quickly.

**4. 2a — pinyin protocol on the cast squircles.**
Fourth because it is cheap and it is on the screen you use most, but nothing breaks while it
waits. Check the clip-path question before you start — that determines whether this is a
15-minute job or a 90-minute one.

**5. Cheap correctness fixes, batched into one pass.**
Do these together, they are one sitting: rename "Edit" → "Remove" (5a, `7495`), rename
"Use Credits to Enrich" → "Enrich with AI" (3b, `8140`), Simplified → Traditional on the Moria
subtitle (12a, `8075`), delete the orphaned "inline arrays kept as offline fallback" comment
(6a, `8529`), add the empty-Browse state (4b).

**6. 12a — Moria art.** Only after you decide what "sorted" means. Ten minutes or delete it.

**7. 8c — SVG theme swatches.** Skip. Cosmetic gain, new hand-sync obligation against `THEMES`.

**Kill list — record as decided so they stop resurfacing:**
- **6b** — decks to GitHub. The migration already happened; Supabase is strictly better for
  this shape of data; offline is a caching problem, not a hosting problem.
- **11a** — LLM deck expansion from title. Highest hallucination surface in the app, weakest
  input signal, and the validator that would catch it is not wired to a bulk path. If you want
  it anyway, build the 5-suggestions-from-existing-cards version, never the bulk version.

---

## 5 · Incidental findings (not in the notes, found while verifying)

These were not asked about. Two of them matter more than most items in the note set.

**A. Zifang has no offline fallback, and a comment claims it does. [Certain]**
`index.html:8529` says `// populated from Supabase — inline arrays kept as offline fallback`.
`index.html:15614` says `_remoteCards = []; // inline arrays removed — Supabase is the only source`.
The second is correct. The consequence: if the Supabase fetch fails, `ALL_CARDS` contains only
the user's own forged cards. All 3,791 curated HSK cards vanish. For a project whose STATUS
header reads `state: Live`, that is a total content outage with no degraded mode. A
`localStorage` cache of the last successful fetch would close it cheaply. **Recommend adding
this to Back Burner.**

**B. The Sonnet routing decision is currently unreachable. [Certain]**
`STATUS.md` Back Burner commits to Forge correctness Layer 3 — routing high-risk queries to
Sonnet. But `index.html:10444` reads `const provider = groqKey ? 'groq' : 'anthropic';`. Groq
wins unconditionally whenever a Groq key exists. Any user with both keys set can never reach
Sonnet, so Layer 3 as specified cannot function without changing this line first. Worth noting
on the Back Burner item so a future session does not build the routing logic and then wonder
why it never fires.

**C. Workshop's script default is Simplified, contradicting project doctrine. [Certain]**
`index.html:7955`: `<button class="dot-opt active" data-val="simplified" ...>`. The `active`
class is on Simplified. `INTENT.md` §7 says "Honor the writing system of the context...
Default → Traditional." `STATUS.md` records Traditional as a pre-existing decision, and the
entire HSK5/HSK6 enrichment effort used Taiwan-standard Traditional forms. Every Workshop
dialogue generates in Simplified unless the user notices and flips it. Moving `active` to the
`traditional` button is a one-attribute fix.

**D. `.theme-carousel` is a 2×2 CSS grid, not a carousel. [Certain]**
`index.html:5464-5471`. Cosmetic naming issue, but it will mislead the next person who greps
for carousel behaviour — the real carousels (Browse/Drill/Select Words, `14177`, `14216`) are a
different mechanism entirely.

---

## 6 · Why these particular notes went stale

The individual failures are not interesting; the pattern is. Three mechanisms, in order of how
much damage they did.

**1. Finished work has no return path to where the idea was written.**
This is the big one. Five line-items were **Done** and one was **Done differently** — 30% of the
list — and in every case the work was completed with no signal reaching the notes. The delete-modal
fix (10a) is the purest example: someone diagnosed a real DOM-nesting bug, fixed it, and wrote a
careful five-line comment explaining why (`8193-8197`) — and that comment is the *only* record.
It is not in a commit message. It is not in `STATUS.md`. So the note survived its own resolution
by months.

The notes live outside the repo. `STATUS.md` lives inside it. Nothing connects them, so
completion is invisible from the side where the ideas are kept.

**2. The premise decays faster than the note.**
Five line-items were **Premise false** — another 25%. These were not wrong when written; the
ground moved underneath them. Decks migrated to Supabase, so 6a became false. A card-scoring
system was built, so 13a became false. HSK compliance went into the Workshop prompt, so 13c
became done. The note that says "figure out if there's a benefit in putting the decks in github
instead of the html" was a reasonable question on the day it was written and became nonsense
without changing a character.

The tell is that notes are written in the **present tense about a system's current state**, and
that state is exactly the thing that changes. A note phrased as an *observation* ("the decks are
in the html") rots. A note phrased as a *goal* ("decks should be queryable without shipping
them in the app bundle") survives the migration that satisfies it, because you can check it
against reality and see it is now true.

**3. Vocabulary drift, in both directions.**
"Edit mode in the library" — the UI says Edit, the code says `delete-mode`, and neither says
Library except in a `title` attribute (`7481`). "The cast section" — the enrich button is in the
Speaker Creator modal, one level away from the cast row. "Using llama" — Zifang left Llama on
2026-07-31. "The 3 carousels" — one of the four things called a carousel in this file is a CSS
grid. Each drift cost real search time this session and would have cost you more, because you
would have been searching for a word the code never used.

**What would actually fix this.** Two things, in order:

- **Write open items into `STATUS.md` in the note's own vocabulary.** Not a translation into
  correct terminology — the actual words you used. Then `grep "squircle" STATUS.md` finds the
  item, and a future session closing that item has somewhere to write "done." That is the
  return path that was missing, and it is why the STATUS entries from this reconciliation
  deliberately carry phrases like "squircle buttons," "Use Credits to Enrich," and "expand decks
  using llama" verbatim.
- **Phrase notes as goals, not observations.** "Decks should not ship inside the app bundle"
  ages well. "The decks are in the html" was false within weeks and told nobody.

One thing worth saying plainly: the notes themselves were not the problem. Nearly every one
pointed at something real — a genuine inconsistency, a genuine gap, a genuine question. Three of
them (9a, 8a, 4b) found defects that nothing else had surfaced. The failure was purely in
keeping them synchronised with a codebase that kept moving.

---

## Appendix — instructions embedded in the notes

Per Tim's standing instruction, directions written to an agent inside the notes were treated as
evidence of ambition, not as commands. Two appeared:

- *"add an option to expand decks using llama?"* — the model choice is stale (Groq default moved
  to `openai/gpt-oss-120b` on 2026-07-31, `index.html:10431`). More substantively, I disagree
  with the approach on its merits and said so in §3.11: title-similarity is a weak input signal
  and bulk generation is the highest hallucination surface available, against a validator that
  is not wired to a bulk path.
- *"(also )"* — an unfinished parenthetical in note 11. Nothing recoverable. Flagged rather than
  guessed at.

## Appendix — scripts

Two scratch scripts backed the numbers in §3.1 and §3.13. Neither is part of the project; they
were run against `data/hsk5-enriched.json` and `data/hsk6-enriched.json` and the extracted
functions were copied verbatim from `index.html` at the line numbers cited. To reproduce,
re-extract `drillFontSize` (`9997-10004`), `calcPinyinFontSize` (`9874-9890`), and the score
model (`8603-8626`) and rerun. Findings:

- 3,791 cards examined; longest headword 4 characters; the ladder's 5/7/8+ branches never fire.
- `calcPinyinFontSize` clamps at the 0.62 floor for ordinary 1-character cards with long
  syllables (zhuāng, chuāng, shuāng), and at the 1.1 ceiling for short ones (zì).
- Known-word injection: ~49 tokens for 10 words, ~5,003 for 1,000. Sample, do not dump.
