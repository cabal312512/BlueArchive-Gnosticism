# 语料构建与检索（schema v2）

以 `02_corpus/coverage_report.md`、`02_corpus/build_manifest.json` 为实际范围基准，统计是快照非空文本记录，不再称全剧情零缺失。

## 首次使用

```powershell
python 03_tools/restore_corpus.py
```

该命令校验SHA256并恢复数据库，已有数据库时不覆盖。需要重建或核对原始表时，按根目录README中的命令另行下载原始数据。

## 日常检索

```powershell
python 03_tools/search.py --test
python 03_tools/search.py -q "私のミスでした" -C 3
python 03_tools/search.py -q "名もなき神" -q2 "司祭"
python 03_tools/search.py -s "黒服" --speaker-exact -v "最終篇"
python 03_tools/search.py --group 10052195 -n 0 -C 0 -o scratch/event854_scene29.json
python 03_tools/search.py --legacy-id 344595 -C 3
python 03_tools/search.py -q "忘却は" -o scratch/forgetfulness.jsonl
```

`-s`只过滤已解析发言者，不会把正文提到角色名误作该角色发言。默认是名字子串匹配，`--speaker-exact`严格匹配。当前所有有角色键的196,511条均已按XXH32对应原名字表。相同显示名不保证相同人物，可用`--speaker-key`按内部键区分；新增未知键仍保留原样，不猜身份。

`-n 0`返回全部，其余返回上限默认50；显示数量是本次返回数。`--group`指定原始Group，`--id`指定v2 ID，`--legacy-id`转换旧库ID。其中151个不等同于当前文本的旧ID，直接返回保留的汇总表旧版本，明确标注aggregate_variant；不伪造当前ID。

`-v`、`-cat`、`-ch`检查同一条元数据别名组合；结果附locations字段，以免活动复刻入口覆盖旧入口。每条记录带原始表名、一基DataList行号、Group内原始行号及发言人解析状态。JSONL实际逐行输出对象。

检索导出是原始语料工作材料，不是直接发给用户的研究报告。正式引文与汇报须另加中文翻译。完整的爱丽丝／未知声音场景译注见 `04_evidence/EV854_29_voice_dialogue_bilingual.md`。

## 安全重建

```powershell
python 03_tools/build_complete_corpus.py --output-dir scratch/new-corpus-build
python 03_tools/search.py --db scratch/new-corpus-build/story_index.db --test
```

输出目录必须为空。脚本不改原始底表，不覆盖当前数据库。先验证，再保留现用数据库和stories目录，最后切换。备份路径见覆盖报告。不要使用旧版README里的`--reindex`或`--rebuild`；重建现在由独立脚本承担。

编号分片按顺序拼接，汇总表只作比对与缺失Group回退；保留段内重复以及原始顺序。不是按一句话的文本内容简单去重。

## 回归检查

`test_corpus.py`检验真实错误场景：前置显示指令、角色子串误配、未知名保留、两套特殊作战隔离、跨分片场景完整、旧ID追溯、正文／发言者分离、上下文与数据库完整性。测试通过不等于全剧情覆盖或所有神学解释成立。

## 本轮补齐

`--speaker-key`按原始角色键精确筛选；`--variants GROUP_ID`导出该Group的版本对照JSON。旧ID共395,866个全部可追溯。79个去除空白后仍不同的Group保留122个对照块；其余3组仅空白差异。23项回归检查通过。角色哈希实现见xxhash32.py，算法规范：https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash_spec.md 。


## 图谱维护

根目录的[gnostic_atlas.html](../gnostic_atlas.html)是四语单文件，直接离线打开。全部数据、译文、脚本与样式在文件内部，资料页可导出JSON、CSV与文字总表。

```powershell
python 03_tools/atlas.py
python 03_tools/atlas.py --export scratch/atlas-data.json
python 03_tools/test_gnostic_atlas.py
```

`atlas.py`只校验或导出，不会重建或覆盖HTML。旧版图谱生成器和一次性论文生成器已移入本地垃圾桶，避免覆盖后续人工修改。

## 当前工具

保留检索、数据库恢复、完整语料构建、源文献下载、图谱检查及相关回归检查；检索使用的`xxhash32.py`保留。临时探查脚本、旧索引构建器和一次性排版脚本已清理。论文仍以根目录作者稿为准，引用定位见[技术索引](../01_sources/paper_citation_index.md)。
