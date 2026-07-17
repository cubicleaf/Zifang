#!/usr/bin/env python3
"""
HSK 5 deck skeleton generator (Stage 1 of the pipeline).

Reads:  data/hsk5-source-2012.txt          (1,300 simplified words, one per line)
Writes: data/hsk5-skeleton.json            (1,291 cards, mechanical fields only)
        data/hsk5-skeleton-diffs.txt       (audit: every place an override flipped a default)

Mechanical fields filled here: id, traditional, simplified, pinyin, category, depth.
Stub fields (LLM Stage 2 fills): english, pos, semanticNote, components[], examples[].

Decisions encoded:
- s2twp.json OpenCC config (Taiwan with phrases)
- 9 NUGGETS dupes dropped
- IDs 2401-3691
- Trad/pinyin override dicts from hsk5-hazard-map.md sections 9 + 4
"""
import json
import sys
from pathlib import Path
from pypinyin import pinyin, Style
import opencc

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "hsk5-source-2012.txt"
OUT = ROOT / "data" / "hsk5-skeleton.json"
DIFF_OUT = ROOT / "data" / "hsk5-skeleton-diffs.txt"

START_ID = 2401

# ---- Decision: drop these 9 (already in NUGGETS deck with same sense) -----
DROP = {"哎", "嗯", "不得了", "多余", "好奇", "进步", "夸张", "系统", "自由"}

# ---- Trad overrides: simp -> trad ----------------------------------------
# Two kinds of overrides here:
# (1) Taiwan-modern overrides where s2twp didn't swap (e.g., 桔子→橘子)
# (2) REVERTS of s2twp's over-aggressive swaps where it picked an IT-specific
#     Taiwan term over the general Taiwan term (e.g., 程序→程式 too narrow,
#     should be 程序 per Tim's locked decision)
TRAD_OVERRIDES = {
    # --- Taiwan-modern swaps s2twp DIDN'T do (we add) ---
    "数码": "數位",       # NOT 數碼
    "桔子": "橘子",       # NOT 桔子
    "冰激凌": "冰淇淋",   # NOT 冰激凌
    "报道": "報導",       # Taiwan media style, NOT 報道
    "系领带": "繫領帶",   # 繫 (tie), NOT 系
    "数据": "資料",       # Taiwan everyday "data", NOT 數據

    # --- s2twp REVERTS (it over-IT-bias-swapped these) ---
    "保存": "保存",       # NOT 儲存 (儲存 is computer-only "save"; 保存 is general)
    "程序": "程序",       # NOT 程式 (per Tim locked decision; semanticNote notes 程式)
    "文件": "文件",       # NOT 檔案 (per Tim locked decision; semanticNote notes 檔案)
    "高级": "高級",       # NOT 高階 (高級 is Taiwan everyday "advanced/senior"; 高階 = "high-rank")
    "对象": "對象",       # NOT 物件 (對象 is "target/dating partner"; 物件 is IT "object")
    "类型": "類型",       # NOT 型別 (類型 is general "type"; 型別 is programming-only)
    "项目": "項目",       # NOT 專案 (項目 is general "items/projects"; 專案 is "case/project file")
    "设备": "設備",       # NOT 裝置 (設備 is "equipment"; 裝置 is "device/installation")
    "粘贴": "黏貼",       # NOT 貼上 (貼上 is verb-only "paste up"; 黏貼 is Taiwan trad of 粘貼)
}

