# 字坊 Pending Queue — §12 replacement
# Replace the contents of §12 in project-knowledge.md with everything below this line.
# Last updated: 2026-04-29 (cleaned: removed completed items, renumbered, reordered by importance)

---

1 · Card and category deletion — users need the ability to delete individual cards (including Forge-created ones) and delete entire custom categories. Needs a confirmation step to prevent accidents. Should also handle what happens when a deleted card is in a drill session or on the struggling list.

2 · Forge input robustness — Forge works well with clear Chinese characters but struggles with English input, gibberish, or trolling. Need an input validation / graceful failure strategy: detect non-Chinese or nonsense input early and return a useful error message instead of a broken or hallucinated card.

3 · Workshop character roster UX review — UX pass on the Workshop tab's character list; scope TBD.

4 · "Understanding Zifang" onboarding section — in-app explainer covering: what each tab does, how Forge works, what the struggling system tracks, how to use settings, and what all the icons mean. Could live as a help modal or a dedicated panel.

5 · HSK 5 generation rule — components[] readings must match compound context — BACKBURNER, captured 2026-04-29. When generating compound HSK 5 cards (e.g., 長輩, 行業, 重複, 著火) where the compound uses a NON-DEFAULT reading of a polysemous character, the `components[]` field for that character MUST list the reading and meaning AS USED IN THIS COMPOUND, not the default reading from earlier HSK levels. Example: for 長輩 the component entry must read `{char:"長", pinyin:"zhǎng", meaning:"elder, to grow"}`, NOT `{char:"長", pinyin:"cháng", meaning:"long"}`. This is a Stage-2 enrichment-prompt rule for the remaining 12 HSK 5 batches. Action when picking back up: harden the batch enrichment agent's priming with this rule explicitly.

6 · Character cross-reference panel (polysemy progression) — BACKBURNER, captured 2026-04-29. Surfaced during HSK 5 deck planning. Chinese deliberately layers new senses/readings onto already-introduced characters as you climb HSK levels (得 de→děi→dé; 长 cháng→zhǎng; 行 xíng→háng; 重 zhòng→chóng; 着 zhe→zháo). Current card structure captures per-character meaning inside `components[]` per card, but there's no UI mechanism that surfaces the cross-deck relationship — i.e., when studying 長輩 (HSK 5, zhǎng) the user can't see "this is the same 長 you learned at HSK 1 as cháng with new reading + new meaning." Feature idea: tap any character in a card's `components[]` strip and get a panel showing every other card in the user's library that uses that character, with the readings/meanings called out so the polysemy progression is visible. Would turn implicit cross-level connections into something explicit. 一字多義 (yī zì duō yì) is one of Mandarin's defining features; deck format honors it at the card level but not at the library level. No urgency, but worth designing properly when it surfaces.
