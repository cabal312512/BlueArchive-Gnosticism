> [!WARNING]
> **ネタバレ注意**
>
> 本文には『ブルーアーカイブ』のメインストーリーの重要なネタバレが含まれます。メインストーリー第1部を読了したプレイヤー向けです。

---

> [!NOTE]
> **翻訳について**
>
> AIによる翻訳のため不自然な表現があるかもしれませんが、私は中国語以外の言語が分からず中国語版しか確認していないので、内容は[中国語版](README.md)を基準にしてください。

<h1 align="center">『ブルーアーカイブ』のGnosticism対応モデル</h1>

『ブルーアーカイブ』の物語とGnosticismの宇宙論のつながりについての個人的な考察です。連邦生徒会長、先生、名もなき神々、無名の司祭、忘れられた神々に対応するGnosticの神話的原型を扱っています。

> これはあくまで私の思いつきや個人的な考えです。話があちこちに飛ぶうえ、AIも大量に使っているので、不正確な部分がたくさんあると思います。

> なぜ『ブルーアーカイブ』とGnosticismを結びつけるのか。[短い説明はこちら](rationale/why_gnosticism_ja.md)。

## 読むならここから

<table width="100%">
<tr>
<td width="9999">

<picture>
<source media="(min-width: 768px)" srcset="assets/readme/reading-desktop.svg">
<img align="right" src="assets/readme/reading.jpg" width="440" alt="机に向かう二人のキャラクター">
</picture>

<p><sub>01</sub>&nbsp;&nbsp;<strong><a href="gnostic_correspondence_ja.md">論文全文</a></strong>：</p>
<blockquote><p>ほぼ全部自分で書きました。AIが書いた文章はひどかったです。今後も更新していきます。中心となる考えはすべてここにまとめてあるので、これだけ読めば十分です。それ以外の文書はすべてAIが書いたものです。</p></blockquote>

<p><sub>02</sub>&nbsp;&nbsp;<strong><a href="glossary/GNOSTIC_GLOSSARY_ja.md">用語解説</a></strong>：</p>
<blockquote><p>この分野に初めて触れる方に向けて、本文に出てくる用語や文献を説明しています。</p></blockquote>

<p><sub>03</sub>&nbsp;&nbsp;<strong><a href="gnostic_atlas.html">Gnosticismの登場存在の関係図</a></strong>：</p>
<blockquote><p>ダウンロード後、HTMLファイルをブラウザで開いてください。</p></blockquote>

<p><sub>04</sub>&nbsp;&nbsp;<strong><a href="01_sources/paper_citation_index.md">引用の技術索引</a></strong>：</p>
<blockquote><p>論文の注と、元のコーパスの番号・データ表・行番号との対応を記録しています。</p></blockquote>

<br clear="all">

</td>
</tr>
</table>

> 私の考えに興味があり、リポジトリをダウンロードした方は、AIに[引き継ぎ文書](AGENTS.md)、[プロジェクトの状況](PROJECT_STATUS.md)、[判断の記録](08_review_queue/decision_log.md)を読ませてから、続きを進めてもらうこともできます。このプロジェクトはそのままAgentに引き継げます。これらの補助文書は中国語です。

---

<details>
<summary><strong>資料の構成</strong></summary>

| ディレクトリ | 内容 |
| --- | --- |
| [01_sources](01_sources/) | 出典の記録、文献一覧、引用の技術索引 |
| [02_corpus](02_corpus/) | コーパスのバージョンと収録範囲の説明 |
| [03_tools](03_tools/) | 検索、コーパス構築、関係図のツール |
| [04_evidence](04_evidence/) | 物語の引用、中国語訳、テーマ別の根拠資料 |
| [05_hypotheses](05_hypotheses/) | 各対応についての考察ノート |
| [06_comparative_analysis](06_comparative_analysis/) | 原典の構造と比較資料 |
| [07_writing](07_writing/) | 以前の草稿と執筆資料 |
| [08_review_queue](08_review_queue/) | 議論での判断と過去の記録 |

</details>

<details>
<summary><strong>ローカルでの検索</strong></summary>

ローカルの調査用コーパスは、固定バージョンのデータスナップショットから作成したもので、空でない日本語の記録を237,386件含んでいます。リポジトリには、読みやすい形式の全文コーパスと圧縮したデータベースが入っています。元データについては外部の入手先と固定リビジョンを記録しています。出典とバージョンは[コーパスの説明](02_corpus/coverage_report.md)を参照してください。

```powershell
python 03_tools/restore_corpus.py
python 03_tools/search.py -q "名もなき神" -C 3
python 03_tools/search.py -q "忘却は" -C 3
```

</details>

<details>
<summary><strong>元データと履歴</strong></summary>

通常の検索には、上記の方法でデータベースを復元するだけで十分です。再構築や元データの照合を行う場合は、先に次のコマンドを実行してください。

```powershell
git clone https://github.com/electricgoat/ba-data.git 02_corpus/ba-data-jp
git -C 02_corpus/ba-data-jp checkout 3428d2a0943bdfe7d6453adfcb06676509972b02
python 03_tools/search.py --test
```

アップロード前のローカルのコミットとタグは、[Git履歴のバックアップ](08_review_queue/archive/pre_github_history.bundle)にすべて保存されています。

</details>

## ライセンス

本プロジェクトのオリジナルの文章、考察・整理した内容、およびコードは、[Creative Commons Attribution 4.0 International（CC BY 4.0）](LICENSE)で公開しています。転載・改変の際は、作者 cabal312512 と[本プロジェクト](https://github.com/cabal312512/BlueArchive-Gnosticism)を出典として明記し、[ライセンスへのリンク](https://creativecommons.org/licenses/by/4.0/)を添え、変更の有無を示してください。ゲーム内テキスト、第三者の文献、外部データはそれぞれの権利と出典を維持し、本プロジェクトのライセンスによって再許諾されるものではありません。以前CC0で公開したバージョンは、この変更の影響を受けません。
