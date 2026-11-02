# 项目状态

更新：2026-11-02，第61轮。

当前新增四语[阅读缘起](rationale/why_gnosticism.md)，说明从游戏的宗教神话借用联想到Gnosticism的理由；保留学生神话原型，纠正事实错误和夸饰。四语术语说明已移入glossary/，README在阅读入口上方用引用样式链接同语言短文；论文仅更新术语说明链接，正文未改。用户第61轮要求改名后上传：四语阅读缘起改用why_gnosticism及语言后缀命名，本轮发布第60轮与本轮全部文档修改。

## 阅读与使用

| 文件 | 用途 |
| --- | --- |
| [中文README](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [English](README.en.md) | 默认中文入口；译版以中文为准 |
| [中文论文](gnostic_correspondence_full.md) · [日语](gnostic_correspondence_ja.md) · [韩语](gnostic_correspondence_ko.md) · [英语](gnostic_correspondence_en.md) | 作者主稿及对应译稿 |
| [阅读缘起](rationale/why_gnosticism.md) | 同目录另有英／日／韩版，宗教与神话借用的简短说明 |
| [术语说明](glossary/GNOSTIC_GLOSSARY.md) | 四语均在glossary/，内容不变 |
| [四语图谱](gnostic_atlas.html) | 单文件，离线打开；自动识别浏览器语言，可手动切换并记忆 |
| [引文索引](01_sources/paper_citation_index.md) | 注释与语料原始定位 |
| [宗教比较](09_religious_comparison/README.md) | 原典与上下文核查，为论文提供材料 |
| [检索与维护工具](03_tools/README.md) | 现用语料工具及单文件图谱检查 |
| [对话索引](CHAT_BACKUP_INDEX.md) · [裁决](08_review_queue/decision_log.md) | 问答与作者决定 |

## 当前维护规则

- 作者会同时修改文件；写入前重读，只改明确授权片段。未经授权不润色中文论文，不运行旧稿件生成器。
- 论文／术语译稿以当前中文为准，既不强化也不弱化判断。日／韩游戏引文用数据库原文；英文保留日文及英译。
- 图谱的原始数据、译文与运行代码都在gnostic_atlas.html内；atlas.py只校验／导出。21体系、370节点、375关系及曲线保留。
- 第48轮宗教开头的当前新增注为95、96、98、99、102；其上下文记录保留，不恢复退役的97、100、101。
- 圣塔归属、会长与旧神的时间关系等问题继续保留，不自动扩展任务。

## 文件整理与发布

- 原始数据不上传、不删除；现有压缩数据库及可读剧情保留。恢复方法见[语料说明](02_corpus/coverage_report.md)。
- 下载原典保留在01_sources/gnostic_readings/downloads和local_archive，均不上传。
- 本地`Trash`收纳已停用脚本、重复产物、截图和临时环境，可随时删除；已被.gitignore排除。scratch已清空。
- 第55轮已发布作者稿和辅助规范；第56轮同步四语README与正式配图，独立工具的凭据和运行数据不进入仓库。
- 对话记录补至第61轮，模型标注GPT 6.1 Sol。过程见[研究日志](00_project_management/research_journal.md)，[本轮详情](08_review_queue/project_cleanup_round52.md)。
