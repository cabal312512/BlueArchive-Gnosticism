> [!WARNING]
> **剧透警告**
>
> 本文包含《蔚蓝档案》主线剧情的重要剧透，适合已读完第一部主线剧情的玩家阅读。

---

> [!NOTE]
> **翻译说明**
>
> 日本語はこちら：[日本語版README](README.ja.md)。AIによる翻訳のため不自然な表現があるかもしれませんが、私は中国語以外の言語が分からず中国語版しか確認していないので、内容は[中国語版](README.md)を基準にしてください。
>
> 한국어는 [한국어판 README](README.ko.md)를 봐 주세요. AI 번역이라 표현이 다소 어색할 수 있으며, 저는 다른 언어를 몰라 중국어판만 검토했으므로 내용은 [중국어판](README.md)을 기준으로 해 주세요.
>
> For English, see [English README](README.en.md). This is an AI translation and may sound awkward; I do not understand the other languages and have reviewed only the Chinese version, so please treat the [Chinese version](README.md) as authoritative.

<h1 align="center">《蔚蓝档案》的Gnosticism对应模型</h1>

这是关于《蔚蓝档案》剧情与Gnosticism宇宙论之间联系的个人研究，讨论了联邦学生会长、老师、无名众神、无名祭司、被遗忘的诸神对应的Gnostic神话原型。

> 这只些是我胡思乱想的个人观点，思维比较跳跃，还用了AI辅助，所以会有很多不准确和考虑不周的地方。非常欢迎大家指正。如果有人愿意来看一看，我真的会很开心！

> 为什么会把《蔚蓝档案》和Gnosticism联系起来？先看这篇[简短说明](rationale/why_gnosticism.md)。

## 阅读入口

<table width="100%">
<tr>
<td width="9999">

<picture>
<source media="(min-width: 768px)" srcset="assets/readme/reading-desktop.svg">
<img align="right" src="assets/readme/reading.jpg" width="440" alt="会长和凛">
</picture>

<p><sub>01</sub>&nbsp;&nbsp;<strong><a href="gnostic_correspondence_full.md">论文全文</a></strong>：</p>
<blockquote><p>这个几乎全是我亲笔写的，会持续更新。核心观点都总结在这里，只看这个就行，其他的文档全是AI写的。</p></blockquote>

<p><sub>02</sub>&nbsp;&nbsp;<strong><a href="glossary/GNOSTIC_GLOSSARY.md">术语说明</a></strong>：</p>
<blockquote><p>面向初次接触相关概念的读者，解释文中的名词与文献。</p></blockquote>

<p><sub>03</sub>&nbsp;&nbsp;<strong><a href="gnostic_atlas.html">Gnosticism角色图谱</a></strong>：</p>
<blockquote><p>下载后浏览器打开HTML文件。</p></blockquote>

<p><sub>04</sub>&nbsp;&nbsp;<strong><a href="01_sources/paper_citation_index.md">引文技术索引</a></strong>：</p>
<blockquote><p>论文注释与原始语料编号、源表行号的对应。</p></blockquote>

<br clear="all">

</td>
</tr>
</table>

> 如果对我的想法感兴趣且下载了仓库，可以让AI看看[交接文档](AGENTS.md)、[项目状态](PROJECT_STATUS.md)与[讨论裁决](08_review_queue/decision_log.md)再继续，这个项目可以直接交给Agent。

---

<details>
<summary><strong>资料目录</strong></summary>

| 目录 | 内容 |
| --- | --- |
| [01_sources](01_sources/) | 来源登记、文献目录与引文技术索引 |
| [02_corpus](02_corpus/) | 语料版本与覆盖说明 |
| [03_tools](03_tools/) | 检索、语料构建与图谱工具 |
| [04_evidence](04_evidence/) | 剧情引文、中文译文与专题证据 |
| [05_hypotheses](05_hypotheses/) | 各项对应的讨论笔记 |
| [06_comparative_analysis](06_comparative_analysis/) | 原典结构与比较资料 |
| [07_writing](07_writing/) | 早期稿件与写作资料 |
| [08_review_queue](08_review_queue/) | 讨论裁决与历史存档 |

</details>

<details>
<summary><strong>本地检索</strong></summary>

本地研究语料来自固定版本的数据快照，包含237,386条非空日文记录。仓库包含完整的可读台词和压缩数据库。原始数据保留外部来源与固定版本，来源与版本见[语料说明](02_corpus/coverage_report.md)。

```powershell
python 03_tools/restore_corpus.py
python 03_tools/search.py -q "名もなき神" -C 3
python 03_tools/search.py -q "忘却は" -C 3
```

</details>

<details>
<summary><strong>原始数据与历史</strong></summary>

日常检索只需恢复上面的数据库。重新构建或运行原始数据核对前，执行：

```powershell
git clone https://github.com/electricgoat/ba-data.git 02_corpus/ba-data-jp
git -C 02_corpus/ba-data-jp checkout 3428d2a0943bdfe7d6453adfcb06676509972b02
python 03_tools/search.py --test
```

上传前的本地提交与标签完整保存在[Git历史备份](08_review_queue/archive/pre_github_history.bundle)。

</details>

## 许可

本项目原创文字、研究整理和代码采用[Creative Commons Attribution 4.0 International（CC BY 4.0）](LICENSE)。游戏文本、第三方文献及外部数据保留各自的权利与来源。
