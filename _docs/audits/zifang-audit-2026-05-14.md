**Document status: Archived — 2026-09-29.** Preserved for historical reference.

# 字坊 Zifang — Audit
*2026-05-14 · Playbook-relative re-evaluation · Compared against 2026-04-29 audit baseline*

---

## 0 · Scope and method

This audit re-evaluates Zifang's design choices against `tims-ux-playbook` (v. 2026-04-29). Per Tim's direction, it covers three lenses:

- **Drift** — places where the playbook describes Zifang inaccurately because the code has changed since the doc was written.
- **New patterns** — choices visible in Zifang that aren't captured anywhere in the playbook yet.
- **Contradictions** — choices that actively conflict with playbook rules.

It does NOT re-derive the taste profile from scratch. Re-derive-fresh was offered and declined; the existing playbook structure was treated as load-bearing and edited around, not torn down.

Sources read this pass: `tims-ux-playbook/SKILL.md` (local copy matches the active plugin skill — no divergence), `zifang-design-system.md` (the locked design system, 741 lines), `zifang-project-knowledge.md`, `zifang-pending-queue.md`, `zifang-ux-audit-2026-04-03.md`, `zifang-audit-2026-04-29.md`, `playbook-multi-project-notes.md`, `playbook-update-notes-2026-04-29.md` (which is a redirect — content moved to `webdev/_docs/`), and direct inspection of `index.html` (18,092 lines, 1.58 MB) and the new `migrate.js`.

No raw chat transcripts were read this pass. Prior audit docs distill the relevant chat history and the code itself is the ground truth.

---

## 1 · The single most important context

**A migration is in flight that changes what this audit means.**

`migrate.js` was created today (2026-05-14). It is a Node script that extracts every inline card array from `index.html` (`NUGGETS`, `HSK1_NUGGETS` through `HSK4_NUGGETS`), merges in `hsk5-skeleton.json` + `hsk5-staging-batch-01.json` + `hsk6-staging-batch-01.json`, and uploads the result to a Supabase Postgres backend. The single-file vanilla-JS constraint — currently described in the playbook as "the constraint is still earning its keep" — is being deliberately retired. Tim has separately stated this Cowork audit is the *wrap-up* for Zifang work in Cowork; future iteration will happen in Claude Code, presumably against the Supabase-backed app.

This matters for the audit in three ways:

1. The 4/29 audit's biggest single finding ("zero audio — the app reinforces silent reading") remains true. It's worth restating, but the migration explains why the past 16 days saw infrastructure work (Supabase prep) instead of features.
2. Any playbook claim that asserts "single-file vanilla JS" as a confirmed preference should be softened — Tim is currently breaking it on purpose.
3. **`migrate.js` ships a hardcoded Supabase `service_role` key.** That key has full admin write access. Hardcoding it in a script that lives in a project folder (and that may follow Tim to GitHub/Netlify) is a real security risk. Move it to an env variable (`process.env.SUPABASE_KEY`) and add `migrate.js` to `.gitignore` or rotate the key after migration. Not a UX issue — flagging because it surfaced while reading the file and would be expensive to discover later.

---

## 2 · What's been resolved since 2026-04-29

The 4/29 audit listed 4 still-open items. Two are now closed:

| 4/29 item | Status 5/14 | Evidence |
|---|---|---|
| Cast surfaced as third pill in Stage (3a, biggest discoverability hole) | **CLOSED** | `.cast-row-btn` row with `id="vocab-picker-trigger"` (词), `id="topic-pill-trigger"` (场), `id="char-roster-btn"` (人). All three triggers sit as peers in a cast row alongside the spicy button. The buried-cast flow problem from 4/03 is solved. |
| Workshop dialogues vanish on close (Z-07) | **CLOSED** | `ARCHIVE_KEY = 'zifang-saved-dialogues'` at line 17880; `.stage-archive-trigger` button; full `.archive-modal-backdrop` + `.archive-modal-card` with title `已儲存 Saved`. |
| Drill setup subtitle still "Configure your session" (2b) | Unverified this pass | Not specifically re-checked in code; carry forward. |
| CSS naming unification (`.cat-bubble` / `.setup-cat-bubble` / `.vocab-cat-pill`) | **STILL OPEN** | Counts in current `index.html`: `.cat-bubble` 47×, `.setup-cat-bubble` 25×, `.vocab-cat-pill` 19×. `.filter-pill` 0×. Now flagged in three consecutive audits (4/03, 4/29, 5/14). |

