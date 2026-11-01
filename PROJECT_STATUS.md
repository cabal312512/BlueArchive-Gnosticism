# 项目状态

更新：2026-11-01，第41轮。

当前在维护作者论文、核查外部审阅意见；本轮完成多语言README及项目更新发布。研究仍按兴趣与具体问题推进；阶段5已展开，论文写作是用户另外授权的工作。

## 当前文件

| 文件 | 当前用途 |
| --- | --- |
| [中文README](README.md)、[日语](README.ja.md)、[韩语](README.ko.md)、[英语](README.en.md) | 默认入口仍为中文；译版注明AI翻译、未审阅及以中文为准 |
| [中文论文](gnostic_correspondence_full.md) | 作者当前主稿；以此为准，未经授权不改写 |
| [术语说明](GNOSTIC_GLOSSARY.md) | 解释文中的英文名词与文献；保留作者修改 |
| [英文译稿](gnostic_correspondence_en.md)、[日文译稿](gnostic_correspondence_ja.md)、[韩文译稿](gnostic_correspondence_ko.md) | 本地已有，本轮一并发布；正文未在本轮改写或校对 |
| [宇宙论图谱](06_comparative_analysis/gnostic_atlas/index.html) | 按文本、版本查关系；下载后用浏览器打开 |
| [引文技术索引](01_sources/paper_citation_index.md) | 保存数据库定位，论文用数字注释 |
| [对话备份](CHAT_BACKUP.md) · [最近对话索引](CHAT_BACKUP_INDEX.md) | 保存问答原话，方便按轮查找 |

## 最近已经处理

- **第37轮：核查两处原典问题。** 确认Tripartite Tractate语境误用，以及Apocryphon of John引文混入解释；见[核查记录](08_review_queue/paper_review_round37.md)。
- **第38轮：用户批准后实际改稿。** 第4.2改为忠实引文和引文外分析；第5.2的TT引文移至第9.2；补注33并清理原注34。见[具体修改](08_review_queue/paper_revision_round38.diff)。此后作者又有修改，以当前主稿为准，旧行号不能当作永久定位。
- **第39轮：核查价值改写的意见。** 认为局部改写有根据，但祭司毁灭现状不自动否定Archons对应；人物对应与价值变化分别论证。仅给建议，没有执行改稿，见[核查记录](08_review_queue/paper_review_round39.md)。
- **记录与入口维护已完成。** 第40轮补回第37–39轮原话、整理状态；第41轮在GitHub作者中文版README上仅加三语入口，并全文翻译三个版本，对应链接到各语言论文与术语说明。

## 研究方向

- 用户固定：会长＝Sophia；伪会长不对应Yaldabaoth。老师对应Luminous Epinoia按大概率方向保留。
- 无名祭司对应Archons，也承接部分Yaldabaoth功能；无名众神本体与Yaldabaoth有关，但不独占这个原型。保留本体位于神圣来源一侧的分支，不硬排其高于Sophia。
- 学生整体与被遗忘诸神联系，光环对应Divine Spark；无需逐个给学生安排Aeon名号。
- 声音按用户对无名众神本体的判断开展讨论；出处事实与解释分别记录。认真考证，允许游戏改写原型，不要求细节照搬。

## 尚待处理

- 是否进一步采用第39轮对“创造性改写”的措辞建议，由作者决定。
- 三份译稿及三份术语说明译本与中文当前稿的一致性还没有逐段核对；README已注明作者仅审阅中文。
- Sanctum Tower归属张力、会长与旧神的时间因果等原有保留问题，仍留在研究笔记中；不自动扩张新任务。

## GitHub与本地

- 仓库：[cabal312512/BlueArchive-Gnosticism](https://github.com/cabal312512/BlueArchive-Gnosticism)，CC0。
- 本次更新基于远端main的`ead7e43e01f7d5d1e3202e6b1363eeaca6150f18`，保留作者在GitHub上修改的中文README原文，只加顶部入口。
- 用户第41轮明确授权全部上传；作者最新本地稿、各语言论文与术语说明、三语README、恢复的记录与状态整理随本次一同发布。对话记录补至第41轮，具体发布提交以Git日志为准。
- 原始数据不上传，本机也不删除；已发布的压缩数据库可用`python 03_tools/restore_corpus.py`恢复。范围见[语料说明](02_corpus/coverage_report.md)。

## 记录放在哪里

当前情况只写在本页；过程写入[研究日志](00_project_management/research_journal.md)，用户决定写入[裁决记录](08_review_queue/decision_log.md)，问答原话追加到[CHAT_BACKUP.md](CHAT_BACKUP.md)。不再向状态页不断追加历次日志。

本轮整理前的状态、指南和任务板见[维护前存档](08_review_queue/archive/maintenance_round40_2026-11-01/)。
