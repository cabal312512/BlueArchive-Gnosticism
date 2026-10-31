# 来源与参考文献登记总表 (Source Registry)

> 2026-10-31修缮，GPT 6.1 Sol。下列游戏来源以当前快照为准；文献或社区链接被登记不等于内容已经核验。

## 当前游戏来源

| ID | 来源 | 固定版本／位置 | 状态 |
| :--- | :--- | :--- | :--- |
| SRC-GAME-01 | HePudding/ba-storybook | 历史阶段使用，已弃用 | 不作为当前检索基准 |
| SRC-GAME-02 | [electricgoat/ba-data](https://github.com/electricgoat/ba-data) | `3428d2a0943bdfe7d6453adfcb06676509972b02`；本地`02_corpus/ba-data-jp/` | 社区维护的客户端数据导出，不称官方发布的学术语料库 |
| SRC-GAME-03 | schema v2 SQLite及生成Markdown | 237,386条非空日文记录；`02_corpus/story_index.db` | 原始表行号可追溯；范围见覆盖报告 |
| SRC-GAME-LEGACY | 修缮前SQLite与Markdown | `02_corpus/backups/pre-repair-980d581/` | 仅作旧引文／版本差异核对 |

## 二、诺斯底主义一手原典文献 (Primary Gnostic Texts)

| 文献 ID | 原典名称 | 归属流派 / 语种 | 核心英译本来源 | 本项目研究重点 |
| :--- | :--- | :--- | :--- | :--- |
| **SRC-GNO-01** | 《约翰秘传》(*Apocryphon of John*) | 塞特派 (Sethian) / 科普特语 (Nag Hammadi II,1; III,1; IV,1; BG 8502,2) | Waldstein/Wisse1995四抄本Synopsis；另参Robinson1988综合英译 | Monad 宇宙起源、Sophia 的流溢与失足、Yaldabaoth 造物、神性火花被困、Luminous Epinoia（光之洞见）救赎干预 |
| **SRC-GNO-02** | 《统治者的本质》(*The Hypostasis of the Archons*) | 塞特派 / 科普特语 (Nag Hammadi II,4) | Roger A. Bullard / Bentley Layton（Robinson1988，161–169页） | 执政者（Archons）的权威、傲慢与无知、对人类的奴役与命名权柄 |
| **SRC-GNO-03** | 《论世界的起源》(*On the Origin of the World*) | 诺斯底派 / 科普特语 (Nag Hammadi II,5) | Hans-Gebhard Bethge / Bentley Layton / Societas Coptica Hierosolymitana（Robinson1988，170–189页） | 混沌的开端、低层世界的生成、智性火花与启蒙 |

---

## 三、前人考据与学术研究 (Secondary Literature & Community Critiques)

| 文献 ID | 作者 / 平台 | 标题 | 发表时间 | 链接 | 核心观点与相关性 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-SEC-01** | イメージの裏切り (Note) | 《【与太考察】偽連邦生徒会長=ヤルダバオート説【ブルーアーカイブ】》 | 2025-12-26 | https://note.com/trashonimage/n/n7b5797e1abbe | 日本玩家提出的真正会长=Sophia、伪会长=Yaldabaoth 假说，涉及会长的过失与老师的救赎 |
| **SRC-SEC-02** | Reddit 社区讨论 | 《Students are Forgotten Gods who want to forgot their divinity》 | 绝对日期未核实 | https://www.reddit.com/r/BlueArchive/comments/1ulceyx/ | 学生主动遗忘神性以体验全新青春可能性的假设 |


## 本轮核对记录

原典重点段落及页面已核对，见 `04_evidence/gnostic_primary_cards.md`；来源文件指纹见primary_source_verification.json。两篇社区原帖正文已读，原帖与评论分开；Reddit绝对日期未确认，旧表的日期不再沿用。进一步综述及书目随越阶段材料暂存，不作为当前阶段任务。用户当前以剧情兴趣讨论为主，无正式论文目标。

## 第25轮Gnostic体系资料

新增本机下载资料共36份，含原典英译、古代传述、学术著作和目录。清单与SHA-256见 `gnostic_readings/download_manifest.json`，核验及排除项见download_validation.json。Turner2001、Waldstein/Wisse1995、Robinson1988、Irenaeus、Hippolytus及Mead1921分别作为整理依据，下载与实际引用分开。图谱与文字目录位于 `06_comparative_analysis/gnostic_atlas/`。

## 第26轮分歧核查补充

- Roelof van den Broek, *Gnostic Religion in Antiquity* (Cambridge, 2013), p.172：Sophia作为Eleleth三位随侍者之一的标准解释。核对该段，未声称通读全书。出版信息：https://www.cambridge.org/core/books/gnostic-religion-in-antiquity/271084C3309208717EB23F3A4CCCF7AA 。
- Zlatko Pleše, *Poetics of the Gnostic Universe* (Brill, NHMS52, 2006)，讨论II 11,22–26的note35：Authorities、rulers、powers及天使的数量关系与计算问题；用于说明不能把十二／七认同当成唯一明文读法。核对该注，未声称通读全书。DOI：https://doi.org/10.1163/9789047404026 。
- 可检索副本、原典定位与具体取舍统一见08_review_queue/atlas_review_resolution.md；AJ-W为综合译文，精确抄本异文仍以Waldstein/Wisse四栏Synopsis核对。


第28轮追加：Revelation21、Genesis6:5–7（BibleGateway KJV）；Tripartite Tractate恢复论（earlychristianwritings.com/text/tripartite.html），AJ唯一神／洪水／Pronoia段。日文Wiki与玩家整理仅用作回查线索，不将其战争总结代替游戏台词。详见04_evidence/nameless_forgotten_followup_2026-10-31.md。


## 第30轮：游戏外本人说明

- 梁主映（isakusan），2024-06-28电Fami刊出、2024年4月采访。Kyrie、宽恕救助与内在潜在神圣段已读；日文：https://news.denfaminicogamer.jp/interview/240628b_jp/2 ，同站中文：https://news.denfaminicogamer.jp/interview/240628b_cn/2 。性质为开发者直接访谈中的创作主题说明，不是官方游戏百科或Gnostic来源确认。
- 2024国际服三周年Q&A原视频线索：https://www.youtube.com/watch?v=x9J9UG_BxOY 。本轮未核原声／字幕；玩家转述存在分歧，不采“所有学生看见一样光环”等绝对说法。
- 游戏内检索与关键19条双语材料见04_evidence/stage5_students_halo_round30.json。