The two closures are real wins. Cast surfacing in particular was the highest-impact UX recommendation from the 4/03 audit and has lived under "still open" for 11 weeks. Whatever pass made that change deserves credit.

---

## 3 · Drift findings — playbook claims that no longer match reality

These are factual errors in the current playbook. They are safe to correct without invoking the cross-project triangulation rule, because correcting a factual mistake is not promoting a new preference.

### D1 · The dot-control animation has been completely re-architected

**Playbook §4 #3 says:** "In Zifang's dot controls, opening is a slow 1.5s bloom while closing is instant."
**Design system §5.6 / §8.1 say:** `max-width: 0 → 20rem` over `1.5s cubic-bezier(0.4, 0, 0.2, 1)`, with pills staggered "0.5s base + 0.2s per pill."

**Reality:** `.dot-options` no longer has a CSS transition at all. The CSS rule literally reads `/* No CSS transition — JS _dcAnimate controls max-width in sync with widths */`. A new pair of functions (`_dcMeasure`, `_dcAnimate`) measures all four control widths once, then drives every frame via `requestAnimationFrame`. The new system guarantees three things, per the comment block in code:

1. **Constant total width** at every frame, so buttons never overlap or leave gaps.
2. **Proximity-based easing**: the button adjacent to the expanding one uses an aggressive power-curve `1 - (1-t)^4` so it clears space fast; the button itself uses `n=2.5`; distant buttons use a gentle `n=2`.
3. **Interruptible**: clicking a different control mid-animation cancels the current rAF loop and starts a new one from current positions.

The asymmetric open/instant-close principle is preserved (and now stated explicitly in a code comment: "delays only on open, so close is instant"). The 1.5s CSS bloom is just gone.

**Why it changed (per the source comment):** independent CSS transitions on sibling buttons got out of sync and caused "bumping and jerkiness." Tim moved to a single rAF owner.

### D2 · The pill stagger timing changed

**Playbook §4 #4 / design system §8.3 say:** "stagger by 0.2s each (0.5, 0.7, 0.9...)".
**Reality:** stagger is `0.1s` apart, base `0.70s` (0.70 → 1.20s for pills 1–6). The CSS comment explains: "Shifted +0.4s to give the button container time to open before pills appear. Stagger gap stays 0.1s — first pill at 0.70s, last at 1.20s."

This is a real refinement, not a bug. The base delay is calibrated against the new rAF container-open duration. The "0.5s base + 0.2s per pill" example in both docs is now misleading.

### D3 · The "slow bloom" easing the playbook names no longer exists

**Playbook §4 Easing says:** "For slow blooms: `cubic-bezier(0.4, 0, 0.2, 1)`."
**Design system §8.1 says** the same.
**Reality:** `cubic-bezier(0.4, 0, 0.2, 1)` appears **zero** times in `index.html`. The dot-control bloom that used to use it is now JS-driven (D1), so the easing string was deleted.

Actual easings in use across the whole file, by count:

| Easing | Uses | Role |
|---|---|---|
| `cubic-bezier(0.25, 0.1, 0.25, 1)` | 30 | Tim's standard `--ease` — confirmed and still dominant |
| `cubic-bezier(0.5, 0, 0.35, 1)` | 5 | Undocumented. Slightly more aggressive ease-out start |
| `cubic-bezier(0.4, 0, 1, 1)` | 4 | Undocumented. This is an ease-**in** (accelerating) — different family entirely |

The two undocumented curves are `[EMERGING]` at best; the standard curve is still solid.

### D4 · "Reserved" fonts are not actually held in reserve

