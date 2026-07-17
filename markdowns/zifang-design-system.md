# 字坊 Zifang — Design System & UX Audit

**Purpose:** This document is the single source of truth for every visual, interactive, and structural decision in the Zifang app. Load this file before making any UI/UX changes. It exists so future agents do not drift from established patterns or reinvent solutions that already exist.

**Last audited:** 2026-04-04
**App file:** `index.html` (~8,840 lines, single-file HTML)
**Deployed:** zifang.netlify.app

---

## 1. DESIGN PHILOSOPHY

Zifang's aesthetic is **ink on rice paper** — a Chinese calligraphic metaphor rendered in web UI. The app should feel like a scholar's desk: warm, textured, quiet, with deliberate accents of color that carry meaning. Every surface is paper. Every accent is ink, jade, vermillion, copper, or gold — materials with cultural weight.

The guiding principles, in priority order:

1. **Paper first.** Background is always a warm off-white (rice). Cards, modals, and panels are lighter rice or white. Nothing is ever cold gray or pure white as the base.
2. **Color carries meaning.** Each tab has a dedicated accent color. Each depth level has a color. Favorites are gold. Custom items are vermillion. Colors are never decorative — they communicate.
3. **Bilingual by default.** Every label, heading, and pill shows Chinese characters first (with hover-pinyin), then English. This is not optional.
4. **Mobile-first, always.** The app is designed at 480px max-width, tested on iPhone 13 Mini. Desktop is just mobile centered on screen.
5. **Touch targets over aesthetics.** Minimum 44x44px for interactive elements. Active states use `transform: scale(0.95)` for tactile feedback.
6. **Quiet animation.** Transitions exist to smooth state changes, never to attract attention. Most transitions are 0.2s ease. Nothing bounces. Nothing overshoots.

---

## 2. COLOR SYSTEM

### 2.1 Base Palette (CSS Custom Properties)

These are the ink-and-paper foundation. They do not change across tabs.

| Token | Hex | Role |
|-------|-----|------|
| `--rice` | `#f5f0e8` | Primary background (the "paper") |
| `--rice-dark` | `#ebe4d6` | Slightly darker paper for contrast (inactive pills, row borders) |
| `--rice-light` | `#faf7f1` | Card backgrounds, modal surfaces, input fields |
| `--sand` | `#ede5d4` | English text pill backgrounds, subtle fill |
| `--sand-border` | `#ddd5c4` | All borders — cards, pills, inputs, dividers |
| `--ink` | `#2c2416` | Primary text color (warm near-black) |
| `--ink-light` | `#5a4e3c` | Secondary text (English translations, descriptions) |
| `--ink-faint` | `#8a7e6c` | Tertiary text (pinyin, labels, inactive tabs) |
| `--ink-ghost` | `#b8ad9a` | Quaternary text (hints, placeholders, timestamps) |
| `--ink-whisper` | `#d0c8b8` | Barely-there text (inactive stars, very subtle UI) |

**Rule:** Never use raw hex for text or borders in new CSS. Always use the tokens. The 5-tier ink hierarchy (ink → ink-light → ink-faint → ink-ghost → ink-whisper) is the entire text color system.

### 2.1.1 Pill Color Ramp Tokens (Dynamic)

All pill-shaped elements (cat-bubble, setup-cat-bubble, pack-toggle, segment-control) use a 20%/70% color ramp over `--rice`. These are computed dynamically using CSS `color-mix()` — **never hardcode the resulting hex values again**.

| Token | Formula | Role |
|-------|---------|------|
| `--accent-pill-bg` | `color-mix(in srgb, var(--accent) 20%, var(--rice))` | Unselected pill background — updates automatically on tab switch |
| `--accent-pill-text` | `color-mix(in srgb, var(--accent) 70%, var(--rice))` | Unselected pill text / selected pill background |
| `--vermillion-pill-bg` | `color-mix(in srgb, var(--vermillion) 20%, var(--rice))` | Unselected bg for custom/forged items |
| `--vermillion-pill-text` | `color-mix(in srgb, var(--vermillion) 70%, var(--rice))` | Unselected text / selected bg for custom/forged items |
| `--gold-pill-bg` | `color-mix(in srgb, var(--gold) 20%, var(--rice))` | Favorites pill unselected bg / selected text |
| `--gold-pill-text` | `color-mix(in srgb, var(--gold) 70%, var(--rice))` | Favorites pill unselected text / selected bg |
| `--mauve-pill-bg` | `color-mix(in srgb, var(--mauve) 20%, var(--rice))` | Struggling pill unselected bg / selected text |
| `--mauve-pill-text` | `color-mix(in srgb, var(--mauve) 70%, var(--rice))` | Struggling pill unselected text / selected bg |
| `--ink-pill-bg` | `color-mix(in srgb, var(--ink) 22%, var(--rice))` | Neutral utility elements (都 button, packs-btn) |

