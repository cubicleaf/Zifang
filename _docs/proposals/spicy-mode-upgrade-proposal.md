# Spicy Mode Upgrade Proposal — Workshop Dialogue Generation

**Status:** Proposal  
**Date:** 2026-04-08  
**Context:** Llama 3.3-70B (via Groq) self-censors even with extensive prompting. Three structural changes to push explicit output quality.

---

## Change 1: Remove JSON Enforcement Mode

### What it is now

The Groq API call includes:

```javascript
response_format: { type: 'json_object' }
```

This tells Groq to force the model into JSON-only output mode. Groq handles this internally by adding constraints to the generation process.

### Why it's a problem

JSON mode activates stricter safety rails. The model treats structured data output differently from narrative output — it self-censors more because "data" feels like it should be production-safe. It's like asking someone to write dirty dialogue on a government form. The format itself suppresses the content.

### The change

**Remove** `response_format: { type: 'json_object' }` from the API call (spicy mode only — keep it for normal mode where it works fine).

**Instead**, add an instruction in the prompt telling the model to wrap its JSON in markdown fences:

```
Return your response as a JSON code block:
```json
{ ... }
```​
```

Then parse the response by extracting content between the fences.

### Fallback / error handling

The current code already has JSON parse error handling (it shows a friendly error message). We add one extra step before parsing: strip markdown fences if present, then attempt `JSON.parse()`. If parsing fails, fall back to the existing error path.

**Risk level:** Medium. The model could occasionally output malformed JSON without the enforcement. But we already handle parse failures, and in practice Llama 3.3-70B is very reliable at producing valid JSON when asked.

### What changes in the code

1. In `generateDialogue()` — conditionally omit `response_format` when `stageState.spicyMode` is true
2. In the response handler — add a fence-stripping step before `JSON.parse()`
3. In the system prompt (spicy branch only) — replace "Return ONLY valid JSON" with "Return your response as a JSON code block wrapped in ```json fences"

---

## Change 2: Tune Sampling Parameters

### What it is now

```javascript
temperature: 0.85
```

That's the only sampling parameter. No `top_p`, no `frequency_penalty`, no `presence_penalty`.

### Why it matters

- **temperature** (0.85) — controls randomness. Already decent. Could push to 0.9–0.95 for spicy mode.
- **top_p** — controls nucleus sampling (which tokens are even considered). Default is 1.0 (consider everything). Lowering to ~0.9 cuts the long tail of boring safe tokens.
- **frequency_penalty** — penalizes tokens that have already appeared. A *negative* value actually *encourages* repetition of specific vocabulary. But more useful here: a small positive value (0.3–0.5) discourages the model from falling into safe-word loops ("感觉", "关系", "一起" used as euphemistic substitutes).
- **presence_penalty** — penalizes tokens that have appeared at all. A small positive value (0.2–0.4) pushes the model to use more diverse vocabulary, potentially reaching for the explicit terms in the lexicon rather than recycling safe words.

### The change

**Spicy mode only** — add these parameters to the API call:

```javascript
temperature: 0.92,
top_p: 0.9,
frequency_penalty: 0.3,
presence_penalty: 0.3
```

Normal mode stays at `temperature: 0.85` with no other params.

### Risk level

Low. These are gentle nudges, not dramatic shifts. If output quality degrades (incoherent text, weird repetition), we can dial them back. The values above are conservative starting points.

### What changes in the code

1. In `generateDialogue()` — build the request body conditionally based on `stageState.spicyMode`
2. Same for `extendDialogue()` — it has its own API call

---

## Change 3: Few-Shot Example Dialogue

### What it is now

The system prompt has:
- A writer persona ("You are an adult Chinese dialogue writer...")
- A tone directive ("This scene must contain overt sexual language...")
- A full vocabulary lexicon (120 terms with pinyin and English)
- Success/failure descriptions in abstract terms

What it does NOT have: a concrete example of what a correct spicy dialogue line looks like.

### Why it matters

LLMs respond far more powerfully to examples than to instructions. The lexicon gives the model words (passive reference material). A few-shot example shows the model those words *in action* — the rhythm, the register, the way profanity weaves into natural speech. It's the difference between giving someone a dictionary and showing them a page from a novel.

### The challenge

Fabricated examples tend to feel manufactured — a model writing examples for another model is an echo chamber. The examples need to feel like real Chinese people talking: messy, funny, unexpected, with profanity that serves an emotional purpose rather than being sprinkled on top.

### The plan

**Source real dialogue** from Chinese film scripts, novels, online forums (Douban, Zhihu, Tieba, Weibo), and TV show transcripts. Specifically looking for:

- Natural swearing in emotional contexts (anger, frustration, banter)
- Sexual language that isn't porn-scripted but feels like real people (flirting, hookup culture, crude jokes between friends)
- Register variety: drunk friends, arguing couples, hookup app conversations, bar encounters

**Curate 3-5 short exchanges** (2-4 lines each) that demonstrate different registers and emotional contexts. Format them as example output showing the exact JSON structure we expect.

**Inject into the system prompt** as a "REFERENCE EXAMPLES — this is the register and explicitness level we expect" section, placed AFTER the lexicon and BEFORE the JSON format spec.

### Sourcing approach

A separate research session (Opus + web search) to find authentic Chinese profane dialogue from:

1. **Film/TV transcripts** — 余華 (Yu Hua) adaptations, 管虎 films, 姜文 films, 愛情公寓, online web dramas
2. **Literature** — 余華《兄弟》, 王朔 novels, 王小波, 六六《蜗居》
3. **Internet culture** — Tieba copypasta, Douban movie reviews with quoted dialogue, Zhihu "what's the most vulgar thing you've heard" threads
4. **Real conversation patterns** — how 脏话 actually functions in different social contexts

### Risk level

Low for implementation. The challenge is curation quality. Bad examples teach bad patterns.

### What changes in the code

1. New JS function `getSpicyExamples()` — returns 3-5 curated example exchanges as a formatted string
2. Injected into the system prompt in the spicy `writerPersona` branch, after the lexicon

---

## Implementation Order

1. **Sampling parameters** (lowest risk, 5 minutes, immediate effect)
2. **Few-shot examples** (pending research, highest potential impact)
3. **JSON mode removal** (medium risk, needs parse fallback, test carefully)

---

## Token Budget Impact

| Component | Est. tokens | When |
|---|---|---|
| Current spicy overhead | ~3,700 | Always (spicy on) |
| Sampling params | 0 | API params, not prompt |
| Few-shot examples (3 exchanges) | ~400–600 | Spicy on |
| JSON mode change | ~0 (swap one instruction for another) | Spicy on |
| **Total spicy overhead after** | **~4,100–4,300** | — |

Still well within Llama 3.3-70B's 32K context window.
