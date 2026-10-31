#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only search of the pinned Japanese corpus (schema v2)."""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "02_corpus/story_index.db"
STORIES_DIR = PROJECT_ROOT / "02_corpus/stories"


def get_db_connection(path=None):
    path = Path(path or DB_PATH).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Missing corpus: {path}. Build with build_complete_corpus.py --output-dir first.")
    conn = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    columns = {r[1] for r in conn.execute("PRAGMA table_info(dialogues)")}
    if "source_row" not in columns:
        conn.close()
        raise ValueError("Legacy schema. Preserve it, build and validate schema v2 before activation.")
    return conn


def get_dialogue_context(conn, center_id, context_lines=2):
    if context_lines < 0:
        raise ValueError("Context size cannot be negative")
    center = conn.execute("SELECT group_id,group_row FROM dialogues WHERE id=?", (center_id,)).fetchone()
    if not center:
        return []
    gid, ordinal = center
    before = conn.execute("SELECT id,speaker_jp,text_jp FROM dialogues WHERE group_id=? AND group_row<? ORDER BY group_row DESC LIMIT ?",
                          (gid, ordinal, context_lines)).fetchall()[::-1]
    after = conn.execute("SELECT id,speaker_jp,text_jp FROM dialogues WHERE group_id=? AND group_row>=? ORDER BY group_row LIMIT ?",
                         (gid, ordinal, context_lines + 1)).fetchall()
    return [(">> " if did == center_id else "   ") + (f"**{spk}**: " if spk else "") + txt
            for did, spk, txt in before + after]


def search_db(conn, query=None, query2=None, not_query=None, speaker=None,
              category=None, volume=None, chapter=None, context_lines=2,
              max_results=50, group_id=None, dialogue_id=None, speaker_exact=False, speaker_key=None):
    sql = ["SELECT d.* FROM dialogues d WHERE 1=1"]
    params = []
    for value, clause in [(query, "d.text_jp LIKE ?"), (query2, "d.text_jp LIKE ?"),
                          (not_query, "d.text_jp NOT LIKE ?")]:
        if value:
            sql.append("AND " + clause); params.append(f"%{value}%")
    if speaker_key:
        sql.append("AND d.speaker_kr=?"); params.append(speaker_key)
    if speaker:
        sql.append("AND d.speaker_jp " + ("= ?" if speaker_exact else "LIKE ?"))
        params.append(speaker if speaker_exact else f"%{speaker}%")
    if any((category, volume, chapter)):
        filters = ["l.group_id=d.group_id"]
        for value, field in [(category, "category"), (volume, "volume")]:
            if value:
                filters.append(f"l.{field} LIKE ?"); params.append(f"%{value}%")
        if chapter:
            filters.append("(l.chapter LIKE ? OR l.episode LIKE ?)"); params.extend([f"%{chapter}%"] * 2)
        sql.append("AND EXISTS (SELECT 1 FROM group_locations l WHERE " + " AND ".join(filters) + ")")
    if group_id is not None:
        sql.append("AND d.group_id=?"); params.append(group_id)
    if dialogue_id is not None:
        sql.append("AND d.id=?"); params.append(dialogue_id)
    sql.append("ORDER BY d.group_id,d.group_row")
    if max_results > 0:
        sql.append("LIMIT ?"); params.append(max_results)
    cur = conn.execute(" ".join(sql), params)
    columns = [r[0] for r in cur.description]
    results = []
    for row in cur.fetchall():
        r = dict(zip(columns, row))
        r["speaker"] = r["speaker_jp"] or "(no parsed speaker; inspect source)"
        r["matched_line"] = r["text_jp"]
        r["context"] = get_dialogue_context(conn, r["id"], context_lines)
        r["locations"] = [dict(zip(("category", "volume", "chapter", "episode"), a))
            for a in conn.execute("SELECT category,volume,chapter,episode FROM group_locations WHERE group_id=?", (r["group_id"],))]
        results.append(r)
    return results


def format_results_markdown(results: List[Dict[str, Any]], query_summary: str) -> str:
    """Format search results as clean Markdown."""
    out = [
        f"# 本地语料检索结果 (Snapshot Corpus Search Results)",
        f"",
        f"- **检索条件**: `{query_summary}`",
        f"- **本次返回数量（可能受 -n 限制）**: `{len(results)}` 条",
        f"",
        f"---",
        f""
    ]

    for i, r in enumerate(results, 1):
        loc = f"{r['category']} / {r['volume']} / {r['chapter']} / {r['episode']}"
        out.append(f"### Result {i}: {loc} (ID: {r['id']}, Group: {r['group_id']})")
        if r['markdown_path']:
            out.append(f"- **Markdown 文本**: [{r['markdown_path']}](<{(PROJECT_ROOT / r['markdown_path']).as_posix()}>)")
        out.append(f"- **原始定位**: `{r['source_file']}:{r['source_row']}` / Group 行 `{r['group_row']}`")
        out.append(f"- **原始角色键**: `{r.get('speaker_kr','')}`；版本：`{r.get('source_version','canonical')}`")
        out.append(f"- **说话者解析**: `{r['speaker_resolution']}`")
        out.append(f"- **说话者**: **{r['speaker']}**")
        out.append(f"- **命中台词**: `{r['matched_line']}`")
        out.append(f"")
        out.append(f"```text")
        out.extend(r["context"])
        out.append(f"```")
        out.append(f"")
        out.append(f"---")
        out.append(f"")

    return "\n".join(out)


