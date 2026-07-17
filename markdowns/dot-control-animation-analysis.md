# Dot Control Animation — Root Cause Analysis & Fix Plan

**Date:** 2026-04-13
**Status:** Diagnosis complete, fix not yet implemented
**File:** `index.html`, CSS lines ~2564–2670, JS lines ~12346–12575

---

## THE TELEPORT BUG — Root Cause Found

The instant "teleport" when pressing a button has ONE root cause that we circled around but never directly fixed:

**The `open` CSS class does double duty — it controls both STYLING (glyph color) and LAYOUT (options max-width + padding-left). The layout changes are instant because there's no CSS transition, and they fire BEFORE the JS animation can intervene.**

Here's the exact frame-by-frame sequence when you click dc-hsk while dc-length is already open:

### Frame-by-frame trace

```
BEFORE CLICK:
  dc-length: width ~140px, open class ON, options visible (max-width:20rem from CSS)
  dc-hsk:    width ~77px,  glyph centered, options hidden (max-width:0)
  dc-speakers: width ~77px, glyph centered
  dc-charset:  width ~77px, glyph centered

CLICK HANDLER (synchronous JS — no paint yet):
  Step 1: remove 'open' from ALL controls
    → dc-length loses 'open' class
    → CSS kicks in INSTANTLY: dc-length options → max-width:0, padding:0
    → dc-length's glyph SNAPS from left-aligned to centered (~25-30px shift)
    ★ THIS IS THE TELEPORT — the glyph visually jumps

  Step 2: add 'open' to dc-hsk
    → CSS kicks in: dc-hsk options → max-width:20rem, padding:0.45rem
    → dc-hsk's glyph shifts slightly left (options takes ~7px from padding)

  Step 3: _dcAnimate('dc-hsk') called
    → Snapshots current widths (still the old values from inline styles)
    → Sets inline max-width:0px on dc-hsk options (overrides the CSS 20rem)
    → Schedules first animation frame via requestAnimationFrame

FIRST PAINT (browser paints before calling rAF):
  → dc-length: glyph has ALREADY jumped to center (from step 1)
  → dc-hsk: options has ~7px from padding-left (set in step 3)
  → All widths still at their pre-click values (animation hasn't started)
  ★ THE USER SEES THE TELEPORT HERE

FIRST rAF TICK (~16ms later):
  → Widths begin changing by < 1px
  → Smooth animation begins... but the damage was already done
```

### Why this happened

The `open` class toggles in the click handler (line 12562-12564) BEFORE `_dcAnimate` is called. The CSS changes from that class toggle are LAYOUT changes (max-width, padding-left) that take effect immediately. The JS animation starts one frame later. That one-frame gap is the teleport.

### Why previous attempts didn't fix it

| Attempt | Why it failed |
|---------|---------------|
| overflow:hidden on parent | Clipped the glyph when content was wider + justify-content:center pushed it left |
| Faster CSS transitions on max-width | Still an independent animation racing the JS width animation |
| Removing CSS transitions from .dot-options | Made the layout snap INSTANT instead of gradual — worse teleport |
| Setting inline max-width:0 in _dcAnimate | Helped for the OPENING button but didn't help the CLOSING button (the one losing its open class) |
| S-curve / ease-in-out easing | Hid the teleport behind a slow start but buttons appeared "stuck" |
| Linear easing | Revealed the teleport clearly since movement was constant |

The key insight we missed every time: **the CLOSING button's layout change is uncontrolled.** We kept trying to fix the opening button, but the glyph teleport comes from the button that was PREVIOUSLY open losing its options content in a single frame.

---

## THE FIX — Separate Layout from Styling

### Principle
The `open` class should ONLY control visual styling (glyph color/highlight). ALL layout (max-width, padding-left on .dot-options) should be controlled by JS inline styles, managed by _dcAnimate on every frame.

### CSS Changes

```css
/* Remove layout properties from the open state — JS handles these */
.dot-control.open .dot-options {
  /* DELETE: max-width: 20rem; */
  /* DELETE: padding-left: 0.45rem; */
  /* This rule becomes empty or is removed entirely.
     The open class now ONLY affects .dot-glyph color. */
}

/* Base .dot-options stays as-is */
.dot-options {
  display: flex;
  align-items: center;
  gap: 0.15rem;
  overflow: hidden;
  max-width: 0;
  padding-left: 0;
  flex-shrink: 0;
}
```

The `open` class now only does:
```css
.dot-control.open .dot-glyph {
  color: var(--mauve);
  background: rgba(125, 80, 128, 0.22);
}
```

### JS Changes — _dcAnimate must manage ALL controls' options

The tick function needs to handle THREE roles, not just the opening button:

```
1. OPENING control:  options max-width grows from 0 → available space
2. CLOSING control:  options max-width shrinks from current → 0
3. IDLE controls:    options max-width stays at 0
```

#### Key additions to _dcAnimate:

