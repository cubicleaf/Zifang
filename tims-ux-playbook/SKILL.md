> **DEPRECATED (2026-07-11).** This file is NO LONGER the source of truth.
> The canonical playbook now lives at `~/Documents/ux-playbook/PLAYBOOK.md` (canon v1.0.0)
> with evidence/ledger at `~/Documents/ux-playbook/corpus/LEDGER.md`. This copy is frozen at
> its 2026-06-10 state, which was carried into canon v1.0.0 in full (fork-check verified).
> Do not edit. Safe to archive or delete during location cleanup.

---
name: tims-ux-playbook
description: "Tim's personal UX/UI design playbook — his confirmed aesthetic preferences, design process, interaction patterns, and anti-patterns distilled from iterative work across multiple web projects. Use this skill whenever doing ANY UI/UX design work for Tim: building new interfaces, styling components, choosing colors, setting animation timing, picking fonts, creating layouts, or making any visual/interaction design decision. Also trigger when Tim asks about design options, A/B comparisons between visual approaches, or says things like 'make it look right', 'dial this in', 'fix the feel', 'too busy', 'too fast', 'slow it down'. Even if Tim doesn't explicitly mention design — if the task involves HTML/CSS/JS that affects what the user sees or interacts with, load this skill."
---

# Tim's UX Playbook

This document captures Tim's confirmed design sensibilities — what he reaches for, what he rejects, and how he works. It exists so you don't have to rediscover his taste from scratch every session.

**Important distinction:** This is a *taste profile*, not a project-specific design system. For project-specific patterns (exact tokens, component inventories, architecture rules), load the relevant project docs. This skill tells you *why* Tim makes the choices he does and what to default to when he hasn't specified.

**Confidence levels:** Preferences marked **[CONFIRMED]** are backed by multiple data points across **two or more distinct projects** (repeated choices, explicit corrections, transcript evidence). Preferences marked **[STRONG SIGNAL]** appeared consistently but with variation across projects, or remain single-project evidence under continued observation. Preferences marked **[EMERGING]** are patterns noticed in limited data — use as defaults but don't fight Tim if he wants something different.

**Provenance caveat (updated 2026-05-23):** This playbook was originally seeded almost entirely from a single project (Zifang). On 2026-05-23 a triangulation audit added Cleveland Greenway Cleanup (GWC), Fernweh, and Generations as evidence sources. Items now marked `[CONFIRMED]` have been corroborated across two or more projects. Items marked `[STRONG SIGNAL]` either showed up in 2+ projects with implementation variation, or remain Zifang-only pending further triangulation. See **Section 11 — Audit Ledger** for the full source-of-evidence record.

---

## 1. HOW TIM WORKS (Process)

Understanding Tim's process is as important as knowing his aesthetic preferences. Design decisions that ignore how he works will frustrate him regardless of how they look.

### The Two-Phase Pattern

Tim's projects follow a consistent creation pattern:

**Phase 1 — Creative Direction.** Tim provides extensive verbal input at the start of a project explaining what he wants and why. This initial briefing is detailed and intentional — it's not casual brainstorming, it's him setting the vision. Take this input seriously. It often contains aesthetic vocabulary and references that should inform every subsequent choice.

**Phase 2 — Obsessive Refinement.** Once a direction is set, Tim iterates relentlessly on execution details. He will go back and forth on exact animation timing, exact font sizes, exact color values, exact spacing until they feel right to him. This is not indecision — it's precision. Don't try to shortcut this process or suggest he's overthinking it. The details are the point.

### What This Means for You

- **When Tim hasn't specified something:** Make your best guess based on his established preferences (documented below), but flag what you chose and why. Don't silently accept defaults.
- **When Tim is iterating:** Give him specific, comparable options. "I can set this to 0.3s, 0.5s, or 0.8s — here's how each would feel" is better than "what timing do you want?"
- **When presenting options:** Tim responds well to 2-3 distinct HTML prototypes with radically different feels along the same outcome. This helps him triangulate his preference faster than incremental tweaks.
- **When explaining changes:** Always state the goal, the problem, and what you did, in plain language. Include exact values — units, colors, durations, easing functions. Tim wants to understand and learn the technical language, not be shielded from it.

### The "Not Yet Finished" Distinction

