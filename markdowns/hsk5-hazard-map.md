# HSK 5 Generation Hazard Map — Synthesis

**Built:** 2026-04-29
**Source list:** `data/hsk5-source-2012.txt` (1,300 words, Hanban Sept 2012, simplified)
**Target IDs:** 2401–3700 (continues from HSK 4)
**Output:** `data/hsk5-staging.json`
**Inputs synthesized from:**
- `markdowns/hsk5-scout-A-trad-taiwan.md` — Trad/Simp + Taiwan-vs-Mainland
- `markdowns/hsk5-scout-B-duplicates.md` — Cross-deck duplicate audit
- `markdowns/hsk5-scout-C-pinyin-hazards.md` — pypinyin override list (~140 entries)
- `markdowns/hsk5-scout-D-grammar-register.md` — Special semanticNote handling (~130 entries)

---

## 1. Headline numbers

| Metric | Value |
|---|---|
| Source list size | 1,300 |
| Hard duplicates with HSK 1–4 | 0 |
| Hard duplicates with original NUGGETS | 9 |
| Cards to generate (drop dupes) | 1,291 |
| Cards needing pinyin override | ~140 |
| Cards needing special grammar note | ~130 |
| Cards needing Trad/Simp or Taiwan-lexical override | ~50 |
| Cards needing **all three** at once | ~20 |
| Net cards needing hand-touch (any) | ~280 / 1,291 (≈22%) |

**Pedagogical headline:** zero overlap with HSK 1–4 — HSK 5 is genuinely additive over the standardized 1–4 deck.

---

## 2. Pre-generation decisions Tim must lock in

These nine choices change downstream output materially. Locking them up front prevents rework.

### D1. OpenCC configuration
- **Option A:** `s2twp.json` (simplified → Taiwan with phrases) — handles 網路/軟體/滑鼠 etc. automatically. Override list shrinks to ~10.
- **Option B:** `s2t.json` (character-only, no phrase dict) — produces 網絡/軟件/鼠標 by default. Override list explodes to ~50.
- **Recommendation:** A. Faster, fewer overrides, fewer hand-mistakes.

### D2. Politically/regionally loaded words
- **国庆节 (line 376):** Keep characters as 國慶節 (Hanban faithful), gloss explains "Oct 1 (PRC) / 國慶日 Oct 10 (Taiwan/ROC)."
- **公元 (line 334):** 西元 (Taiwan) or 公元 (Hanban)? **Recommend 公元 with semantic note flagging Taiwan's 西元.**
- **土豆 (line 950):** False-friend trap. Hanban gloss is "potato." In Taiwan, 土豆 = peanut. Recommend keep characters as 土豆, gloss = "potato (Mainland) / **PEANUT in Taiwan** — see semanticNote." semanticNote calls out the regional split explicitly. Tim can override.
- **人民币 (line 782):** Keep as-is. RMB is RMB. No ambiguity.

### D3. Computer-vs-general lexical ambiguity
- **文件 (990):** Keep 文件 trad. semanticNote: "computer file in Taiwan = 檔案."
- **程序 (122):** Keep 程序 trad. semanticNote: "software program in Taiwan = 程式."
- **数据 (886):** Use **資料** for "data" (Taiwan everyday); semanticNote flags 數據 for "statistics."

### D4. Pinyin deck-wide rules (must match HSK 4 precedent — Tim to confirm)
- **期** in 期待/期间/过期/时期/日期: `qī` or `qí`? *Standard mainland is `qī`; Taiwan often `qí`.*
- **质** in 本质/物质/性质: `zhì` (mainland) or `zhí` (Taiwan)?
- **企业**: `qǐyè` (mainland) or `qìyè` (Taiwan)?
- **角色** (537): `juésè` — both scouts confirm. Lock as `juésè`.
- **下载** (1017): `xiàzài` (Taiwan) — lock.
- **血** (1055): `xuè` (formal/standard) — lock.