```javascript
function _dcAnimate(openId) {
  // ... existing setup ...

  // NEW: identify the previously-open control BEFORE toggling the class
  var prevOpenEl = row.querySelector('.dot-control.open');
  var prevOpenIdx = prevOpenEl ? all.indexOf(prevOpenEl) : -1;

  // NEW: snapshot options state for the previously-open control
  var prevOptW = 0;
  var prevPadL = 0;
  if (prevOpenIdx !== -1) {
    var prevOpts = all[prevOpenIdx].querySelector('.dot-options');
    prevOptW = prevOpts.offsetWidth; // or parseFloat of inline maxWidth
    prevPadL = parseFloat(getComputedStyle(prevOpts).paddingLeft) || 0;
  }

  // NOW toggle the open class (after snapshotting)
  all.forEach(function(c) { c.classList.remove('open'); });
  if (openId) {
    document.getElementById(openId).classList.add('open');
  }

  // Set INITIAL inline styles to prevent any CSS flash
  all.forEach(function(c, i) {
    var opts = c.querySelector('.dot-options');
    if (i === openIdx) {
      opts.style.maxWidth = '0px';
      opts.style.paddingLeft = '0';
    } else if (i === prevOpenIdx) {
      // FREEZE the closing control's options at its current size
      opts.style.maxWidth = prevOptW + 'px';
      opts.style.paddingLeft = prevPadL + 'px';
    } else {
      opts.style.maxWidth = '0px';
      opts.style.paddingLeft = '0';
    }
  });

  // In the tick function:
  function tick(now) {
    var t = /* ... */;

    // ... width calculations as before ...

    // Sync ALL controls' options in the same frame as widths
    all.forEach(function(c, i) {
      var opts = c.querySelector('.dot-options');

      if (i === openIdx) {
        // OPENING: grow options to fill available space
        var availW = Math.max(0, currentWidth[i] - glyphW);
        opts.style.maxWidth = availW + 'px';
        // Ramp padding smoothly from 0 to 0.45rem
        opts.style.paddingLeft = (0.45 * Math.min(t * 2, 1)) + 'rem';
      } else if (i === prevOpenIdx) {
        // CLOSING: shrink options from current to 0
        var closingW = prevOptW * (1 - t);
        opts.style.maxWidth = Math.max(0, closingW) + 'px';
        opts.style.paddingLeft = (prevPadL * (1 - t)) + 'px';
      } else {
        // IDLE: locked at 0
        opts.style.maxWidth = '0px';
        opts.style.paddingLeft = '0';
      }
    });
  }

  // At animation end: clear inline styles, let CSS handle resting state
  // (CSS .open class now only does glyph color, so no layout jump)
  // Set final max-width/padding inline for the open control
  if (openIdx !== -1) {
    all[openIdx].querySelector('.dot-options').style.maxWidth = '20rem';
    all[openIdx].querySelector('.dot-options').style.paddingLeft = '0.45rem';
  }
}
```

#### Critical change to click handler:

The `open` class toggle should move INSIDE `_dcAnimate`, not happen in the click handler. This ensures the class toggle and the inline style freezing happen in the correct order with no gap.

```javascript
// CURRENT (buggy):
container.classList.add('open');   // ← CSS layout change fires HERE
_dcAnimate(container.id);         // ← JS tries to fix it HERE (too late)

// FIXED:
_dcAnimate(container.id);         // ← JS handles everything, including class toggle
```

The click handler becomes:
```javascript
container.addEventListener('click', (e) => {
  const btn = e.target.closest('.dot-opt');
  if (btn) { /* ... handle selection ... */ _dcAnimate(null); return; }
  const wasOpen = container.classList.contains('open');
  _dcAnimate(wasOpen ? null : container.id);
});
```

And `_dcAnimate` handles the class toggle internally after freezing inline styles.

---

## EASING — What to use

After all the experiments, the right answer for easing is:

**Start with pure linear (constant velocity).** The normalization constraint guarantees buttons can't collide. Linear means every button starts moving on frame 1 and moves at a constant rate. No stalling, no jerking.

Once the teleport is fixed and linear feels smooth, THEN consider adding a **gentle ease-out** (like `1-(1-t)^1.5`) to give a soft landing. Don't add ease-in — that's what caused the "stalling" sensation.

Duration: **1.2–1.5 seconds** felt right for the overall pace. Start at 1.2s.

---

## IMPLEMENTATION CHECKLIST

1. **Move open class toggle INTO _dcAnimate** — snapshot previous state, freeze inline styles, THEN toggle class
2. **Remove max-width and padding-left from `.dot-control.open .dot-options` CSS** — open class becomes styling-only
3. **Manage ALL controls' options in the tick function** — opening, closing, AND idle
4. **Animate padding-left** — don't snap it, ramp from 0 to 0.45rem over the animation
5. **Set resting-state inline styles at animation end** — so the open control's options stay visible after animation completes
6. **Test all scenarios:**
   - Click button from homeostasis (all closed)
   - Click different button while one is open (switch)
   - Click same button to close it
   - Click outside to close
   - Rapid clicking (interrupt mid-animation)
   - Click a dot-opt pill to select value and close

---

## NON-NEGOTIABLES (from Tim)

- No teleporting (instant position jumps)
- No jerkiness (sudden acceleration that throws a button into/near another)
- No buttons touching or getting too close
- All buttons must start moving immediately on click
- Movement must feel fluid and synchronized
- Bezier/easing: whatever accomplishes the above — no attachment to any particular curve