**Playbook §3 says:** "Reserved literary fonts: He loads fonts like LXGW WenKai TC, DM Serif Display, Literata — but holds them in reserve for specific future contexts rather than deploying everything at once."
**Design system §3.1 says:** Literata is "Available but unused in current build." DM Serif Display "Available but unused." LXGW WenKai TC "Available but reserved for future literary contexts."

**Reality:** All three are deployed.

- **Literata** appears 5× in base CSS (lines 2261, 2308, 2319, 2326, 2338) and as `meaningFont` in the `default` and `night-study` drill themes.
- **LXGW WenKai TC** is `charFont` in the `bamboo-grove` drill theme.
- **DM Serif Display** is `meaningFont` in `bamboo-grove`.

Additionally, three fonts are imported in the Google Fonts `@import` (line 8) and used in drill themes but documented **nowhere**:

- **IBM Plex Sans** — `excerptFont` in `bamboo-grove`
- **Raleway** — `meaningFont` in `clean-slate`
- **Lato** — `excerptFont` in `clean-slate`

The "reserved" framing was probably always more aspirational than descriptive. The accurate framing: Tim loads a broad font library and deploys fonts per-theme/per-context. Drill themes especially function as font-and-color bundles.

### D5 · Circle-button sizing has drifted

**Design system §5.1 says:** "Circle Button (`.spicy-btn`, `.group-btn`, `.apikey-btn`) — Size: 2.8rem x 2.8rem."

**Reality:** The newer `.cast-row-btn` family (the vocab/topic/cast triggers, and the spicy button which now uses `class="cast-row-btn spicy-btn"`) is `2.7rem × 2.7rem`. The `.dot-glyph` is `2.6rem × 2.6rem`. The "2.8rem circle button" archetype is no longer accurate as a single value — there's a family ranging 2.6–2.8rem. See C4 below for the touch-target implication.

### D6 · `project-knowledge.md` is still stale (re-stating the 4/29 finding)

The 4/29 audit's Tier-1 #1 was "update `project-knowledge.md` to reflect actual line count, feature state, and missing audit/checklist file references." This is still not done. Quick confirmation:

- Doc claims `index.html` is ~7,600 lines. Actual: 18,092.
- Doc claims "vermillion (Drill), gold (Workshop)" accent mapping. Code in `setTabAccent()` (line 10423) is **blue** (Drill) and **deep rose** `#8b2252` (Workshop). The doc has been wrong about the accent map for at least two audit cycles.
- Doc still lists Z-04 / Z-05 / Z-07 status from before the Cast row and dialogue-archive shipped.
- The session-system section is accurate (added 2026-04-26) but it lives in a doc whose top-line facts are wrong, which limits how much future sessions will trust it.

This is a doc-hygiene problem, not a UX problem, but it's load-bearing for every future Claude session that loads it before working on Zifang. Worth fixing in the same pass that updates the playbook.

---

## 4 · New patterns — choices not yet in the playbook

Per the 2026-04-29 ledger rule, single-project patterns do not get promoted to `[CONFIRMED]` and do not get pushed into the playbook body. They get recorded as candidates for the next cross-project audit (which will be the Claude Code pass). Each entry below is sized like a future ledger row — rich enough that the next audit can pick them up without re-discovering them.

### N1 · The squircle clip-path shape primitive

A single global SVG `<clipPath id="squircle-clip" clipPathUnits="objectBoundingBox">` is now referenced by **12 distinct `url(#squircle-clip)` declarations** in the stylesheet (with the string `squircle-clip` appearing 19 times total across CSS, JS, and comments), applied across pills, dot-opts, cast-row buttons, cards, and other interactive surfaces. It functions as a system-level shape primitive — anywhere the design calls for a "rounded square that isn't quite a rounded-rectangle," Tim now reaches for `clip-path: url(#squircle-clip)` rather than `border-radius: 8px`.

