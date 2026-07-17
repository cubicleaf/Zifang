# The Ideal Squircle — A Complete Breakdown

*Everything you need to know about the shape, where it comes from, how it works, and how it's built in this project. Written for humans, not computers.*

---

## What Even Is a Squircle?

A squircle is a shape that lives exactly halfway between a square and a circle. Not a rounded square — something more precise and more interesting than that.

Here's the difference:

- A **square** has four perfectly sharp 90° corners. Brutal. Unnatural. Nothing in the physical world actually has corners that sharp.
- A **circle** is perfectly round all the way around, with no flat sides at all.
- A **rounded rectangle** (what CSS `border-radius` gives you) is a square with circle arcs glued onto the corners. The transition from flat side to curved corner is abrupt — you can feel the "seam" where the curve begins.
- A **squircle** has *no seam*. The curve flows out of the corner and gradually, continuously melts into the flat side. There is no moment where it snaps from "straight" to "curved." It's all one smooth, uninterrupted line.

That last point is the whole game. The squircle feels organic in a way rounded rectangles never quite do.

---

## Why Does This Matter? The Perception Thing

Your eye is very good at detecting where something changes character. When a straight line abruptly becomes a circular arc (which is what `border-radius` does), your visual system registers that transition even if you can't consciously name it. It reads as slightly mechanical, slightly manufactured.

A squircle eliminates that transition point entirely. The curvature changes *gradually* across the whole shape — near the corner it curves sharply, near the middle of a side it curves almost not at all, and everything in between is a smooth ramp. Your eye glides around it without catching on anything.

This is why squircles feel "softer" and "more considered" than rounded rectangles, even when they're the same overall size and the corners look similar at a glance.

---

## The Math Behind It (Don't Worry, It's Not That Bad)

The squircle comes from a formula called a **superellipse**, invented by the Danish designer and mathematician Piet Hein in 1959. He was trying to solve a traffic problem — seriously, a real traffic roundabout in Stockholm — and ended up creating one of the most influential shapes in modern design.

The formula for a regular ellipse (a stretched circle) looks like this:

```
(x/a)² + (y/b)² = 1
```

The `²` means "squared" — multiplied by itself. A superellipse just swaps that `²` for a different number called the *exponent*. For a squircle specifically, the exponent is `4`:

```
(x/a)⁴ + (y/b)⁴ = 1
```

When the exponent is `2` you get a circle. When it approaches infinity you get a perfect square. At exactly `4` you get the squircle — balanced right in the middle. The exponent is the dial between "round" and "sharp," and `4` is where it tastes exactly right.

You don't need to remember any of this math to use squircles. But it's worth knowing the shape has a mathematical reason for looking the way it does — it's not arbitrary.

---

## Apple Made This Famous

Apple switched their app icons to squircles in 2013 with iOS 7. Before that, app icons were rounded rectangles. After, they were squircles. The change felt more modern and more considered, and the design world largely followed.

The specific Apple exponent is reportedly around `5` rather than `4`, making their corners slightly more aggressive (sharper edges, more "square-feeling" while still being smooth). Our implementation uses `4` — the classic Piet Hein version — which is slightly softer.

Every major tech company now uses squircles for icons and UI elements. It's become the default shape for "premium button" in modern design.

---

## How Squircles Are Actually Drawn on Screen

Here's where things get technical, but we'll keep it grounded.

A browser can't draw a mathematical superellipse directly. Instead, we approximate it using something called a **Bézier curve** — a curve defined by "control points" that pull the line in specific directions, like magnets. Four control points per corner, eight corners total (two per side of the square), approximates the superellipse very accurately.

In this project, the squircle is stored as an **SVG path** — a set of drawing instructions, like a very precise connect-the-dots. The path for this project's squircle looks like this:

```
M 0.07322,0.92678
C 0.14645,1 0.26430,1 0.5,1
C 0.73570,1 0.85355,1 0.92678,0.92678
C 1,0.85355 1,0.73570 1,0.5
C 1,0.26430 1,0.14645 0.92678,0.07322
C 0.85355,0 0.73570,0 0.5,0
C 0.26430,0 0.14645,0 0.07322,0.07322
C 0,0.14645 0,0.26430 0,0.5
C 0,0.73570 0,0.85355 0.07322,0.92678
Z
```

Reading this is easier than it looks:

- `M` means "move to" — pick up the pen and start here
- `C` means "draw a curve to" — the three numbers after it are two control points (the magnets) and the destination
- `Z` means "close the shape" — draw a straight line back to where we started (though in this case the shape is already closed)

All the numbers are between `0` and `1` because the shape is defined in *proportional* terms rather than pixels. `0` is the left or top edge, `1` is the right or bottom edge, `0.5` is the exact middle. This means the same shape definition works on a 20px button and a 200px button — the browser scales the coordinates to fit whatever size the element actually is.

---