**Pill state pattern (universal):**
- Unselected: `background: var(--X-pill-bg); color: var(--X-pill-text)`
- Selected/active: `background: var(--X-pill-text); color: var(--X-pill-bg)` ← just swap them

**Critical rule:** `cat-custom`, `cat-bubble.forged-deck`, and `pack-toggle.forged.loaded` all use `--vermillion-pill-*`. They must stay identical — this is what unifies Library 自創 pills and Forged deck chips.

### 2.2 Accent Colors (Tab-Contextual)

The `--accent` and `--accent-soft` custom properties are swapped dynamically by `setTabAccent()` in JS when the user switches tabs. Every component that uses `var(--accent)` automatically recolors.

| Tab | Accent | Hex | Soft (12% opacity) | Semantic Meaning |
|-----|--------|-----|---------------------|------------------|
| Browse (瀏覽) | Jade | `#2d6a4f` | `rgba(45,106,79,0.12)` | Exploration, nature, library |
| Drill (練習) | Blue | `#4682b4` | `rgba(70,130,180,0.12)` | Study, focus, practice |
| Forge (鍛造) | Vermillion | `#c84b31` | `rgba(200,75,49,0.12)` | Fire, creation, transformation |
| Workshop (工坊) | Deep Rose | `#8b2252` | `rgba(139,34,82,0.12)` | Craft, conversation, warmth |

**How it works in JS:**
```javascript
function setTabAccent(tabName) {
  const root = document.documentElement;
  root.style.setProperty('--accent', accents[tabName].color);
  root.style.setProperty('--accent-soft', accents[tabName].soft);
}
```

**Rule:** Components should use `var(--accent)` and `var(--accent-soft)`, NOT hardcoded tab colors. The only exceptions are elements that must keep their color regardless of tab (e.g., favorites star is always gold, depth pills have fixed colors).

### 2.3 Semantic Colors (Fixed, Not Tab-Dependent)

| Token | Hex | Used For |
|-------|-----|----------|
| `--gold` | `#b8860b` | Favorites, settings, premium features |
| `--gold-soft` | `rgba(184,134,11,0.1)` | Gold pill backgrounds, highlight badges |
| `--vermillion` | `#c84b31` | Errors, warnings, "struggling" state, Custom category, Forge accent |
| `--vermillion-soft` | `rgba(200,75,49,0.12)` | Error backgrounds, struggling dot color |
| `--blue` | `#4682b4` | Drill mode accent, "meaning" mode, loading states |
| `--blue-soft` | `rgba(70,130,180,0.12)` | Loading status backgrounds |
| `--copper` | `#B87333` | Forge-specific (defined but lightly used) |
| `--mauve` | `#7d5080` | Workshop dot controls, topic pills |
| `--mauve-light` | `#b08ab5` | Workshop hover states |
| `--mauve-soft` | `rgba(125,80,128,0.13)` | Workshop pill backgrounds |

### 2.4 Depth-Level Colors

Cards and list items use depth to communicate richness of content:

| Depth | Background | Text Color | Meaning |
|-------|------------|------------|---------|
| Basic (基礎) | `--jade-soft` | `--jade` | Simple entry, few components |
| Intermediate (中級) | `--gold-soft` | `--gold` | Moderate detail |
| Rich/Deep (深入) | `--vermillion-soft` | `--vermillion` | Full breakdown with examples, components, notes |

### 2.5 Flashcard Themes (Drill Tab Only)

Three optional themes override Drill card styling via `[data-drill-theme]` CSS attribute selectors:

| Theme | Name | Card BG | Text | Feel |
|-------|------|---------|------|------|
| Night Study (夜讀) | `night-study` | `#2c2416` dark charcoal | `#f5f0e8` warm cream | Late night study session |
| Bamboo Grove (竹林) | `bamboo-grove` | `#f0f5ee` sage-tinted | `#2d6a4f` jade | Natural, calm, forest |
| Clean Slate (素紙) | `clean-slate` | `#ffffff` pure white | `#888888` gray | Modern minimalism |

**Rule:** Themes only affect `flip-card-face` and its children. They do not touch the rest of the Drill UI (progress dots, navigation, grade buttons).

---

## 3. TYPOGRAPHY

### 3.1 Font Stack

| Role | Font | Weight(s) | Where Used |
|------|------|-----------|------------|
| Chinese display | `Noto Serif TC` | 400, 600, 700, 900 | Card characters, titles, headings, drill characters |
| Chinese UI | `Noto Sans TC` | 300, 400, 500, 700 | Tab labels, category pills, setup labels, dialogue text |
| Latin body | `Inter` | 300, 400, 500, 600, 700 | Pinyin, English text, inputs, buttons, all Latin UI |
| Chinese literary | `LXGW WenKai TC` | 400, 700 | Available but reserved for future literary contexts |
| Display serif | `DM Serif Display` | — | Available but unused in current build |
| Prose serif | `Literata` | 400, 600 (+ italic) | Available but unused in current build |