### D5. Duplicates with NUGGETS deck (9 cards)
**Recommendation: DROP all 9 from HSK 5 generation.** Cards: 哎, 嗯, 不得了, 多余, 好奇, 进步, 夸张, 系统, 自由. Optionally tag the existing NUGGETS cards with `alsoIn:["hsk5"]` so they surface under the HSK 5 deck filter. Net cards to generate: **1,291**.

### D6. Measurement words deck-wide policy
- **厘米/吨/克/升:** Keep Hanban form (釐米/噸/克/升). semanticNote on each: "Taiwan everyday: 公分/公噸/公克/公升."

### D7. ID range
- Reserve **2401–3691** for HSK 5 (1,291 cards if we drop the 9 dupes).
- If we keep all 1,300 and tag dupes: 2401–3700.
- **Recommendation: 2401–3691** (drop dupes).

### D8. Card depth
- All cards: `depth: "basic"` to match HSK 4 precedent. Stratification was rejected in the prep questions.

### D9. Example sentence policy
- 2 examples per card minimum (HSK 4 precedent).
- Each example MUST contain the target word/phrase.
- Pinyin on every example.
- For separable verbs: at least one example must show the split form.
- For heteronyms: examples must disambiguate the reading in context.

---

## 3. Trad/Simp + Taiwan override list (LOCKED)

### Tier 1 — Hard overrides (Taiwan-modern, override OpenCC default)

| Simp | Default trad | **Override to** | Why |
|---|---|---|---|
| 网络 | 網絡 | **網路** | Taiwan universal |
| 软件 | 軟件 | **軟體** | Taiwan universal |
| 硬件 | 硬件 | **硬體** | Taiwan universal |
| 鼠标 | 鼠標 | **滑鼠** | Taiwan universal |
| 数码 | 數碼 | **數位** | Taiwan universal |
| 光盘 | 光盤 | **光碟** | Taiwan universal |
| 桔子 | 桔子 | **橘子** | Character variant |
| 冰激凌 | 冰激凌 | **冰淇淋** | Taiwan universal |
| 报道 | 報道 | **報導** | Taiwan media style |
| 数据 | 數據 | **資料** (when sense=data) | See D3 |

### Tier 2 — Character-merge traps (one simp char → multiple trad chars in deck)

These need per-card hand-confirmation; OpenCC s2twp may get them right, but verify each:

- **发 family** (8 cards: 发表/发愁/发达/发抖/发挥/发明/发票/发言) → all → **發** (NEVER 髮). Spot-check one to confirm pipeline.
- **复 family**: 重复 → **重複**, 复制 → **複製**, 恢复 → **恢復**. Three different trad chars from same simp.
- **系 family**: 系/系统 → **系/系統** (lineage); 系领带 → **繫領帶** (繫, tie). Different trad.
- **干 family**: 干燥/干脆 → **乾燥/乾脆** (dry); 干活儿 → **幹活兒** (work). Opposite directions.
- **制 family**: 制定/制度/限制/控制 → **制** (regulate); 制造/制作 → **製造/製作** (manufacture).
- **后 family**: 后背/后果/落后 → **後**. All three same direction.
- **余 family**: 多余/其余/业余 → all **餘** (surplus, not surname).
- **划** (413): if gloss=plan/demarcate → **劃**; if gloss=paddle → **划**. Tim picks gloss → trad follows.

---

## 4. Pinyin override list (LOCKED — pypinyin alone WILL ship wrong)

Full table in `hsk5-scout-C-pinyin-hazards.md`. Headline categories:

### High-confidence WRONG-by-default — manual override required (~50)