Tim juggles multiple projects and has switching costs. If a design choice in one of his projects looks unpolished or inconsistent with his taste, it's more likely he hasn't gotten to it yet than that he chose it deliberately. Ask before assuming a choice is intentional in a project he describes as "still cooking."

What Tim refines *first* when time is scarce reveals what bothers him most. That priority ordering is itself taste data.

### Decision Hierarchy by Project Type [STRONG SIGNAL]

Tim's projects consistently exhibit an implicit decision hierarchy in their code — a stable priority ordering between accessibility, performance, aesthetics, and cleverness. But **the order varies by project type**, and trying to apply a single universal hierarchy will produce friction.

**Observed patterns (2026-05-23 triangulation):**
- **Conversion/utility projects** (GWC): Accessibility → Performance → Aesthetics → Cleverness. Things have to work, fast, before they get to look good.
- **Functional/content projects** (Generations): Accessibility → Robust Interaction → Aesthetics → Clever Effects. Similar to conversion but with more room for interaction polish.
- **Aesthetic-forward projects** (Fernweh): Aesthetics → Simplicity → Cleverness → Accessibility. The experience itself is the point; accessibility is acknowledged but secondary to the affective intent.

The meta-rule is that Tim's code *has* an implicit hierarchy, even when he hasn't named it. **Read the hierarchy from the project type before evaluating individual choices** — what looks like a violation in one project type may be a legitimate trade-off in another. If you're not sure what type a project is, ask Tim. Don't assume.

This is a meta-principle for evaluating Tim's work, not a prescription for new work. When building new components, default to the order appropriate to the project's intent.

---

## 2. VISUAL IDENTITY — What Tim Reaches For

### Color Temperature [CONFIRMED]

Tim gravitates toward **warm** palettes. His base colors across projects use warm off-whites, warm near-blacks, and earth-toned neutrals. He avoids cool grays and sterile whites.

- **Backgrounds:** Warm off-whites (cream, rice, parchment range — think `#f5f0e8` to `#faf7f1`). Never pure `#ffffff` as a page background. Never cool gray (`#f5f5f5`, `#e5e5e5`).
- **Text:** Warm near-black (`#2c2416` range) rather than pure `#000000`. His text hierarchy uses warm desaturated tones, not gray scale.
- **Borders/Dividers:** Sand-toned, not gray (`#ddd5c4` range, not `#cccccc`).
- **Shadows:** Always warm-tinted rgba using ink tones (e.g., `rgba(44,36,22,0.08)`). Never pure black shadows (`rgba(0,0,0,x)`).

**Backlog signal [STRONG SIGNAL]:** Tim noted wanting to shift Cleveland Greenway project "to brown, SLOWW everything down" — reinforcing warm color temperature and deliberate pacing as cross-project instincts.

### Color as Meaning [CONFIRMED]

Colors in Tim's work are never decorative — they always communicate something. Each color earns its place by mapping to a function, state, or category. If you're adding a new color, you need a reason for it to exist.

Common semantic mappings he's established:
- **Gold/amber:** Favorites, premium, settings
- **Vermillion/red-orange:** Creation, fire, custom content, errors, warnings
- **Jade/deep green:** Exploration, nature, calm
- **Blue (steel):** Study, focus, practice
- **Deep rose/mauve:** Craft, conversation, warmth

### Accent Architecture [CONFIRMED]

Tim uses a dynamic accent system where context determines the accent color. In Zifang, each tab swaps `--accent` via CSS custom properties. Components reference the variable, not the color — so everything recolors automatically when context changes.

When building new projects, propose a similar approach: define the accent semantically, swap it by context, and let components inherit.

### The Color Ramp Pattern — `color-mix()` [CONFIRMED]

Tim's pill-shaped UI elements (filter bubbles, deck chips, segment controls) use a two-tone tinted appearance derived from the accent color — a light-tinted background with a medium-tinted text. The formula is always: blend the semantic color at **20% into the base background** for the pill bg, and at **70% into the base background** for the pill text.

**The wrong approach** (what kept happening before): manually computing the blended hex values and hardcoding them. This produces values like `#CDD5C9` and `#69927D` that are correct once but drift in future sessions as slight variations accumulate.

**The right approach**: CSS `color-mix()` computes the blend natively and stays reactive to variable changes:

```css
/* In :root — define once, use everywhere */
--accent-pill-bg:   color-mix(in srgb, var(--accent) 20%, var(--rice));
--accent-pill-text: color-mix(in srgb, var(--accent) 70%, var(--rice));

/* For fixed semantic colors, same pattern: */
--vermillion-pill-bg:   color-mix(in srgb, var(--vermillion) 20%, var(--rice));
--vermillion-pill-text: color-mix(in srgb, var(--vermillion) 70%, var(--rice));
--gold-pill-bg:         color-mix(in srgb, var(--gold)       20%, var(--rice));
--gold-pill-text:       color-mix(in srgb, var(--gold)       70%, var(--rice));
--mauve-pill-bg:        color-mix(in srgb, var(--mauve)      20%, var(--rice));
--mauve-pill-text:      color-mix(in srgb, var(--mauve)      70%, var(--rice));
```

**State pattern is always a swap** — unselected and selected just invert each other:
```css
.pill.unselected { background: var(--accent-pill-bg);   color: var(--accent-pill-text); }
.pill.selected   { background: var(--accent-pill-text); color: var(--accent-pill-bg);   }
```

**The bonus**: because `--accent-pill-bg` uses `var(--accent)`, and `setTabAccent()` already updates `--accent` when the user switches tabs, all pills recolor automatically at no extra JS cost. This is what Tim always wanted — and why the manual hex values existed in the first place (failed attempts to solve this before `color-mix()` was viable).

`color-mix()` is supported in all modern browsers (Chrome 111+, Safari 16.2+, Firefox 113+). Use it without hesitation in Tim's projects. If building for an environment that requires older browser support, flag it — but that has not been a constraint in any of Tim's current projects.

### Material Metaphor & Paper Texture [CONFIRMED]

Tim's projects reach for **paper, ink, and earth-material vocabulary**, not digital-flat surfaces. The expression varies across projects, but the underlying instinct is consistent: surfaces should feel like material, not pixels.

**Three observed forms (2026-05-23 triangulation):**

1. **Literal texture overlay** (Zifang, Generations): A `body::before` pseudo-element with an SVG fractal-noise texture at very low opacity (`opacity: 0.02–0.025`). Visually almost invisible, but it kills the "screen-flat" feeling. The texture survives even on dark backgrounds (Generations adapts it for dark context).

2. **Material naming/vocabulary** (GWC, Fernweh): Token names use material words — `--parchment`, `--ink`, `--loam`, `--dirt` — even when no literal texture is applied. The naming choice carries the metaphor forward into how Claude/Tim think about the surface. Pairs with manuscript/serif typography to reinforce it.

3. **Ambient material gestures** (Fernweh): CSS gradients that imitate uneven paper aging, "kintsugi gold" rules drawn over ink seams, manuscript-like reveal pacing. The material isn't simulated — it's *gestured at*.

**For new projects:** Default to at least one of these three forms. The cheapest is name-the-tokens-after-materials. Adding the noise overlay costs ~5 lines of CSS and one inline SVG; it's worth proposing for any project that wants to feel less "screen." Don't apply all three at once — pick the form that fits the project's affective intent.

---

## 3. TYPOGRAPHY [CONFIRMED]

### Font Philosophy

Tim uses purpose-specific font assignments, not a single-font stack. Each script and role gets its own typeface:

- **Chinese display:** Serif (Noto Serif TC) for characters that should feel literary/substantial
- **Chinese UI:** Sans-serif (Noto Sans TC) for labels, buttons, navigation
- **Latin/English:** Clean sans-serif (Inter) for all Western text
- **Reserved literary fonts:** He loads fonts like LXGW WenKai TC, DM Serif Display, Literata — but holds them in reserve for specific future contexts rather than deploying everything at once

### Size Hierarchy [CONFIRMED]

The primary content (e.g., Chinese characters) is always the largest element on screen. Supporting content (pinyin, English) is always smaller, in a consistent hierarchy: **characters > pinyin > English > labels > micro text**.

Tim cares deeply about font sizing and will iterate on sizes across multiple sessions until they feel right. Don't approximate — get specific with `rem` values and be prepared to adjust by 0.05rem increments.

---

## 4. ANIMATION & TIMING [CONFIRMED]

This is one of Tim's strongest preference areas. He has iterated extensively on timing across multiple projects and multiple sessions.

### Core Principles

1. **No bounce. No overshoot. No spring physics.** Everything eases smoothly. Tim has never once requested or approved a bouncing animation. This is a hard rejection.

