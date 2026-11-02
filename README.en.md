[中文](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · English

This is an AI translation and may sound awkward; I do not understand the other languages and have reviewed only the Chinese version, so please treat the [Chinese version](README.md) as authoritative.

# Blue Archive and Gnosticism: A Correspondence Model

This is a personal study of the story of *Blue Archive* and its correspondences with the cosmology of Gnosticism. It focuses on the General Student Council President, Sensei, the Nameless Gods, the Nameless Priests, the Forgotten Gods, and the students' halos.

These are just my own rambling thoughts and personal views. My thinking jumps around, and I used a lot of AI, so there will be plenty of inaccuracies.

## Where to Start

- **[Full paper](gnostic_correspondence_en.md)**: I wrote most of this myself. The AI did a poor job of writing it. All the main ideas are collected here, so this is the only file you need to read; all the other documents were written by AI.
- **[Glossary](GNOSTIC_GLOSSARY_en.md)**: Explains the terms and literature mentioned in the paper for readers new to the subject.
- **[Cosmology atlas](gnostic_atlas.html)**: Download it and open the HTML file in a browser.
- **[Technical citation index](01_sources/paper_citation_index.md)**: Maps the paper's notes to the original corpus IDs, source tables, and row numbers.

If you're interested in my ideas and have downloaded the repository, you can have an AI read the [agent guide](AGENTS.md), [research conversations](CHAT_BACKUP.md), [current status](PROJECT_STATUS.md), and [decision log](08_review_queue/decision_log.md), then continue from there. This project can be handed directly to an agent. These supporting documents are in Chinese.

## Repository Contents

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

## Searching Locally

The local research corpus comes from a fixed data snapshot and contains 237,386 non-empty Japanese records. The repository includes the complete readable corpus and a compressed database. The raw data's external source and fixed revision are recorded; see the [corpus documentation](02_corpus/coverage_report.md) for the source and version.

```powershell
python 03_tools/restore_corpus.py
python 03_tools/search.py -q "名もなき神" -C 3
python 03_tools/search.py -q "忘却は" -C 3
```

## Raw Data and History

For everyday searches, you only need to restore the database as shown above. Before rebuilding it or checking the original data, run:

```powershell
git clone https://github.com/electricgoat/ba-data.git 02_corpus/ba-data-jp
git -C 02_corpus/ba-data-jp checkout 3428d2a0943bdfe7d6453adfcb06676509972b02
python 03_tools/search.py --test
```

The local commits and tags from before the upload are preserved in full in the [Git history backup](08_review_queue/archive/pre_github_history.bundle).

## License

The project's original writing, research notes, and code are released under [CC0 1.0 Universal](LICENSE). Game text, third-party literature, and external data retain their respective rights and sources; this project's CC0 declaration does not change them.