# ---- Pinyin overrides: simp -> correct pinyin -----------------------------
# Built from Scout C high-confidence list + locked HSK 4 precedents.
# Tones: 1=ā 2=á 3=ǎ 4=à neutral=no diacritic.
PINYIN_OVERRIDES = {
    # High-confidence wrong-by-default (Scout C)
    "曾经": "céngjīng",
    "重复": "chóngfù",
    "的确": "díquè",
    "干脆": "gāncuì",
    "干燥": "gānzào",
    "干活儿": "gànhuór",
    "怪不得": "guàibude",
    "行业": "hángyè",
    "好客": "hàokè",
    "好奇": "hàoqí",
    "系领带": "jìlǐngdài",
    "角色": "juésè",
    "桔子": "júzi",
    "会计": "kuàijì",
    "空闲": "kòngxián",
    "乐器": "yuèqì",
    "了不起": "liǎobuqǐ",
    "牛仔裤": "niúzǎikù",
    "尽快": "jǐnkuài",
    "尽量": "jǐnliàng",
    "似的": "shìde",
    "摔倒": "shuāidǎo",
    "生长": "shēngzhǎng",
    "倒霉": "dǎoméi",
    "系统": "xìtǒng",
    "相处": "xiāngchǔ",
    "相似": "xiāngsì",
    "调皮": "tiáopí",
    "调整": "tiáozhěng",
    "挑战": "tiǎozhàn",
    "讨价还价": "tǎojiàhuánjià",
    "着火": "zháohuǒ",
    "着凉": "zháoliáng",
    "召开": "zhàokāi",
    "长辈": "zhǎngbèi",
    "应付": "yìngfù",
    "应用": "yìngyòng",
    "挣": "zhèng",
    "看不起": "kànbuqǐ",
    "忍不住": "rěnbuzhù",
    "舍不得": "shěbude",
    "说不定": "shuōbudìng",
    "不得了": "bùdéliǎo",  # for completeness if undropped
    "一辈子": "yíbèizi",
    "一旦": "yídàn",
    "一律": "yílǜ",
    "一致": "yízhì",
    "一再": "yízài",
    "不断": "búduàn",
    "不见得": "bújiànde",
    "不耐烦": "búnàifán",
    "不要紧": "búyàojǐn",
    "使劲儿": "shǐjìnr",
    "结实": "jiēshi",
    # 长 split per word
    "长城": "Chángchéng",
    "长江": "Chángjiāng",
    "长途": "chángtú",
    "长辈": "zhǎngbèi",
    # 行 split
    "行业": "hángyè",
    "行人": "xíngrén",
    "行为": "xíngwéi",
    "行动": "xíngdòng",
    # 重 split
    "重大": "zhòngdà",
    "重量": "zhòngliàng",
    # 数 — standalone shù
    "数": "shù",
    # 数据 → trad 資料 → pinyin zīliào
    "数据": "zīliào",
    # 数码 → trad 數位 → pinyin shùwèi
    "数码": "shùwèi",
    # 朝 standalone
    "朝": "cháo",
    # 觉 split
    "自觉": "zìjué",
    # 角 split
    "角度": "jiǎodù",
    # 处 split
    "相处": "xiāngchǔ",
    # 划 — Hanban gloss is "to plan / paddle" — needs Tim's gloss decision; defaulting to huà (plan, more common HSK 5 sense)
    "划": "huà",
    # 厦 split
    "大厦": "dàshà",
    # 答应 light
    "答应": "dāying",
    # 道理 — keep full tone (dictionary standard)
    # neutral-tone words pypinyin may miss
    "玻璃": "bōli",
    "脖子": "bózi",
    "大方": "dàfang",
    "耽误": "dānwu",
    "糊涂": "hútu",
    "学问": "xuéwen",
    "在乎": "zàihu",
    "委屈": "wěiqu",
    "运气": "yùnqi",
    "戒指": "jièzhi",
    "兄弟": "xiōngdi",
    "痛快": "tòngkuai",
    "小气": "xiǎoqi",
    "佩服": "pèifu",
    "孝顺": "xiàoshùn",  # actually 顺 stays full per most dicts; verify
    "显得": "xiǎnde",
    "老实": "lǎoshi",
    "老婆": "lǎopo",
    "称呼": "chēnghu",
    # 血 — formal standard (HSK 4 precedent)
    "血": "xuè",
    # 似 standalone in 似乎/似的 — note 似乎 is sì, 似的 is shì
    "似乎": "sìhū",
    # 处理 — chǔlǐ (manage, process)
    "处理": "chǔlǐ",
    # 看望 — kànwàng
    # 颗 — kē
    # 鞭炮 — biānpào
    # 标点 — biāodiǎn
    # 标志 — biāozhì
    # 表达 — biǎodá
    # 病毒 — bìngdú
    # 玻璃 — bōli (already)
    # 不安 — bù'ān (no sandhi, audit only)
    "不安": "bù'ān",
    "不然": "bùrán",
    "不如": "bùrú",
    "不足": "bùzú",
    # 出色 — chūsè
    # 处女 — not in list
    # 充电器 — chōngdiànqì
    # 床帘 — not in list
    # 朝 in compounds
    # 称 standalone — chēng (call) — HSK 5 likely "to call/weigh"
    "称": "chēng",
    "称呼": "chēnghu",
    "称赞": "chēngzàn",
    # 沉默 — chénmò
    # 趁 — chèn
    # 重 standalone — heavy = zhòng (HSK 5 sense)
    # 出 standalone (not entry)
    # 厨房 — not entry
    # 处 standalone — chǔ (manage) or chù (place)
    # 春 — not standalone
    # 串 — not in list
    # 闯 — chuǎng
    # 创造 — chuàngzào
    # 吹 — chuī
    # 词汇 — cíhuì
    # 辞职 — cízhí
    # 此外 — cǐwài
    # 次要 — cìyào
    # 刺激 — cìjī
    # 匆忙 — cōngmáng
    # 从此 — cóngcǐ
    # 从而 — cóng'ér
    # 从前 — cóngqián
    # 从事 — cóngshì
    # 粗糙 — cūcāo
    # 促进 — cùjìn
    # 促使 — cùshǐ
    # 醋 — cù
    # 催 — cuī
    # 存在 — cúnzài
    # 措施 — cuòshī
    # 答应 (handled)
    # 达到 — dádào
    # 打工 — dǎgōng
    # 打交道 — dǎjiāodào
    # 打喷嚏 — dǎpēntì
    # 打听 — dǎtīng
    # 大方 (handled)
    # 大厦 (handled)
    # 大象 — dàxiàng
    # 大型 — dàxíng
    # 呆 — dāi
    # 代表 — dàibiǎo
    # 代替 — dàitì
    # 贷款 — dàikuǎn
    # 待遇 — dàiyù
    # 担任 — dānrèn
    # 单纯 — dānchún
    # 单调 — dāndiào
    # 单独 — dāndú
    # 单位 — dānwèi
    # 单元 — dānyuán
    # 耽误 (handled)
    # 胆小鬼 — dǎnxiǎoguǐ
    # 淡 — dàn
    # 当地 — dāngdì
    # 当心 — dāngxīn
    # 挡 — dǎng
    # 导演 — dǎoyǎn
    # 导致 — dǎozhì
    # 岛屿 — dǎoyǔ
    # 倒霉 (handled)
    # 道德 — dàodé
    # 道理 — dàolǐ
    # 登记 — dēngjì
    # 等待 — děngdài
    # 等于 — děngyú
    # 滴 — dī
    # 的确 (handled)
    # 敌人 — dírén
    # 地道 — depends on sense; keep full tone dìdào (tunnel) by default
    # 地理 — dìlǐ
    # 地区 — dìqū
    # 地毯 — dìtǎn
    # 地位 — dìwèi
    # 地震 — dìzhèn
    # 递 — dì
    # 点心 — diǎnxin
    "点心": "diǎnxin",
    # 电池 — diànchí
    # 电台 — diàntái
    # 钓 — diào
    # 顶 — dǐng
    # 动画片 — dònghuàpiàn
    # 冻 — dòng
    # 洞 — dòng
    # 豆腐 — dòufu
    "豆腐": "dòufu",
    # 逗 — dòu
    # 独立 — dúlì
    # 独特 — dútè
    # 度过 — dùguò
    # 断 — duàn
    # 堆 — duī
    # 对比 — duìbǐ
    # 对待 — duìdài
    # 对方 — duìfāng
    # 对手 — duìshǒu
    # 对象 — duìxiàng
    # 兑换 — duìhuàn
    # 吨 — dūn
    # 蹲 — dūn
    # 顿 — dùn
    # 多亏 — duōkuī
    # 多余 (dropped)
    # 朵 — duǒ
    # 躲藏 — duǒcáng
    # 恶劣 — èliè
    # 耳环 — ěrhuán
    # 发言 — fāyán
    # 罚款 — fákuǎn
    # 法院 — fǎyuàn
    # 翻 — fān
    # 繁荣 — fánróng
    # 反而 — fǎn'ér
    # 反复 — fǎnfù
    # 反应 — fǎnyìng
    # 反映 — fǎnyìng
    # 反正 — fǎnzhèng
    # 范围 — fànwéi
    # 方 — fāng
    # 方案 — fāng'àn
    # 方式 — fāngshì
    # 妨碍 — fáng'ài
    # 仿佛 — fǎngfú
    # 非 — fēi
    # 肥皂 — féizào
    # 废话 — fèihuà
    # 分别 — fēnbié
    # 分布 — fēnbù
    # 分配 — fēnpèi
    # 分手 — fēnshǒu
    # 分析 — fēnxī
    # 纷纷 — fēnfēn
    # 奋斗 — fèndòu
    # 风格 — fēnggé
    # 风景 — fēngjǐng
    # 风俗 — fēngsú
    # 风险 — fēngxiǎn
    # 疯狂 — fēngkuáng
    # 讽刺 — fěngcì
    # 否定 — fǒudìng
    # 否认 — fǒurèn
    # 扶 — fú
    # 服装 — fúzhuāng
    # 幅 — fú
    # 辅导 — fǔdǎo
    # 妇女 — fùnǚ
    # 复制 — fùzhì
    # 改革 — gǎigé
    # 改进 — gǎijìn
    # 改善 — gǎishàn
    # 改正 — gǎizhèng
    # 盖 — gài
    # 概括 — gàikuò
    # 概念 — gàiniàn
    # 干脆 (handled)
    # 干燥 (handled)
    # 赶紧 — gǎnjǐn
    # 赶快 — gǎnkuài
    # 感激 — gǎnjī
    # 感受 — gǎnshòu
    # 感想 — gǎnxiǎng
    # 干活儿 (handled)
    # 钢铁 — gāngtiě
    # 高档 — gāodàng
    # 高级 — gāojí
    # 搞 — gǎo
    # 告别 — gàobié
    # 格外 — géwài
    # 隔壁 — gébì
    # 个别 — gèbié
    # 个人 — gèrén
    # 个性 — gèxìng
    # 各自 — gèzì
    # 根 — gēn
    # 根本 — gēnběn
    # 工厂 — gōngchǎng
    # 工程师 — gōngchéngshī
    # 工具 — gōngjù
    # 工人 — gōngrén
    # 工业 — gōngyè
    # 公布 — gōngbù
    # 公开 — gōngkāi
    # 公平 — gōngpíng
    # 公寓 — gōngyù
    # 公元 — gōngyuán
    # 公主 — gōngzhǔ
    # 功能 — gōngnéng
    # 恭喜 — gōngxǐ
    # 贡献 — gòngxiàn
    # 沟通 — gōutōng
    # 构成 — gòuchéng
    # 姑姑 — gūgu
    "姑姑": "gūgu",
    # 姑娘 — gūniang
    "姑娘": "gūniang",
    # 古代 — gǔdài
    # 古典 — gǔdiǎn
    # 股票 — gǔpiào
    # 骨头 — gǔtou
    "骨头": "gǔtou",
    # 鼓舞 — gǔwǔ
    # 鼓掌 — gǔzhǎng
    # 固定 — gùdìng
    # 挂号 — guàhào
    # 乖 — guāi
    # 拐弯 — guǎiwān
    # 怪不得 (handled)
    # 关闭 — guānbì
    # 观察 — guānchá
    # 观点 — guāndiǎn
    # 观念 — guānniàn
    # 官 — guān
    # 管子 — guǎnzi
    "管子": "guǎnzi",
    # 冠军 — guànjūn
    # 光滑 — guānghuá
    # 光临 — guānglín
    # 光明 — guāngmíng
    # 光盘 — guāngpán → trad 光碟; pinyin guāngdié for Taiwan; HSK Hanban form pinyin = guāngpán
    # 广场 — guǎngchǎng
    # 广大 — guǎngdà
    # 广泛 — guǎngfàn
    # 归纳 — guīnà
    # 规矩 — guījǔ → actually guīju (light tone)
    "规矩": "guīju",
    # 规律 — guīlǜ
    # 规模 — guīmó
    # 规则 — guīzé
    # 柜台 — guìtái
    # 滚 — gǔn
    # 锅 — guō
    # 国庆节 — guóqìngjié
    # 国王 — guówáng
    # 果然 — guǒrán
    # 果实 — guǒshí
    # 过分 — guòfèn
    # 过敏 — guòmǐn
    # 过期 — guòqī
    # 哈 — hā
    # 海关 — hǎiguān
    # 海鲜 — hǎixiān
    # 喊 — hǎn
    # 行业 (handled)
    # 豪华 — háohuá
    # 好客 (handled)
    # 好奇 (handled)
    # 合法 — héfǎ
    # 合理 — hélǐ
    # 合同 — hétong
    "合同": "hétong",
    # 合影 — héyǐng
    # 合作 — hézuò
    # 何必 — hébì
    # 何况 — hékuàng
    # 和平 — hépíng
    # 核心 — héxīn
    # 恨 — hèn
    # 猴子 — hóuzi
    "猴子": "hóuzi",
    # 后背 — hòubèi
    # 后果 — hòuguǒ
    # 呼吸 — hūxī
    # 忽然 — hūrán
    # 忽视 — hūshì
    # 胡说 — húshuō
    # 胡同 — hútòng
    "胡同": "hútòng",
    # 壶 — hú
    # 蝴蝶 — húdié
    # 糊涂 (handled)
    # 花生 — huāshēng
    # 划 (handled)
    # 华裔 — huáyì
    # 滑 — huá
    # 化学 — huàxué
    # 话题 — huàtí
    # 怀念 — huáiniàn
    # 怀孕 — huáiyùn
    # 缓解 — huǎnjiě
    # 幻想 — huànxiǎng
    # 慌张 — huāngzhāng
    # 黄金 — huángjīn
    # 灰 — huī
    # 灰尘 — huīchén
    # 灰心 — huīxīn
    # 挥 — huī
    # 恢复 — huīfù
    # 汇率 — huìlǜ
    # 婚礼 — hūnlǐ
    # 婚姻 — hūnyīn
    # 活跃 — huóyuè
    # 火柴 — huǒchái
    # 伙伴 — huǒbàn
    # 或许 — huòxǔ
    # 机器 — jīqì
    # 肌肉 — jīròu
    # 基本 — jīběn
    # 激烈 — jīliè
    # 及格 — jígé
    # 极其 — jíqí
    # 急忙 — jímáng
    # 急诊 — jízhěn
    # 集合 — jíhé
    # 集体 — jítǐ
    # 集中 — jízhōng
    # 计算 — jìsuàn
    # 记录 — jìlù
    # 记忆 — jìyì
    # 纪录 — jìlù
    # 纪律 — jìlǜ
    # 纪念 — jìniàn
    # 系领带 (handled)
    # 寂寞 — jìmò
    # 夹子 — jiāzi
    "夹子": "jiāzi",
    # 家庭 — jiātíng
    # 家务 — jiāwù
    # 家乡 — jiāxiāng
    # 嘉宾 — jiābīn
    # 甲 — jiǎ
    # 假如 — jiǎrú
    # 假设 — jiǎshè
    # 假装 — jiǎzhuāng
    # 价值 — jiàzhí
    # 驾驶 — jiàshǐ
    # 嫁 — jià
    # 坚决 — jiānjué
    # 坚强 — jiānqiáng
    # 肩膀 — jiānbǎng
    # 艰巨 — jiānjù
    # 艰苦 — jiānkǔ
    # 兼职 — jiānzhí
    # 捡 — jiǎn
    # 剪刀 — jiǎndāo
    # 简历 — jiǎnlì
    # 简直 — jiǎnzhí
    # 建立 — jiànlì
    # 建设 — jiànshè
    # 建筑 — jiànzhù
    # 健身 — jiànshēn
    # 键盘 — jiànpán
    # 讲究 — jiǎngjiu  (light tone)
    "讲究": "jiǎngjiu",
    # 讲座 — jiǎngzuò
    # 酱油 — jiàngyóu
    # 交换 — jiāohuàn
    # 交际 — jiāojì
    # 交往 — jiāowǎng
    # 浇 — jiāo
    # 胶水 — jiāoshuǐ
    # 角度 (handled)
    # 狡猾 — jiǎohuá
    # 教材 — jiàocái
    # 教练 — jiàoliàn
    # 教训 — jiàoxun  (light second syllable)
    "教训": "jiàoxun",
    # 阶段 — jiēduàn
    # 结实 (handled)
    # 接触 — jiēchù
    # 接待 — jiēdài
    # 接近 — jiējìn
    # 节省 — jiéshěng
    # 结构 — jiégòu
    # 结合 — jiéhé
    # 结论 — jiélùn
    # 结账 — jiézhàng
    # 戒 — jiè
    # 戒指 — jièzhi  (handled)
    # 届 — jiè
    # 借口 — jièkǒu
    # 金属 — jīnshǔ
    # 尽快 (handled)
    # 尽量 (handled)
    # 紧急 — jǐnjí
    # 谨慎 — jǐnshèn
    # 尽力 — jìnlì
    "尽力": "jìnlì",
    # 进步 (dropped)
    # 进口 — jìnkǒu
    # 近代 — jìndài
    # 经典 — jīngdiǎn
    # 经商 — jīngshāng
    # 经营 — jīngyíng
    # 精力 — jīnglì
    # 精神 — jīngshén  (also jīngshen depending on sense)
    # 酒吧 — jiǔbā
    # 救 — jiù
    # 救护车 — jiùhùchē
    # 舅舅 — jiùjiu  (light)
    "舅舅": "jiùjiu",
    # 居然 — jūrán
    # 桔子 (handled)
    # 巨大 — jùdà
    # 具备 — jùbèi
    # 具体 — jùtǐ
    # 俱乐部 — jùlèbù
    # 据说 — jùshuō
    # 捐 — juān
    # 决赛 — juésài
    # 决心 — juéxīn
    # 角色 (handled)
    # 绝对 — juéduì
    # 军事 — jūnshì
    # 均匀 — jūnyún
    # 卡车 — kǎchē
    # 开发 — kāifā
    # 开放 — kāifàng
    # 开幕式 — kāimùshì
    # 开水 — kāishuǐ
    # 砍 — kǎn
    # 看不起 (handled)
    # 看望 — kànwàng
    # 靠 — kào
    # 颗 — kē
    # 可见 — kějiàn
    # 可靠 — kěkào
    # 可怕 — kěpà
    # 克 — kè
    # 克服 — kèfú
    # 刻苦 — kèkǔ
    # 客观 — kèguān
    # 课程 — kèchéng
    # 空间 — kōngjiān
    # 空闲 (handled)
    # 控制 — kòngzhì
    # 口味 — kǒuwèi
    # 夸 — kuā
    # 夸张 (dropped)
    # 会计 (handled)
    # 宽 — kuān
    # 昆虫 — kūnchóng
    # 扩大 — kuòdà
    # 辣椒 — làjiāo
    # 拦 — lán
    # 烂 — làn
    # 朗读 — lǎngdú
    # 劳动 — láodòng
    # 劳驾 — láojià
    # 老百姓 — lǎobǎixìng
    # 老板 — lǎobǎn
    # 老婆 (handled)
    # 老实 (handled)
    # 老鼠 — lǎoshǔ
    # 姥姥 — lǎolao  (light)
    "姥姥": "lǎolao",
    # 乐观 — lèguān
    # 雷 — léi
    # 类型 — lèixíng
    # 冷淡 — lěngdàn
    # 厘米 — límǐ
    # 离婚 — líhūn
    # 梨 — lí
    # 理论 — lǐlùn
    # 理由 — lǐyóu
    # 力量 — lìliàng
    # 立即 — lìjí
    # 立刻 — lìkè
    # 利润 — lìrùn
    # 利息 — lìxī
    # 利益 — lìyì
    # 利用 — lìyòng
    # 连忙 — liánmáng
    # 连续 — liánxù
    # 联合 — liánhé
    # 恋爱 — liàn'ài
    # 良好 — liánghǎo
    # 粮食 — liángshi  (light)
    "粮食": "liángshi",
    # 亮 — liàng
    # 了不起 (handled)
    # 列车 — lièchē
    # 临时 — línshí
    # 灵活 — línghuó
    # 铃 — líng
    # 零件 — língjiàn
    # 零食 — língshí
    # 领导 — lǐngdǎo
    # 领域 — lǐngyù
    # 浏览 — liúlǎn
    # 流传 — liúchuán
    # 流泪 — liúlèi
    # 龙 — lóng
    # 漏 — lòu
    # 陆地 — lùdì
    # 陆续 — lùxù
    # 录取 — lùqǔ
    # 录音 — lùyīn
    # 轮流 — lúnliú
    # 论文 — lùnwén
    # 逻辑 — luójí
    # 落后 — luòhòu
    # 骂 — mà
    # 麦克风 — màikèfēng
    # 馒头 — mántou  (light)
    "馒头": "mántou",
    # 满足 — mǎnzú
    # 毛病 — máobìng
    # 矛盾 — máodùn
    # 冒险 — màoxiǎn
    # 贸易 — màoyì
    # 眉毛 — méimao  (light)
    "眉毛": "méimao",
    # 媒体 — méitǐ
    # 煤炭 — méitàn
    # 美术 — měishù
    # 魅力 — mèilì
    # 梦想 — mèngxiǎng
    # 秘密 — mìmì
    # 秘书 — mìshū
    # 密切 — mìqiè
    # 蜜蜂 — mìfēng
    # 面对 — miànduì
    # 面积 — miànjī
    # 面临 — miànlín
    # 苗条 — miáotiao
    "苗条": "miáotiao",
    # 描写 — miáoxiě
    # 敏感 — mǐngǎn
    # 名牌 — míngpái
    # 名片 — míngpiàn
    # 名胜古迹 — míngshènggǔjì
    # 明确 — míngquè
    # 明显 — míngxiǎn
    # 明星 — míngxīng
    # 命令 — mìnglìng
    # 命运 — mìngyùn
    # 摸 — mō
    # 模仿 — mófǎng
    # 模糊 — móhu
    "模糊": "móhu",
    # 模特 — mótè
    # 摩托车 — mótuōchē
    # 陌生 — mòshēng
    # 某 — mǒu
    # 木头 — mùtou
    "木头": "mùtou",
    # 目标 — mùbiāo
    # 目录 — mùlù
    # 目前 — mùqián
    # 哪怕 — nǎpà
    # 难怪 — nánguài
    # 难免 — nánmiǎn
    # 脑袋 — nǎodai
    "脑袋": "nǎodai",
    # 内部 — nèibù
    # 内科 — nèikē
    # 嫩 — nèn
    # 能干 — nénggàn
    # 能源 — néngyuán
    # 嗯 (dropped)
    # 年代 — niándài
    # 年纪 — niánjì
    # 念 — niàn
    # 宁可 — nìngkě
    # 牛仔裤 (handled)
    # 农村 — nóngcūn
    # 农民 — nóngmín
    # 农业 — nóngyè
    # 浓 — nóng
    # 女士 — nǚshì
    # 欧洲 — Ōuzhōu
    # 偶然 — ǒurán
    # 拍 — pāi
    # 派 — pài
    # 盼望 — pànwàng
    # 培训 — péixùn
    # 培养 — péiyǎng
    # 赔偿 — péicháng
    # 佩服 (handled)
    # 配合 — pèihé
    # 盆 — pén
    # 碰 — pèng
    # 批 — pī
    # 批准 — pīzhǔn
    # 披 — pī
    # 疲劳 — píláo
    # 匹 — pǐ
    # 片 — piàn
    # 片面 — piànmiàn
    # 飘 — piāo
    # 拼音 — pīnyīn
    # 频道 — píndào
    # 平 — píng
    # 平安 — píng'ān
    # 平常 — píngcháng
    # 平等 — píngděng
    # 平方 — píngfāng
    # 平衡 — pínghéng
    # 平静 — píngjìng
    # 平均 — píngjūn
    # 评价 — píngjià
    # 凭 — píng
    # 迫切 — pòqiè
    # 破产 — pòchǎn
    # 破坏 — pòhuài
    # 期待 — qīdài
    # 期间 — qījiān
    # 其余 — qíyú
    # 奇迹 — qíjì
    # 企业 — qǐyè  (HSK 4 mainland-pinyin precedent locked)
    "企业": "qǐyè",
    # 启发 — qǐfā
    # 气氛 — qìfēn
    # 汽油 — qìyóu
    # 谦虚 — qiānxū
    # 签 — qiān
    # 前途 — qiántú
    # 浅 — qiǎn
    # 欠 — qiàn
    # 枪 — qiāng
    # 强调 — qiángdiào
    # 强烈 — qiángliè
    # 墙 — qiáng
    # 抢 — qiǎng
    # 悄悄 — qiāoqiāo
    # 瞧 — qiáo
    # 巧妙 — qiǎomiào
    # 切 — qiē  (HSK 5 standalone usually qiē "to cut")
    "切": "qiē",
    # 亲爱 — qīn'ài
    # 亲切 — qīnqiè
    # 亲自 — qīnzì
    # 勤奋 — qínfèn
    # 青 — qīng
    # 青春 — qīngchūn
    # 青少年 — qīngshàonián
    # 轻视 — qīngshì
    # 轻易 — qīngyì
    # 清淡 — qīngdàn
    # 情景 — qíngjǐng
    # 情绪 — qíngxù
    # 请求 — qǐngqiú
    # 庆祝 — qìngzhù
    # 球迷 — qiúmí
    # 趋势 — qūshì
    # 取消 — qǔxiāo
    # 娶 — qǔ
    # 去世 — qùshì
    # 圈 — quān
    # 权力 — quánlì
    # 权利 — quánlì
    # 全面 — quánmiàn
    # 劝 — quàn
    # 缺乏 — quēfá
    # 确定 — quèdìng
    # 确认 — quèrèn
    # 群 — qún
    # 燃烧 — ránshāo
    # 绕 — rào
    # 热爱 — rè'ài
    # 热烈 — rèliè
    # 热心 — rèxīn
    # 人才 — réncái
    # 人口 — rénkǒu
    # 人类 — rénlèi
    # 人民币 — rénmínbì
    # 人生 — rénshēng
    # 人事 — rénshì
    # 人物 — rénwù
    # 人员 — rényuán
    # 忍不住 (handled)
    # 日常 — rìcháng
    # 日程 — rìchéng
    # 日历 — rìlì
    # 日期 — rìqī
    # 日用品 — rìyòngpǐn
    # 日子 — rìzi
    "日子": "rìzi",
    # 如何 — rúhé
    # 如今 — rújīn
    # 软 — ruǎn
    # 软件 — trad is 軟體, so pinyin must match: ruǎntǐ (体/體 = tǐ)
    "软件": "ruǎntǐ",
    # 弱 — ruò
    # 洒 — sǎ
    # 嗓子 — sǎngzi
    "嗓子": "sǎngzi",
    # 色彩 — sècǎi
    # 杀 — shā
    # 沙漠 — shāmò
    # 沙滩 — shātān
    # 傻 — shǎ
    # 晒 — shài
    # 删除 — shānchú
    # 闪电 — shǎndiàn
    # 扇子 — shànzi
    "扇子": "shànzi",
    # 善良 — shànliáng
    # 善于 — shànyú
    # 伤害 — shānghài
    # 商品 — shāngpǐn
    # 商务 — shāngwù
    # 商业 — shāngyè
    # 上当 — shàngdàng
    # 蛇 — shé
    # 舍不得 (handled)
    # 设备 — shèbèi
    # 设计 — shèjì
    # 设施 — shèshī
    # 射击 — shèjī
    # 摄影 — shèyǐng
    # 伸 — shēn
    # 身材 — shēncái
    # 身份 — shēnfèn
    "身份": "shēnfèn",
    # 深刻 — shēnkè
    # 神话 — shénhuà
    # 神秘 — shénmì
    # 升 — shēng
    # 生产 — shēngchǎn
    # 生动 — shēngdòng
    # 生长 (handled)
    # 声调 — shēngdiào
    # 绳子 — shéngzi
    "绳子": "shéngzi",
    # 省略 — shěnglüè
    # 胜利 — shènglì
    # 失眠 — shīmián
    # 失去 — shīqù
    # 失业 — shīyè
    # 诗 — shī
    # 狮子 — shīzi
    "狮子": "shīzi",
    # 湿润 — shīrùn
    # 石头 — shítou
    "石头": "shítou",
    # 时差 — shíchā
    # 时代 — shídài
    # 时刻 — shíkè
    # 时髦 — shímáo
    # 时期 — shíqī
    # 时尚 — shíshàng
    # 实话 — shíhuà
    # 实践 — shíjiàn
    # 实习 — shíxí
    # 实现 — shíxiàn
    # 实验 — shíyàn
    # 实用 — shíyòng
    # 食物 — shíwù
    # 使劲儿 (handled)
    # 始终 — shǐzhōng
    # 士兵 — shìbīng
    # 市场 — shìchǎng
    # 似的 (handled)
    # 事实 — shìshí
    # 事物 — shìwù
    # 事先 — shìxiān
    # 试卷 — shìjuàn
    # 收获 — shōuhuò
    # 收据 — shōujù
    # 手工 — shǒugōng
    # 手术 — shǒushù
    # 手套 — shǒutào
    # 手续 — shǒuxù
    # 手指 — shǒuzhǐ
    # 首 — shǒu
    # 寿命 — shòumìng
    # 受伤 — shòushāng
    # 书架 — shūjià
    # 梳子 — shūzi
    "梳子": "shūzi",
    # 舒适 — shūshì
    # 输入 — shūrù
    # 蔬菜 — shūcài
    # 熟练 — shúliàn
    # 属于 — shǔyú
    # 鼠标 — trad is 滑鼠, so pinyin must match: huáshǔ
    "鼠标": "huáshǔ",
    # 数 — shù (HSK 5 standalone "number")
    # 数据 (handled trad; pinyin = shùjù)
    # 数码 (handled)
    # 摔倒 (handled)
    # 甩 — shuǎi
    # 双方 — shuāngfāng
    # 税 — shuì
    # 说不定 (handled)
    # 说服 — shuōfú
    # 丝绸 — sīchóu
    # 丝毫 — sīháo
    # 私人 — sīrén
    # 思考 — sīkǎo
    # 思想 — sīxiǎng
    # 撕 — sī
    # 似乎 (handled)
    # 搜索 — sōusuǒ
    # 宿舍 — sùshè
    # 随身 — suíshēn
    # 随时 — suíshí
    # 随手 — suíshǒu
    # 碎 — suì
    # 损失 — sǔnshī
    # 缩短 — suōduǎn
    # 所 — suǒ
    # 锁 — suǒ
    # 台阶 — táijiē
    # 太极拳 — tàijíquán
    # 太太 — tàitai
    "太太": "tàitai",
    # 谈判 — tánpàn
    # 坦率 — tǎnshuài
    # 烫 — tàng
    # 逃 — táo
    # 逃避 — táobì
    # 桃 — táo
    # 淘气 — táoqi
    "淘气": "táoqi",
    # 讨价还价 (handled)
    # 套 — tào
    # 特色 — tèsè
    # 特殊 — tèshū
    # 特征 — tèzhēng
    # 疼爱 — téng'ài
    # 提倡 — tíchàng
    # 提纲 — tígāng
    # 提问 — tíwèn
    # 题目 — tímù
    # 体会 — tǐhuì
    # 体贴 — tǐtiē
    # 体现 — tǐxiàn
    # 体验 — tǐyàn
    # 天空 — tiānkōng
    # 天真 — tiānzhēn
    # 调皮 (handled)
    # 调整 (handled)
    # 挑战 (handled)
    # 通常 — tōngcháng
    # 统一 — tǒngyī
    # 痛苦 — tòngkǔ
    # 痛快 (handled)
    # 偷 — tōu
    # 投入 — tóurù
    # 投资 — tóuzī
    # 透明 — tòumíng
    # 突出 — tūchū
    # 土地 — tǔdì
    # 土豆 — tǔdòu
    # 吐 — tǔ
    # 兔子 — tùzi
    "兔子": "tùzi",
    # 团 — tuán
    # 推辞 — tuīcí
    # 推广 — tuīguǎng
    # 推荐 — tuījiàn
    # 退 — tuì
    # 退步 — tuìbù
    # 退休 — tuìxiū
    # 歪 — wāi
    # 外公 — wàigōng
    # 外交 — wàijiāo
    # 完美 — wánměi
    # 完善 — wánshàn
    # 完整 — wánzhěng
    # 玩具 — wánjù
    # 万一 — wànyī
    # 王子 — wángzǐ
    # 网络 — trad is 網路, so pinyin = wǎnglù (路 = lù)
    "网络": "wǎnglù",
    # 往返 — wǎngfǎn
    # 危害 — wēihài
    # 威胁 — wēixié
    # 微笑 — wēixiào
    # 违反 — wéifǎn
    # 围巾 — wéijīn
    # 围绕 — wéirào
    # 唯一 — wéiyī
    # 维修 — wéixiū
    # 伟大 — wěidà
    # 尾巴 — wěiba
    "尾巴": "wěiba",
    # 委屈 (handled)
    # 未必 — wèibì
    # 未来 — wèilái
    # 位于 — wèiyú
    # 位置 — wèizhi
    "位置": "wèizhi",
    # 胃 — wèi
    # 胃口 — wèikǒu
    # 温暖 — wēnnuǎn
    # 温柔 — wēnróu
    # 文件 — wénjiàn
    # 文具 — wénjù
    # 文明 — wénmíng
    # 文学 — wénxué
    # 文字 — wénzì
    # 闻 — wén
    # 吻 — wěn
    # 稳定 — wěndìng
    # 问候 — wènhòu
    # 卧室 — wòshì
    # 握手 — wòshǒu
    # 屋子 — wūzi
    "屋子": "wūzi",
    # 无奈 — wúnài
    # 无数 — wúshù
    # 无所谓 — wúsuǒwèi
    # 武术 — wǔshù
    # 勿 — wù
    # 物理 — wùlǐ
    # 物质 — wùzhì  (HSK 4 zhì precedent)
    # 雾 — wù
    # 吸取 — xīqǔ
    # 吸收 — xīshōu
    # 戏剧 — xìjù
    # 系 — xì (lineage/department sense)
    "系": "xì",
    # 系统 (dropped)
    # 细节 — xìjié
    # 瞎 — xiā
    # 下载 — xiàzài (Taiwan pinyin; trad 下載)
    "下载": "xiàzài",
    # 报道 — trad is 報導 (Taiwan), so pinyin = bàodǎo (導 = dǎo, NOT 道 dào)
    "报道": "bàodǎo",
    # 冰激凌 — trad is 冰淇淋, so pinyin = bīngqílín (NOT bīngjīlíng)
    "冰激凌": "bīngqílín",
    # 光盘 — trad is 光碟, so pinyin = guāngdié (碟 = dié)
    "光盘": "guāngdié",
    # 信号 — s2twp gives 訊號, pinyin = xùnhào (訊 = xùn)
    "信号": "xùnhào",
    # 搜索 — s2twp gives 搜尋, pinyin = sōuxún (尋 = xún)
    "搜索": "sōuxún",
    # 吓 — xià
    # 夏令营 — xiàlìngyíng
    # 鲜艳 — xiānyàn
    # 显得 (handled)
    # 显然 — xiǎnrán
    # 显示 — xiǎnshì
    # 县 — xiàn
    # 现代 — xiàndài
    # 现实 — xiànshí
    # 现象 — xiànxiàng
    # 限制 — xiànzhì
    # 相处 (handled)
    # 相当 — xiāngdāng
    # 相对 — xiāngduì
    # 相关 — xiāngguān
    # 相似 (handled)
    # 香肠 — xiāngcháng
    # 享受 — xiǎngshòu
    # 想念 — xiǎngniàn
    # 想象 — xiǎngxiàng
    # 项 — xiàng
    # 项链 — xiàngliàn
    # 项目 — xiàngmù
    # 象棋 — xiàngqí
    # 象征 — xiàngzhēng
    # 消费 — xiāofèi
    # 消化 — xiāohuà
    # 消极 — xiāojí
    # 消失 — xiāoshī
    # 销售 — xiāoshòu
    # 小麦 — xiǎomài
    # 小气 (handled)
    # 孝顺 — xiàoshùn
    # 效率 — xiàolǜ
    # 歇 — xiē
    # 斜 — xié
    # 写作 — xiězuò
    # 血 (handled)
    # 心理 — xīnlǐ
    # 心脏 — xīnzàng
    # 欣赏 — xīnshǎng
    # 信号 — xìnhào
    # 信任 — xìnrèn
    # 行动 (handled)
    # 行人 (handled)
    # 行为 (handled)
    # 形成 — xíngchéng
    # 形容 — xíngróng
    # 形式 — xíngshì
    # 形势 — xíngshì
    # 形象 — xíngxiàng
    # 形状 — xíngzhuàng
    # 幸亏 — xìngkuī
    # 幸运 — xìngyùn
    # 性质 — xìngzhì  (HSK 4 zhì precedent)
    # 兄弟 (handled)
    # 胸 — xiōng
    # 休闲 — xiūxián
    # 修改 — xiūgǎi
    # 虚心 — xūxīn
    # 叙述 — xùshù
    # 宣布 — xuānbù
    # 宣传 — xuānchuán
    # 学历 — xuélì
    # 学术 — xuéshù
    # 学问 (handled)
    # 寻找 — xúnzhǎo
    # 询问 — xúnwèn
    # 训练 — xùnliàn
    # 迅速 — xùnsù
    # 押金 — yājīn
    # 牙齿 — yáchǐ
    # 延长 — yáncháng
    # 严肃 — yánsù
    # 演讲 — yǎnjiǎng
    # 宴会 — yànhuì
    # 阳台 — yángtái
    # 痒 — yǎng
    # 样式 — yàngshì
    # 腰 — yāo
    # 摇 — yáo
    # 咬 — yǎo
    # 要不 — yàobù
    # 业务 — yèwù
    # 业余 — yèyú
    # 夜 — yè
    # 一辈子 (handled)
    # 一旦 (handled)
    # 一律 (handled)
    # 一再 (handled)
    # 一致 (handled)
    # 依然 — yīrán
    # 移动 — yídòng
    # 移民 — yímín
    # 遗憾 — yíhàn
    # 疑问 — yíwèn
    # 乙 — yǐ
    # 以及 — yǐjí
    # 以来 — yǐlái
    # 亿 — yì
    # 义务 — yìwù
    # 议论 — yìlùn
    # 意外 — yìwài
    # 意义 — yìyì
    # 因而 — yīn'ér
    # 因素 — yīnsù
    # 银 — yín
    # 印刷 — yìnshuā
    # 英俊 — yīngjùn
    # 英雄 — yīngxióng
    # 迎接 — yíngjiē
    # 营养 — yíngyǎng
    # 营业 — yíngyè
    # 影子 — yǐngzi
    "影子": "yǐngzi",
    # 应付 (handled)
    # 应用 (handled)
    # 硬 — yìng
    # 硬件 — trad is 硬體, so pinyin must match: yìngtǐ
    "硬件": "yìngtǐ",
    # 拥抱 — yōngbào
    # 拥挤 — yōngjǐ
    # 勇气 — yǒngqì
    # 用功 — yònggōng
    # 用途 — yòngtú
    # 优惠 — yōuhuì
    # 优美 — yōuměi
    # 优势 — yōushì
    # 悠久 — yōujiǔ
    # 犹豫 — yóuyù
    # 油炸 — yóuzhá
    # 游览 — yóulǎn
    # 有利 — yǒulì
    # 幼儿园 — yòu'éryuán
    # 娱乐 — yúlè
    # 与其 — yǔqí
    # 语气 — yǔqì
    # 玉米 — yùmǐ
    # 预报 — yùbào
    # 预订 — yùdìng
    # 预防 — yùfáng
    # 元旦 — Yuándàn
    # 员工 — yuángōng
    # 原料 — yuánliào
    # 原则 — yuánzé
    # 圆 — yuán
    # 愿望 — yuànwàng
    # 乐器 (handled)
    # 晕 — yūn
    # 运气 (handled)
    # 运输 — yùnshū
    # 运用 — yùnyòng
    # 灾害 — zāihài
    # 再三 — zàisān
    # 在乎 (handled)
    # 在于 — zàiyú
    # 赞成 — zànchéng
    # 赞美 — zànměi
    # 糟糕 — zāogāo
    # 造成 — zàochéng
    # 则 — zé
    # 责备 — zébèi
    # 摘 — zhāi
    # 窄 — zhǎi
    # 粘贴 — zhāntiē
    # 展开 — zhǎnkāi
    # 展览 — zhǎnlǎn
    # 占 — zhàn
    # 战争 — zhànzhēng
    # 长辈 (handled)
    # 涨 — zhǎng
    # 掌握 — zhǎngwò
    # 账户 — zhànghù
    # 招待 — zhāodài
    # 着火 (handled)
    # 着凉 (handled)
    # 召开 (handled)
    # 照常 — zhàocháng
    # 哲学 — zhéxué
    # 针对 — zhēnduì
    # 珍惜 — zhēnxī
    # 真实 — zhēnshí
    # 诊断 — zhěnduàn
    # 阵 — zhèn
    # 振动 — zhèndòng
    # 争论 — zhēnglùn
    # 争取 — zhēngqǔ
    # 征求 — zhēngqiú
    # 睁 — zhēng
    # 整个 — zhěnggè
    # 整齐 — zhěngqí
    # 整体 — zhěngtǐ
    # 正 — zhèng
    # 证件 — zhèngjiàn
    # 证据 — zhèngjù
    # 政府 — zhèngfǔ
    # 政治 — zhèngzhì
    # 挣 (handled)
    # 支 — zhī
    # 支票 — zhīpiào
    # 执照 — zhízhào
    # 直 — zhí
    # 指导 — zhǐdǎo
    # 指挥 — zhǐhuī
    # 至今 — zhìjīn
    # 至于 — zhìyú
    # 志愿者 — zhìyuànzhě
    # 制定 — zhìdìng
    # 制度 — zhìdù
    # 制造 — zhìzào
    # 制作 — zhìzuò
    # 治疗 — zhìliáo
    # 秩序 — zhìxù
    # 智慧 — zhìhuì
    # 中介 — zhōngjiè
    # 中心 — zhōngxīn
    # 中旬 — zhōngxún
    # 种类 — zhǒnglèi
    # 重大 (handled)
    # 重量 (handled)
    # 周到 — zhōudào
    # 猪 — zhū
    # 竹子 — zhúzi
    "竹子": "zhúzi",
    # 逐步 — zhúbù
    # 逐渐 — zhújiàn
    # 主持 — zhǔchí
    # 主动 — zhǔdòng
    # 主观 — zhǔguān
    # 主人 — zhǔrén
    # 主任 — zhǔrèn
    # 主题 — zhǔtí
    # 主席 — zhǔxí
    # 主张 — zhǔzhāng
    # 煮 — zhǔ
    # 注册 — zhùcè
    # 祝福 — zhùfú
    # 抓 — zhuā
    # 抓紧 — zhuājǐn
    # 专家 — zhuānjiā
    # 专心 — zhuānxīn
    # 转变 — zhuǎnbiàn
    # 转告 — zhuǎngào
    # 装 — zhuāng
    # 装饰 — zhuāngshì
    # 装修 — zhuāngxiū
    # 状况 — zhuàngkuàng
    # 状态 — zhuàngtài
    # 撞 — zhuàng
    # 追 — zhuī
    # 追求 — zhuīqiú
    # 咨询 — zīxún
    # 姿势 — zīshì
    # 资格 — zīgé
    # 资金 — zījīn
    # 资料 — zīliào
    # 资源 — zīyuán
    # 紫 — zǐ
    # 自从 — zìcóng
    # 自动 — zìdòng
    # 自豪 — zìháo
    # 自觉 — zìjué
    # 自私 — zìsī
    # 自由 (dropped)
    # 自愿 — zìyuàn
    # 字母 — zìmǔ
    # 字幕 — zìmù
    # 综合 — zōnghé
    # 总裁 — zǒngcái
    # 总共 — zǒnggòng
    # 总理 — zǒnglǐ
    # 总算 — zǒngsuàn
    # 总统 — zǒngtǒng
    # 总之 — zǒngzhī
    # 阻止 — zǔzhǐ
    # 组 — zǔ
    # 组成 — zǔchéng
    # 组合 — zǔhé
    # 组织 — zǔzhī
    # 最初 — zuìchū
    # 醉 — zuì
    # 尊敬 — zūnjìng
    # 遵守 — zūnshǒu
    # 作品 — zuòpǐn
    # 作为 — zuòwéi
    # 作文 — zuòwén
}


