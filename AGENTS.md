# Agent交接指南

更新：2026-11-02，第59轮。先读[项目状态](PROJECT_STATUS.md)与[裁决记录](08_review_queue/decision_log.md)，不要把历史日志当成当前任务。

## 当前执行规则

- 第59轮：按用户截图删除四语README独立语言导航行，原位换横线；常显翻译说明中的原有语言链接保留。不要恢复已删的重复导航。

- 第58轮：四语README完整翻译说明已取消折叠，移至语言导航下方、正文标题上方，用GitHub原生NOTE蓝色提示框常显。不要再收进details；原说明文字和链接完整保留。

- 第57轮补充：四语README阅读入口外框须撑满阅读区；GitHub的table百分比宽度会被样式覆盖，使用单格td width=9999实现填满但不溢出。四条说明用原生blockquote呈现灰色文字及左竖线，手机图片在前。桌面picture使用assets/readme/reading-desktop.svg上下留白容器（内嵌原JPEG），让配图下移；手机仍用原JPEG。两张都是正式排版资源。作者文字不变，检查见08_review_queue/readme_design_round57.json。

- 第56轮四语README统一排版，顶部剧透提醒；assets/readme/reading.jpg为用户提供的正式配图，不能当垃圾截图清理。桌面右浮动、手机图在入口上方，用单格外框承载浮动图文，不改回挤压手机的两列布局。保留作者原文和完整翻译声明；论文及术语本轮未改。检查记录见08_review_queue/readme_design_round56.json。

- 第55轮补充：本地垃圾桶目录已改名为Trash，.gitignore同步；历史对话中的旧路径保留原话，不再创建旧目录。发布前按当前中文同步作者自行修改的章节顺序、删句和表述，不能只同步AI改过的段落。

- 第55轮用户明确要求全部上传。当前作者稿、第53–54轮四语术语和指定段落、项目记录及DeepSeek辅助规范纳入发布；原始数据、凭据、运行数据、缓存与垃圾桶继续排除。下方“仅本地”是当时状态，以本条为准。

- 第54轮最终授权仅扩写论文原第178行的承接与矛盾提出。第179行及后文作者解答恢复原样；三译同步这一处。不要把讨论中作者尚未表达完整的“平静触及”等口述擅自写成哲学定论或扩大修改范围。过程与最终范围见08_review_queue/paper_expansion_round54.json。

- 第53轮最新分工：论文、术语说明、README、译文与短段落由主助手直接写改，不再让DeepSeek起草。DeepSeek仅做耗时的大批量全文阅读、检索、对照与取证，给内部报告；不为其报告润色，不满时用简短反馈续接同一会话补查。它不得直接改本项目文档。独立入口F:/DeepSeekHarness/Invoke-DeepSeek.ps1，项目用deepseek/Invoke-Review.ps1与Follow-Up.ps1；先提供资料副本，只读、无Shell及write/edit。凭据、运行时、日志和缓存全留F盘独立目录，禁止入Git。
- 四语术语说明已按当前中文扩为42条，三个用词移至后部；本轮另定点改Epinoia论文段并同步三译，作者其他同时修改保留。当前仅本地完成，见[记录](08_review_queue/glossary_and_helper_round53.md)。

