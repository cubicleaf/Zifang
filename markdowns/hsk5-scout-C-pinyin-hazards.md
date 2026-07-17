# HSK 5 Pinyin Hazards — Scout C Report

Source: `/Users/cubicleaf/Documents/webdev/Chinese shit/data/hsk5-source-2012.txt` (1,300 entries, Simplified).

Scope: every word likely to be mishandled by `pypinyin` (or any default-tone, no-context engine). The "Likely auto-output" column reflects the kind of output a naive default lookup would emit (most common reading per character, no sandhi, no neutralisation). False positives are intentionally retained — easier to skip a flagged row than to miss a wrong row.

Notation: tones marked with diacritics; neutral tone shown without a diacritic (e.g., `péngyou`).

---

## Master hazard table

| # | Simplified | Hazard Type | Likely auto-output (wrong) | Correct pinyin | Why |
|---|---|---|---|---|---|
| 1 | 爱护 | sandhi (4+4) — actually no sandhi, but check | àihù | àihù | OK, listed for audit only — sometimes engines mis-tone hù |
| 2 | 安慰 | neutral / no-sandhi check | ānwèi | ānwèi | OK, audit only |
| 3 | 熬夜 | tone | áoyè | áoyè | audit |
| 4 | 把握 | sandhi check | bǎwò | bǎwò | audit |
| 5 | 薄 | heteronym | báo | báo / bó | 薄 reads `báo` (thin physical) vs `bó` (slim/meagre, e.g., 单薄). Default may pick wrong reading per context. Flag for manual choice. |
| 6 | 宝贝 | neutral tone | bǎobèi | bǎobèi (also bǎobei colloq.) | Often pronounced with neutral 2nd syllable in speech; pypinyin will keep full bèi. Decide which standard to follow — keep bǎobèi for HSK consistency. |
| 7 | 背 | heteronym | bèi | bèi (back, recite) / bēi (carry) | Standalone 背 is ambiguous. As a single-character entry, pypinyin returns bèi; if the deck sense is "carry on back" it's bēi. Verify gloss. |
| 8 | 背景 | heteronym | bèijǐng | bèijǐng | Correct as bèi here; flagged because 背 is a known heteronym. |
| 9 | 被子 | neutral tone | bèizǐ | bèizi | 子 is neutral here. pypinyin Style.TONE typically gives bèizi correctly via its neutral-tone dictionary, but Style.TONE3 may emit bei4zi3. |
| 10 | 鞭炮 | tone | biānpào | biānpào | audit |
| 11 | 便 | heteronym | biàn | biàn (convenient) / pián (cheap, 便宜) | Single-char entry — sense matters. As HSK 5 standalone "便" usually = "then/convenient" → biàn. Flag. |
| 12 | 标志 | tone | biāozhì | biāozhì | audit |
| 13 | 玻璃 | neutral tone | bōlí | bōli | 璃 normally light tone in 玻璃. pypinyin may keep lí. |
| 14 | 脖子 | neutral tone | bózǐ | bózi | 子 light tone. |
| 15 | 不安 | bù sandhi | bù'ān | bù'ān | 不 + 1st tone → stays bù. No change, audit only. |
| 16 | 不得了 | bù sandhi + 了 reading | bùdéle | bùdéliǎo | 了 reads `liǎo` here ("can't be helped"), not perfective `le`. Sandhi: 不 stays bù before 2nd tone dé. |
| 17 | 不断 | bù sandhi | bùduàn | búduàn | 不 + 4th tone → bú. |
| 18 | 不见得 | bù sandhi + neutral | bùjiàndé | bújiànde | 不 + 4th → bú. 得 here is light tone `de`. |
| 19 | 不耐烦 | bù sandhi | bùnàifán | búnàifán | 不 + 4th → bú. |
| 20 | 不然 | bù sandhi | bùrán | bùrán | 不 + 2nd → stays bù. audit. |
| 21 | 不如 | bù sandhi | bùrú | bùrú | 不 + 2nd → bù. audit. |
| 22 | 不要紧 | bù sandhi | bùyàojǐn | búyàojǐn | 不 + 4th → bú. |
| 23 | 不足 | bù sandhi | bùzú | bùzú | 不 + 2nd → bù. audit. |
| 24 | 步骤 | tone | bùzhòu | bùzhòu | audit |
| 25 | 曾经 | heteronym | zēngjīng | céngjīng | 曾 has two readings: `céng` (formerly) and `zēng` (great-grand). pypinyin default is often zēng → wrong here. |
| 26 | 叉子 | neutral tone | chāzǐ | chāzi | 子 light. |
| 27 | 长途 | 长 heteronym | zhǎngtú | chángtú | 长 = cháng (long) here, not zhǎng. pypinyin default for 长 is often cháng so this may pass — but always audit any 长 word. |
| 28 | 朝 | heteronym | cháo | cháo / zhāo | Standalone 朝 — sense determines reading. cháo = toward/dynasty; zhāo = morning. HSK 5 sense usually cháo. Flag. |
| 29 | 重复 | 重 heteronym | zhòngfù | chóngfù | 重 = chóng (again), not zhòng (heavy). pypinyin default is zhòng → WRONG. |
| 30 | 出色 | tone | chūsè | chūsè | audit |
| 31 | 除夕 | tone | chúxī | chúxī | audit |
| 32 | 窗帘 | tone | chuānglián | chuānglián | audit |
| 33 | 醋 | tone | cù | cù | audit |
| 34 | 答应 | neutral tone | dāyīng | dāying | 应 light tone in 答应. |
| 35 | 大方 | neutral tone | dàfāng | dàfang | 方 light tone (meaning "generous"). pypinyin keeps dàfāng. |
| 36 | 大厦 | heteronym | dàshà | dàshà | 厦 = shà (big building) here, not xià (place name 厦门). pypinyin default may give xià. |
| 37 | 单纯 | tone | dānchún | dānchún | audit |
| 38 | 耽误 | neutral tone | dānwù | dānwu | 误 light tone in 耽误. |
| 39 | 胆小鬼 | tone | dǎnxiǎoguǐ | dǎnxiǎoguǐ | audit |
| 40 | 当地 | 当 heteronym | dāngdì | dāngdì | 当 = dāng (at) here. dàng (proper) is alt reading. Default usually dāng → OK; flag. |
| 41 | 当心 | 当 heteronym | dāngxīn | dāngxīn | dāng. audit. |
| 42 | 倒霉 | 倒 heteronym | dàoméi | dǎoméi | 倒 = dǎo (fall) here, not dào (pour/inverse). pypinyin default usually dǎo. Flag. |
| 43 | 到达 | tone | dàodá | dàodá | audit |
| 44 | 道理 | neutral tone | dàolǐ | dàoli | 理 light in 道理 in casual speech; standard dictionaries keep dàolǐ — DO NOT neutralise; audit only. |
| 45 | 的确 | 的 heteronym | de què / dí què | díquè | 的 reads `dí` here, not `de` (particle) or `dì` (target). pypinyin default `de` → WRONG. |
| 46 | 地道 | neutral tone + heteronym | dìdào | dìdao (authentic) / dìdào (tunnel) | Two senses, two pinyins. Authentic = dìdao with neutral; tunnel = dìdào full tone. Manual override required per gloss. |
| 47 | 地理 | tone | dìlǐ | dìlǐ | audit |
| 48 | 顶 | tone | dǐng | dǐng | audit |
| 49 | 动画片 | 片 heteronym | dònghuàpiàn | dònghuàpiàn (also piān) | 片 = piàn or piān. In 动画片, common reading is piàn (per Xinhua); some dictionaries piān. Confirm deck preference. |
| 50 | 豆腐 | neutral tone | dòufǔ | dòufu | 腐 light tone. pypinyin keeps fǔ. |
| 51 | 顿 | classifier; neutral after numerals | dùn | dùn | Standalone full tone OK; flagged because in compounds like 一顿饭 it can sound light, but standard keeps dùn. |
| 52 | 多亏 | tone | duōkuī | duōkuī | audit |
| 53 | 朵 | classifier — full tone OK | duǒ | duǒ | audit |
| 54 | 耳环 | tone | ěrhuán | ěrhuán | audit |
| 55 | 发抖 | tone | fādǒu | fādǒu | audit |
| 56 | 发挥 | tone | fāhuī | fāhuī | audit |
| 57 | 仿佛 | tone | fǎngfú | fǎngfú | audit |
| 58 | 非 | tone | fēi | fēi | audit |
| 59 | 肥皂 | tone | féizào | féizào | audit |
| 60 | 分别 | tone | fēnbié | fēnbié | audit |
| 61 | 分布 | tone | fēnbù | fēnbù | audit |
| 62 | 分配 | tone | fēnpèi | fēnpèi | audit |
| 63 | 分手 | tone | fēnshǒu | fēnshǒu | audit |
| 64 | 服装 | tone | fúzhuāng | fúzhuāng | audit |
| 65 | 妇女 | tone | fùnǚ | fùnǚ | audit |
| 66 | 干脆 | 干 heteronym | gàncuì | gāncuì | 干 = gān (dry) here, not gàn (do). pypinyin default often gàn → WRONG. |
| 67 | 干燥 | 干 heteronym | gànzào | gānzào | 干 = gān. Same risk as above. |
| 68 | 干活儿 | 干 heteronym + erhua | gànhuór | gànhuór | 干 = gàn (do/work) here — opposite of above. ALSO erhua: 活 + 儿 → huór, must merge. pypinyin will give `gàn huó ér` (3 syllables) — WRONG. |
| 69 | 赶紧 | tone | gǎnjǐn | gǎnjǐn | audit |
| 70 | 高档 | tone | gāodàng | gāodàng | audit |
| 71 | 个别 | 个 neutral?? | gèbié | gèbié | 个 here is full 4th tone; flagged because as classifier it's often light (一个 = yíge). audit. |
| 72 | 个人 | 个 heteronym/full tone | gèrén | gèrén | full tone here. audit. |
| 73 | 个性 | 个 full tone | gèxìng | gèxìng | audit. |
| 74 | 各自 | tone | gèzì | gèzì | audit |
| 75 | 公布 | tone | gōngbù | gōngbù | audit |
| 76 | 公主 | tone | gōngzhǔ | gōngzhǔ | audit |
| 77 | 姑姑 | neutral tone (reduplication) | gūgū | gūgu | Reduplicated kin term — second syllable light tone. pypinyin keeps gū. |
| 78 | 骨头 | neutral tone | gǔtóu | gǔtou | 头 light in 骨头. |
| 79 | 怪不得 | neutral tone | guàibùdé | guàibude | 不 + 得 both light here ("no wonder"). pypinyin will full-tone both. |
| 80 | 关闭 | tone | guānbì | guānbì | audit |
| 81 | 管子 | neutral tone | guǎnzǐ | guǎnzi | 子 light. |
| 82 | 光临 | tone | guānglín | guānglín | audit |
| 83 | 锅 | tone | guō | guō | audit |
| 84 | 国庆节 | tone | guóqìngjié | guóqìngjié | audit |
| 85 | 哈 | tone | hā | hā | audit |
| 86 | 行业 | 行 heteronym | xíngyè | hángyè | 行 = háng (line/profession). pypinyin default xíng → WRONG. |
| 87 | 豪华 | tone | háohuá | háohuá | audit |
| 88 | 好客 | 好 heteronym | hǎokè | hàokè | 好 = hào (to like, fond of) here, not hǎo (good). pypinyin default hǎo → WRONG. |
| 89 | 好奇 | 好 heteronym | hǎoqí | hàoqí | 好 = hào here. Same risk. |
| 90 | 合同 | neutral?? | hétóng | hétong | 同 sometimes light in 合同; standard dictionary keeps hétóng. Audit; HSK 4 precedent likely full tone. |
| 91 | 何必 | tone | hébì | hébì | audit |
| 92 | 何况 | tone | hékuàng | hékuàng | audit |
| 93 | 猴子 | neutral tone | hóuzǐ | hóuzi | 子 light. |
| 94 | 后背 | 背 heteronym | hòubèi | hòubèi | bèi (back) — correct; flag because 背 is a known heteronym. |
| 95 | 胡同 | neutral tone | hútóng | hútòng (or hútong) | Standard pinyin: hútòng. pypinyin may give hútóng (default tóng) → WRONG. |
| 96 | 糊涂 | neutral tone | hútú | hútu | 涂 light in 糊涂. |
| 97 | 划 | heteronym | huà | huà / huá | 划 = huà (plan) or huá (paddle, scratch). Standalone — sense decides. HSK 5 entry likely huà; flag. |
| 98 | 华裔 | tone | huáyì | huáyì | audit |
| 99 | 化学 | tone | huàxué | huàxué | audit |
| 100 | 缓解 | tone | huǎnjiě | huǎnjiě | audit |
| 101 | 灰尘 | neutral tone? | huīchén | huīchén | full tone standard. audit. |
| 102 | 火柴 | tone | huǒchái | huǒchái | audit |
| 103 | 伙伴 | tone | huǒbàn | huǒbàn | audit |
| 104 | 或许 | tone | huòxǔ | huòxǔ | audit |
| 105 | 计算 | tone | jìsuàn | jìsuàn | audit |
| 106 | 系领带 | 系 heteronym | xìlǐngdài | jìlǐngdài | 系 = jì (tie/fasten) here, not xì (system). pypinyin default xì → WRONG. |
| 107 | 寂寞 | tone | jìmò | jìmò | audit |
| 108 | 夹子 | 夹 heteronym + neutral | jiāzǐ / jiázǐ | jiāzi | 夹 = jiā (clip) usually; 子 light tone. pypinyin may give jiá (also valid for 夹 = double-layered). |
| 109 | 家务 | tone | jiāwù | jiāwù | audit |
| 110 | 假如 | 假 heteronym | jiǎrú | jiǎrú | 假 = jiǎ (false/if) here, not jià (vacation). Default usually jiǎ → OK; flag. |
| 111 | 假设 | 假 heteronym | jiǎshè | jiǎshè | jiǎ. audit. |
| 112 | 假装 | 假 heteronym | jiǎzhuāng | jiǎzhuāng | jiǎ. audit. |
| 113 | 嫁 | tone | jià | jià | audit |
| 114 | 肩膀 | tone | jiānbǎng | jiānbǎng | audit |
| 115 | 艰巨 | tone | jiānjù | jiānjù | audit |
| 116 | 艰苦 | tone | jiānkǔ | jiānkǔ | audit |
| 117 | 兼职 | tone | jiānzhí | jiānzhí | audit |
| 118 | 角度 | 角 heteronym | jiǎodù / juédù | jiǎodù | 角 = jiǎo (angle/corner) here, not jué (role). pypinyin default usually jiǎo → OK. Flag. |
| 119 | 角色 | 角 heteronym | jiǎosè | juésè | 角 = jué (role) here. pypinyin default jiǎo → WRONG. |
| 120 | 教材 | 教 heteronym | jiàocái | jiàocái | jiào (4th) here. 教 also reads jiāo (1st). Default usually jiào → OK; flag. |
| 121 | 教练 | 教 heteronym | jiàoliàn | jiàoliàn | jiào. audit. |
| 122 | 教训 | 教 heteronym | jiàoxùn | jiàoxùn | jiào. audit. |
| 123 | 接触 | tone | jiēchù | jiēchù | audit |
| 124 | 结实 | neutral tone + 结 heteronym | jiéshí | jiēshi | 结 = jiē (1st tone) here ("sturdy"), and 实 light. pypinyin default jiéshí → WRONG (both syllables off). |
| 125 | 结构 | 结 heteronym | jiégòu | jiégòu | jié here. flag. |
| 126 | 结合 | 结 heteronym | jiéhé | jiéhé | jié. audit. |
| 127 | 结论 | 结 heteronym | jiélùn | jiélùn | jié. audit. |
| 128 | 结账 | 结 heteronym | jiézhàng | jiézhàng | jié. audit. |
| 129 | 戒指 | neutral tone | jièzhǐ | jièzhi | 指 light in 戒指. |
| 130 | 借口 | tone | jièkǒu | jièkǒu | audit |
| 131 | 尽快 | 尽 heteronym | jìnkuài | jǐnkuài | 尽 = jǐn (3rd) here ("as much as possible"), not jìn (4th, "exhaust"). pypinyin default often jìn → WRONG. |
| 132 | 尽量 | 尽 heteronym | jìnliàng | jǐnliàng | jǐn here. WRONG default. |
| 133 | 尽力 | 尽 heteronym | jǐnlì / jìnlì | jìnlì | Here 尽 = jìn (4th, "use all"). Opposite of above two. Manual disambiguation required. |
| 134 | 紧急 | tone | jǐnjí | jǐnjí | audit |
| 135 | 谨慎 | tone | jǐnshèn | jǐnshèn | audit |
| 136 | 决赛 | tone | juésài | juésài | audit |
| 137 | 觉 | heteronym | jué | jué (feel) / jiào (sleep) | Standalone — sense decides. As HSK 5 entry usually 自觉/感觉 sense → jué. Flag. |
| 138 | 角色 | (already flagged above) | | | duplicate — skip |
| 139 | 桔子 | tone (variant char) | jiézǐ | júzi | 桔 here = 橘 (orange) → jú; 子 light. pypinyin may give jié (default for 桔 = jié in herbal sense) → WRONG. |
| 140 | 卡车 | 卡 heteronym | qiǎchē | kǎchē | 卡 = kǎ (card/truck) here, not qiǎ (stuck). pypinyin default kǎ — usually OK. Flag. |
| 141 | 看不起 | bù sandhi (between 4th tones) | kànbùqǐ | kànbuqǐ | 不 here is light tone in V-不-V potential structure; standard is kànbuqǐ. pypinyin will give bú or bù full tone → WRONG. |
| 142 | 颗 | classifier | kē | kē | audit |
| 143 | 课程 | tone | kèchéng | kèchéng | audit |
| 144 | 空闲 | 空 heteronym | kōngxián | kòngxián | 空 = kòng (4th, "free time") here, not kōng (1st, "empty"). pypinyin default kōng → WRONG. |
| 145 | 空间 | 空 heteronym | kōngjiān | kōngjiān | kōng correct. Flag. |
| 146 | 控制 | tone | kòngzhì | kòngzhì | audit |
| 147 | 口味 | tone | kǒuwèi | kǒuwèi | audit |
| 148 | 会计 | 会 heteronym | huìjì | kuàijì | 会 = kuài (4th, "accounting") here, not huì (meet). pypinyin default huì → WRONG. |
| 149 | 落后 | 落 heteronym | luòhòu | luòhòu | luò here. 落 also reads là (leave behind), lào. Default luò → OK; flag. |
| 150 | 老百姓 | tone | lǎobǎixìng | lǎobǎixìng | audit |
| 151 | 老婆 | neutral tone | lǎopó | lǎopo | 婆 light in 老婆. |
| 152 | 老实 | neutral tone | lǎoshí | lǎoshi | 实 light in 老实. |
| 153 | 老鼠 | tone | lǎoshǔ | lǎoshǔ | audit |
| 154 | 姥姥 | neutral tone | lǎolǎo | lǎolao | Reduplicated kin term — second syllable light. |
| 155 | 乐观 | 乐 heteronym | yuèguān | lèguān | 乐 = lè (happy) here, not yuè (music). pypinyin default may give yuè → WRONG. |
| 156 | 乐器 | 乐 heteronym | lèqì | yuèqì | 乐 = yuè here ("musical instrument"). Opposite case. pypinyin default lè → WRONG. |
| 157 | 厘米 | tone | límǐ | límǐ | audit |
| 158 | 离婚 | tone | líhūn | líhūn | audit |
| 159 | 良好 | tone | liánghǎo | liánghǎo | audit |
| 160 | 粮食 | tone | liángshí | liángshi | 食 sometimes light. Standard liángshi (per Xinhua). pypinyin liángshí → potentially WRONG. |
| 161 | 了不起 | 了 heteronym | lebùqǐ | liǎobuqǐ | 了 = liǎo (3rd, "finish/be able"), not particle le. AND 不 → bu light. Triple-trap. pypinyin will likely give le bù qǐ. |
| 162 | 临时 | tone | línshí | línshí | audit |
| 163 | 灵活 | tone | línghuó | línghuó | audit |
| 164 | 铃 | tone | líng | líng | audit |
| 165 | 流泪 | tone | liúlèi | liúlèi | audit |
| 166 | 龙 | tone | lóng | lóng | audit |
| 167 | 漏 | tone | lòu | lòu | audit |
| 168 | 陆地 | tone | lùdì | lùdì | audit |
| 169 | 陆续 | tone | lùxù | lùxù | audit |
| 170 | 录取 | tone | lùqǔ | lùqǔ | audit |
| 171 | 录音 | tone | lùyīn | lùyīn | audit |
| 172 | 论文 | 论 heteronym | lùnwén | lùnwén | lùn (essay). 论 also reads lún (Lúnyǔ). Default lùn → OK; flag. |
| 173 | 逻辑 | tone | luójí | luójí | audit |
| 174 | 馒头 | neutral tone | mántóu | mántou | 头 light in 馒头. |
| 175 | 麦克风 | tone | màikèfēng | màikèfēng | audit |
| 176 | 矛盾 | tone | máodùn | máodùn | audit |
| 177 | 眉毛 | neutral tone | méimáo | méimao | 毛 light in 眉毛. |
| 178 | 媒体 | tone | méitǐ | méitǐ | audit |
| 179 | 美术 | tone | měishù | měishù | audit |
| 180 | 蜜蜂 | tone | mìfēng | mìfēng | audit |
| 181 | 描写 | tone | miáoxiě | miáoxiě | audit |
| 182 | 模仿 | 模 heteronym | mófǎng | mófǎng | mó here ("model/imitate"). 模 also reads mú (mold, 模样). Default mó → OK; flag. |
| 183 | 模糊 | 模 heteronym | móhú | móhu | mó. 糊 light in 模糊. pypinyin keeps hú → potentially WRONG. |
| 184 | 模特 | 模 heteronym | mótè | mótè | mó. audit. |
| 185 | 摩托车 | tone | mótuōchē | mótuōchē | audit |
| 186 | 木头 | neutral tone | mùtóu | mùtou | 头 light in 木头. |
| 187 | 哪怕 | tone | nǎpà | nǎpà | audit |
| 188 | 难免 | 难 heteronym | nánmiǎn | nánmiǎn | nán here. 难 also reads nàn (calamity). Default nán → OK; flag. |
| 189 | 脑袋 | neutral tone | nǎodài | nǎodai | 袋 light in 脑袋. |
| 190 | 嫩 | tone | nèn | nèn | audit |
| 191 | 嗯 | interjection | ng | ǹg / ńg / ňg / ǹ (varies) | pypinyin handles 嗯 as ńg or similar; verify. Flag for manual standardisation. |
| 192 | 年纪 | tone | niánjì | niánjì | audit |
| 193 | 牛仔裤 | 仔 heteronym | niúzǐkù | niúzǎikù | 仔 = zǎi here ("kid/cowboy"), not zǐ. pypinyin default zǐ → WRONG. |
| 194 | 农村 | tone | nóngcūn | nóngcūn | audit |
| 195 | 女士 | tone | nǚshì | nǚshì | audit |
| 196 | 偶然 | tone | ǒurán | ǒurán | audit |
| 197 | 盼望 | tone | pànwàng | pànwàng | audit |
| 198 | 培训 | tone | péixùn | péixùn | audit |
| 199 | 培养 | tone | péiyǎng | péiyǎng | audit |
| 200 | 赔偿 | tone | péicháng | péicháng | audit |
| 201 | 佩服 | neutral tone | pèifú | pèifu | 服 light in 佩服. |
| 202 | 盆 | tone | pén | pén | audit |
| 203 | 批 | tone | pī | pī | audit |
| 204 | 批准 | tone | pīzhǔn | pīzhǔn | audit |
| 205 | 披 | tone | pī | pī | audit |
| 206 | 疲劳 | tone | píláo | píláo | audit |
| 207 | 匹 | classifier | pǐ | pǐ | audit |
| 208 | 片 | 片 heteronym | piàn | piàn (slice, classifier) / piān (film) | Standalone 片 — sense ambiguous. piàn most common. Flag. |
| 209 | 片面 | 片 heteronym | piànmiàn | piànmiàn | piàn. audit. |
| 210 | 飘 | tone | piāo | piāo | audit |
| 211 | 拼音 | tone | pīnyīn | pīnyīn | audit |
| 212 | 频道 | tone | píndào | píndào | audit |
| 213 | 平 | tone | píng | píng | audit |
| 214 | 平安 | tone | píng'ān | píng'ān | audit |
| 215 | 平常 | tone | píngcháng | píngcháng | audit |
| 216 | 凭 | tone | píng | píng | audit |
| 217 | 迫切 | tone | pòqiè | pòqiè | audit |
| 218 | 破产 | tone | pòchǎn | pòchǎn | audit |
| 219 | 破坏 | tone | pòhuài | pòhuài | audit |
| 220 | 期待 | tone | qīdài | qīdài | audit |
| 221 | 其余 | tone | qíyú | qíyú | audit |
| 222 | 奇迹 | tone | qíjì | qíjì | audit |
| 223 | 企业 | tone | qǐyè | qǐyè | audit |
| 224 | 启发 | tone | qǐfā | qǐfā | audit |
| 225 | 气氛 | tone | qìfēn | qìfēn | audit. (Note: officially qìfēn, but some speakers say qìfèn — standard is fēn.) |
| 226 | 谦虚 | tone | qiānxū | qiānxū | audit |
| 227 | 浅 | tone | qiǎn | qiǎn | audit |
| 228 | 欠 | tone | qiàn | qiàn | audit |
| 229 | 强烈 | 强 heteronym | qiángliè | qiángliè | qiáng. 强 also reads qiǎng (force) and jiàng (stubborn). Default qiáng → OK; flag. |
| 230 | 强调 | 强 heteronym + 调 heteronym | qiángdiào | qiángdiào | qiáng + diào. 调 also reads tiáo. Default usually correct — flag. |
| 231 | 抢 | tone | qiǎng | qiǎng | audit |
| 232 | 悄悄 | reduplication | qiāoqiāo | qiāoqiāo | OK as full tone. audit. (Some speakers neutralise 2nd, but standard keeps both.) |
| 233 | 瞧 | tone | qiáo | qiáo | audit |
| 234 | 切 | heteronym | qiē | qiē (cut) / qiè (close to) | Standalone — sense matters. HSK entry likely qiē. Flag. |
| 235 | 亲爱 | tone | qīn'ài | qīn'ài | audit |
| 236 | 亲切 | 切 heteronym | qīnqiè | qīnqiè | qiè here. pypinyin default qiē → WRONG. |
| 237 | 亲自 | tone | qīnzì | qīnzì | audit |
| 238 | 勤奋 | tone | qínfèn | qínfèn | audit |
| 239 | 青 | tone | qīng | qīng | audit |
| 240 | 青春 | tone | qīngchūn | qīngchūn | audit |
| 241 | 青少年 | tone | qīngshàonián | qīngshàonián | audit |
| 242 | 轻视 | tone | qīngshì | qīngshì | audit |
| 243 | 轻易 | tone | qīngyì | qīngyì | audit |
| 244 | 清淡 | tone | qīngdàn | qīngdàn | audit |
| 245 | 情景 | tone | qíngjǐng | qíngjǐng | audit |
| 246 | 情绪 | tone | qíngxù | qíngxù | audit |
| 247 | 请求 | tone | qǐngqiú | qǐngqiú | audit |
| 248 | 庆祝 | tone | qìngzhù | qìngzhù | audit |
| 249 | 球迷 | tone | qiúmí | qiúmí | audit |
| 250 | 趋势 | tone | qūshì | qūshì | audit |
| 251 | 取消 | tone | qǔxiāo | qǔxiāo | audit |
| 252 | 娶 | tone | qǔ | qǔ | audit |
| 253 | 圈 | heteronym | quān | quān (circle) / juàn (pen for animals) | Standalone — sense decides. HSK 5 likely quān. Flag. |
| 254 | 权力 | tone | quánlì | quánlì | audit |
| 255 | 权利 | tone | quánlì | quánlì | audit (homophone with 权力 — both correct) |
| 256 | 全面 | tone | quánmiàn | quánmiàn | audit |
| 257 | 缺乏 | tone | quēfá | quēfá | audit |
| 258 | 群 | tone | qún | qún | audit |
| 259 | 燃烧 | tone | ránshāo | ránshāo | audit |
| 260 | 绕 | tone | rào | rào | audit |
| 261 | 热爱 | tone | rè'ài | rè'ài | audit |
| 262 | 热烈 | tone | rèliè | rèliè | audit |
| 263 | 人才 | tone | réncái | réncái | audit |
| 264 | 忍不住 | bù sandhi | rěnbùzhù | rěnbuzhù | 不 light here in V-不-V potential. pypinyin gives full bù → WRONG. |
| 265 | 日子 | neutral tone | rìzǐ | rìzi | 子 light. |
| 266 | 软 | tone | ruǎn | ruǎn | audit |
| 267 | 弱 | tone | ruò | ruò | audit |
| 268 | 嗓子 | neutral tone | sǎngzǐ | sǎngzi | 子 light. |
| 269 | 沙漠 | tone | shāmò | shāmò | audit |
| 270 | 沙滩 | tone | shātān | shātān | audit |
| 271 | 删除 | tone | shānchú | shānchú | audit |
| 272 | 闪电 | tone | shǎndiàn | shǎndiàn | audit |
| 273 | 扇子 | 扇 heteronym + neutral | shānzǐ / shànzǐ | shànzi | 扇 = shàn (4th, fan) here, not shān (1st, fan-as-verb). pypinyin may default shān → WRONG. Plus 子 light. |
| 274 | 善良 | tone | shànliáng | shànliáng | audit |
| 275 | 善于 | tone | shànyú | shànyú | audit |
| 276 | 蛇 | tone | shé | shé | audit |
| 277 | 舍不得 | bù sandhi + neutral | shěbùdé | shěbude | 不 + 得 both light. pypinyin will full-tone → WRONG. |
| 278 | 设备 | tone | shèbèi | shèbèi | audit |
| 279 | 摄影 | tone | shèyǐng | shèyǐng | audit |
| 280 | 伸 | tone | shēn | shēn | audit |
| 281 | 神秘 | tone | shénmì | shénmì | audit |
| 282 | 升 | tone | shēng | shēng | audit |
| 283 | 生长 | 长 heteronym | shēngcháng | shēngzhǎng | 长 = zhǎng (grow) here. pypinyin default cháng → WRONG. |
| 284 | 声调 | 调 heteronym | shēngdiào | shēngdiào | diào here. 调 also reads tiáo. Default diào → OK; flag. |
| 285 | 绳子 | neutral tone | shéngzǐ | shéngzi | 子 light. |
| 286 | 省略 | tone | shěnglüè | shěnglüè | audit |
| 287 | 失眠 | tone | shīmián | shīmián | audit |
| 288 | 狮子 | neutral tone | shīzǐ | shīzi | 子 light. |
| 289 | 湿润 | tone | shīrùn | shīrùn | audit |
| 290 | 石头 | neutral tone | shítóu | shítou | 头 light in 石头. |
| 291 | 时髦 | tone | shímáo | shímáo | audit |
| 292 | 实话 | tone | shíhuà | shíhuà | audit |
| 293 | 食物 | tone | shíwù | shíwù | audit |
| 294 | 使劲儿 | erhua | shǐjìnér | shǐjìnr | 儿 = erhua suffix; merge with previous syllable. pypinyin yields 3 syllables → WRONG. |
| 295 | 似的 | 似 heteronym + neutral | sìde / sìdì | shìde | 似 = shì (4th) here ("like/as"), not sì. AND 的 = de light. pypinyin will give sìde or sì de — WRONG. |
| 296 | 似乎 | 似 heteronym | shìhū | sìhū | 似 = sì here. Opposite of 似的. pypinyin default sì → OK; but 乎 sometimes light. |
| 297 | 收据 | tone | shōujù | shōujù | audit |
| 298 | 手指 | tone | shǒuzhǐ | shǒuzhǐ | audit |
| 299 | 首 | tone | shǒu | shǒu | audit |
| 300 | 寿命 | tone | shòumìng | shòumìng | audit |
| 301 | 梳子 | neutral tone | shūzǐ | shūzi | 子 light. |
| 302 | 数 | heteronym | shù | shù (number) / shǔ (count) | Standalone — sense decides. As HSK noun → shù; as verb (count) → shǔ. Manual override. |
| 303 | 数据 | 数 heteronym | shǔjù | shùjù | shù here ("number/data"). pypinyin default shù → OK. Flag. |
| 304 | 数码 | 数 heteronym | shǔmǎ | shùmǎ | shù here. Flag. |
| 305 | 摔倒 | 倒 heteronym | shuāidào | shuāidǎo | 倒 = dǎo (fall) here. pypinyin default may pick dào → WRONG. |
| 306 | 甩 | tone | shuǎi | shuǎi | audit |
| 307 | 双方 | tone | shuāngfāng | shuāngfāng | audit |
| 308 | 说不定 | bù sandhi | shuōbùdìng | shuōbudìng | 不 light in V-不-X. pypinyin → WRONG. |
| 309 | 说服 | 说 heteronym | shuōfú | shuìfú (older) / shuōfú (modern) | Older standard shuìfú; modern textbook shuōfú. Confirm deck preference; pypinyin will give shuōfú by default. |
| 310 | 丝绸 | tone | sīchóu | sīchóu | audit |
| 311 | 丝毫 | tone | sīháo | sīháo | audit |
| 312 | 撕 | tone | sī | sī | audit |
| 313 | 似的 | (already flagged) | | | duplicate — skip |
| 314 | 宿舍 | 宿 heteronym | sùshè | sùshè | sù here. 宿 also reads xiǔ (night, classifier), xiù. Default sù → OK; flag. |
| 315 | 随身 | tone | suíshēn | suíshēn | audit |
| 316 | 太极拳 | tone | tàijíquán | tàijíquán | audit |
| 317 | 太太 | neutral tone | tàitài | tàitai | Reduplicated — second light. pypinyin keeps tài. |
| 318 | 谈判 | tone | tánpàn | tánpàn | audit |
| 319 | 坦率 | tone | tǎnshuài | tǎnshuài | audit |
| 320 | 烫 | tone | tàng | tàng | audit |
| 321 | 逃 | tone | táo | táo | audit |
| 322 | 逃避 | tone | táobì | táobì | audit |
| 323 | 桃 | tone | táo | táo | audit |
| 324 | 淘气 | tone | táoqì | táoqì | audit |
| 325 | 讨价还价 | 还 heteronym | tǎojiàháijià / tǎojiàhuánjià | tǎojiàhuánjià | 还 = huán here ("return"), not hái (also/still). pypinyin default hái → WRONG. |
| 326 | 套 | classifier | tào | tào | audit |
| 327 | 特征 | tone | tèzhēng | tèzhēng | audit |
| 328 | 疼爱 | tone | téng'ài | téng'ài | audit |
| 329 | 提倡 | tone | tíchàng | tíchàng | audit |
| 330 | 体贴 | tone | tǐtiē | tǐtiē | audit |
| 331 | 调皮 | 调 heteronym | diàopí | tiáopí | 调 = tiáo here ("naughty"), not diào. pypinyin default may pick diào → WRONG. |
| 332 | 调整 | 调 heteronym | diàozhěng | tiáozhěng | 调 = tiáo here. pypinyin default may pick diào → WRONG. |
| 333 | 挑战 | 挑 heteronym | tiāozhàn | tiǎozhàn | 挑 = tiǎo (3rd) here ("provoke"), not tiāo (1st, "carry/pick"). pypinyin default tiāo → WRONG. |
| 334 | 通常 | tone | tōngcháng | tōngcháng | audit |
| 335 | 统一 | yī sandhi | tǒngyī | tǒngyī | 一 here is part of compound, full 1st tone — no sandhi (because 一 is the 2nd character of a compound, not the proclitic). Audit only. |
| 336 | 痛苦 | tone | tòngkǔ | tòngkǔ | audit |
| 337 | 痛快 | tone | tòngkuài | tòngkuai | 快 sometimes light in 痛快 (per Xinhua). Flag. |
| 338 | 偷 | tone | tōu | tōu | audit |
| 339 | 透明 | tone | tòumíng | tòumíng | audit |
| 340 | 突出 | tone | tūchū | tūchū | audit |
| 341 | 土豆 | tone | tǔdòu | tǔdòu | audit |
| 342 | 吐 | heteronym | tù | tǔ (spit) / tù (vomit) | Standalone — sense decides. pypinyin default tǔ. HSK 5 sense usually tù (vomit). Flag. |
| 343 | 兔子 | neutral tone | tùzǐ | tùzi | 子 light. |
| 344 | 团 | tone | tuán | tuán | audit |
| 345 | 推辞 | tone | tuīcí | tuīcí | audit |
| 346 | 推广 | tone | tuīguǎng | tuīguǎng | audit |
| 347 | 推荐 | tone | tuījiàn | tuījiàn | audit |
| 348 | 退步 | tone | tuìbù | tuìbù | audit |
| 349 | 退休 | tone | tuìxiū | tuìxiū | audit |
| 350 | 歪 | tone | wāi | wāi | audit |
| 351 | 完美 | tone | wánměi | wánměi | audit |
| 352 | 玩具 | tone | wánjù | wánjù | audit |
| 353 | 万一 | tone | wànyī | wànyī | audit |
| 354 | 网络 | tone | wǎngluò | wǎngluò | audit |
| 355 | 往返 | tone | wǎngfǎn | wǎngfǎn | audit |
| 356 | 微笑 | tone | wēixiào | wēixiào | audit |
| 357 | 违反 | tone | wéifǎn | wéifǎn | audit |
| 358 | 围巾 | tone | wéijīn | wéijīn | audit |
| 359 | 围绕 | tone | wéirào | wéirào | audit |
| 360 | 唯一 | tone | wéiyī | wéiyī | audit |
| 361 | 维修 | tone | wéixiū | wéixiū | audit |
| 362 | 伟大 | tone | wěidà | wěidà | audit |
| 363 | 尾巴 | neutral tone | wěibā | wěiba | 巴 light in 尾巴. |
| 364 | 委屈 | neutral tone | wěiqū | wěiqu | 屈 light in 委屈 (per Xinhua). Flag. |
| 365 | 卧室 | tone | wòshì | wòshì | audit |
| 366 | 屋子 | neutral tone | wūzǐ | wūzi | 子 light. |
| 367 | 无奈 | tone | wúnài | wúnài | audit |
| 368 | 无所谓 | tone | wúsuǒwèi | wúsuǒwèi | audit |
| 369 | 武术 | tone | wǔshù | wǔshù | audit |
| 370 | 勿 | tone | wù | wù | audit |
| 371 | 物理 | tone | wùlǐ | wùlǐ | audit |
| 372 | 雾 | tone | wù | wù | audit |
| 373 | 系 | heteronym | xì | xì (system) / jì (tie) | Standalone. As HSK noun "system/department" → xì; as verb "tie" → jì. Manual choice. |
| 374 | 系统 | 系 heteronym | jìtǒng | xìtǒng | 系 = xì here. pypinyin default may give jì → WRONG. |
| 375 | 细节 | tone | xìjié | xìjié | audit |
| 376 | 瞎 | tone | xiā | xiā | audit |
| 377 | 下载 | 载 heteronym | xiàzài | xiàzài | zài (4th, "load/download") here. 载 also reads zǎi (year/record). Default zài → OK; flag. |
| 378 | 吓 | heteronym | xià | xià / hè | 吓 = xià (scare) usually; hè in 恐吓. pypinyin default xià → OK; flag. |
| 379 | 夏令营 | tone | xiàlìngyíng | xiàlìngyíng | audit |
| 380 | 鲜艳 | 鲜 heteronym | xiānyàn | xiānyàn | xiān here. 鲜 also reads xiǎn (rare). Default xiān → OK; flag. |
| 381 | 显得 | neutral?? | xiǎndé | xiǎnde | 得 light here. pypinyin keeps dé → potentially WRONG. |
| 382 | 县 | tone | xiàn | xiàn | audit |
| 383 | 现象 | tone | xiànxiàng | xiànxiàng | audit |
| 384 | 相处 | 处 heteronym | xiāngchù | xiāngchǔ | 处 = chǔ (3rd, "get along") here, not chù (4th, "place"). pypinyin default may give chù → WRONG. |
| 385 | 相当 | 当 heteronym | xiāngdāng | xiāngdāng | dāng here. flag. |
| 386 | 相对 | tone | xiāngduì | xiāngduì | audit |
| 387 | 相关 | tone | xiāngguān | xiāngguān | audit |
| 388 | 相似 | 似 heteronym | xiāngshì | xiāngsì | 似 = sì here. pypinyin default may give shì → WRONG. |
| 389 | 香肠 | tone | xiāngcháng | xiāngcháng | audit |
| 390 | 享受 | tone | xiǎngshòu | xiǎngshòu | audit |
| 391 | 想念 | tone | xiǎngniàn | xiǎngniàn | audit |
| 392 | 想象 | tone | xiǎngxiàng | xiǎngxiàng | audit |
| 393 | 项链 | tone | xiàngliàn | xiàngliàn | audit |
| 394 | 象棋 | tone | xiàngqí | xiàngqí | audit |
| 395 | 象征 | tone | xiàngzhēng | xiàngzhēng | audit |
| 396 | 消费 | tone | xiāofèi | xiāofèi | audit |
| 397 | 消化 | tone | xiāohuà | xiāohuà | audit |
| 398 | 消极 | tone | xiāojí | xiāojí | audit |
| 399 | 消失 | tone | xiāoshī | xiāoshī | audit |
| 400 | 销售 | tone | xiāoshòu | xiāoshòu | audit |
| 401 | 小麦 | tone | xiǎomài | xiǎomài | audit |
| 402 | 小气 | neutral?? | xiǎoqì | xiǎoqi | 气 sometimes light in 小气 (stingy). Flag. |
| 403 | 孝顺 | neutral tone | xiàoshùn | xiàoshun | 顺 light in 孝顺. |
| 404 | 效率 | tone | xiàolǜ | xiàolǜ | audit |
| 405 | 歇 | tone | xiē | xiē | audit |
| 406 | 斜 | tone | xié | xié | audit |
| 407 | 写作 | tone | xiězuò | xiězuò | audit |
| 408 | 血 | heteronym | xuè | xuè (formal) / xiě (colloquial) | Standalone. Both readings standard. Pick one for deck. |
| 409 | 心理 | tone | xīnlǐ | xīnlǐ | audit |
| 410 | 心脏 | tone | xīnzàng | xīnzàng | audit |
| 411 | 行动 | 行 heteronym | hángdòng | xíngdòng | 行 = xíng here. pypinyin default xíng → OK. Flag. |
| 412 | 行人 | 行 heteronym | hángrén | xíngrén | xíng. flag. |
| 413 | 行为 | 行 heteronym + 为 heteronym | hángwéi | xíngwéi | xíng + wéi. flag. |
| 414 | 形成 | tone | xíngchéng | xíngchéng | audit |
| 415 | 形势 | tone | xíngshì | xíngshì | audit |
| 416 | 幸运 | tone | xìngyùn | xìngyùn | audit |
| 417 | 兄弟 | neutral tone | xiōngdì | xiōngdi | 弟 sometimes light in 兄弟 (per Xinhua). Two senses: xiōngdì (formal "brothers"), xiōngdi (colloquial "younger brother/buddy"). Flag. |
| 418 | 胸 | tone | xiōng | xiōng | audit |
| 419 | 休闲 | tone | xiūxián | xiūxián | audit |
| 420 | 虚心 | tone | xūxīn | xūxīn | audit |
| 421 | 叙述 | tone | xùshù | xùshù | audit |
| 422 | 宣布 | tone | xuānbù | xuānbù | audit |
| 423 | 学历 | tone | xuélì | xuélì | audit |
| 424 | 学问 | neutral tone | xuéwèn | xuéwen | 问 light in 学问. |
| 425 | 寻找 | tone | xúnzhǎo | xúnzhǎo | audit |
| 426 | 询问 | tone | xúnwèn | xúnwèn | audit |
| 427 | 训练 | tone | xùnliàn | xùnliàn | audit |
| 428 | 迅速 | tone | xùnsù | xùnsù | audit |
| 429 | 押金 | tone | yājīn | yājīn | audit |
| 430 | 牙齿 | neutral?? | yáchǐ | yáchǐ | full tone standard. audit. |
| 431 | 延长 | 长 heteronym | yáncháng | yáncháng | cháng here. pypinyin default cháng → OK. Flag. |
| 432 | 严肃 | tone | yánsù | yánsù | audit |
| 433 | 演讲 | tone | yǎnjiǎng | yǎnjiǎng | audit |
| 434 | 宴会 | tone | yànhuì | yànhuì | audit |
| 435 | 阳台 | tone | yángtái | yángtái | audit |
| 436 | 痒 | tone | yǎng | yǎng | audit |
| 437 | 样式 | tone | yàngshì | yàngshì | audit |
| 438 | 腰 | tone | yāo | yāo | audit |
| 439 | 摇 | tone | yáo | yáo | audit |
| 440 | 咬 | tone | yǎo | yǎo | audit |
| 441 | 要不 | yào + 不 sandhi | yàobù | yàobù | 不 stays bù before 4th of next clause; here standalone. Flag. |
| 442 | 业务 | tone | yèwù | yèwù | audit |
| 443 | 业余 | tone | yèyú | yèyú | audit |
| 444 | 夜 | tone | yè | yè | audit |
| 445 | 一辈子 | yī sandhi + 子 neutral | yībèizi | yíbèizi | 一 + 4th tone → yí. AND 子 light. Two hazards. pypinyin → WRONG. |
| 446 | 一旦 | yī sandhi | yīdàn | yídàn | 一 + 4th → yí. WRONG by default. |
| 447 | 一律 | yī sandhi | yīlǜ | yílǜ | 一 + 4th → yí. WRONG. |
| 448 | 一再 | yī sandhi | yīzài | yīzài | 一 + 4th → yí. (Some sources keep yī when emphatic; standard yí.) WRONG by default. |
| 449 | 一致 | yī sandhi | yīzhì | yízhì | 一 + 4th → yí. WRONG. |
| 450 | 依然 | tone | yīrán | yīrán | audit |
| 451 | 移动 | tone | yídòng | yídòng | audit |
| 452 | 移民 | tone | yímín | yímín | audit |
| 453 | 遗憾 | tone | yíhàn | yíhàn | audit |
| 454 | 疑问 | tone | yíwèn | yíwèn | audit |
| 455 | 乙 | tone | yǐ | yǐ | audit |
| 456 | 以及 | tone | yǐjí | yǐjí | audit |
| 457 | 以来 | tone | yǐlái | yǐlái | audit |
| 458 | 亿 | tone | yì | yì | audit |
| 459 | 义务 | tone | yìwù | yìwù | audit |
| 460 | 议论 | 论 heteronym | yìlùn | yìlùn | lùn here. flag. |
| 461 | 意外 | tone | yìwài | yìwài | audit |
| 462 | 意义 | tone | yìyì | yìyì | audit |
| 463 | 因而 | tone | yīn'ér | yīn'ér | audit |
| 464 | 因素 | tone | yīnsù | yīnsù | audit |
| 465 | 银 | tone | yín | yín | audit |
| 466 | 印刷 | tone | yìnshuā | yìnshuā | audit |
| 467 | 英俊 | tone | yīngjùn | yīngjùn | audit |
| 468 | 英雄 | tone | yīngxióng | yīngxióng | audit |
| 469 | 迎接 | tone | yíngjiē | yíngjiē | audit |
| 470 | 营养 | tone | yíngyǎng | yíngyǎng | audit |
| 471 | 营业 | tone | yíngyè | yíngyè | audit |
| 472 | 影子 | neutral tone | yǐngzǐ | yǐngzi | 子 light. |
| 473 | 应付 | 应 heteronym | yīngfù | yìngfù | 应 = yìng (4th, "respond/cope") here, not yīng (1st, "should"). pypinyin default yīng → WRONG. |
| 474 | 应用 | 应 heteronym | yīngyòng | yìngyòng | 应 = yìng here. WRONG default. |
| 475 | 硬 | tone | yìng | yìng | audit |
| 476 | 硬件 | tone | yìngjiàn | yìngjiàn | audit |
| 477 | 拥抱 | tone | yōngbào | yōngbào | audit |
| 478 | 拥挤 | tone | yōngjǐ | yōngjǐ | audit |
| 479 | 勇气 | tone | yǒngqì | yǒngqì | audit |
| 480 | 用功 | tone | yònggōng | yònggōng | audit |
| 481 | 用途 | tone | yòngtú | yòngtú | audit |
| 482 | 优惠 | tone | yōuhuì | yōuhuì | audit |
| 483 | 悠久 | tone | yōujiǔ | yōujiǔ | audit |
| 484 | 犹豫 | tone | yóuyù | yóuyù | audit |
| 485 | 油炸 | tone | yóuzhá | yóuzhá | audit |
| 486 | 游览 | tone | yóulǎn | yóulǎn | audit |
| 487 | 有利 | tone | yǒulì | yǒulì | audit |
| 488 | 幼儿园 | tone | yòu'éryuán | yòu'éryuán | audit |
| 489 | 娱乐 | 乐 heteronym | yúlè | yúlè | lè here ("entertainment"). Default may give yuè → POTENTIALLY WRONG. |
| 490 | 与其 | tone | yǔqí | yǔqí | audit |
| 491 | 语气 | tone | yǔqì | yǔqì | audit |
| 492 | 玉米 | tone | yùmǐ | yùmǐ | audit |
| 493 | 预报 | tone | yùbào | yùbào | audit |
| 494 | 预订 | tone | yùdìng | yùdìng | audit |
| 495 | 预防 | tone | yùfáng | yùfáng | audit |
| 496 | 元旦 | tone | yuándàn | yuándàn | audit |
| 497 | 员工 | tone | yuángōng | yuángōng | audit |
| 498 | 原料 | tone | yuánliào | yuánliào | audit |
| 499 | 原则 | tone | yuánzé | yuánzé | audit |
| 500 | 圆 | tone | yuán | yuán | audit |
| 501 | 愿望 | tone | yuànwàng | yuànwàng | audit |
| 502 | 乐器 | (already flagged) | | | duplicate |
| 503 | 晕 | heteronym | yūn | yūn (faint) / yùn (motion sickness) | Standalone — sense decides. HSK 5 likely yūn (dizzy). Flag. |
| 504 | 运气 | neutral tone | yùnqì | yùnqi | 气 light in 运气. |
| 505 | 运输 | tone | yùnshū | yùnshū | audit |
| 506 | 运用 | tone | yùnyòng | yùnyòng | audit |
| 507 | 灾害 | tone | zāihài | zāihài | audit |
| 508 | 再三 | tone | zàisān | zàisān | audit |
| 509 | 在乎 | neutral tone | zàihū | zàihu | 乎 light in 在乎. |
| 510 | 在于 | tone | zàiyú | zàiyú | audit |
| 511 | 赞成 | tone | zànchéng | zànchéng | audit |
| 512 | 赞美 | tone | zànměi | zànměi | audit |
| 513 | 糟糕 | tone | zāogāo | zāogāo | audit |
| 514 | 造成 | tone | zàochéng | zàochéng | audit |
| 515 | 则 | tone | zé | zé | audit |
| 516 | 责备 | tone | zébèi | zébèi | audit |
| 517 | 摘 | tone | zhāi | zhāi | audit |
| 518 | 窄 | tone | zhǎi | zhǎi | audit |
| 519 | 粘贴 | 粘 heteronym | zhāntiē | zhāntiē | zhān. 粘 also reads nián. Default zhān → OK; flag. |
| 520 | 展开 | tone | zhǎnkāi | zhǎnkāi | audit |
| 521 | 展览 | tone | zhǎnlǎn | zhǎnlǎn | audit |
| 522 | 占 | tone | zhàn | zhàn | audit |
| 523 | 战争 | tone | zhànzhēng | zhànzhēng | audit |
| 524 | 长辈 | 长 heteronym | chángbèi | zhǎngbèi | 长 = zhǎng (elder) here. pypinyin default cháng → WRONG. |
| 525 | 涨 | heteronym | zhǎng | zhǎng (rise) / zhàng (swell) | Standalone — sense decides. HSK 5 sense usually zhǎng (price rise). Flag. |
| 526 | 掌握 | tone | zhǎngwò | zhǎngwò | audit |
| 527 | 账户 | tone | zhànghù | zhànghù | audit |
| 528 | 招待 | neutral?? | zhāodài | zhāodài | full tone standard. audit. |
| 529 | 着火 | 着 heteronym | zheguǒ / zhuóhuǒ | zháohuǒ | 着 = zháo here ("catch fire"). pypinyin default zhe (particle) or zhuó → WRONG. |
| 530 | 着凉 | 着 heteronym | zheliáng / zhuóliáng | zháoliáng | 着 = zháo here ("catch cold"). WRONG default. |
| 531 | 召开 | 召 heteronym | zhāokāi | zhàokāi | 召 = zhào (4th, "convene") here, not zhāo (1st). pypinyin default zhāo → WRONG. |
| 532 | 照常 | tone | zhàocháng | zhàocháng | audit |
| 533 | 哲学 | tone | zhéxué | zhéxué | audit |
| 534 | 针对 | tone | zhēnduì | zhēnduì | audit |
| 535 | 珍惜 | tone | zhēnxī | zhēnxī | audit |
| 536 | 真实 | tone | zhēnshí | zhēnshí | audit |
| 537 | 诊断 | tone | zhěnduàn | zhěnduàn | audit |
| 538 | 阵 | tone | zhèn | zhèn | audit |
| 539 | 振动 | tone | zhèndòng | zhèndòng | audit |
| 540 | 争论 | tone | zhēnglùn | zhēnglùn | audit |
| 541 | 争取 | tone | zhēngqǔ | zhēngqǔ | audit |
| 542 | 征求 | tone | zhēngqiú | zhēngqiú | audit |
| 543 | 睁 | tone | zhēng | zhēng | audit |
| 544 | 整个 | 个 neutral | zhěnggè | zhěnggè | full tone standard. audit. |
| 545 | 整齐 | tone | zhěngqí | zhěngqí | audit |
| 546 | 整体 | tone | zhěngtǐ | zhěngtǐ | audit |
| 547 | 正 | heteronym | zhèng | zhèng (correct) / zhēng (1st month, 正月) | Standalone usually zhèng. Flag. |
| 548 | 证件 | tone | zhèngjiàn | zhèngjiàn | audit |
| 549 | 证据 | tone | zhèngjù | zhèngjù | audit |
| 550 | 政府 | tone | zhèngfǔ | zhèngfǔ | audit |
| 551 | 政治 | tone | zhèngzhì | zhèngzhì | audit |
| 552 | 挣 | heteronym | zhēng | zhèng (earn) / zhēng (struggle, 挣扎) | Standalone — sense decides. HSK sense (earn money) → zhèng. pypinyin default zhēng → WRONG. |
| 553 | 支 | tone | zhī | zhī | audit |
| 554 | 支票 | tone | zhīpiào | zhīpiào | audit |
| 555 | 执照 | tone | zhízhào | zhízhào | audit |
| 556 | 直 | tone | zhí | zhí | audit |
| 557 | 指导 | tone | zhǐdǎo | zhǐdǎo | audit |
| 558 | 指挥 | tone | zhǐhuī | zhǐhuī | audit |
| 559 | 至今 | tone | zhìjīn | zhìjīn | audit |
| 560 | 至于 | tone | zhìyú | zhìyú | audit |
| 561 | 志愿者 | tone | zhìyuànzhě | zhìyuànzhě | audit |
| 562 | 制定 | tone | zhìdìng | zhìdìng | audit |
| 563 | 制度 | tone | zhìdù | zhìdù | audit |
| 564 | 制造 | tone | zhìzào | zhìzào | audit |
| 565 | 制作 | tone | zhìzuò | zhìzuò | audit |
| 566 | 治疗 | tone | zhìliáo | zhìliáo | audit |
| 567 | 秩序 | tone | zhìxù | zhìxù | audit |
| 568 | 智慧 | tone | zhìhuì | zhìhuì | audit |
| 569 | 中介 | tone | zhōngjiè | zhōngjiè | audit |
| 570 | 中旬 | tone | zhōngxún | zhōngxún | audit |
| 571 | 种类 | 种 heteronym | zhǒnglèi | zhǒnglèi | zhǒng (kind) here. 种 also reads zhòng (plant). Default zhǒng → OK; flag. |
| 572 | 重大 | 重 heteronym | chóngdà | zhòngdà | 重 = zhòng here. pypinyin default zhòng → OK. Flag. (NB: 重 reverse case from 重复.) |
| 573 | 重量 | 重 heteronym | chóngliàng | zhòngliàng | zhòng. flag. |
| 574 | 周到 | tone | zhōudào | zhōudào | audit |
| 575 | 猪 | tone | zhū | zhū | audit |
| 576 | 竹子 | neutral tone | zhúzǐ | zhúzi | 子 light. |
| 577 | 逐步 | tone | zhúbù | zhúbù | audit |
| 578 | 逐渐 | tone | zhújiàn | zhújiàn | audit |
| 579 | 主持 | tone | zhǔchí | zhǔchí | audit |
| 580 | 主任 | tone | zhǔrèn | zhǔrèn | audit |
| 581 | 主席 | tone | zhǔxí | zhǔxí | audit |
| 582 | 煮 | tone | zhǔ | zhǔ | audit |
| 583 | 注册 | tone | zhùcè | zhùcè | audit |
| 584 | 祝福 | tone | zhùfú | zhùfú | audit |
| 585 | 抓 | tone | zhuā | zhuā | audit |
| 586 | 抓紧 | tone | zhuājǐn | zhuājǐn | audit |
| 587 | 转变 | 转 heteronym | zhuǎnbiàn | zhuǎnbiàn | zhuǎn here. 转 also reads zhuàn (rotate). Default zhuǎn → OK; flag. |
| 588 | 转告 | 转 heteronym | zhuǎngào | zhuǎngào | zhuǎn. flag. |
| 589 | 装饰 | tone | zhuāngshì | zhuāngshì | audit |
| 590 | 装修 | tone | zhuāngxiū | zhuāngxiū | audit |
| 591 | 状况 | tone | zhuàngkuàng | zhuàngkuàng | audit |
| 592 | 状态 | tone | zhuàngtài | zhuàngtài | audit |
| 593 | 撞 | tone | zhuàng | zhuàng | audit |
| 594 | 追 | tone | zhuī | zhuī | audit |
| 595 | 追求 | tone | zhuīqiú | zhuīqiú | audit |
| 596 | 咨询 | tone | zīxún | zīxún | audit |
| 597 | 姿势 | tone | zīshì | zīshì | audit |
| 598 | 资格 | tone | zīgé | zīgé | audit |
| 599 | 资金 | tone | zījīn | zījīn | audit |
| 600 | 资料 | tone | zīliào | zīliào | audit |
| 601 | 资源 | tone | zīyuán | zīyuán | audit |
| 602 | 紫 | tone | zǐ | zǐ | audit |
| 603 | 自从 | tone | zìcóng | zìcóng | audit |
| 604 | 自动 | tone | zìdòng | zìdòng | audit |
| 605 | 自豪 | tone | zìháo | zìháo | audit |
| 606 | 自觉 | 觉 heteronym | zìjiào | zìjué | 觉 = jué here ("aware"). pypinyin default jué → OK. Flag. |
| 607 | 自私 | tone | zìsī | zìsī | audit |
| 608 | 自由 | tone | zìyóu | zìyóu | audit |
| 609 | 自愿 | tone | zìyuàn | zìyuàn | audit |
| 610 | 字母 | tone | zìmǔ | zìmǔ | audit |
| 611 | 字幕 | tone | zìmù | zìmù | audit |
| 612 | 综合 | tone | zōnghé | zōnghé | audit |
| 613 | 总裁 | tone | zǒngcái | zǒngcái | audit |
| 614 | 总共 | tone | zǒnggòng | zǒnggòng | audit |
| 615 | 总理 | tone | zǒnglǐ | zǒnglǐ | audit |
| 616 | 总算 | tone | zǒngsuàn | zǒngsuàn | audit |
| 617 | 总统 | tone | zǒngtǒng | zǒngtǒng | audit |
| 618 | 总之 | tone | zǒngzhī | zǒngzhī | audit |
| 619 | 阻止 | tone | zǔzhǐ | zǔzhǐ | audit |
| 620 | 组成 | tone | zǔchéng | zǔchéng | audit |
| 621 | 组合 | tone | zǔhé | zǔhé | audit |
| 622 | 组织 | tone | zǔzhī | zǔzhī | audit |
| 623 | 最初 | tone | zuìchū | zuìchū | audit |
| 624 | 醉 | tone | zuì | zuì | audit |
| 625 | 尊敬 | tone | zūnjìng | zūnjìng | audit |
| 626 | 遵守 | tone | zūnshǒu | zūnshǒu | audit |
| 627 | 作品 | tone | zuòpǐn | zuòpǐn | audit |
| 628 | 作为 | 为 heteronym | zuòwéi | zuòwéi | wéi (2nd) here ("as/serve as"). 为 also reads wèi (4th, "for"). Default wéi → OK; flag. |
| 629 | 作文 | tone | zuòwén | zuòwén | audit |

