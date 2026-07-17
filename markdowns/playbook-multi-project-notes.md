# UX Playbook — Multi-Project Expansion Notes

**Purpose:** Latent planning notes for when Tim is ready to expand the UX Playbook beyond Zifang to cover all his web apps. Created during the April 9 2026 audit. These notes are NOT active — they're context for the future comprehensive cross-project analysis Tim mentioned.

---

## The Core Problem to Solve

Tim builds inherently different types of interfaces: a Chinese learning app (Zifang) has very different UX needs than a nature/cycling project (Cleveland Greenway) or a music/audio tool (Billy). The playbook needs to distinguish between:

1. **Universal Tim preferences** — warm colors, no bounce, 44px touch targets, slow animations, tactile feedback. These apply everywhere.
2. **Domain-specific patterns** — dot controls, flashcard flip animations, pinyin sizing. These are bespoke to one project.
3. **Transferable principles** — asymmetric timing is a *principle* that applies broadly, but the exact values (1.8s open / instant close) are Zifang-specific.

## Proposed Architecture (When Ready)

### Level 1: Universal Principles (SKILL.md core)
- Color temperature (warm)
- Animation philosophy (no bounce, slow, asymmetric)
- Touch targets (44px+)
- Typography approach (purpose-specific fonts, hierarchy)
- Interaction philosophy (tactile, progressive disclosure)
- Process (two-phase pattern, obsessive refinement)
- Anti-patterns (13 confirmed, all universal)

### Level 2: Project Registry (SKILL.md section or linked file)
A lightweight table that tells the agent:

```
| Project | Design System Doc | Accent System | Feel/Metaphor |
|---------|------------------|---------------|---------------|
| Zifang | zifang-design-system.md | Tab-contextual (jade/blue/vermillion/mauve) | Scholar's desk, ink on rice paper |
| Greenway | TBD | Nature-toned (browns, greens) | Outdoor journal, slow and earthy |
| Billy | TBD | TBD | TBD |
| WebDev Master | TBD | Module-dependent | Reference/documentation |
```

### Level 3: Per-Project Design System Docs (external files)
The detailed token lists, component inventories, and architecture rules. Already exists for Zifang. Would be created for each new project.

## What to Watch For as Projects Multiply

### Potential Bleed Points
- **Animation timing:** Zifang's 1.8s dot bloom would feel absurd on a quick-action cycling app
- **Color palette:** Warm rice paper base is Tim-universal, but the accent system (jade/vermillion/mauve) is deeply Zifang. Other projects need their own semantic color mapping.
- **Font stacks:** Noto Serif TC / Noto Sans TC are Chinese-specific. Other projects need different display fonts while likely keeping Inter for Latin.
- **Component metaphors:** "Cards as paper" works for a learning app. A cycling app might use "cards as trail markers" or "cards as map pins."
- **Information density:** Zifang is dense (character + pinyin + English + depth + category per card). Other projects may be more spacious.

### Shared Infrastructure That Works Everywhere
- The `--accent` / `--accent-soft` swap pattern
- The 5-tier ink hierarchy system (adapt hex values, keep the structure)
- The formula-based color ramp (20%/70% blend) for derived states
- Modal float-up pattern (scale 0.96→1, translateY 8→0)
- Pill selector component with scale(0.95) press feedback
- CSS custom property architecture (tokens in :root, swap in JS)

## How to Run the Cross-Project Analysis

When Tim is ready, the process should be:

1. **Gather all HTML project files** — read each one, extract CSS variables, font stacks, animation timings, component patterns
2. **Diff against the playbook** — what matches, what diverges, what's project-specific
3. **Interview Tim** (AskUserQuestion tool) about divergences: "You used 0.15s transitions on Greenway but 0.25s on Zifang — was that a deliberate feel difference or did you just not think about it?"
4. **Tag each preference** as universal vs project-specific based on evidence + Tim's answers
5. **Build the project registry** and per-project design system docs
6. **Update the playbook** with the multi-level architecture

## Agent Observations from This Audit

The codebase audit agent found 277 hardcoded color values in Zifang alone. If this pattern exists across other projects, the cross-project analysis will need to address color tokenization as a systemic issue, not just a Zifang issue.

The webdev master reference already contains Zifang-specific sections (tab transitions, color system, component replicas). If Tim builds showcase modules for other projects too, the reference becomes a de facto visual specification that the playbook should reference.

The session transcript analysis revealed that Tim's refinement pattern (Phase 2: obsessive iteration) applies most intensely to animation timing and color values. Font choices and layout decisions tend to settle faster. This priority ordering should inform how much detail the playbook captures per domain.

---

*Created: 2026-04-09*
*Status: Latent — activate when Tim begins cross-project analysis*