- 当前图谱入口为根目录[gnostic_atlas.html](gnostic_atlas.html)，四语单文件；顶部只有语言按钮，截图所示标题区已删除。自动按浏览器首选语言选择，可手动切换并记忆；存储被禁用也可使用。
- 图谱数据、875条内容的三语映射与脚本均内嵌。保留21体系、370节点、375条关系及全部曲线；检查／导出用03_tools/atlas.py，不从旧生成器重建。旧脚本、重复产物、截图和临时环境已移入本地垃圾桶，可删除且不上传；原典资料与原始数据另行保留。
- 用户第52轮授权整理项目、迁移HTML及更新路径，完成后同步GitHub。论文仅更新链接目标，不改作者正文。第51轮已同步作者认可的新开头；详见[维护记录](08_review_queue/project_cleanup_round52.md)。
- 作者会同时修改文件；每次落笔前重新读当前稿，只替换授权片段并确认写前未变化。禁止用旧快照或一次性脚本覆盖整篇。
- 三语论文／术语说明以当前中文为准，不增减判断力度。日／韩游戏台词直接用同源数据库原文，英文保留日文并附英译；韩文差异先查ScriptKr，不据差异判定AI增写。数据库定位见[记录](01_sources/paper_translation_quotes_round42.json)。
- 论文以解释Gnosticism对应为主，术语与文献用英文。查准原话，少废话；日语台词前用日文名，中文译文前用中文名，无发言人的引文标“译文”。
- **每轮结束前把用户、过程回复和最终回复实际追加到CHAT_BACKUP.md并回读确认，AI标题标GPT 6.1 Sol。** 不把项目摘要当逐字备份，缺乏原话时不补造。
- PROJECT_STATUS.md只维护当前说明；过程追加research_journal，用户决定写decision_log。原始数据、下载原典和垃圾桶不上传、不误删；根目录README.md继续作为中文默认入口。
- 用户认可另贴日文简介中“控制”译为“支配欲”；不再当误译改掉。第48轮现用新增注为95、96、98、99、102，不恢复退役注。旧审阅差异与作者原件存档用于追溯，不能覆盖当前稿。

下列基础规则继续适用；若涉及旧状态描述，以上方当前规则及后续用户指令为准。

> **紧急交接提示 (Handover Notice)**：
> 如果你是刚刚接手本项目的 AI Agent（即便你没有任何先前的对话上下文），**请立即完整阅读本文档、根目录下的 `PROJECT_STATUS.md` 以及 `08_review_queue/decision_log.md`**。本文档包含你接手此项目所需的一切背景、方法论标准、目录架构、假说定义与操作工具。

---

## 1. 项目定位与核心使命 (Project Mission)

本项目是用户出于兴趣开展的《蔚蓝档案》剧情与诺斯底神话对应研究，以讨论和理解剧情为主，不按正式科研项目推进。

- **核心研究问题**：
  游戏《蔚蓝档案》的底层宇宙结构，是否系统性地参考了古代诺斯底主义（尤其是纳格哈马迪文库塞特派核心文献《约翰秘传》*Apocryphon of John* 中的索菲亚、雅尔达巴奥特、神性流溢、神性火花及光之洞见等观念）？在这一宇宙模型中，联邦学生会长、老师、无名众神、无名祭司、被遗忘的诸神以及当代学生分别处于怎样的本体论与叙事功能位置？
- **当前目标**：查清剧情、讨论有意思的神话对应，整理便于回看的笔记；当前不以论文发表为目标。

---

## 2. 职责划分与协作铁律 (Roles & Hard Rules)

1. **用户（User）是主要研究者、理论提出者与最终仲裁者**。
   - 所有重大人物对应定论、论文最终大纲、新神话模型的采纳，必须由用户决断。
   - **必须严格遵守 `08_review_queue/decision_log.md` 中用户已拍板的定论**（例如：会长＝索菲亚已 100% 定死；伪会长 ≠ Yaldabaoth）。
2. **严禁脑补或张冠李戴剧情（最高红线）**：
   - 任何关于游戏角色性格、行为、事件因果的描述，**必须先亲自查阅 `02_corpus/stories/` 或通过 `03_tools/search.py` 检索原文**！
   - 严禁凭印象瞎编或混淆角色（例如：严禁将前代行“不知火花耶”的独断专行超人控制论混淆到温和亲切的“联邦学生会长”头上）。
3. **日文引用必须附带中文翻译**：
   - 在向用户汇报或编写任何文档时，**凡是引用日文原文台词，必须在紧随其后附上准确的中文翻译**，确保用户无需懂日文也能完全理解。
4. **对话记录原话完整备份铁律（`CHAT_BACKUP.md`，含具体模型标注）**：
   - 根目录下的 [`CHAT_BACKUP.md`](CHAT_BACKUP.md) 用于一字不差地备份用户与 AI 的每一轮问答原话。
   - **每一轮对话结束前，必须将本轮的用户原话与 AI 回复更新追加到 `CHAT_BACKUP.md` 中，且必须在 AI 发言标题处明确标上当前的具体模型名称（例如 `### 【AI (Agent - Gemini 4 Argon Low) 原话】`）**（平时无需读取该文件，仅在上下文丢失需恢复细节时查阅）。