---

## High-confidence WRONG-by-default cases (must override)

These are the rows where pypinyin's default reading is almost certainly incorrect. These are the priority manual-overrides.

| Simplified | Correct |
|---|---|
| 曾经 | céngjīng |
| 重复 | chóngfù |
| 的确 | díquè |
| 干脆 | gāncuì |
| 干燥 | gānzào |
| 干活儿 | gànhuór (also erhua merge) |
| 怪不得 | guàibude |
| 行业 | hángyè |
| 好客 | hàokè |
| 好奇 | hàoqí |
| 系领带 | jìlǐngdài |
| 角色 | juésè |
| 桔子 | júzi |
| 会计 | kuàijì |
| 空闲 | kòngxián |
| 乐器 | yuèqì |
| 了不起 | liǎobuqǐ |
| 牛仔裤 | niúzǎikù |
| 尽快 | jǐnkuài |
| 尽量 | jǐnliàng |
| 似的 | shìde |
| 摔倒 | shuāidǎo |
| 生长 | shēngzhǎng |
| 倒霉 | dǎoméi |
| 系统 | xìtǒng |
| 相处 | xiāngchǔ |
| 相似 | xiāngsì |
| 调皮 | tiáopí |
| 调整 | tiáozhěng |
| 挑战 | tiǎozhàn |
| 讨价还价 | tǎojiàhuánjià |
| 着火 | zháohuǒ |
| 着凉 | zháoliáng |
| 召开 | zhàokāi |
| 长辈 | zhǎngbèi |
| 应付 | yìngfù |
| 应用 | yìngyòng |
| 挣 | zhèng |
| 看不起 | kànbuqǐ |
| 忍不住 | rěnbuzhù |
| 舍不得 | shěbude |
| 说不定 | shuōbudìng |
| 不得了 | bùdéliǎo |
| 一辈子 | yíbèizi |
| 一旦 | yídàn |
| 一律 | yílǜ |
| 一致 | yízhì |
| 不断 | búduàn |
| 不见得 | bújiànde |
| 不耐烦 | búnàifán |
| 不要紧 | búyàojǐn |
| 使劲儿 | shǐjìnr |
| 结实 | jiēshi |