## The Three Key Numbers

The squircle's character is defined by three measurements, all derived from the original favorites button SVG that was drawn on a 20-unit grid:

| Number | Value | What it controls |
|--------|-------|------------------|
| `a` | `0.07322` | Where the curve *starts* — 7.3% in from each corner |
| `b` | `0.14645` | The first control point — exactly `2 × a` |
| `c` | `0.26430` | The second control point — how quickly the curve transitions |

`a` is the most important. It's the distance from the corner where the edge "stops being straight and starts being squircle." At 7.3%, the flat sides take up about 85% of each edge, and the squircle corner curve takes up the remaining 15% at each end. This ratio is what makes it feel like a squircle rather than a rounded rectangle — the flat sections are long and confident, the corners are tight and crisp.

If `a` were larger (say 0.2), the flat sections would be shorter and the corners would be bigger — rounder, more "pill-like." If `a` were smaller (say 0.03), the corners would be almost imperceptibly small — more like a rectangle with barely-softened edges.

---

## How It's Applied in This Project

There are two layers to how squircles work here:

### Layer 1: The Clip Path

The SVG path above is wrapped in something called a `<clipPath>` — a kind of stencil. When you apply a clip path to an HTML element, the browser only renders the parts of that element that fall inside the stencil's shape. Everything outside gets cut away.

```html
<clipPath id="squircle-clip" clipPathUnits="objectBoundingBox">
  <path d="M 0.07322,0.92678 ..."/>
</clipPath>
```

The `clipPathUnits="objectBoundingBox"` part is what makes the proportional coordinate system work — it tells the browser "interpret these coordinates as fractions of the element's own size, not as pixels."

This definition is written *once* in the HTML file, invisibly (in a `0×0` SVG that doesn't take up any space), and then any element anywhere on the page can reference it by name:

```css
clip-path: url(#squircle-clip);
```

That one CSS line is all it takes. The browser looks up `#squircle-clip`, applies the stencil to the element at whatever size it is, and the result is a squircle.

### Layer 2: What Gets Clipped

The clip path cuts the *visual output* of an element — its background color, its borders, its contents. It does not change the element's size, padding, or position in the layout. A 40×40px button with a squircle clip path still occupies 40×40px of space; it just looks like a squircle visually.

This is important: **applying a clip path is a purely cosmetic operation**. It cannot break spacing, cannot affect animation math, cannot change how other elements are positioned relative to it.

One thing to be aware of: clip paths also cut away `box-shadow` (drop shadows) and visible `border` lines, because those are rendered as part of the element's visual output. If a button has a shadow or a border, those disappear under the clip. In this project, all squircle buttons either have no shadow/border, or use inner background-color tricks instead.

---

## Why Not Just Use `border-radius`?

`border-radius: 50%` gives you a circle. `border-radius: 12px` gives you a rounded rectangle. You cannot get a true squircle from `border-radius` alone, because:

1. `border-radius` always draws corners using circular arcs. The seam between the arc and the straight edge is always there, even if it's subtle.
2. You can do tricks with `border-radius` to get *closer* to a squircle (e.g., `border-radius: 30% 70% / 30% 70%` style nonsense), but the result is inconsistent, hard to maintain, and doesn't actually solve the mathematical problem.
3. Clip paths are the correct tool for this job.

---

## The Gold Standard: The Favorites Button

The squircle definition in this project was derived directly from the **favorites button SVG on the browse carousel** — the original hand-crafted button drawn on a 20-unit grid. That button is the reference implementation. The three numbers (`0.07322`, `0.14645`, `0.26430`) are derived from its exact proportions, divided by 20 to convert from absolute grid coordinates to proportional 0–1 space.

Everything else on the page that looks like a squircle — the glyph buttons (度/級/人/字), the pill buttons (短/中/長), the forge category buttons, etc. — all use this same definition. One shape, drawn once, referenced everywhere. That's what makes the design feel coherent rather than "sort of rounded."

---

## Quick Reference

| Term | Plain English |
|------|---------------|
| Superellipse | The math formula that defines the squircle shape |
| Exponent (`n=4`) | The "dial" between circle and square; 4 is the sweet spot |
| Bézier curve | A curve defined by magnetic "control points" |
| SVG path | A set of drawing instructions stored as text |
| `clipPathUnits="objectBoundingBox"` | "Use proportional coordinates, not pixels" |
| `clip-path: url(#squircle-clip)` | The one CSS line that applies the squircle to any element |
| `a = 0.07322` | Where the corner curve starts — 7.3% in from each corner |

---

*The Chinese word for squircle doesn't really exist yet as a standard term — the shape is too new. The closest poetic equivalent might be* 方圓兼備「fāng yuán jiān bèi」*— "possessing both squareness and roundness." It's a classical idiom used to describe someone who is both principled (square) and adaptable (round). Piet Hein would have loved that.*
