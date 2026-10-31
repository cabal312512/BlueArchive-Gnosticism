# Apocryphon of John图谱外部评价：核查与修订

2026-10-31，GPT 6.1 Sol。评价原文见atlas_external_review_2026-10-31.txt。原版基准为Git提交4c85a2e；修订生成脚本、关系数据和前端，不仅手改HTML。

## 逐项判断

| 评价项目 | 判断 | 已处理 |
| --- | --- | --- |
| 同tier的同工关系不画线 | 采纳 | 支持横向、逆向与跨分组关系，不再仅画向下线 |
| Twelve／Seven总括与成员混排断线 | 采纳 | 总括与成员分开，名单按所属分列，逐条核对可见边 |
| 折叠后层号整体改变 | 采纳其误导问题 | AJ改用稳定语义分组，不将可见行序编号伪装成位阶 |
| Barbelo四属性及Autogenes只有单一来源 | 采纳 | 请求、应允／显现及Father／Mother生成分别连线 |
| Autogenes绝不低于任何属性 | 接受三重结构的重要性，不采用绝对数值排名 | 按Father–Mother–Son及Pentad分组；原文没有逐项编号的完整本体等级表 |
| Wisdom与Sophia分成两位 | 采纳，修正本方旧判断 | 合并Sophia / Wisdom；Eleleth随侍三项、四灯共十二项，未重复计数 |
| Sophia被放在迟悔灵魂下方 | 采纳 | 原本Aeon与居所、群体及第九处暂居状态分别显示 |
| Adamas—Seth—Seed缺谱系 | 采纳 | 保留四灯安置线，增加其子／seed关系 |
| Seven Powers确定就是十二名单中的七位，绝非另一种展开 | 不全采纳 | 保留十二名列、七天配置、powers展开及相关关系；不直接逐项认同，也不画成已定的低一级人口 |
| Adam缺上界形象与母之力量 | 采纳 | 造形、上界image、Sophia→Yaldabaoth→Adam力量转移分开；补Five Lights及Epinoia援助 |
| Life、Counterfeit、Fate都从Adam派生 | 采纳 | Life标神圣来向；Counterfeit与Fate连下层统治者并作用于人 |
| Eve与Earthly Seth用同一种子节点关系 | 采纳 | Eve分造形、取Adam部分力量及Epinoia显现；Seth保留生子及上界援助 |
| Five Seals归给Epinoia | 采纳 | 由Barbelo／Pronoia连接其自述行动 |

## 分歧核查

### Wisdom / Sophia：改变本方原判断

II 8,18–20的Wisdom与9,25起的Sophia同用希腊借词。但本次合并不只依据同词，还核了随侍位置与现成学术解释。Roelof van den Broek, *Gnostic Religion in Antiquity*（Cambridge, 2013），p.172明确将Sophia解释为Eleleth的三位随侍者之一。因此本篇主视图合并；不将其他文本全部Wisdom／Sophia名号全局合一。

- [Cambridge出版信息](https://www.cambridge.org/core/books/gnostic-religion-in-antiquity/271084C3309208717EB23F3A4CCCF7AA)
- [p.172相关段落的检索副本](https://gnosis.study/library/%D0%93%D0%BD%D0%BE%D0%B7%D0%B8%D1%81/%D0%98%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/ENG/van%20den%20Broek%20R.%20-%20Gnostic%20religion%20in%20antiquity.pdf)
- 原典：Waldstein/Wisse1995，Synopsis20–24；II 8,18–20、9,25起。

### 十二／七：评价的认同过于肯定

长本先列十二Authorities及七天、五深渊的配置，又叙述Archons产生powers，再将七重powers与Authorities结合。原文没有给出一张将不同名列逐项等同的无歧义对照表；不能单靠重名就认定身份关系全部解决。

Zlatko Pleše, *Poetics of the Gnostic Universe*（Brill, NHMS52, 2006），讨论II 11,22–26的note35区分十二Authorities、七rulers、powers及其天使，并指出数字演算本身存在问题。因此外部评价的“绝不是另一种powers展开”不是唯一可采用的读法。

采用：保留不同名列及其关联，具体认同标为解释。图上同排用来消除伪精确的高低，不表示证明完全相同或完全独立。

- [Pleše书目与DOI](https://doi.org/10.1163/9789047404026)
- [note35相关段落的检索副本](https://gnosis.study/library/%D0%93%D0%BD%D0%BE%D0%B7%D0%B8%D1%81/%D0%98%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/ENG/Ple%C5%A1e%20Z.%20-%20Poetics%20of%20the%20Gnostic%20Universe.%20Narrative%20and%20Cosmology%20in%20the%20Apocryphon%20of%20John.pdf)
- 原典II 10,26–12,25；[Wisse可检索译文](https://www.earlychristianwritings.com/text/apocryphonjohn.html)。

## 来源与图面约定

AJ-W.txt是Wisse综合译文转载，不是额外一份独立的NHC II校勘本；快查用它，精确异文仍以四栏Synopsis为准。第九处按原文记录在其子之上、直到缺陷修正，不把完整八／九层结构额外补入。

edges允许多个来源，区分生成、安置、力量、范型、援助、控制、名列，并保存定位。实线为文本关系，虚线为对应解释；点击可逐项查来源。tier只作排版，parent仅作旧数据主关联兼容字段，不再决定AJ完整来源关系。

本轮修正原典底图，不自动更改游戏人物对应，也不恢复已排除的失忆／三次降临等H7论据。