**Rule:** Chinese characters always use `Noto Serif TC` (display/headings) or `Noto Sans TC` (UI/body). Latin text always uses `Inter`. Never mix these assignments.

### 3.2 Size Scale

The app uses `rem` units throughout. Key sizes:

| Element | Size | Context |
|---------|------|---------|
| App title (字坊) | `2rem` | Header h1 |
| Card character | `1.9rem` | Browse card `.card-char` |
| Drill character | `3.2rem` | Flashcard front face |
| Component character | `2.8rem` | Expanded card breakdown |
| Tab Chinese label | `1.38rem` | Navigation tabs |
| Section title | `1.4–1.6rem` | Setup titles, stage title, forge title |
| Body text | `0.82–0.95rem` | English translations, descriptions |
| Pinyin | `0.72–1.05rem` | Varies by context (card pinyin is dynamically sized) |
| Labels/captions | `0.65–0.75rem` | Detail labels, pill text, depth badges |
| Micro text | `0.58–0.68rem` | Related word pinyin, usage counts, hints |

**Rule:** Character display should always be the largest element on any screen. Pinyin is always smaller than its associated characters. English is always smaller than pinyin.

### 3.3 Dynamic Pinyin Sizing

The app has a sophisticated pinyin width-matching system:

1. `calcPinyinFontSize()` — Estimates font size to make pinyin roughly match character width using character-count heuristics
2. `matchPinyinWidth()` — Uses a canvas-based binary search to precisely match pinyin width to the measured character element width (DOM measurement)
3. `formatCardPinyin()` — Adds `|` pipe separators between semantic groups in pinyin (e.g., 4-char words become 2|2, 6-char become 3|3)

**Rule:** Never hardcode pinyin font sizes on card views. Always use the dynamic sizing system.

---

## 4. SPACING & LAYOUT

### 4.1 App Shell

| Property | Value | Why |
|----------|-------|-----|
| Max width | `480px` | Mobile-first; iPhone 13 Mini viewport |
| Centering | `margin: 0 auto` | Centers the app column on wider screens |
| Height | `100dvh` | Dynamic viewport height (accounts for mobile browser chrome) |
| Overflow | Body: `overflow-x: clip`, Main: flex column | No horizontal scroll ever |
| Content scroll | Each tab manages its own overflow | Browse has internal scroll container; Stage scrolls the tab content |

### 4.2 Padding Conventions

| Context | Padding | Rationale |
|---------|---------|-----------|
| Header | `2rem 1.5rem 1.5rem` | Generous top breathing room |
| Tab nav | `0 1.5rem` | Matches header horizontal padding |
| Filter bar | `0.75rem 1.5rem` | Compact but touchable |
| Cards | `18px 20px` | Slightly asymmetric for visual comfort |
| Modals | `1rem 1.25rem` (header), `0.8rem 1.2rem` (body) | Tighter than cards — modals are focused spaces |
| Inputs | `0.55rem 0.6rem` to `0.6rem 0.75rem` | Consistent internal padding on all form elements |

**Rule:** Horizontal padding on the main layout is always `1.5rem` (24px). This is the "rail" — all content aligns to it.

### 4.3 Gap Conventions

| Context | Gap | Where |
|---------|-----|-------|
| Between cards | `0.75rem` | Browse container |
| Between pills | `0.5rem` | Category bubbles, stage pills, preset rows |
| Between form fields | `0.6rem` | Character creator, settings |
| Between dot control options | `0.15rem` | Workshop dot options (tight, compact) |
| Between buttons in a row | `0.5–0.75rem` | Action rows, button groups |

### 4.4 Border Radius Scale

| Token | Value | Used On |
|-------|-------|---------|
| `--radius` | `12px` | Cards, modals, settings panel |
| `--radius-sm` | `8px` | Inputs, buttons, smaller containers |
| `20px` (pill radius) | `20px` | All pill-shaped elements (category bubbles, nav buttons, roster chips) |
| `50%` (circle) | `50%` | Dot controls, spicy button, help button, progress dots |
| `14px` or `16px` | — | Modal cards (slightly larger than standard `--radius`) |

**Rule:** Rectangular containers get `--radius` (12px). Small interactive elements get `--radius-sm` (8px). Anything pill-shaped gets `20px`. Anything circular gets `50%`. Do not introduce new radius values.

---

## 5. COMPONENT INVENTORY

### 5.1 Buttons

The app has several button archetypes. Each serves a distinct purpose.

**Primary Action Button** (`.start-btn`, `.stage-generate-btn`, `.feedback-submit`)
- No background, text-only, uses `--accent` color
- Font: `Noto Serif TC`, weight 900, size 1.4–1.6rem
- Hover: `scale(1.05)`, opacity 0.8
- Active: `scale(0.97)`
- Used for: Starting drills, generating dialogues, submitting forms