**Why this is interesting beyond Zifang:** the squircle gives a softer, more organic silhouette than CSS `border-radius` does at the same nominal radius, and `clipPathUnits="objectBoundingBox"` lets one path serve every size. This was a deferred candidate in the 4/29 ledger (`squircle-breakdown.md` was a source doc) and has since gone from candidate to load-bearing. Memory already has a `feedback_svg_squircle_rule.md` entry (strip SVG background shapes inside clip-path buttons; crop viewBox to icon content only). The playbook body still says nothing about squircles.

**Promote when:** a second project adopts a clip-path shape primitive (Greenway in particular would be a natural fit for a different shape — a "trail-marker" diamond or similar).

### N2 · Coordinated-sibling rAF animation

This is the deeper pattern underneath D1. The dot-control rewrite is not really about the dot controls — it's the answer to a general problem: when multiple sibling elements all animate at once and have to share a fixed-width container, independent CSS transitions desync and produce bumping. The fix is to write one rAF loop that owns the entire row, treats all siblings as part of a single layout, and uses proximity-based easing (adjacent element accelerates fast, distant elements ease gently).

Memory already has `feedback_cascade_defer_render.md` describing a related pattern (for the 都 pill cascade, run setTimeouts first then `setTimeout(renderX, cascadeDuration)` so heavy renders don't bunch up the stagger). The dot-control rewrite is the next evolution: don't just defer; orchestrate.

**Why this is interesting beyond Zifang:** any project with a row of expandable/collapsible siblings (filter bars, segmented controls, expanding cards) will hit the same desync problem. The pattern transfers.

**Promote when:** a second project uses rAF-orchestrated sibling animation OR the inverse — a project tolerates the CSS-transition desync and Tim deliberately accepts it (which would tell us the threshold for when this pattern is worth its complexity).

### N3 · `filter: blur()` as a containing-block trap (named anti-pattern)

The design system §11 anti-pattern #2 already calls this out specifically: "Never use `filter: blur()` on tab content. This creates a new containing block and traps `position:fixed` modals inside the tab instead of the viewport." The playbook does **not** name this anti-pattern. Its closest neighbor is anti-pattern #8 ("layout-breaking overflow"), which is the same family of bug but a different surface.

This is also a live contradiction (see C1 below), but separate from the contradiction question, the playbook should absorb the anti-pattern itself — `filter: blur()` is dangerous on any element whose descendants include `position: fixed` elements, not just tab content. This is general CSS knowledge that the playbook should encode so it doesn't have to be re-learned via another bug.

**Promote when:** any second project either avoids `filter: blur()` deliberately, or hits the same containing-block trap. Either confirms the anti-pattern is real beyond Zifang.

### N4 · Per-theme font tokens (themes as font+color bundles)

Playbook §3 frames typography as fixed purpose-specific assignments: Chinese display → Noto Serif TC, Chinese UI → Noto Sans TC, Latin → Inter. Drill themes now drive `--drill-char-font`, `--drill-meaning-font`, `--drill-excerpt-font` as CSS variables, so a theme like `bamboo-grove` ships its own typography stack (`LXGW WenKai TC` + `DM Serif Display` + `IBM Plex Sans`) on top of its color stack.

This isn't a contradiction — drill themes are explicitly carved out in the playbook as a context where the rules relax. But the *pattern* of theming-by-CSS-variable-bundle is new and worth recording. It's how Zifang gets meaningful variation inside a tight design system without exploding the system.

**Promote when:** a second project ships a "themes" or "modes" layer that swaps multiple tokens via CSS variable bundles. Greenway's "to brown, SLOWW everything down" instinct is a candidate.

### N5 · The "reserved fonts" framing was wrong (and is therefore not a pattern)

This is a *meta*-finding, not a pattern: the playbook's idea that Tim "holds fonts in reserve for specific future contexts" doesn't describe how he actually works. He loads the library and uses what fits the theme. Worth flagging because future audits will keep mis-classifying this otherwise.

---

## 5 · Contradictions — Zifang choices that conflict with the playbook

### C1 · `filter: blur()` on tab content is still present (and elaborated)

The 4/29 audit's Tier-1 recommendation #5 said: "Replace `filter: blur()` tab transition with opacity-only fade. (Already exists as `tabFadeIn`.)"

**Reality (lines 184–202):** the `filter: blur()` transition has been *expanded* into a two-phase sequential animation. Keyframes `zfTabBlurOut` (`opacity 1→0, filter blur(0)→blur(6px)`) and `zfTabBlurIn` (the inverse) each run for 280ms; the in-animation is delayed 280ms so they don't overlap. The `tabFadeIn` keyframe the audit recommended still exists at line 180 — unused. There is also still an explicit comment in JS (line 8731) noting "tab transitions use filter:blur which breaks…" — i.e., the code knows about the trap and elaborated the broken pattern anyway.

This is not a small choice. It's a multi-audit conscious decision. Possible explanations: (a) Tim prefers the blur feel enough to accept the modal-trap risk, (b) the modal-trap hasn't bitten in practice yet because no modal opens mid-tab-transition, (c) Tim didn't realize the audit recommendation also said the alternative was already implemented.

**Resolution: needs a Tim decision.** If (a), the playbook should absorb the carve-out: "Tim accepts the `filter: blur()` containing-block risk on tab transitions because the blur feel is worth more than the modal-safety guarantee." If (b) or (c), this should actually be fixed. Either way, the playbook should name the anti-pattern (N3 above).

### C2 · Pure white / pure gray in the `clean-slate` drill theme

`clean-slate` ships: `cardBg: '#ffffff'`, `charColor: '#333333'`, `pinyinColor: '#999999'`, `meaningColor: '#333333'`, `excerptColor: '#888888'`, `cardBorder: '1px solid #e8e8e8'`. This directly contradicts playbook anti-pattern #1 ("Pure black or cool gray anything. No `#000`, no `#333`, no `#f5f5f5`") and design system §11 anti-pattern #1.

**But** the design system §2.5 documents `clean-slate` deliberately with these exact values for a "Modern minimalism" feel, and the playbook §9 acknowledges "dark theming in specific contexts (flashcard themes, spicy modal easter egg)" as an explicit carve-out.

**Resolution: not a real contradiction — it's an acknowledged exception that's poorly signposted.** The fix is editorial, not technical: playbook anti-pattern #1 should explicitly reference the flashcard-theme carve-out so future sessions don't try to "correct" `clean-slate` into warm tones.

### C3 · Generic web reds `#dc2626` / `#b91c1c`

`color: #dc2626` appears at lines 5885 and 6017. `color: #b91c1c` appears at lines 6256 and 6463. These are Tailwind's red-600 and red-700 — cooler and more saturated than the system's `--vermillion #c84b31`, and not in the token set. They're used as text color (probably danger/error states — delete modal, destructive confirmation copy).

This contradicts (a) "color as meaning / use tokens" (these should be `var(--vermillion)` or a proper `--danger` token), (b) the warm palette principle (Tailwind reds are deliberately cool-saturated), and (c) the "never raw hex for text or borders" rule the design system states in §2.1.

**Resolution: playbook wins, low severity.** Convert to `var(--vermillion)` or define `--danger: #c84b31` as a semantic alias. This is exactly the kind of slip-in that anti-pattern #12 (hardcoded color ramp) exists to catch.

### C4 · Touch targets under 44px on new components

Playbook §5: "Minimum 44x44px for interactive elements... Tim experienced a rage-inducing incident where a star button collapsed to 26px... Touch target sizing is **non-negotiable**."

**Reality:**

| Component | Size | px (16px root) |
|---|---|---|
| `.cast-row-btn` (vocab/topic/cast triggers + spicy) | `2.7rem × 2.7rem` | 43.2 × 43.2 |
| `.dot-glyph` (workshop dot controls) | `2.6rem × 2.6rem` | 41.6 × 41.6 |
| `.spicy-btn` / `.group-btn` / `.apikey-btn` (per design-system §5.1) | `2.8rem × 2.8rem` | 44.8 × 44.8 ✓ |

The `.cast-row-btn` family is interesting: this is the brand-new component that *resolved* the long-standing buried-Cast flow problem, and it shipped 0.8px below the playbook's "non-negotiable" floor. The `.dot-glyph` has been under-44 for longer.

There's also a pattern worth noting: Zifang's circular controls keep landing right around the 44px threshold. 2.8rem passes; 2.6–2.7rem fails. The fix is trivial (bump to 2.75rem = 44px exactly or 2.8rem), but the more useful playbook update is to frame **2.75rem as the minimum** for any circular interactive element, so the next time someone uses `2.7rem` because it "looks right" they catch it before shipping.

**Resolution: playbook wins. Bump `.cast-row-btn` to 2.75rem; bump `.dot-glyph` to 2.75rem.**

### C5 · Hardcoded hex everywhere (re-stating)

138 six-digit hex occurrences in `index.html`. The most-repeated raw-hex values:

- `#c84b31` × 12 — should be `var(--vermillion)`
- `#b8860b` × 11 — should be `var(--gold)`
- `#5a3800` × 9 — undocumented gold-darker, no token
- `#2c2416` × 9 — should be `var(--ink)`
- `#2d6a4f` × 8 — should be `var(--jade)`
- `#f5f0e8` × 7 — should be `var(--rice)`
- `#faf7f1` × 6 — should be `var(--rice-light)`
- `#8b2252` × 6 — should be `var(--mauve-deep)` (doesn't exist as token; should)
- `#D67D68` × 3, `#feedba` × 2 — undocumented one-offs

This was already known (4/29 multi-project notes: "277 hardcoded color values"). Not new, but still true. No playbook change needed — the rule is already in place. The systemic CSS sweep this implies is a Zifang fix, not a playbook fix.

---

## 6 · localStorage schema sprawl — worse than 4/29 thought

The 4/29 audit said "19 keys, three prefix conventions." Current count: **27 distinct keys, four prefix patterns** (`zf_`, `zifang-`, `nugget-`, bare). The most striking finding:

```
zf_packs_v2, zf_packs_v3, zf_packs_v4, zf_packs_v5, zf_packs_v6, zf_packs_v7, zf_packs_v8
```

Seven versioned pack-storage keys, plus the original `zf_packs_`. This is a schema-migration archaeology layer that should have been consolidated long ago. Each `vN` key represents a moment where the data shape changed and rather than migrate the old key, a new versioned key was added.

This connects directly to `migrate.js`: if Tim is moving to Supabase, the localStorage schema gets to start clean on the other side. But during the transition window, the old keys are still doing work — and if any of them is the actual source of truth for some surface, the migration will lose data without anyone noticing.

**Recommendation:** before flipping the Supabase switch, dump what each `zf_packs_vN` key actually stores in a fresh browser, identify the last one that's actively written, and confirm `migrate.js` is sourcing from that one (currently it sources from inline HTML arrays + JSON files, not localStorage — so user-created cards in the Custom deck and any user-deck memberships may not be in the migration path at all). This is a data-integrity question worth answering before the migration ships.

This isn't a playbook finding — it's a Zifang-specific operational note. But it earns a mention here because the Cowork-to-Claude-Code handoff is the moment to fix it.

---

## 7 · Proposed playbook changes

Split into two categories per the 2026-04-29 ledger rule: **safe corrections** (factual fixes to existing claims, can be made on single-project evidence) and **ledger candidates** (new patterns and refinements that need a second project before promotion).

### 7a · Safe corrections (apply on Tim's approval)

**SC1 — Section 4 #3 (Animation):** Replace the "1.5s bloom" example with an accurate description of the current rAF-driven dot-control behavior, OR generalize the example. Suggested rewrite:

> **Asymmetric timing is intentional.** Tim's most distinctive animation choice: different durations for open vs. close. Where this principle has been most refined (Zifang's dot controls), opening takes ~1+ seconds with a coordinated multi-element animation while closing is instant. This isn't laziness — it's deliberate organic feel. If building a new expandable/collapsible component, propose asymmetric timing.

**SC2 — Section 4 Easing:** Remove the line that names `cubic-bezier(0.4, 0, 0.2, 1)` as "for slow blooms." That curve is no longer in the code. Keep `cubic-bezier(0.25, 0.1, 0.25, 1)` as the confirmed standard. Add an `[EMERGING]` note for `cubic-bezier(0.5, 0, 0.35, 1)` and `cubic-bezier(0.4, 0, 1, 1)` as undocumented additions seen in Zifang, to be characterized when a second project either adopts or rejects them.

**SC3 — Section 4 #4 (Stagger):** The example "stagger by 0.2s each (0.5, 0.7, 0.9...)" is wrong. Replace with a principle-only statement: "Stagger pill/option entrances in sequence; the exact gap and base delay should be tuned to the container's own open animation, not picked off a fixed value."

**SC4 — Section 3 (Typography):** Soften the "reserved fonts" claim. Suggested rewrite:

> Tim loads a broad font library and deploys fonts per-theme or per-context as needed. The base assignment is Noto Serif TC (Chinese display) / Noto Sans TC (Chinese UI) / Inter (Latin), and most surfaces use only those. Themes and special contexts may bring in additional faces — Zifang's drill themes use Literata, LXGW WenKai TC, DM Serif Display, IBM Plex Sans, Raleway, and Lato across four theme variants. "Reserved for future use" was never quite the right framing.

**SC5 — Section 7 (Anti-patterns) #1:** Add an explicit flashcard-theme carve-out so future sessions don't try to "correct" the `clean-slate` theme's pure-white background:

> 1. **Pure black or cool gray anything.** No `#000`, no `#333`, no `#f5f5f5`. Everything should be warm-tinted. *Exception: explicitly themed surfaces (Zifang's `clean-slate` drill theme, the spicy-modal easter egg) may deliberately use cool tones as part of their feel — verify with Tim before "correcting."*

**SC6 — Section 5 (Spacing/Layout) — Touch Targets:** Tighten the rule so 2.7rem doesn't get used by mistake. Suggested rewrite:

> Minimum **44x44px** for interactive elements. Tim experienced a rage-inducing incident where a star button collapsed to 26px and broke the grid. In rem-based projects this means a circular control should be **≥ 2.75rem** (44px exactly at default root). 2.6–2.7rem looks close but is below the threshold. Touch target sizing is non-negotiable.

**SC7 — Section 11 (Audit Ledger):** Append a new row for 2026-05-14 (text in §8 below).

### 7b · Ledger candidates (record now, promote later)

These should be added to the ledger as deferred considerations from this audit, not folded into the body. They are the prep work for the next audit (Claude Code, project #2) to evaluate and either promote or discard.

| Candidate | Source | Promote when |
|---|---|---|
| **Squircle clip-path as a shape primitive** (N1) | `squircle-breakdown.md` + 12 `url(#squircle-clip)` declarations in `index.html` | Second project adopts any global clip-path shape primitive |
| **Coordinated-sibling rAF animation pattern** (N2) | `index.html` `_dcMeasure` / `_dcAnimate` + source comment block | Second project uses rAF-orchestrated sibling animation, OR a project deliberately accepts CSS-transition desync (which tells us the threshold) |
| **`filter: blur()` as a containing-block-trap anti-pattern** (N3) | design-system §11 #2; `index.html` lines 184–202 + comment line 9922 | Second project either avoids `filter: blur()` deliberately or hits the same trap |
| **Per-theme font tokens (theme as font+color bundle)** (N4) | `index.html` THEMES object lines 15870–15910 | Second project ships a "themes" or "modes" layer that swaps multiple tokens together |
| **The single-file vanilla-JS constraint is being retired** | `migrate.js` (Supabase backend migration in progress 2026-05-14) | At project #2 review, decide whether single-file is still a CONFIRMED preference or just an early-stage default Tim moves past once a project earns a backend |

### 7c · Not proposed for the playbook (but should be fixed in Zifang)

These are real findings but they live in Zifang's design-system doc and code, not the playbook. They should be tracked in the pending queue, not the playbook update:

- C1 needs a Tim decision (keep the blur transition vs. revert to `tabFadeIn`).
- C3 hex-red sweep (replace `#dc2626` / `#b91c1c` with `var(--vermillion)`).
- C4 touch-target bumps on `.cast-row-btn` and `.dot-glyph`.
- C5 hardcoded hex sweep across `index.html`.
- D6 `project-knowledge.md` refresh.
- §6 localStorage schema audit before Supabase migration ships.

---

## 8 · Proposed ledger row for Section 11

To be appended at the end of the existing ledger table:

```
| 2026-05-14 | Zifang | _docs/audits/zifang-audit-2026-05-14.md | Drift corrections to Section 3 (typography — "reserved fonts" reframed), Section 4 (animation — 1.5s bloom example, stagger numbers, slow-bloom easing string), Section 5 (touch target floor tightened to 2.75rem), Section 7 (anti-pattern #1 flashcard-theme carve-out). No promotions to [CONFIRMED]. Ledger candidates added (recorded here for future cross-project evaluation, not promoted into body): squircle clip-path shape primitive (now 12 `url(#squircle-clip)` references in Zifang, was a deferred candidate 2026-04-29); coordinated-sibling rAF animation (the dot-control rewrite — replaces the prior CSS bloom); filter:blur() containing-block-trap as a named anti-pattern; per-theme font tokens; the single-file vanilla-JS constraint is now being deliberately retired (Supabase migration in flight). Live contradiction noted but not resolved in the playbook: tab transitions still use filter:blur() despite design-system §11 #2 forbidding it — needs Tim's call on whether this is a carve-out he wants to keep or a real fix. |
```

---

## 9 · Things to explicitly preserve (don't touch on the playbook update pass)

- **Section 2 — Color temperature, color as meaning, accent architecture, color-mix() pill ramp pattern.** All still accurate; 19 `color-mix()` uses in `index.html` confirm the pattern is holding.
- **Section 4 — Core animation principles (no bounce, slow over snappy, opacity + transform together, instant active states).** All still accurate. Only the specific examples and easing string need correction.
- **Section 5 — Mobile-first 480px, generous padding / tight gaps, border-radius scale.** Still accurate. Only the touch-target floor needs tightening (SC6).
- **Section 6 — Modal float-up pattern (`scale(0.96) translateY(8px)`).** Verified across 7 modals in `index.html`. Pattern is solid.
- **Section 7 anti-patterns #2–#12.** All still hold. Only #1 needs the flashcard-theme carve-out (SC5).
- **Section 8 — Interaction philosophy (tactile, information on demand, bilingual by default).** All still accurate.
- **Section 11 ledger structure and rules.** The provenance caveat and "no [CONFIRMED] without project #2" rule are doing exactly what they were designed to do — gating this audit's natural tendency to over-promote single-project patterns. Keep them.

---

## 10 · What this audit deliberately did NOT do

- Did not re-derive the taste profile from scratch (Tim declined the option).
- Did not edit `tims-ux-playbook/SKILL.md`. Per the agreed deliverable, this audit is review-first; the playbook edit is a second pass after Tim reads this doc.
- Did not read raw chat transcripts. The prior audit docs distill the relevant chat history, and the code is the ground truth.
- Did not audit content data (HSK4 Taiwan-modern overrides, HSK5 component readings, chengyu schema) — the 4/29 audit covered these and they're not playbook-relevant.
- Did not modify `project-knowledge.md` even though it's stale. That's a separate hygiene task; doing it inside this audit would muddy the deliverable.
- Did not address the audio gap. The 4/29 audit's #1 finding (zero audio in a project explicitly built for someone whose stated bottleneck is the spoken-anxiety gap) is restated by reference: still true, still the biggest single-feature recommendation, still trivially shippable via `speechSynthesis`. Not a playbook issue, so not expanded here.

---

*Audit complete. Next step: Tim reviews the proposed changes in §7. On approval, second pass writes them into `tims-ux-playbook/SKILL.md` and appends the ledger row.*
