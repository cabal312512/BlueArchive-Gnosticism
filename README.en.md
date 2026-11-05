> [!WARNING]
> **Spoiler warning**
>
> This article contains major spoilers for the main story of Blue Archive. It is intended for players who have finished Part 1 of the main story.

---

> [!NOTE]
> **Translation notes**
>
> This is an AI translation and may sound awkward; I do not understand the other languages and have reviewed only the Chinese version, so please treat the [Chinese version](README.md) as authoritative.

<h1 align="center">Blue Archive and Gnosticism: A Correspondence Model</h1>

This is a personal study of the connections between the story of *Blue Archive* and the cosmology of Gnosticism. It discusses the Gnostic mythological prototypes corresponding to the General Student Council President, Sensei, the Nameless Gods, the Nameless Priests, and the Forgotten Gods.

> These are just my own rambling thoughts and personal views. My thinking jumps around, and I used a lot of AI, so there will be plenty of inaccuracies.

> Why connect Blue Archive with Gnosticism? Start with this [short explanation](rationale/why_gnosticism_en.md).

## Where to Start

<table width="100%">
<tr>
<td width="9999">

<picture>
<source media="(min-width: 768px)" srcset="assets/readme/reading-desktop.svg">
<img align="right" src="assets/readme/reading.jpg" width="440" alt="Two characters working at a desk">
</picture>

<p><sub>01</sub>&nbsp;&nbsp;<strong><a href="gnostic_correspondence_en.md">Full paper</a></strong>:</p>
<blockquote><p>I wrote almost all of this myself. I will keep updating it. All the main ideas are collected here, so this is the only file you need to read; all the other documents were written by AI.</p></blockquote>

<p><sub>02</sub>&nbsp;&nbsp;<strong><a href="glossary/GNOSTIC_GLOSSARY_en.md">Glossary</a></strong>:</p>
<blockquote><p>Explains the terms and literature mentioned in the paper for readers new to the subject.</p></blockquote>

<p><sub>03</sub>&nbsp;&nbsp;<strong><a href="gnostic_atlas.html">Gnosticism Character Atlas</a></strong>:</p>
<blockquote><p>Download it and open the HTML file in a browser.</p></blockquote>

<p><sub>04</sub>&nbsp;&nbsp;<strong><a href="01_sources/paper_citation_index.md">Technical citation index</a></strong>:</p>
<blockquote><p>Maps the paper&#x27;s notes to the original corpus IDs, source tables, and row numbers.</p></blockquote>

<br clear="all">

</td>
</tr>
</table>

> If you're interested in my ideas and have downloaded the repository, you can have an AI read the [handover guide](AGENTS.md), [project status](PROJECT_STATUS.md), and [decision log](08_review_queue/decision_log.md), then continue from there. This project can be handed directly to an agent. These supporting documents are in Chinese.

---

<details>
<summary><strong>Repository Contents</strong></summary>

| Directory | Contents |
| --- | --- |
| [01_sources](01_sources/) | Source records, bibliography, and technical citation index |
| [02_corpus](02_corpus/) | Corpus version and coverage information |
| [03_tools](03_tools/) | Search, corpus-building, and atlas tools |
| [04_evidence](04_evidence/) | Story quotations, Chinese translations, and evidence by topic |
| [05_hypotheses](05_hypotheses/) | Notes on the individual correspondences |
| [06_comparative_analysis](06_comparative_analysis/) | Structures in the primary texts and comparative material |
| [07_writing](07_writing/) | Earlier drafts and writing material |
| [08_review_queue](08_review_queue/) | Discussion decisions and historical archives |

</details>

<details>
<summary><strong>Searching Locally</strong></summary>

The local research corpus comes from a fixed data snapshot and contains 237,386 non-empty Japanese records. The repository includes the complete readable corpus and a compressed database. The raw data's external source and fixed revision are recorded; see the [corpus documentation](02_corpus/coverage_report.md) for the source and version.

```powershell
python 03_tools/restore_corpus.py
python 03_tools/search.py -q "名もなき神" -C 3
python 03_tools/search.py -q "忘却は" -C 3
```

</details>

<details>
<summary><strong>Raw Data and History</strong></summary>

For everyday searches, you only need to restore the database as shown above. Before rebuilding it or checking the original data, run:

```powershell
git clone https://github.com/electricgoat/ba-data.git 02_corpus/ba-data-jp
git -C 02_corpus/ba-data-jp checkout 3428d2a0943bdfe7d6453adfcb06676509972b02
python 03_tools/search.py --test
```

The local commits and tags from before the upload are preserved in full in the [Git history backup](08_review_queue/archive/pre_github_history.bundle).

</details>

## License

The project's original writing, research notes, and code are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). When sharing or adapting this material, credit cabal312512 and [this project](https://github.com/cabal312512/BlueArchive-Gnosticism), provide a [license link](https://creativecommons.org/licenses/by/4.0/), and indicate whether changes were made. Game text, third-party literature, and external data retain their respective rights and sources and are not relicensed by this project. Versions previously released under CC0 are unaffected by this change.