**Ghost Button** (`.nav-btn`, `.restart-btn`, `.stage-regenerate-btn`)
- Border: `1px solid --sand-border`
- Background: `--rice-light` or transparent
- Border-radius: `20px` (pill shape)
- Hover: border and text change to `--accent`
- Active: `scale(0.95)`
- Used for: Navigation, secondary actions

**Pill Button / Category Bubble** (`.cat-bubble`, `.setup-cat-bubble`, `.topic-preset-btn`)
- Pill shape (`border-radius: 20px`)
- Two states: selected (accent bg + white text) and unselected (rice-dark bg + faint text)
- Active: `scale(0.95)` for tactile press feedback
- Font: `Noto Sans TC`, 0.9–1.1rem
- Used for: Category filters, drill setup, topic selection

**Circle Button** (`.spicy-btn`, `.group-btn`, `.apikey-btn`)
- Size: `2.8rem x 2.8rem`
- Shape: perfect circle (`border-radius: 50%`)
- Border: `2px solid --sand-border`
- Background: `--rice-light`
- Hover: border color changes to semantic color, `scale(1.08)`
- Active state: semantic background fill + glow shadow
- Used for: Toggle features (spicy mode, group mode)

**Segment Control** (`.segment-btn`, `.mode-seg-btn`)
- Grouped buttons in a rounded container
- Active segment gets full accent background + white text
- Inactive segments are transparent with faded accent text
- Used for: Card/list view toggle, Chinese→English / English→Chinese mode

**Icon Button** (`.settings-btn`, `.scroll-top-btn`, `.roster-manage-btn`)
- Background: none
- Color: `--ink-faint` at 0.4–0.55 opacity
- Hover: increased opacity, sometimes rotation (settings gear: `rotate(45deg)`)
- Size: varies (1.9rem to 2.4rem)
- Used for: Utility actions, navigation aids

### 5.2 Cards

**Browse Card** (`.card`)
- Background: `--rice-light`
- Border: `1px solid --sand-border`
- Border-radius: `--radius` (12px)
- Shadow: `--shadow-sm` (very subtle)
- Hover: `--shadow-md`, `translateY(-1px)`, left accent bar fades in (3px wide, `--jade`)
- Expanded state: details section animates open via `max-height` (0 → 1200px, 0.6s ease)
- Structure: top row (character + pills), pinyin, English; details below divider

**Flip Card** (`.flip-card-container`)
- Size: 300px x 300px
- Perspective: `800px`
- Flip: `rotateY(180deg)`, 0.5s ease
- Both faces: same container dimensions (enforced min/max-height: 300px)
- Front: character centered, pinyin reveal below
- Back: meaning, pinyin, semantic excerpt

**Compact List Row** (`.compact-row`)
- 5-column grid: `1.5rem 4.5rem 5.5rem 1fr auto`
- Columns: fav star | character | pinyin | English | depth badge
- Border-bottom: `1px solid --rice-dark`
- Hover: `--rice-light` background
- Click navigates to card view with that card expanded

### 5.3 Modals

All modals follow the same pattern:

**Backdrop:** Fixed position, `inset: 0`, semi-transparent ink overlay (`rgba(44,36,22,0.45)`), fades in via `opacity 0.25s ease`

**Card:** Centered with flexbox, `max-width: 380–440px`, `border-radius: 14–16px`, `--rice` background, subtle shadow (`0 8px 40px rgba(44,36,22,0.18)`)

**Entry animation:** Card scales from `0.96` to `1` and translates from `8px` to `0` vertically, matching the opacity transition. This creates a gentle "float up and solidify" effect.

**Close button:** Top-right, `28px x 28px`, circle (`border-radius: 50%`), `×` character or SVG, hover gets `--sand` background.

**Modals in the app:**
1. Vocab Picker Modal — word selection for Workshop
2. Topic Modal — topic/scene selection for Workshop
3. Character Creator Modal — persona creation
4. Spicy Password Modal — LOTR Moria gate theme (dark, atmospheric, unique)
5. Forge Sonnet Modal — API key entry for Claude
6. Forge Help Modal — step-by-step API key guide
7. Settings Overlay — tabbed settings panel
8. Model Warning Modal — confirmation before switching to paid model
9. Feedback Modal — user feedback form

