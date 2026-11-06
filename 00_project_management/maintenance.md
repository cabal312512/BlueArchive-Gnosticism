# 项目维护说明

这里放工具与文件维护方法。当前理论只看[当前理论与保留问题](../08_review_queue/decision_log.md)，当前接续事项只看[项目状态](../PROJECT_STATUS.md)。

## 各份记录只负责一件事

| 文档 | 写什么 | 什么时候改 |
| --- | --- | --- |
| [AGENTS.md](../AGENTS.md) | 长期协作要求与项目核心约定 | 长期规则确实改变时 |
| [PROJECT_STATUS.md](../PROJECT_STATUS.md) | 接续时必须知道的当前事项、未完成工作与发布状态 | 接续信息改变时，直接更新当前说明，不追加流水 |
| [decision_log.md](../08_review_queue/decision_log.md) | 当前采用的理论、明确排除与保留问题 | 作者改变理论或采用新的判断时 |
| [CHAT_BACKUP.md](../CHAT_BACKUP.md)及[索引](../CHAT_BACKUP_INDEX.md) | 实际问答原话与定位 | 每轮追加、回读；不重写旧话 |
| [research_journal.md](research_journal.md) | 已做事项、关键结果和必要的文件定位 | 有实际工作时简短追加；不复制整套当前状态 |
| 08_review_queue中的专题记录 | 具体核查材料、差异和证据 | 有需要追溯的实质核查时；普通排版不另外造一套报告 |

用户消息决定任务，不维护任务板，不另做阶段路线。讨论中的建议、AI评价和待核问题不自动变成任务或作者裁决。一次普通修改通常只动目标文件、追加对话；有实际操作就在日志留一条。无需为了同一件事再改AGENTS、状态、裁决和旧审阅报告。

审阅记录、哈希和行号是当时的快照，不随新稿反复刷新。历史原话不改；旧记录的工作结论不能自动覆盖当前稿。旧裁决全文保存在[decision_history.md](../08_review_queue/decision_history.md)，不作为执行指南。

## 文件入口

- 根目录README.md是默认中文入口；另有README.en／ja／ko.md。四篇论文也在根目录，中文为gnostic_correspondence_full.md。
- glossary/存四语术语说明；rationale/存why_gnosticism及_en／_ja／_ko版，不改名README。
- 01_sources登记来源、原典目录与[引文技术索引](../01_sources/paper_citation_index.md)；02_corpus存语料、数据库及覆盖说明。
- 03_tools是现用工具；04_evidence是引文证据；05_hypotheses是专题笔记；06_comparative_analysis是原典与比较资料。
- 07_writing保留写作定位资料；08_review_queue保留专题核查和历史；[09_reality_inquiry](../09_reality_inquiry/README.md)是作者独立的现实世界研究，原宗教比较资料并入其religious_comparison/。
- Trash/仅放已停用、可随时删除的东西，不上传。作者原稿、有效证据、原始数据和原典不能当垃圾清理。

## 语料与引文

检索库来自固定版本客户端数据。具体覆盖、统计和恢复方法以[覆盖说明](../02_corpus/coverage_report.md)为准，工具用法见[03_tools](../03_tools/README.md)。回归通过不等于全剧情覆盖或理论成立。

```powershell
python 03_tools/search.py --test
python 03_tools/search.py -q "私のミスでした" -C 3
python 03_tools/search.py -q "名もなき神" -q2 "司祭"
python 03_tools/search.py -s "黒服" -v "最終篇"
```

日／韩台词按同源记录分别提取TextJp／ScriptKr，韩日差异先查数据库，不能仅据差异判定AI增写。既有定位见[引用记录](../01_sources/paper_translation_quotes_round42.json)。在中文论文和中文汇报中，日文人物名用日文，中文译文的人名用中文；无发言人的引文标“译文”。

## 论文与README排版

- 四篇论文标题居中；下方语言导航为贴合文字宽度的居中单格框，格内文字水平、垂直居中。不加章节横线。
- 英／日／韩论文的剧透警告下，分别用常显NOTE框标明AI翻译可能不准确、以中文为准，并链接中文原文。
- 注释仅保留文献／章节／话数／对白位置及必要链接；每组一段，不另换行重复注号，不放论证或解释。活动剧情标活动自己的话数，不混作主线话数。
- 文末资料和注释分别用details折叠。正文用sup中的显式锚点链接，文末用note-N锚点和普通编号；不要恢复会被GitHub移出折叠区的自动脚注。改格式时保持全部注号、引用顺序、原话及出处。
- 四语README顶部保留剧透提醒，完整翻译声明以NOTE框常显，不收进details；不恢复已删的重复语言导航。
- README阅读入口用单格td width=9999填满阅读区，桌面配图右侧、手机图片在前。assets/readme/reading.jpg和reading-desktop.svg是正式资源，不能当垃圾截图。
- 先按当前中文同步作者所有改动，不能只处理AI自己改过的段落。作者写作、事实核查和译文忠实是不同工作，不混为理论已经证实。

## 图谱

根目录[gnostic_atlas.html](../gnostic_atlas.html)是四语离线单文件，数据、译文与脚本内嵌；顶部只有语言按钮，自动按浏览器语言选择并支持手动记忆。保留21体系、370节点、375关系、全部曲线及875条内容的三语映射；不要用旧生成器重建覆盖。

```powershell
python 03_tools/atlas.py
python 03_tools/atlas.py --export scratch/atlas-data.json
```

## DeepSeek与发布

GitHub服务操作优先使用已连接的GitHub插件，包括读取远端、创建提交和发布。先发现并检查插件能力；仅在所需能力缺失时使用其他方式。本地Git用于差异检查、版本管理和验证同步状态，不默认走命令行认证或推送。 插件连接不可用时，可按会话授权使用本机既有SSH密钥；第115轮作者明确提示可用SSH，已验证GitHub的443端口可用。私钥不复制、不输出、不上传。

DeepSeek只辅助耗时的内部资料工作，提供资料副本、只读且关闭Shell与write/edit；报告核事实与定位，不为报告润色。主助手自己决定如何改读者文档。独立入口F:/DeepSeekHarness/Invoke-DeepSeek.ps1，项目入口deepseek/Invoke-Review.ps1与Follow-Up.ps1，完整规范见[deepseek/README.md](../deepseek/README.md)。凭据、运行时、输入副本、输出、日志和缓存全部留F盘独立目录，不进Git、不落C盘。

发布前检查实际改动清单和.gitignore；note/及专用导出报告、Trash、原始客户端数据、下载原典和运行凭据继续排除。可公开的压缩检索库与可读语料保留。不要强制覆盖远端或重写作者并行修改；发布后核对远端与本地状态。