---

## Summary by category

- **Light/neutral tone risk:** ~55 entries. Includes -子 endings (脖子, 叉子, 尺子, 影子, etc.), -头 endings (骨头, 木头, 石头, 馒头, 眉毛 wait — that's 毛), reduplicated kin terms (姑姑, 姥姥, 太太), and idiomatic neutralisations (糊涂, 老实, 大方, 老婆, 学问, 委屈, 在乎, 运气, 戒指, 道理, 兄弟, 痛快, 小气, 答应, 耽误, 佩服, 显得, 孝顺, 怪不得, 舍不得, 说不定, 看不起, 忍不住, 见得).
- **Heteronyms (多音字):** ~70 entries. Highest-risk characters: 长 (cháng/zhǎng), 行 (xíng/háng), 重 (zhòng/chóng), 着 (zháo/zhe/zhuó), 系 (xì/jì), 了 (le/liǎo), 数 (shù/shǔ), 觉 (jué/jiào), 角 (jiǎo/jué), 调 (diào/tiáo), 倒 (dǎo/dào), 应 (yīng/yìng), 好 (hǎo/hào), 干 (gān/gàn), 尽 (jǐn/jìn), 切 (qiē/qiè), 似 (sì/shì), 划 (huà/huá), 处 (chǔ/chù), 朝 (cháo/zhāo), 曾 (céng/zēng), 乐 (lè/yuè), 召 (zhāo/zhào), 挑 (tiāo/tiǎo), 挣 (zhēng/zhèng), 仔 (zǐ/zǎi), 还 (hái/huán), 当 (dāng/dàng), 卡 (kǎ/qiǎ), 扇 (shān/shàn), 模 (mó/mú), 假 (jiǎ/jià), 教 (jiāo/jiào), 结 (jié/jiē), 厦 (xià/shà), 转 (zhuǎn/zhuàn), 强 (qiáng/qiǎng/jiàng), 鲜 (xiān/xiǎn), 涨 (zhǎng/zhàng), 论 (lùn/lún), 落 (luò/là/lào), 难 (nán/nàn), 吓 (xià/hè), 圈 (quān/juàn), 晕 (yūn/yùn), 正 (zhèng/zhēng), 桔 (jú/jié), 粘 (zhān/nián), 种 (zhǒng/zhòng), 为 (wéi/wèi), 片 (piàn/piān), 血 (xuè/xiě), 吐 (tǔ/tù), 圈, 朝, 划, 系, 数, 觉, 便 (biàn/pián).
- **不 sandhi:** 12 entries (不安, 不得了, 不断, 不见得, 不耐烦, 不然, 不如, 不要紧, 不足, 看不起, 忍不住, 舍不得, 说不定, 怪不得, 要不). Of these, the ones that change to bú: 不断, 不见得, 不耐烦, 不要紧. The ones that go light (bu): 看不起, 忍不住, 舍不得, 说不定, 怪不得, 不见得 (the 不-as-V不V infix), 不得了.
- **一 sandhi:** 5 entries (一辈子, 一旦, 一律, 一再, 一致). All shift to yí before 4th tone. (Note: 统一 and 唯一 keep yī because 一 sits at the end of a fixed compound, no sandhi applied.)
- **Erhua:** 2 entries (干活儿, 使劲儿). Both require merging 儿 into the previous syllable suffix `r`.

**Approximate totals:** ~140 unique hazard rows in HSK 5 (vs ~25 in HSK 4 / 600 words). Roughly 5x the per-word hazard rate, consistent with HSK 5's heavier load of two-character heteronym compounds.

---

## Recommendation on tooling approach

Use `pypinyin` with `style=Style.TONE` as the base layer, then apply a **manual override dictionary** keyed on the Simplified word. This is the same approach HSK 4 settled on, and it scales cleanly here because:

1. The total override count (~140) is small enough to maintain by hand and review at deck-build time.
2. `pypinyin` already handles most -子/-头 light tones via its built-in neutral-tone dictionary, so the override file mostly captures heteronym disambiguation, sandhi, and edge-case neutrals.
3. A whole-word lookup keyed on the Simplified string is unambiguous and idempotent — no risk of double-applied sandhi.

Suggested structure:

```python
PINYIN_OVERRIDES = {
    "曾经": "céngjīng",
    "重复": "chóngfù",
    "的确": "díquè",
    # ... ~140 entries
}

def get_pinyin(simplified: str) -> str:
    if simplified in PINYIN_OVERRIDES:
        return PINYIN_OVERRIDES[simplified]
    return " ".join(p[0] for p in pinyin(simplified, style=Style.TONE))
```

**Why not** `pypinyin` heuristic-only (no overrides): pypinyin's word-level dictionary covers some of these (e.g., 行业 hángyè, 重复 chóngfù are in its phrase dict and will resolve correctly), but coverage is uneven and version-dependent. For a deck shipped to learners, false confidence is worse than no confidence — every wrong tone is a learner repeating the wrong sound. An override list is a one-time investment that makes the build deterministic.

**Why not** a separate engine (e.g., `xpinyin`, `cjklib`, online API): pypinyin is the most actively maintained and has the largest phrase dictionary. Switching engines just trades one set of edge cases for another. The override pattern is engine-agnostic and survives engine swaps.

**Suggested workflow:**
1. Run pypinyin over the full 1300-word list with `Style.TONE`.
2. Diff against this hazard table. Where pypinyin already matches the "Correct pinyin" column, drop the row from the override list.
3. Build the override list from whatever's left (likely 80–100 entries after pypinyin's phrase dict catches the easy ones).
4. Hand-verify the override list against Pleco / Xinhua dictionary before shipping.
5. Add a unit test that asserts every override produces its expected output — guards against silent breakage if pypinyin updates its dictionary.

**Erhua handling:** pypinyin has an `errors` callback and an erhua-aware mode (`heteronym=False, style=Style.TONE`) but does not auto-merge 儿 suffixes. The two HSK 5 erhua words (干活儿, 使劲儿) belong in the override list as full pinyin strings with the merged `r` suffix.

**1 / 不 sandhi:** pypinyin does NOT apply sandhi by default. There is no flag to enable it reliably for compounds. All 不/一 sandhi cases must be in the override list. This is the single biggest source of HSK 5 hazards numerically.