**Rule:** Every new modal must use the backdrop + card pattern. Entry animation is always scale(0.96→1) + translateY(8→0) + opacity(0→1) at 0.25s. The Spicy Password modal is the ONE exception to the rice-paper aesthetic (it's deliberately dark/atmospheric as an easter egg).

### 5.4 Pills / Badges

**Category Pill** (`.cat-bubble`)
- Pill shape (20px radius)
- Selected: accent bg + white text
- Unselected: `--rice-dark` bg, `--ink-faint` text, `--sand-border` border
- Special variants: Favorites (gold), Custom (vermillion)

**Depth Pill** (`.pill.depth`)
- Small (0.3rem 0.6rem padding)
- Colors tied to depth level (jade/gold/vermillion)
- Font: 0.7rem, weight 500

**POS Pill** (`.pill.pos`)
- Blue tint (`--pos-blue` bg, `--pos-blue-text`)
- Shows part of speech for vocab items

**Dot Option Pill** (`.dot-opt`)
- Workshop controls
- No background by default, text only
- Hover/active: `--mauve-soft` bg, `--mauve-light` text
- Staggered entrance animation (0.5s, 0.7s, 0.9s... delay per pill)

### 5.5 Inputs

**Text Input** (`.search-input`, `.stage-text-input`, `.forge-input`, `.vocab-picker-search input`)
- Border: `1px solid --sand-border`
- Border-radius: `--radius-sm` (8px)
- Background: `--rice-light`
- Font: `Inter`, 0.82–0.9rem
- Placeholder color: `--ink-ghost`
- Focus: border changes to `--accent`, optional focus ring (`box-shadow: 0 0 0 2px --accent-soft`)
- Forge input focus uses vermillion instead of accent

**Select** (`.stage-select`)
- Same styling as text input
- Custom dropdown arrow via SVG background-image
- `appearance: none` / `-webkit-appearance: none`

**Password Input** (`.spicy-pw-input`)
- Dark theme exception: dark border, transparent-ish background, light text
- Focus: blue glow ring
- Error state: red border + shake animation (0.35s, ±6px translateX)

### 5.6 The Dot Controls (Workshop)

This is a unique interaction pattern — circular glyphs that expand to reveal pill options when tapped.

**Structure:** A circle (`.dot-glyph`, 2.6rem) displaying a Chinese character (度/級/人/字), with a hidden `.dot-options` container beside it.

**Interaction:** Tap/click toggles `.open` class. Options slide out horizontally with a long, smooth transition (`max-width 0→20rem` at 1.5s cubic-bezier(0.4,0,0.2,1)`) while individual pills stagger-fade in (0.5s base + 0.2s per pill).

**Close:** Instant — pills vanish immediately (no delay on close), container collapses.

**Color:** Default is `--ink-faint` glyph on `--rice-light` circle. Open/hover state is `--mauve` on `--mauve-soft`.

**Rule:** This asymmetric timing (slow open, instant close) is intentional and must be preserved. It creates a "blooming" effect that feels organic.

---

## 6. INTERACTION PATTERNS

### 6.1 Hover Pinyin System

Chinese text throughout the app uses a custom hover-pinyin system:

- **Desktop:** `mouseenter` → show pinyin below character, `mouseleave` → hide
- **Mobile:** Long-press (500ms) → show pinyin for 2 seconds, then auto-hide
- **Implementation:** `.hover-pinyin` wrapper with `.hp-pinyin` child positioned absolutely below
- **Pinyin appearance:** `opacity: 0 → 1`, 0.3s ease, with white text-shadow for legibility over any background

**Rule:** Every Chinese label in the UI should use the `hoverPinyin(chars, pinyin)` JS helper. This is what makes the app a learning tool, not just a tool with Chinese on it.

### 6.2 Card Expand/Collapse

Browse cards expand on click to reveal details (components, examples, related words).

- Animation: `max-height: 0 → 1200px`, `opacity: 0 → 1`, both at 0.6s with `var(--ease)` cubic-bezier
- A left accent bar (3px, jade) fades to `opacity: 1` on expanded cards
- Only one card expands at a time is NOT enforced — multiple can be open simultaneously

### 6.3 Flip Card

Drill flashcards use a 3D CSS flip:

- Container has `perspective: 800px`
- Card rotates `0 → 180deg` on Y axis, 0.5s ease
- Both faces use `backface-visibility: hidden`
- Touch swipe left/right navigates between cards (mobile)
- Keyboard: spacebar flips, arrow keys navigate (Z-01 completed)

### 6.4 Progress Dots

Drill session progress shown as dots:

- Dot size: 7px circles
- Gap: 3.5px (dynamically computed by `computeDotLayout()` for optimal grid)
- States: neutral (`--rice-dark`), current (`--accent`, scale 1.3), got-it (jade at 40% opacity), struggling (vermillion at 45% opacity)
- Hover: `scale(2.2)` — intentionally dramatic for easy targeting
- Clickable for direct navigation

### 6.5 Grade Buttons

After flipping a drill card:

- Two buttons: Wrong (vermillion) and Got It (jade)
- Default opacity: 0.4 (ghosted until tapped)
- Marked state: full opacity
- Active: `scale(0.94)` for press feedback

### 6.6 Tab Switching

- Accent color swaps instantly via CSS custom property update
- Content fades in via `tabFadeIn` keyframe (opacity 0→1, 0.2s ease-out)
- **Critical rule from code comment:** Tab content must NEVER use `filter: blur()` because it creates a new containing block that traps position:fixed modals

### 6.7 Scroll-to-Top Button

- Fixed position, bottom-right of app column
- 36px circle, `--rice-light` bg, `--sand-border` border
- Appears at scroll threshold (`opacity 0→1`, 0.3s ease)
- Active: `scale(0.9)`

---

## 7. SHADOW SYSTEM

| Token | Value | Used On |
|-------|-------|---------|
| `--shadow-sm` | `0 1px 3px rgba(44,36,22,0.08)` | Cards at rest, scroll-to-top button |
| `--shadow-md` | `0 4px 12px rgba(44,36,22,0.1)` | Cards on hover, setup card, character creator |
| Modal shadow | `0 8px 40px rgba(44,36,22,0.18), 0 0 0 1px rgba(44,36,22,0.06)` | All floating modals |
| Settings shadow | `0 12px 40px rgba(44,36,22,0.25)` | Settings overlay, feedback modal |

**Rule:** Shadows always use ink-toned rgba (44,36,22), never pure black. This keeps them warm and consistent with the paper aesthetic.

---

## 8. ANIMATION CATALOG

### 8.1 Timing Tokens

| Duration | Easing | Used For |
|----------|--------|----------|
| 0.1s | ease | Dot hover (fast response) |
| 0.15s | ease | Button press, micro-interactions |
| 0.2s | ease / ease-out | Standard transition (color, bg, border, opacity) |
| 0.25s | ease / cubic-bezier(0.25,0.1,0.25,1) | Modal open/close |
| 0.3s | ease / `var(--ease)` | Card shadow, hover states, tab fade |
| 0.5s | ease / `var(--ease)` | Card expand opacity, flip card rotation, pinyin reveal |
| 0.6s | `var(--ease)` | Card expand max-height + margin |
| 1.5s | cubic-bezier(0.4,0,0.2,1) | Dot control expansion (intentionally slow bloom) |

**`var(--ease)` = `cubic-bezier(0.25, 0.1, 0.25, 1)`** — A gentle ease-out with a soft start. Used for the most visible, content-level animations (card expand, divider color).

### 8.2 Named Keyframes

| Name | What It Does | Duration | Where |
|------|-------------|----------|-------|
| `tabFadeIn` | `opacity: 0 → 1` | 0.2s ease-out | Tab content appearance |
| `glow-pulse` | `box-shadow: 0 → 5px accent → 0` | 1s ease | Card highlight after scroll-to (`.glow`) |
| `pulse-bg` | `opacity: 1 → 0.7 → 1` | 1.5s infinite | Loading status messages |
| `spicyShake` | `translateX: 0 → -6 → 6 → -4 → 4 → 0` | 0.35s ease | Password error shake |

### 8.3 Principles

1. **No spring/bounce physics.** Everything eases, nothing overshoots.
2. **Asymmetric open/close.** Dot controls: 1.5s open, instant close. This is intentional — organic bloom.
3. **Opacity for presence, transform for position.** Elements fade in with opacity AND translate/scale in with transform simultaneously.
4. **Active states are instant.** Button presses (`scale(0.95)`) have no transition delay — they respond immediately to touch.
5. **Stagger for sequences.** Dot option pills stagger by 0.2s each (0.5, 0.7, 0.9...). This creates a cascade effect.

---

## 9. TAB-BY-TAB CAPABILITY MAP

### 9.1 瀏覽 Browse — "The Library"

**What it does now:**
- Search across pinyin, Chinese characters, and English (accent-stripped for pinyin fuzzy matching)
- Filter by category: All, Favorites, Vocab, Expression, Idiom, Concept, Custom
- Two views: Card view (expandable details) and Compact list view
- Card details show: character breakdown grid, example sentences with border-left accent, related words as mini-pills
- Favorites system: star toggle on cards and list rows, persisted to localStorage
- Horizontal scroll pill strip for categories (iOS-style)
- Hover-pinyin on all Chinese labels

**What could be added (future):**
- Z-03 (completed: pill strip is already horizontal scroll)
- Search history / recent searches
- Sort options (by pinyin, by category, by depth, by date added)
- Spaced repetition indicators (heat map of last-reviewed dates)
- Tap a related word to navigate to that card if it exists in the library
- Batch operations (select multiple → add to drill → start session)

### 9.2 練習 Drill — "The Practice Room"

**What it does now:**
- Setup screen: category selection, card count stepper, mode toggle (中→英 or 英→中)
- "All" button to drill entire filtered set
- "Struggling" category (Z-02 completed: cross-session wrong-answer tracking in localStorage)
- Flashcard session: 3D flip cards, progress dots with direct navigation
- Keyboard shortcuts (Z-01 completed: spacebar flip, arrow key navigation)
- Grade buttons (Wrong / Got It) with struggling pile integration
- Completion screen with stats (total, got-it, struggling, accuracy)
- Drill themes (Night Study, Bamboo Grove, Clean Slate) via Settings
- Favorite toggle on drill cards
- "Look up" button on card front to jump to Browse

**What could be added (future):**
- Spaced repetition algorithm (SM-2 or similar)
- Session history / streak tracking
- Timed mode (speed drill with countdown)
- Audio playback (TTS for pronunciation)
- Writing practice mode (trace characters on mobile)
- Reverse drill: show components, guess the compound

### 9.3 鍛造 Forge — "The Smithy"

**What it does now:**
- Input any Chinese word/phrase
- AI generates a fully enriched nugget card via API
- Two API options: Groq (free, Llama model) and Anthropic (Claude Sonnet, paid)
- API keys stored in localStorage, entered via Settings or inline modals
- Help modal with step-by-step Groq API key instructions
- Generated cards include: traditional/simplified, pinyin, English, category, depth, components, examples, related words, semantic notes
- Cards saved to localStorage as custom nuggets (appear in Browse with "Custom" filter)
- Status messages: loading (pulse animation), success, error with close button

**What could be added (future):**
- Z-04: Edit-before-save (inline field editing on preview)
- Z-05: Export/import custom cards as JSON
- Batch forge: paste a list of words, generate all at once
- "Forge from context" — paste a sentence, extract and forge all unknown words
- Quality scoring: flag low-confidence AI outputs
- Integration with Drill: "Forge & Drill" flow

### 9.4 工坊 Workshop — "The Stage"

**What it does now:**
- Vocab picker: modal with search, category filters, select/clear/random controls
- Topic selection: preset pills (Surprise me, Eating out, Getting around, At work, Shopping, Social life, Daily life) + custom input
- Four dot controls: Length (短/中/長), HSK Level (1-6), Speakers (2-4), Character Set (簡/繁)
- Character roster: create/edit/delete personas with name, role, want, fear, quirk, style, notes
- "Enrich" characters via AI to flesh out personality
- Spicy mode: password-gated adult content toggle (LOTR Moria gate easter egg)
- Group mode: balances dialogue volume for group reading
- Generates contextual dialogues via Groq API
- Output shows: scene setting, character cards, dialogue lines with Chinese/pinyin/English, vocab highlighting, cultural notes
- Regenerate button for fresh output

**What could be added (future):**
- Z-06: Roster UX review
- Z-07: Save dialogues to localStorage
- Z-08: Continue/extend a conversation
- Dialogue replay with audio TTS
- Print-friendly dialogue export (PDF)
- Grammar pattern extraction from generated dialogue
- "Conversation prep" integration — generate practice dialogues for specific contacts
- Scene templates beyond topic pills (restaurant argument, job interview, dating, etc.)
- Difficulty adaptation: if user marks too many words as unknown, auto-suggest lower HSK level

---

## 10. GLOBAL PATTERNS & CONVENTIONS

### 10.1 Click Delegation

All click handlers use `e.target.closest('.selector')` — NEVER `e.target.classList.contains()`. This ensures clicks on child elements (SVGs inside buttons, spans inside links) correctly bubble to the intended handler.

### 10.2 Bilingual Labels

Every UI label follows the pattern: **Chinese characters first, English second**. The Chinese uses `hoverPinyin()` wrapper for on-demand pinyin. Examples from the code:

- Tab: `瀏覽 Browse`, `練習 Drill`, `鍛造 Forge`, `工坊 Workshop`
- Category pills: `詞彙`, `表達`, `成語`, `概念`, `自創`
- Depth pills: `基礎 Basic`, `中級 Intermediate`, `深入 Deep`
- POS pills: `名 Noun`, `動 Verb`, `形 Adjective`

**Rule:** Never add English-only labels. Every new label gets a Chinese equivalent with pinyin.

### 10.3 Selected/Unselected State Convention

The app uses a consistent pattern for toggle-able elements:

- **Selected:** Accent color background (or accent-soft), accent or white text
- **Unselected:** `--rice-dark` background, `--ink-faint` text, `--sand-border` border
- **Transition:** CSS class toggle (`.unselected` / `.selected` / `.active`), 0.2s ease on background + color + border-color

This applies to: category bubbles, setup category bubbles, topic presets, vocab category pills, segment controls, roster chips, dot options.

### 10.4 Mobile Long-Press vs Desktop Hover

- **Desktop:** `mouseenter`/`mouseleave` on `.hover-pinyin` elements
- **Mobile:** `touchstart` begins a 500ms timer. If held, pinyin shows for 2 seconds then auto-hides. If released early (tap), the normal click action fires. `touchmove` cancels the timer.
- **Never use inline `ontouchstart` handlers** — all touch logic is delegated via document-level listeners.

### 10.5 localStorage Keys

The app persists user state across sessions:

| Key | Contents |
|-----|----------|
| Favorites | Set of nugget IDs |
| Struggling | Set of nugget IDs (wrong 2+ times) |
| Custom nuggets | Array of user-created nugget objects |
| API keys | Groq and Anthropic keys |
| Workshop characters | Roster of saved personas |
| Drill theme | Selected flashcard theme name |
| Model preference | Groq or Anthropic |

### 10.6 Paper Texture

The `body::before` pseudo-element applies a subtle fractal noise SVG texture over the entire viewport:

```css
background: url("data:image/svg+xml,...feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'...");
opacity: 0.03;
pointer-events: none;
z-index: 0;
```

This is barely visible but creates a tactile "paper" feel. It must remain on all pages.

---

## 11. ANTI-PATTERNS — WHAT NOT TO DO

1. **Never use pure gray.** All neutrals derive from the ink/rice spectrum (warm undertone). Using `#333`, `#666`, `#ccc` etc. breaks the aesthetic.

2. **Never use `filter: blur()` on tab content.** This creates a new containing block and traps position:fixed modals inside the tab instead of the viewport. (There's a code comment warning about this.)

3. **Never introduce new colors without semantic meaning.** Every color in the system communicates something (tab identity, depth, state, category). Decorative color is not allowed.

4. **Never hardcode accent colors in components.** Use `var(--accent)` and `var(--accent-soft)` so components automatically recolor per tab.

5. **Never skip the bilingual label pattern.** All user-facing text needs Chinese + English with hover-pinyin.

6. **Never use inline `ontouchstart` or `ontouchmove`.** All touch handlers go through the document-level delegation system.

7. **Never assume a fixed number of nuggets.** The library grows via Forge. All rendering is dynamic — no hardcoded indices.

8. **Never add emojis to the UI.** The spicy button devil face (U+1F608) and the empty-state face are the only exceptions, and both serve specific purposes.

9. **Never split the file.** Everything stays in one HTML file. This is an architecture rule, not a suggestion.

10. **Never use `e.target.classList.contains()` for click delegation.** Always use `e.target.closest()`.

---

## 12. ACCESSIBILITY NOTES (Current State)

**What exists:**
- `role="tablist"` and `role="tab"` on navigation
- Touch targets generally meet 44px minimum
- Color is never the sole indicator (pills have text labels alongside color)
- Focus states on inputs (border-color change + optional ring)

**What's missing (future improvement areas):**
- No `aria-selected` on active tabs
- No `aria-expanded` on expandable cards
- No `aria-label` on icon-only buttons (settings gear, scroll-to-top)
- No keyboard navigation for Browse cards or category pills
- No skip-to-content link
- Focus trap not implemented in modals
- Insufficient color contrast on `--ink-ghost` text against `--rice` background (4.5:1 WCAG AA may fail)
- Screen reader testing not performed
- No reduced-motion media query for users who prefer minimal animation

---

## 13. RESPONSIVE BEHAVIOR

The app has ONE breakpoint at 380px (`@media (max-width: 380px)`):

| Property | Default | Small Screen |
|----------|---------|-------------|
| Header padding | `2rem 1.5rem 1.5rem` | `1.5rem 1rem 1rem` |
| Header h1 size | `2rem` | `1.7rem` |
| Setup card padding | `2rem` | `1.5rem` |
| Drill character size | `3.2rem` | `2.8rem` |
| Card character size | `1.9rem` | `1.7rem` |
| Pill font size | `0.7rem` | `0.65rem` |
| Tab gap | `2rem` | `1.5rem` |
| Tab font size | `1.05rem` | `0.95rem` |

**Rule:** The app is designed for 480px and below. There are no tablet or desktop breakpoints because the max-width constraint means it always renders as a phone-width column. The 380px breakpoint exists solely for very small devices (iPhone SE, etc.).

---

## 14. ICON SYSTEM

The app uses inline SVGs throughout — no icon font, no icon sprite. All SVGs come from a consistent style:

- **Stroke width:** 1.5px (Solar icon set aesthetic)
- **Size:** Typically 24x24 viewBox, displayed at various sizes
- **Color:** `currentColor` (inherits from parent)
- **Fill:** Mix of filled paths and stroked paths with `opacity: 0.5` for layered depth

Icons are used for: tab navigation, view toggle (card/list), settings gear, close buttons (×), favorite star (bookmark shape), delete (trash can), add character (person + plus).

**Rule:** Keep using inline SVGs with `currentColor`. Never add an icon font or external SVG sprite. New icons should match the Solar-style aesthetic (1.5px stroke, rounded caps, layered opacity).

---

## 15. DOCUMENT STATUS

This design system represents the app as of 2026-04-04. It should be updated whenever:

- New components are added
- Color tokens change
- Animation timing changes
- New tabs or major features are introduced
- Accessibility improvements are made

**Load this file alongside `project-knowledge.md` before any UI session.**