def get_traditional(simp: str, converter) -> str:
    if simp in TRAD_OVERRIDES:
        return TRAD_OVERRIDES[simp]
    return converter.convert(simp)


def get_pinyin(simp: str) -> str:
    if simp in PINYIN_OVERRIDES:
        return PINYIN_OVERRIDES[simp]
    syllables = [p[0] for p in pinyin(simp, style=Style.TONE)]
    return "".join(syllables) if len(syllables) <= 2 else "".join(syllables)


def main():
    if not SRC.exists():
        print(f"ERROR: source list not found at {SRC}", file=sys.stderr)
        sys.exit(1)

    converter = opencc.OpenCC("s2twp")
    cards = []
    diff_log = []
    next_id = START_ID
    skipped = []

    with SRC.open(encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    for simp in words:
        if simp in DROP:
            skipped.append(simp)
            continue

        # Trad
        s2twp_default = converter.convert(simp)
        trad = get_traditional(simp, converter)
        if trad != s2twp_default:
            diff_log.append(f"TRAD  {simp}: s2twp='{s2twp_default}' overridden -> '{trad}'")

        # Pinyin
        py_default = "".join(p[0] for p in pinyin(simp, style=Style.TONE))
        py = get_pinyin(simp)
        if py != py_default:
            diff_log.append(f"PIN   {simp}: pypinyin='{py_default}' overridden -> '{py}'")

        cards.append({
            "id": next_id,
            "traditional": trad,
            "simplified": simp,
            "pinyin": py,
            "english": "",
            "category": "hsk5",
            "depth": "basic",
            "pos": "",
            "semanticNote": "",
            "components": [],
            "examples": [],
        })
        next_id += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    with DIFF_OUT.open("w", encoding="utf-8") as f:
        f.write(f"# HSK 5 skeleton — override audit log\n")
        f.write(f"# Source words: {len(words)}; dropped (NUGGETS dupes): {len(skipped)}; cards generated: {len(cards)}\n")
        f.write(f"# ID range: {START_ID}-{next_id - 1}\n")
        f.write(f"# Trad overrides applied: {sum(1 for d in diff_log if d.startswith('TRAD'))}\n")
        f.write(f"# Pinyin overrides applied: {sum(1 for d in diff_log if d.startswith('PIN'))}\n\n")
        f.write("\n".join(diff_log))
        f.write("\n")

    print(f"OK: {len(cards)} skeleton cards written to {OUT}")
    print(f"    ID range: {START_ID}-{next_id - 1}")
    print(f"    Dropped (NUGGETS dupes): {sorted(skipped)}")
    print(f"    Override diff log: {DIFF_OUT}")


if __name__ == "__main__":
    main()
