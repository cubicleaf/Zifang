# HSK Framework Deep Dive: Raising the Quality of Nuggets Stage

## What is HSK?

The Hanyu Shuiping Kaoshi (汉语水平考试) is China's standardized Mandarin proficiency test, administered by the Ministry of Education. It defines six levels of competency, each with precise boundaries around vocabulary, grammar, topics, and communicative function. Rather than inventing our own difficulty scale, aligning Stage's output to HSK gives us a battle-tested, globally recognized framework that learners already understand.

## The Six Levels at a Glance

**HSK 1** (150 words, 54 grammar points): Survival basics. Simple subject-verb-object sentences. Topics limited to greetings, numbers, family, food, time, weather. Register is entirely casual/formulaic. Think: ordering coffee, introducing yourself, asking directions.

**HSK 2** (300 words, 79 grammar points): Daily life. Introduces 了 (completed action), 过 (experience), basic comparisons (比), and simple connectors (因为...所以). Topics expand to shopping, transport, hobbies, health. Still short, concrete sentences but can now express basic sequences of events.

**HSK 3** (600 words, 87 grammar points): Turning point. Learners can hold real conversations. Introduces 把 construction, passive voice (被), result complements (verb + 到/完/好), and conditional clauses (如果...就). Topics include travel, work, education, plans. Sentences grow to 2-3 clauses. This is where "textbook Chinese" starts becoming "real Chinese."

**HSK 4** (1,200 words, 112 grammar points): Fluency threshold. Complex sentence patterns: 不但...而且 (not only...but also), 无论...都 (regardless), 既然...就 (since...then). Abstract topics emerge: society, culture, environment, career ambitions. Register shifts toward semi-formal. Dialogue can sustain nuanced opinions and mild debate.

**HSK 5** (2,500 words, 109 grammar points): Professional/academic fluency. Four-character idioms (成语) appear naturally. Formal written register is expected. Topics include economics, politics, philosophy, technology. Sentence structures feature nested clauses, rhetorical devices, and sophisticated hedging (恐怕, 未必, 不见得).

**HSK 6** (5,000+ words, 66 new grammar points): Near-native. Literary and classical expressions surface. Register spans the full spectrum from slang to formal written Chinese. Abstract reasoning, irony, cultural allusions, and domain-specific jargon are all fair game.

## What This Changes in Stage

**Before:** A vague "formality" dropdown (casual / neutral / formal) and a separate "register" control. These are imprecise, overlap in meaning, and don't map to any recognized standard. A learner selecting "neutral" gets no guarantees about what grammar or vocabulary will appear in the surrounding dialogue.

**After:** A single HSK Level selector (1-6). This one control constrains *everything*:

- **Vocabulary scope** — The LLM is instructed to use only words within the target HSK level (excluding the user's chosen vocab, which may be at any level). This prevents the common LLM failure of casually dropping HSK 5 words into a "beginner" dialogue.
- **Grammar patterns** — Each level has a defined grammar inventory. The system prompt will list key patterns the model should favor and explicitly ban patterns above the target level. For example, at HSK 2, the model can use 了 and 过 but must not use 把 or 被 constructions.
- **Sentence complexity** — HSK 1-2 caps at simple SVO with one clause. HSK 3 allows 2-3 clauses. HSK 4+ permits complex multi-clause structures. This is enforced in the prompt via explicit clause-count guidance.
- **Topic coherence** — The topic/setting presets will be filtered or annotated by level. A "job interview" scenario doesn't belong at HSK 1. A "buying fruit" scenario is perfect for it.
- **Register and tone** — HSK 1-2 dialogues are casual and concrete. HSK 4+ introduces polite/formal registers. HSK 6 can include literary flourishes. This replaces the old formality dropdown entirely.

## Common LLM Pitfalls This Solves

Research revealed several recurring problems when LLMs generate "level-appropriate" Chinese without strict constraints. First, vocabulary bleed: models default to their most natural phrasing, which tends to land around HSK 4-5 regardless of the requested level. Second, grammar escalation: even when vocabulary is controlled, models slip in advanced grammar (把, 被, complex complements) because those structures feel more "natural" in context. Third, topic mismatch: models generate topically complex scenarios (debating philosophy) while claiming to use simple words, creating a cognitive dissonance for learners. The HSK framework addresses all three by giving the system prompt concrete, enforceable rules rather than vibes.

## Implementation Priority

This is a strict upgrade with no tradeoffs. The formality and register dropdowns get replaced by a single, cleaner HSK level picker. The system prompt gets rewritten with level-specific constraints. The UI actually gets simpler (one control instead of two), and the output gets dramatically more accurate for the learner's actual ability level. Every learner who's studied Chinese formally already knows their HSK level, so the mental model is instant.