Heteronyms where pypinyin's default reading is wrong for the HSK 5 sense:
- 重复 → **chóngfù** (not zhòngfù)
- 曾经 → **céngjīng** (not zēngjīng)
- 倒霉 → **dǎoméi** (audit — usually OK)
- 的确 → **díquè** (not déquè/díquè)
- 长辈 → **zhǎngbèi** / 长城 → **chángchéng** / 长江 → **chángjiāng** / 长途 → **chángtú** — 长 splits per word
- 着火 → **zháohuǒ** / 着凉 → **zháoliáng** (not zhe)
- 角色 → **juésè** (not jiǎosè)
- 系统 → **xìtǒng** / 系领带 → **jì lǐngdài** (xì vs jì)
- 调整 → **tiáozhěng** / 声调 → **shēngdiào** (tiáo vs diào)
- 看不起 → **kànbuqǐ** / 舍不得 → **shěbude** (V-不-V neutral)
- 干 → **gān** in 干燥 / **gàn** in 干活儿 (split)
- 尽快 → **jǐnkuài** / 尽力 → **jìnlì** (split within HSK 5 itself)
- 乐器 → **yuèqì** / 乐观 → **lèguān** (yuè vs lè)
- 朝 → cháo (toward/dynasty) standalone
- 重大 → **zhòngdà** / 重量 → **zhòngliàng** / 重复 → **chóngfù** (split)
- 行业 → **hángyè** / 行人 → **xíngrén** / 行为 → **xíngwéi** / 行动 → **xíngdòng** (split)
- 应付 → **yìngfù** / 应用 → **yìngyòng** (yìng not yīng)
- 好客 → **hàokè** / 好奇 → **hàoqí** (hào not hǎo)

### bù sandhi — auto-handle in pipeline (~12)
不断 → búduàn, 不见得 → bújiànde, 不耐烦 → búnàifán, 不要紧 → búyàojǐn. (Not 不然/不如/不足 — those keep bù.)

### yī sandhi — auto-handle (~5)
一辈子 → yíbèizi, 一旦 → yídàn, 一律 → yílǜ, 一再 → yízài, 一致 → yízhì.
NOTE: 统一/唯一 do NOT sandhi (一 is final).

### Erhua — hand-fix (~2)
干活儿 → gànhuór, 使劲儿 → shǐjìnr.

### Light-tone words pypinyin may miss (~30)
玻璃 → bōli, 脖子 → bózi, 答应 → dāying, 大方 → dàfang, 耽误 → dānwu, 糊涂 → hútu, 学问 → xuéwen, 在乎 → zàihu, 朋友 → péngyou, etc.

---

## 5. Special semanticNote handling

Full lists in `hsk5-scout-D-grammar-register.md`. Pipeline must enforce:

### Separable verbs (~35) — semanticNote MUST mention split form
Hard cases: 离婚, 结婚, 退休, 结账, 上当, 倒霉, 吃亏, 操心, 拐弯, 握手, 流泪, 受伤, 打工, 打交道, 打喷嚏, 打听, 干活儿, 告别, 集合, 系领带, 鼓掌, 道歉, 出席, 失业, 失眠, 救火, 挂号, 报到, 发愁, 发言, 罚款, 兼职, 恋爱, 怀孕, 辞职, 经商, 着火, 着凉, 注册, 投资, 分手, 结婚, 嫁/娶 pair.

**Rule:** at least one example sentence must show the split form (e.g., 退了休, 結過婚).

### Classical / formal register (~28) — semanticNote flags register
勿, 甲/乙, 则, 之 (component), 何必, 何况, 仿佛, 与其, 至于, 至今, 此外, 从而, 因而, 凭, 所, 某, 一旦, 一律, 一致, 一再, 善于, 属于, 位于, 在于, 等于, 总之, 居然, 难免, 未必, 毕竟, 的确, 据说, 反正, 总算, 难怪, 怪不得.

**Rule:** semanticNote includes "formal/written register" or "classical-flavored — use sparingly in casual speech."

### Measure words (~21) — semanticNote MUST list noun classes
册 (books), 朵 (flowers/clouds), 顿 (meals/scoldings), 滴 (drops), 堆 (piles), 幅 (paintings/maps), 颗 (small round things — heart/star/bullet/candy/tooth), 匹 (horses/cloth), 片 (slices/expanses), 圈 (laps), 群 (animals/people), 套 (sets), 团 (lumps/groups), 阵 (bursts), 项 (list-items), 顶 (hats/tents), 根 (long-thin), 支 (pen-shaped/songs/troops), 则 (news items), 所 (institutions), 届 (sessions).

### Paired conjunctions (~10) — semanticNote MUST show full construction
与其...不如, 何况 (with 连...都), 哪怕...也, 既然...就/那, 除非...否则, 万一...就, 不如, 宁可...也不, 一旦...就, 要不, 反而 (with 不...反而 expectation reversal).