def run_self_test(path=None):
    import unittest
    import test_corpus
    test_corpus.DATABASE_PATH = Path(path or DB_PATH)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_corpus)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def legacy_variant_result(conn, legacy_id, context_lines=2):
    cur = conn.execute("SELECT * FROM legacy_variants WHERE legacy_id=?", (legacy_id,))
    row = cur.fetchone()
    if row is None: return None
    r = dict(zip([d[0] for d in cur.description], row))
    loc = conn.execute("SELECT category,volume,chapter,episode FROM group_locations WHERE group_id=? LIMIT 1", (r["group_id"],)).fetchone()
    if loc: r.update(zip(("category","volume","chapter","episode"), loc))
    else: r.update(category="その他_シナリオ",volume=f"Group_{r['group_id']}",chapter="未分類",episode="legacy_variant")
    r.update(id=f"legacy:{legacy_id}", source_version="aggregate_variant", speaker=r["speaker_jp"] or "(hidden/unnamed label)",
             matched_line=r["text_jp"], markdown_path=None, locations=[], context=[])
    from build_complete_corpus import read_rows, BA_DATA_DIR, load_character_mappings, extract_speaker
    source = BA_DATA_DIR / "DB" / r["source_file"]
    rows = [(i,x) for i,x in enumerate(read_rows(source),1) if x["GroupId"]==r["group_id"] and x.get("TextJp","").strip()]
    center = next(i for i,(n,_) in enumerate(rows) if n==r["source_row"])
    mapping,_=load_character_mappings()
    for n,x in rows[max(0,center-context_lines):center+context_lines+1]:
        jp,_=extract_speaker(x.get("ScriptKr",""),mapping)
        r["context"].append((">> " if n==r["source_row"] else "   ")+(f"**{jp}**: " if jp else "")+x["TextJp"].strip())
    return r


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-q", "--query")
    p.add_argument("-q2", "--query2")
    p.add_argument("--not-query")
    p.add_argument("-s", "--speaker", "-c", "--character")
    p.add_argument("--speaker-exact", action="store_true")
    p.add_argument("--speaker-key", help="Exact internal Korean speaker key; distinguishes identical display names")
    p.add_argument("-cat", "--category")
    p.add_argument("-v", "--volume")
    p.add_argument("-ch", "--chapter")
    p.add_argument("--group", type=int)
    p.add_argument("--variants", type=int, metavar="GROUP_ID", help="Export preserved source difference blocks as JSON")
    p.add_argument("--id", type=int)
    p.add_argument("--legacy-id", type=int)
    p.add_argument("--db", type=Path, default=DB_PATH)
    p.add_argument("-C", "--context", type=int, default=2)
    p.add_argument("-n", "--max-results", type=int, default=50, help="0 returns all matching records")
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("--test", action="store_true")
    a = p.parse_args()
    if a.context < 0 or a.max_results < 0:
        p.error("Context and maximum results must be nonnegative")
    if a.test:
        sys.exit(0 if run_self_test(a.db) else 1)
    if not any((a.query, a.query2, a.speaker, a.category, a.volume, a.chapter,
                a.group is not None, a.id is not None, a.legacy_id is not None, a.variants is not None, a.speaker_key)):
        p.error("Specify a query, filter, group, ID, or --test")
    try:
        conn = get_db_connection(a.db)
    except (FileNotFoundError, ValueError, sqlite3.Error) as exc:
        p.error(str(exc))
    with conn:
        if a.variants is not None:
            data=[{"group_id":r[0],"operation":r[1],"aggregate":json.loads(r[2]),"canonical":json.loads(r[3])} for r in conn.execute("SELECT * FROM source_variants WHERE group_id=?",(a.variants,))]
            content=json.dumps(data,ensure_ascii=False,indent=2)+"\n"
            if a.output:
                a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(content,encoding="utf-8")
            else: print(content)
            return
        results = None
        if a.legacy_id is not None:
            if a.id is not None:
                p.error("Use either --id or --legacy-id")
            old = conn.execute("SELECT dialogue_id,match_kind FROM legacy_ids WHERE legacy_id=?", (a.legacy_id,)).fetchone()
            if not old: p.error("Unknown legacy ID")
            if old[0] is None:
                variant=legacy_variant_result(conn,a.legacy_id,a.context)
                if variant is None: p.error("Missing preserved legacy variant")
                results=[variant]
            else: a.id = old[0]
        if results is None:
            results = search_db(conn, a.query, a.query2, a.not_query, a.speaker,
                a.category, a.volume, a.chapter, a.context, a.max_results,
                a.group, a.id, a.speaker_exact, a.speaker_key)
    summary = {k: str(v) if isinstance(v, Path) else v for k, v in vars(a).items() if v is not None}
    if a.output and a.output.suffix.lower() in (".json", ".jsonl"):
        content = ("\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n" if a.output.suffix.lower() == ".jsonl"
                   else json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    else:
        content = format_results_markdown(results, json.dumps(summary, ensure_ascii=False))
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(content, encoding="utf-8")
        print(f"Saved {len(results)} records to {a.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