5. **灵活适度的比较尺度（切忌死板教条）**：
   - 《蔚蓝档案》是一款电子游戏，它参考了诺斯底主义的宇宙结构与原型，但并不意味着游戏必须在所有细节上死板遵守诺斯底教条（如无需强求 100% 照搬“内在精神概念”，也不用把老师的肉身凡人设定强行往基督教“道成肉身”或复杂神学概念上贴靠）。
6. **材料性质严格分层**：
   - **A 级：直接文本证据**（游戏或原典直接言明，如“会长亲口承认自己的ミス/错误”、“步提及会长史上最年少就任”）。
   - **B 级：结构性对应**（叙事因果与功能高度平行，如“索菲亚犯错 ➔ 召来 Epinoia”与“会长失误 ➔ 召来老师”）。
   - **C 级：象征符号对应**（光环、数值、专有名词、宗教符号）。
   - **D 级：推测性假说**（研究者推论，尚无直接文本锚点）。

---

## 3. 七大核心研究假说与当前审定状态 (Hypotheses H1 ~ H7)

- **H1【联邦学生会长 对应 索菲亚 (Sophia)】—— 【用户已确认 100% 成立，暂时定死】**：
  会长在序章与最终篇自承判断失误（`私のミスでした`），在第 2 部序章被确认为“史上最年轻就任（史上最年少での就任）”，伴侣对应按用户解释保留（不冒充明确自述单身的台词）、温和亲切（展现高维本源的纯净人性）；索菲亚在诺斯底体系中是最年轻/最后一位永世（Aeon），因过失导致失衡，随后悔悟并展开补救。
  - *保留待考问题*：① 基沃托斯/无名众神与会长失误的时间因果关系（会长极为神秘，信息极少，暂作保留）；② 索菲亚作为 Yaldabaoth 之母及神力被夺的对应关系（暂作保留）。
- **H2【无名众神/无名祭司 对应 低层造物秩序 (Demiurge / Yaldabaoth & Archons)】**：
  无名众神是基沃托斯现行秩序确立前的旧神；无名祭司类似七位执政者（Archons），崇拜旧秩序并试图支配世界。（注：伪会长与 Yaldabaoth 无关，已排除）。
- **H3【被遗忘的诸神 与 当代学生的神性本体 (Forgotten Gods & Students)】**：
  当代学生携带着神性本质，神秘（Mystic）与恐怖（Terror）构成了神性的两面（如白子之于阿努比斯、爱丽丝之于 AL-1S/王女）。
- **H4【学生光环 对应 神性火花 (Halo as Divine Spark)】**：
  头顶的光环（ヘイロー）作为更高神圣世界遗留于个体之中的“神性火花（Divine Spark）”表征。
- **H5【名字、遗忘与本体论地位 (Naming, Memory & Ontic Status)】**：
  “失去名字便失去存在”、“真名（神名文字）赋予权柄”，与诺斯底命名神学存在深层关联。
- **H6【被遗忘的诸神 与 Monad 之下的神圣存在 (Pleroma Emanations)】**：
  考证《约翰秘传》中高于物质造物主的纯粹神圣流溢（Barbelo、Autogenes、Aeons、Adamas、Seed of Seth）与基沃托斯诸神本源的关系。
- **H7【老师 对应 光之洞见 (Teacher as Luminous Epinoia)】—— 【大概率成立】**：
  在索菲亚犯错之后，最高神界派遣光之洞见（Luminous Epinoia）帮助人类；会长犯错后引入“老师”指引学生走出扭曲结局。老师与学生平静美好的日常相处，呼应着高维本源的纯净与日常奇迹（老师作为“外在人物”系游戏编写剧本之必然需要，保留但不作为障碍）。

---

## 4. 工作区目录架构导览 (Workspace Layout)