2. **Slow and deliberate over fast and snappy.** Tim has explicitly requested slower animations on multiple occasions ("SLOWW everything down", "Fernweh needs to be 2x a slow", "fade transitions could be improved" on Generations). When in doubt, err toward slower. A 0.3s transition is safer than a 0.15s one. A 0.5s entrance is safer than a 0.25s one.

3. **Asymmetric timing is intentional.** Tim's most distinctive animation choice: different durations for open vs. close. In Zifang's dot controls, opening is a slow 1.5s bloom while closing is instant. This isn't laziness — it's deliberate organic feel. If building a new expandable/collapsible component, propose asymmetric timing.

4. **Stagger sequences, don't batch.** When multiple elements appear (e.g., a row of pills), they should cascade in with staggered delays (0.2s apart), not all appear simultaneously. This creates a "reveal" feeling.

5. **Opacity + transform together.** Elements enter by fading in AND moving/scaling simultaneously. The standard entrance pattern is `opacity 0→1` paired with either `translateY(small→0)` or `scale(0.96→1)`. Never just pop in.

6. **Active/press states are instant.** Button presses (`scale(0.95)`) should have zero transition delay — immediate tactile feedback on touch. The animation principles about "slow and deliberate" apply to *entrances and transitions*, not to user input response.

7. **Cascade-then-render: container first, content second.** When the page or a major section loads, the container/skeleton lays out first (often at `opacity: 0` or with a deliberate short delay), and then content cascades into it. This was observed identically across Zifang, GWC, Generations, and Fernweh. The pattern produces a "settled then revealed" feel rather than a "popped in" feel. Implementation varies: explicit staged keyframes (Generations: structure → title at 50ms → subtitle at 1000ms → cards at 2000ms+), CSS comments naming the intent (GWC), or a global initial delay before any reveal begins (Fernweh's 300ms pre-reveal pause). The key is: **don't render content into an unsettled container**. Let the container exist first.

### Timing Reference

These are Tim's established comfort zones for common transitions:

| Type | Duration | Notes |
|------|----------|-------|
| Micro-interaction (hover color, border) | 0.2–0.3s | Standard |
| Modal/panel entrance | 0.25s | Scale + translate + fade |
| Content reveal (accordion, expand) | 0.5–0.6s | Can go longer for large reveals |
| Ambient/atmospheric | 1.0–1.5s | Slow blooms, environment transitions |
| Button press | Instant | scale(0.95), no transition-duration |

### Easing

Tim uses custom cubic-beziers, not keyword easings. His standard curve is `cubic-bezier(0.25, 0.1, 0.25, 1)` — a gentle ease-out with a soft start. For slow blooms: `cubic-bezier(0.4, 0, 0.2, 1)`.

---

## 5. SPACING & LAYOUT [CONFIRMED]

### Mobile-First, Single-Column

Tim designs at **480px max-width**, tested on iPhone 13 Mini viewport. Desktop is just the mobile layout centered. He has not built responsive multi-column layouts — the pattern is a single column that looks good at mobile width and doesn't break at desktop.

### Touch Targets [CONFIRMED]

Minimum **44x44px** for interactive elements. Tim experienced a rage-inducing incident where a star button collapsed to 26px and broke the grid. Touch target sizing is non-negotiable.

### Generous Padding, Tight Gaps

Tim likes breathing room around containers (1.5rem horizontal padding as the "rail") but tight spacing between related items (0.5rem gaps between pills, 0.75rem between cards). The pattern: macro-spacing is generous, micro-spacing is compact.

### Border Radius Scale [CONFIRMED]

Tim uses a deliberate radius system, not arbitrary values:
- **Rectangular containers:** 12px
- **Small interactive elements:** 8px
- **Pill-shaped elements:** 20px
- **Circles:** 50%

Don't introduce new radius values without a reason.

---

## 6. COMPONENT PATTERNS [CONFIRMED]

### Buttons — Minimal Chrome

Tim's buttons tend toward minimal visual weight. His primary action buttons are often text-only with no background — just accent-colored text in a heavy serif weight. Ghost buttons (border, no fill) are for secondary actions. Full-fill buttons are rare and reserved for selected/active states of toggles.

The universal active state: `scale(0.95)` on press. This is Tim's tactile feedback pattern.

### Cards — Paper Metaphor

Cards are the primary content container. They sit on a warm paper background with subtle warm shadows. On hover, shadow deepens slightly and the card may lift 1px. Tim uses left-side accent bars (thin, 3px) to indicate state on cards.

### Modals — Float Up and Solidify

Every modal follows the same entrance: backdrop fades in (warm ink overlay, ~45% opacity) while the card scales from 0.96→1 and translates from 8px→0, all at 0.25s. This "float up" pattern is consistent and should be preserved in all new modals.

### Pills — The Universal Selector

Pill-shaped elements (20px radius) are Tim's go-to for selection UI: category filters, tags, option selectors. Two states: selected (accent fill + white text) and unselected (muted bg + faint text). Always with `scale(0.95)` press feedback.

### Icon Buttons — The SVG IS the Button [CONFIRMED]

When Tim hands over an SVG that already includes its own background shape (e.g. a squircle/rounded-square `opacity="0.5"` fill behind the glyph), that SVG **is the entire button face** — not an icon to be placed inside another button shell. Don't wrap it in a `div`/`button` that has its own `background`, `border`, or `border-radius`. That produces a "squircle inside a squircle" — a small icon floating inside a larger duplicate button shape.

**The right approach:** size the wrapper to match the SVG's intended display size, set the wrapper's background/border/radius to none/transparent, and let `svg { width: 100%; height: 100%; }` so the SVG's own background path fills the clickable area. Use `currentColor` in the SVG paths so it inherits the theme's ink color and responds to hover state changes.

**Two-state toggle icons** (e.g. expand/collapse): bake both SVGs into the markup stacked on top of each other, and crossfade between them via a `data-state` attribute + CSS transition (opacity/scale/rotate). Don't swap `innerHTML` — that kills any CSS transition, producing an instant snap (anti-pattern #6).

---

## 7. ANTI-PATTERNS — What Tim Rejects [CONFIRMED]

These are things that have caused frustration, explicit correction, or negative reactions. Avoid them.

1. **Pure black or cool gray anything.** No `#000`, no `#333`, no `#f5f5f5`. Everything should be warm-tinted.
2. **Bouncing/spring animations.** No elastic easing, no overshoot. Ever.
3. **Decorative color.** Every color must mean something. No color for color's sake.
4. **Cluttered UI / visual noise.** Tim pushes back on "too busy." When in doubt, remove elements rather than add them. He's simplified topic presets from 15 to 6, stripped unnecessary affordances.
5. **Small touch targets.** The 26px star incident. Never again.
6. **Instant state changes without transitions.** Things appearing/disappearing without animation feels broken. Even a 0.2s fade is better than a snap. **Reconfirmed across all 2026-05-23 audits** — Generations had a `display:none` → `display:flex` backdrop snap, Fernweh's overlay technique papers over the same anti-pattern.
7. **Transitions defined only on the active state.** This causes snap-to-end on removal. Tim caught this bug across multiple projects. Define transitions on the base class, not just the `.active` or `.go` state. **Reconfirmed in Fernweh (2026-05-23)** — transitions only on `.show` / `.char.on` / `.mist.on` would surface as snap-to-end if fade timing shortened.
8. **Layout-breaking overflow.** Never `height: 100dvh; overflow: hidden` on main containers — it traps content. Use `min-height` with managed internal scroll. (Exception: a full-screen immersive single-pane experience like Fernweh's parchment view, where overflow:hidden is deliberate — confirm intent before flagging.)
9. **Silent defaults.** Don't make design choices without flagging them. Tim wants to know what you chose and why, even if it's minor.
10. **Removing elements without checking references.** Always verify `getElementById` and event listener references before removing HTML elements. Tim has been burned by cascading breaks.
11. **Skipping the explanation.** Tim is learning web development. Every change needs: what was the goal, what was the problem, what did you do. Include exact CSS values, exact timing, exact colors. Teach the vocabulary.
12. **Hardcoding computed color ramp values.** If a color is derived from another color (e.g., "jade at 20% opacity blended into rice"), never store the computed hex result as a static value. Use `color-mix()` so the relationship stays live. Hardcoded ramp values (`#CDD5C9`, `#69927D`, etc.) look fine initially but drift across sessions, producing near-identical-but-not-quite colors everywhere. See Section 2 "The Color Ramp Pattern" for the correct approach.
13. **Double-housing a self-contained icon SVG.** If an SVG already draws its own background shape (squircle, circle, etc.), don't also give its wrapper a `background`/`border`/`border-radius` and shrink the SVG inside it. The SVG *is* the button. See Section 6 "Icon Buttons — The SVG IS the Button." Caused a recurring bug across Marius/P&C collapse-toggle buttons (2026-06-10).

---

## 8. INTERACTION PHILOSOPHY [CONFIRMED]

### Tactile Over Visual

Tim prefers interactions that feel physical. Button presses scale down. Cards lift on hover. Elements bloom open rather than snap. The metaphor is handling real objects — paper, buttons, cards — not clicking pixels.

### Information on Demand

Tim uses progressive disclosure: hover-pinyin (desktop) / long-press-pinyin (mobile), expandable cards, dot controls that bloom options. The resting state of the UI should be clean and quiet. Detail appears when requested and retreats when attention moves elsewhere.

### Affordance Signals for Hidden Features [STRONG SIGNAL]

Progressive disclosure only works if users can *find* the hidden features. Tim's projects consistently respect this — every nested or interaction-revealed feature has *some* signal that it exists — but there's a **consistent gap pattern** that's worth flagging.

**Where signals are present (2026-05-23 triangulation):**
- Zifang: dot controls have visible dot affordances; expandable cards show subtle chevrons
- GWC: the CTA itself is the affordance for the modal — explicit and unambiguous
- Generations: desktop hover-then-click is self-evident; navigation hints fade in after the user settles
- Fernweh: navigation hint fades in deliberately after user settles, signaling forward motion

**The recurring gap — secondary affordances:**
- Generations mobile two-tap (emphasize → open) has no affordance signal for the second tap
- Fernweh skip-forward has no signal at all; backward navigation is hint-only

**The principle:** Every interaction-revealed feature should have *some* signal — even a small one. If a project has a primary interaction that's well-signaled, but a secondary interaction (two-tap, skip-back, alt-modifier) that isn't, the secondary is likely a real usability gap, not an intentional easter egg. Ask Tim if the missing signal is deliberate before assuming it's intentional.

### Bilingual by Default

In Tim's Chinese-learning projects, every label shows Chinese first (with hover-pinyin access), then English. This is non-negotiable in that context. In other projects, the principle still applies: primary content first, supporting context available on interaction.

---

## 9. WHAT TIM DOESN'T CARE ABOUT (or hasn't specified)

Being honest about gaps prevents false confidence. These areas don't yet have strong signal:

- **Desktop-specific layouts:** Tim designs mobile-first and hasn't invested in desktop-specific experiences
- **Dark mode (as a system preference):** He has dark theming in specific contexts (flashcard themes, spicy modal easter egg, Generations dark surface) but no system-wide dark mode preference expressed
- **Icon style:** Uses SVG icons but hasn't expressed strong preference for a specific icon family or style
- **Grid vs. flexbox preference:** Uses both as needed, no strong philosophical preference
- **SEO/performance optimization:** Not a stated priority in his current work
- **Accessibility beyond touch targets:** Knows there are gaps (documented in Zifang audit; GWC missing `prefers-reduced-motion`, modal focus trap; Fernweh accessibility comes last in implicit hierarchy by design) but hasn't prioritized fixes yet
- **Multi-page architecture:** GWC's success.html is the only confirmed multi-page case so far. No cross-page navigation patterns established.

---

## 10. USING THIS SKILL

When you load this skill for a design task:

1. **Check for a project-specific design system doc first.** This playbook gives you Tim's general taste. The project doc gives you exact tokens and components. Use both.
2. **Read the project type before evaluating choices.** Conversion site, content site, aesthetic-forward — the implicit decision hierarchy (Section 1) varies by type. What looks like a violation in one type may be a legitimate priority trade-off in another.
3. **Default to the preferences here when the project doc doesn't cover something.** Warm colors, slow animations, no bounce, minimal button chrome, 44px touch targets, cascade-then-render entrances.
4. **Flag your choices.** Tim wants to see what you decided and why. Don't silently implement defaults — even if they match this playbook perfectly, call them out.
5. **Propose, don't prescribe.** Give Tim 2-3 options with specific values when you're in unfamiliar territory. He'll tell you which direction to go and then you'll iterate together on the details.
6. **Explain in plain language.** Tim is actively learning web development. Use technical terms but always define them on first use. State which language (CSS, JS, HTML) you're working in. Include exact values.

---

## 11. AUDIT LEDGER

This ledger tracks every audit, design-system event, or evaluation pass that has either modified this playbook or been considered for inclusion. The purpose is to keep the playbook's confidence levels honest by exposing exactly what evidence supports them.

**Rules of the ledger:**

1. Every audit on any project should add a row, even when no playbook changes follow. "None — single-project evidence" is a valid and useful entry — it captures the *deliberate non-decision* and prevents the same change from being re-proposed naively in a future session.
2. A preference is only eligible for promotion to `[CONFIRMED]` once it appears in audits across at least **two distinct projects**. Until then, it stays `[STRONG SIGNAL]` or unmarked, no matter how strongly it shows up in a single project.
3. When integrating a change, name the section that was modified so future readers can trace cause and effect.
4. Append-only. Don't rewrite past entries — if a previous decision was wrong, add a new row that supersedes it and cite the original date.

### Ledger

| Date | Project | Source Doc | Playbook Changes Integrated |
|------|---------|------------|------------------------------|
| 2026-04-03 | Zifang | `markdowns/zifang-ux-audit-2026-04-03.md` | (Pre-ledger, retrospective entry.) Initial taste profile drafted from baseline UX audit. Section 2 (color), Section 3 (typography), Section 5 (spacing), Section 6 (component patterns), and Section 7 (anti-patterns) seeded from Zifang findings. |
| 2026-04-13 | Zifang | `markdowns/zifang-design-system.md` (locked); `markdowns/squircle-breakdown.md` | Color-mix pill ramp pattern promoted to `[CONFIRMED]` in Section 2. Anti-pattern #12 added (no hardcoded color ramp values). Last full-playbook timestamp prior to this entry. |
| 2026-04-29 | Zifang | `markdowns/zifang-audit-2026-04-29.md` | Section 11 (this ledger) introduced. Provenance caveat added near top. **No individual preferences promoted or added** — single-project evidence judged insufficient for cross-project taste claims. The following proposed additions were considered and deferred: paper-texture as cross-project pattern, body-portal tooltip technique, cascade-then-render timing rule, SVG-in-squircle cropping rule, discoverability-of-nested-features principle, Decision Hierarchy section. All recorded here for re-evaluation when project #2 reaches comparable polish. Asymmetric open/close timing was already in Section 4 #3 — no edit needed. |
| 2026-05-23 | Cleveland Greenway Cleanup (GWC) | `_meta/audits/playbook audits/2026-05-23_gwc-fernweh-generations/gwc-ux-audit-2026-05-23.md`; `gwc-playbook-audit-2026-05-23.md` | First non-Zifang audit. **Findings:** paper-texture present in modified form (material vocabulary — loam, dirt, parchment — without literal noise overlay); cascade-then-render present and CSS-commented; discoverability principle present (CTA is explicit affordance); decision hierarchy present in aspirational order (a11y → perf → aesthetics → cleverness). Body-portal tooltip and SVG-in-squircle absent (no use case — GWC has no tooltips and uses a circle clip-path, not squircle). **New candidate proposed:** mode-aware semantic token scoping — re-pinning CSS tokens inside a mode selector (e.g., `body.light-mode .modal { --cream: ...; }`) so descendants inherit correctly without per-element overrides. Single-project for now; defer. |
| 2026-05-23 | Fernweh | `_meta/audits/playbook audits/2026-05-23_gwc-fernweh-generations/fernweh-ux-audit-2026-05-23.md`; `fernweh-playbook-audit-2026-05-23.md` | Second non-Zifang audit. **Findings:** paper-texture present in strongest form (token names `--parchment`/`--ink`, manuscript fonts, kintsugi gold rule); cascade-then-render present (modified — implemented via animation sequencing with 300ms pre-reveal pause); discoverability present with gap (navigation hints fade in deliberately, but skip-forward has no signal); decision hierarchy present but **inverted** (aesthetics → simplicity → cleverness → accessibility) — this is the key finding that establishes the "hierarchy order depends on project type" rule now in Section 1. Anti-pattern #7 (transitions only on active state) reconfirmed — papered over by overlay technique but architecturally present. Body-portal tooltip and SVG-in-squircle absent (no use case — no tooltips, no SVG, no images). **New candidate proposed:** deliberate latency as aesthetic signal (4.5s blank-parchment pause before first word). Extends "slow and deliberate" from animation timing into intentional stillness as affective threshold. Single-project for now; defer. |
| 2026-05-23 | Generations | `_meta/audits/playbook audits/2026-05-23_gwc-fernweh-generations/generations-ux-audit-2026-05-23.md`; `generations-playbook-audit-2026-05-23.md` | Third non-Zifang audit. **Findings:** paper-texture present in literal form (identical `body::before` SVG fractal noise at `opacity: 0.025`, adapted for dark context); cascade-then-render present (explicit staged keyframes: structure → title 50ms → subtitle 1000ms → cards 2000ms+); discoverability partially present (two-tap mobile pattern lacks affordance signal — gap); decision hierarchy present in aspirational order. Body-portal tooltip absent (no tooltips — though morph clone IS appended to `<body>` to escape carousel overflow, that's a different use case). SVG-in-squircle absent (no use case). **New candidate proposed:** morph-clone shared-element transition (card expands into fullscreen viewer, clone preserves carousel layout, extensively documented inline). Architecturally consistent with "tactile over visual." Single-project for now; defer. |
| 2026-05-23 | **Synthesis (orchestrator)** | This audit | **Promotions to `[CONFIRMED]`** (2+ project corroboration): (1) Material Metaphor & Paper Texture added to Section 2 with three documented expressions (literal overlay, material naming, ambient gestures); (2) Cascade-then-render added to Section 4 as Core Principle #7. **Promotions to `[STRONG SIGNAL]`**: (3) Affordance Signals for Hidden Features added to Section 8, including the recurring "secondary affordance gap" pattern; (4) Decision Hierarchy by Project Type added to Section 1 — meta-principle confirmed, but order is project-type-dependent (Fernweh's inversion drove this nuance). **Remain deferred** (0–1 project corroboration): body-portal tooltip technique (no use case in any of GWC/Fernweh/Generations — defer until a tooltip-using project audits); SVG-in-squircle cropping rule (no use case — defer until an icon-grid or avatar-style project audits). **New candidates logged**: mode-aware token scoping (GWC), deliberate latency as aesthetic signal (Fernweh), morph-clone shared-element transition (Generations). Anti-pattern #6 and #7 reconfirmed with new examples. Anti-pattern #8 softened with explicit exception note for full-screen immersive contexts (Fernweh). Provenance caveat updated to reflect first cross-project triangulation. |

### How to read this ledger

If you are a future Claude session loading this skill: before proposing any addition to the playbook, scan the ledger. If the pattern you want to add appears only in audits of a single project, your default should be to defer — record it in the ledger as a deferred consideration rather than push it into the body. The body of this playbook is not a notepad for "things noticed in one project." It is a record of preferences that have proven themselves portable.

### Deferred Items — Watching For

These items have been observed but not yet corroborated across enough projects to enter the playbook body. When auditing a future project, check explicitly for these:

| Deferred Item | Seen In | Why Still Deferred | What Would Promote It |
|--------------|---------|-------------------|----------------------|
| Body-portal tooltip technique | Zifang only | No tooltip use case in GWC, Fernweh, or Generations | Audit of a project with hover-reveals or supplementary tooltip content |
| SVG-in-squircle cropping rule | Zifang only | No use case in GWC (circle clip-path), Fernweh (no SVG), Generations (no icon grid) | Audit of a project with icon grids or avatar-style imagery |
| Mode-aware semantic token scoping | GWC only (2026-05-23) | Solves a real cross-project problem but only observed once | Same pattern appearing in any future multi-mode project |
| Deliberate latency as aesthetic signal | Fernweh only (2026-05-23) | Extends Section 4 timing but conceptually distinct (stillness, not motion) | Another aesthetic-forward project using intentional empty time as threshold |
| Morph-clone shared-element transition | Generations only (2026-05-23) | Sophisticated pattern, architecturally consistent with "tactile" but only one implementation | A similar card-to-fullscreen or shared-element pattern in any other project |

---

*Last updated: 2026-05-23*
*Confidence basis: Zifang design system audit, 8+ session transcripts, direct conversation about process and preferences, Notion project backlog review, **first cross-project triangulation pass complete** (GWC + Fernweh + Generations, 2026-05-23). Items now marked `[CONFIRMED]` have been corroborated across 2+ projects; see Section 11 for the audit ledger.*
*Next update: When a future project audit corroborates a currently-deferred item, or surfaces a new pattern that appears in 2+ projects.*