### Multi-reading characters (~13) — semanticNote disambiguates
薄, 背, 便, 朝, 称, 冲, 划, 切, 数, 系, 涨, 挣, 扇.

### Colloquial register flags (~4)
搞 (informal "do/make/get"), 瞧 (informal "look"), 滚 (rude "scram"), 切 (interjection of disdain).

---

## 6. Words to DROP from generation (9)

Already in NUGGETS deck with same sense. Either skip, or tag NUGGETS cards with `alsoIn:["hsk5"]`:

| HSK 5 word | NUGGETS id | Recommendation |
|---|---|---|
| 哎 | 145 | DROP, optionally tag |
| 嗯 | 134 | DROP, optionally tag |
| 不得了 | 57 | DROP, optionally tag |
| 多余 | 34 | DROP, optionally tag |
| 好奇 | 80 | DROP, optionally tag |
| 进步 | 53 | DROP, optionally tag |
| 夸张 | 77 | DROP, optionally tag |
| 系统 | 33 | DROP, optionally tag |
| 自由 | 56 | DROP, optionally tag |

**Note:** existing card id 57 stores 不得了 as `búdéliǎo` (sandhi spelling). Standard dictionary form is `bùdéliǎo`. If kept, normalize.

---

## 7. Pipeline implications

The four scouts collectively identified ~280 cards that need hand-attention out of 1,291 (≈22%). This means:
1. **Pure pypinyin auto-fill is not viable** — must apply override dict.
2. **Pure OpenCC auto-fill is not viable** — must apply Taiwan-modern override dict (smaller if `s2twp.json` is used).
3. **LLM enrichment is mandatory** for semanticNote/components/examples, but the LLM must be primed with the special-handling lists above to avoid generic notes for separable verbs and measure words.

See `markdowns/hsk5-pipeline-proposal.md` (next doc) for the recommended generation pipeline.

---

## 8. LOCKED decisions (Tim approved 2026-04-29)

1. **OpenCC config:** `s2twp.json` (Taiwan with phrases). Verified handles 14/18 worst-case lexical swaps automatically. Override list shrinks to ~12 words.
2. **期/质/企业 pinyin:** Match HSK 4 precedent — `qī`, `zhì`, `qǐyè` (mainland-pinyin standard, since Hanban pinyin is mainland-default. HSK 4 set this with 學期 → xuéqī, 質量 → zhìliàng).
3. **数据 trad:** `資料` (Taiwan everyday). semanticNote flags 數據 for stats/figures.
4. **NUGGETS duplicates:** DROP all 9 from generation. Tag existing NUGGETS cards with `alsoIn:["hsk5"]`. Net cards to generate: 1,291.
5. **国庆节/公元:** Hanban form (國慶節, 公元) with semanticNote explaining ROC/Taiwan split (國慶日 Oct 10, 西元).
6. **土豆:** Hanban form 土豆, gloss = "potato (Mainland)", semanticNote LOUD warning that in Taiwan 土豆 = peanut and potato = 馬鈴薯.

---

## 9. Override list for OpenCC s2twp (verified 2026-04-29)

These words come out wrong from `s2twp.json`. Hardcode override:

| Simp | s2twp output | **Override to** |
|---|---|---|
| 数码 | 數碼 | **數位** |
| 桔子 | 桔子 | **橘子** |
| 冰激凌 | 冰激凌 | **冰淇淋** |
| 报道 | 報道 | **報導** |
| 系领带 | 系領帶 | **繫領帶** |
| 数据 | 數據 | **資料** |
| 角色 | (verify) | confirm trad as 角色, pinyin = juésè |

All other Tier 1 lexical swaps from Scout A are handled correctly by s2twp. Spot-checked: 网络→網路, 软件→軟體, 硬件→硬體, 鼠标→滑鼠, 光盘→光碟, 干燥→乾燥, 干活儿→幹活兒, 重复→重複, 复制→複製, 恢复→恢復, 制造→製造, 制定→制定, 系统→系統.