```
Blue Archive Project Gnosis/
├── AGENTS.md                  # 【必读】本交接与运行核心指南
├── PROJECT_STATUS.md          # 【必读】实时研发进度与任务看板
├── CHAT_BACKUP.md             # 【每轮必更新】用户与 AI 一问一答原话完整备份（平时不用读）
├── gnostic_correspondence_full.md # 作者论文
├── gnostic_atlas.html         # 四语离线单文件图谱
├── GNOSTIC_GLOSSARY.md         # 读者术语说明
├── README.md                  # 项目概况与人类可读介绍
├── prompt.txt                 # 项目发起时的原始详细指导书
├── .gitignore                 # 版本控制过滤规则
│
├── 00_project_management/     # 项目管理与日志
│   ├── roadmap.md             # 7个阶段完整技术路线图
│   ├── task_board.md          # 详细任务进度追踪（TODO / IN_PROGRESS / DONE）
│   └── research_journal.md    # 研发工作流水日志
│
├── 01_sources/                # 来源与参考文献登记
│   └── source_registry.md     # 游戏语料、纳格哈马迪原典与学术论文清单
│
├── 02_corpus/                 # 固定版本文本快照与派生语料
│   ├── ba-data-jp/            # 固定提交的客户端JSON数据导出；版本见覆盖报告
│   ├── story_index.db         # 237,386 条非空日文记录的schema v2检索数据库
│   ├── stories/               # 3,403 个生成Markdown（含活动等类别，按Series与元数据入口区分）
│   └── coverage_report.md     # 语料覆盖率与版本完整性检验报告
│
├── 03_tools/                  # 考据与检索引擎脚本
│   ├── search.py              # 核心：日文剧情台词多维度全文检索工具
│   ├── build_complete_corpus.py# 从 ba-data-jp 构建全量数据库与 Markdown 的生成脚本
│   └── README.md              # 检索脚本用法详细说明
│
├── 04_evidence/               # 结构化证据库
├── 05_hypotheses/             # 7 大假说专题研究文档
│   ├── H1_president_sophia.md
│   ├── H2_nameless_gods_demiurge.md
│   ├── H3_forgotten_gods_students.md
│   ├── H4_halo_divine_spark.md
│   ├── H5_names_identity.md
│   ├── H6_divine_hierarchy.md
│   └── H7_teacher_luminous_epinoia.md
│
├── 06_comparative_analysis/   # 比较神话与结构对照
│   └── gnostic_cosmology.md   # 纳格哈马迪原典宇宙论与流溢谱系
│
├── 07_writing/                # 早期稿件与写作资料
└── 08_review_queue/           # 用户仲裁与决策队列
    └── decision_log.md        # 【必读】用户已批准的正式裁决与方法论指示
```

---

## 5. 核心工具运行指南 (How to Search Corpus)

工作区已内置全量日文剧情台词检索引擎：[`03_tools/search.py`](03_tools/search.py)。

```powershell
# 1. 运行检索与解析回归检查（实际范围见覆盖报告）
python 03_tools/search.py --test

# 2. 基础关键词检索（查找会长的错误）
python 03_tools/search.py -q "私のミスでした" -C 3

# 3. 多关键词与逻辑（同时包含“名もなき神”和“司祭”）
python 03_tools/search.py -q "名もなき神" -q2 "司祭"

# 4. 指定角色发言检索（查看黑服所有台词）
python 03_tools/search.py -s "黒服" -v "最終篇"
```

---

## 6. 新 Agent 接手标准 SOP (Handover SOP)

如果你是新唤醒的 Agent，请严格执行以下 4 步恢复工作：
1. **核对进度与裁决**：读取 [`PROJECT_STATUS.md`](PROJECT_STATUS.md) 与 [`08_review_queue/decision_log.md`](08_review_queue/decision_log.md)。
2. **核对任务板**：读取 [`00_project_management/task_board.md`](00_project_management/task_board.md)。
3. **验证环境**：运行 `python 03_tools/search.py --test` 确认当前快照检索与解析回归检查通过（不等于全部发布内容覆盖）。
4. **遵守每轮更新铁律**：每次回答确保日文附带中文翻译，并将问答原话追加备份至 `CHAT_BACKUP.md`。
