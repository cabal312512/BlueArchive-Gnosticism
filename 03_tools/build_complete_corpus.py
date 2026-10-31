#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a traceable Japanese script index from a pinned local data snapshot.

Numbered DB shards are concatenated in numeric order. The unnumbered aggregate
is an overlap check and fallback for groups absent from the shards, never an
additional copy of the same scene. Repeated lines *within* a scene are preserved.
Build into an empty independent directory; activation is a separate operation.
"""
import argparse
import hashlib
import json
import re
import sqlite3
import subprocess
from collections import defaultdict, Counter
from difflib import SequenceMatcher
from pathlib import Path
from xxhash32 import xxh32

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BA_DATA_DIR = PROJECT_ROOT / "02_corpus" / "ba-data-jp"
DB_PATH = PROJECT_ROOT / "02_corpus" / "story_index.db"
STORIES_DIR = PROJECT_ROOT / "02_corpus" / "stories"
VOLUME_NAMES = {0: "第0篇_プロローグ", 1: "第1篇_対策委員会編",
    2: "第2篇_時計じかけの花のパヴァーヌ編", 3: "第3篇_エデン条約編",
    4: "第4篇_カルバノの兎編", 5: "第5篇_百花繚乱編", 6: "第6篇",
    100: "最終篇_あまねく奇跡の始発点編"}


def read_rows(path):
    return json.loads(path.read_text(encoding="utf-8"))["DataList"]


class SpeakerMapping(dict):
    """Display-name lookup retains the official hash-key relation."""
    by_hash = None


def load_character_mappings():
    names = defaultdict(set)
    ids = {}
    for row in read_rows(BA_DATA_DIR / "DB/ScenarioCharacterNameExcelTable.json"):
        kr, jp = row.get("NameKR", "").strip(), row.get("NameJP", "").strip()
        ids[row["CharacterName"]] = jp
        if kr and jp:
            names[kr].add(jp)
    # Only unambiguous table names; preserve unknown aliases instead of guessing.
    mapping = SpeakerMapping({kr: next(iter(jps)) for kr, jps in names.items() if len(jps) == 1})
    mapping.by_hash = ids
    mapping.update({"선생님": "先生", "선생": "先生", "총학생회장": "連邦生徒会長",
                    "검은 양복": "黒服", "무명의 사제": "無名の司祭"})
    return mapping, ids


def load_group_metadata():
    print("[2/5] Building Scenario Group metadata index...")
    group_map = defaultdict(list)

    # 1. ScenarioModeExcelTable
    mode_file = BA_DATA_DIR / "DB" / "ScenarioModeExcelTable.json"
    with open(mode_file, 'r', encoding='utf-8') as f:
        mode_data = json.load(f)

    for r in mode_data['DataList']:
        mtype = r.get('ModeType', '')
        subtype = r.get('SubType', '')
        vol = r.get('VolumeId', 0)
        disp_vol = r.get('DisplayVolumeId', '')
        chap = r.get('ChapterId', 0)
        ep = r.get('EpisodeId', 0)

        # Categorize
        if mtype == 'SpecialOperation':
            cat = "特殊作戦"
            vol_name = (f"特殊作戦_デカグラマトン編_Vol.{vol}" if subtype == "Series1"
                        else f"特殊作戦_Series2_Vol.{vol}")
            chap_name = f"第{chap}章"
            ep_name = f"第{ep}話"
        elif mtype == 'Prologue':
            if subtype == 'Series2':
                cat = "主線_第2部"
                vol_name = "第2部_プロローグ"
            else:
                cat = "主線_第1部"
                vol_name = "第1部_プロローグ"
            chap_name = f"第{chap}章"
            ep_name = f"第{ep}話"
        elif mtype == 'Main':
            if subtype == 'Series2' or disp_vol != '':
                cat = "主線_第2部"
                v_num = disp_vol if disp_vol != '' else vol
                vol_name = f"第2部_Vol.{v_num}" if v_num != 0 else "第2部_Vol.0_連邦生徒会編"
            else:
                cat = "主線_第1部"
                vol_name = VOLUME_NAMES.get(vol, f"第{vol}篇")
            chap_name = f"第{chap}章"
            ep_name = f"第{ep}話"
        elif mtype == 'Sub':
            cat = "グループストーリー"
            vol_name = f"グループ_{vol}"
            chap_name = f"第{chap}章"
            ep_name = f"第{ep}話"
        elif mtype == 'Mini':
            cat = "ミニストーリー"
            vol_name = f"ミニ_{vol}"
            chap_name = f"第{chap}章"
            ep_name = f"第{ep}話"
        else:
            cat = mtype
            vol_name = f"Vol.{vol}"
            chap_name = f"第{chap}章"
            ep_name = f"第{ep}話"

        meta = {
            'category': cat,
            'volume': vol_name,
            'chapter': chap_name,
            'episode': ep_name,
            'mode_type': mtype,
            'sub_type': subtype
        }

        for gid in r.get('FrontScenarioGroupId', []):
            group_map[gid].append(dict(meta))
        for gid in r.get('BackScenarioGroupId', []):
            meta_back = dict(meta)
            meta_back['episode'] = f"{ep_name}_後編"
            group_map[gid].append(meta_back)

    # 2. EventContentScenarioExcelTable
    event_file = BA_DATA_DIR / "DB" / "EventContentScenarioExcelTable.json"
    with open(event_file, 'r', encoding='utf-8') as f:
        ev_data = json.load(f)

    for r in ev_data['DataList']:
        eid = r.get('EventContentId', 0)
        order = r.get('Order', 0)
        meta = {
            'category': "イベント",
            'volume': f"Event_{eid}",
            'chapter': f"Scene_{order}",
            'episode': f"Scene_{order}",
            'mode_type': "Event",
            'sub_type': ""
        }
        for gid in r.get('ScenarioGroupId', []):
            group_map[gid].append(dict(meta))

    # 3. AcademyFavorScheduleExcelTable (Bond)
    favor_file = BA_DATA_DIR / "DB" / "AcademyFavorScheduleExcelTable.json"
    with open(favor_file, 'r', encoding='utf-8') as f:
        favor_data = json.load(f)

    for r in favor_data['DataList']:
        cid = r.get('CharacterId', 0)
        rank = r.get('FavorRank', 0)
        order = r.get('OrderInGroup', 0)
        gid = r.get('ScenarioSriptGroupId')
        if gid:
            group_map[gid].append({
                'category': "絆ストーリー",
                'volume': f"Char_{cid}",
                'chapter': f"絆_{rank}",
                'episode': f"Ep_{order}",
                'mode_type': "Favor",
                'sub_type': ""
            })

    print(f"  Indexed {len(group_map)} total scenario groups.")
    return {gid: list({tuple(m.items()): m for m in metas}.values())
            for gid, metas in group_map.items()}



def resolve_speaker(raw, mapping):
    by_hash = getattr(mapping, "by_hash", None)
    if by_hash is not None:
        key = xxh32(raw.encode("utf-8"))
        if key in by_hash:
            return by_hash[key], "table_hash_key"
    if raw in mapping:
        return mapping[raw], "exact_display_alias"
    return raw, "unresolved"


def classify_text(script, names):
    if any(line.lower().startswith("#q;") for line in script.splitlines()):
        return "quiz_question_and_choices"
    if names:
        return "named_dialogue" if len(names) == 1 else "multiple_named_dialogue"
    lines = [line.strip() for line in script.splitlines() if line.strip()]
    if any(re.match(r"^\[(?:ns|s)\d*\]", line) for line in lines):
        return "choice_text"
    for token, kind in [("#na;", "unnamed_text"), ("#title;", "title"),
        ("#place;", "place"), ("#nextepisode;", "next_episode"),
        ("#ending;", "ending"), ("#stm;", "screen_text"),
        ("#str;", "screen_text"), ("#st;", "screen_text")]:
        if any(line.lower().startswith(token) for line in lines): return kind
    if lines and all(line.startswith("#") or re.match(r"^\d+;", line) for line in lines):
        return "control_or_display_text"
    return "plain_unlabelled_text"


def speaker_commands(script):
    """Only commands bearing actual dialogue, not character pose/display lines."""
    found = []
    for line in script.splitlines():
        parts = line.split(";")
        if len(parts) >= 3 and parts[0].lower() in ("#na", "#q") and ";".join(parts[2:]).strip():
            found.append(parts[1].strip())
        elif len(parts) >= 4 and parts[0].isdigit() and ";".join(parts[3:]).strip():
            found.append(parts[1].strip())
    return found


def extract_speaker(script_kr, kr2jp):
    names = speaker_commands(script_kr)
    if len(names) != 1:
        return "", ""
    return resolve_speaker(names[0], kr2jp)[0], names[0]


def build_database_and_markdown(output_dir):
    output_dir = Path(output_dir).resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"Build directory must be empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = output_dir / "story_index.db"
    stories_dir = output_dir / "stories"
    mapping, _ = load_character_mappings()
    locations = load_group_metadata()
    raw_dir = BA_DATA_DIR / "DB"
    shards = sorted(raw_dir.glob("ScenarioScriptExcelTable[0-9]*.json"),
                    key=lambda p: int(re.search(r"(\d+)\.json$", p.name).group(1)))
    if not shards:
        raise ValueError("No numbered script shards; inspect source layout before building")
    groups = defaultdict(list)
    source_manifest = []
    for path in shards:
        rows = read_rows(path)
        source_manifest.append({"file": path.name, "rows": len(rows),
                                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        for index, row in enumerate(rows, 1):
            groups[row["GroupId"]].append((path.name, index, row))
    aggregate_path = raw_dir / "ScenarioScriptExcelTable.json"
    aggregate_groups = defaultdict(list)
    for index, row in enumerate(read_rows(aggregate_path), 1):
        aggregate_groups[row["GroupId"]].append((aggregate_path.name, index, row))
    fallback_groups = sorted(aggregate_groups.keys() - groups.keys())
    for gid in fallback_groups:
        groups[gid] = aggregate_groups[gid]
    # Explicit discrepancy inventory. Never silently merge row-level variants.
    differences = []
    for gid in sorted(aggregate_groups.keys() & groups.keys()):
        a = [(r[2].get("TextJp", ""), r[2].get("ScriptKr", "")) for r in aggregate_groups[gid]]
        b = [(r[2].get("TextJp", ""), r[2].get("ScriptKr", "")) for r in groups[gid]]
        if a != b:
            differences.append({"group_id": gid, "aggregate_rows": len(a), "shard_rows": len(b),
                                "japanese_sequence_equal": [x[0] for x in a] == [x[0] for x in b]})
    conn = sqlite3.connect(db_path)
    conn.executescript("""
    CREATE TABLE dialogues (
      id INTEGER PRIMARY KEY, group_id INTEGER NOT NULL, category TEXT NOT NULL,
      volume TEXT NOT NULL, chapter TEXT NOT NULL, episode TEXT NOT NULL,
      speaker_jp TEXT, speaker_kr TEXT, text_jp TEXT NOT NULL, text_kr TEXT,
      selection_group INTEGER, source_file TEXT NOT NULL, source_row INTEGER NOT NULL,
      group_row INTEGER NOT NULL, speaker_resolution TEXT NOT NULL,
      markdown_path TEXT, text_kind TEXT NOT NULL, speaker_key INTEGER, UNIQUE(source_file, source_row));
    CREATE TABLE group_locations (group_id INTEGER, category TEXT, volume TEXT,
      chapter TEXT, episode TEXT, mode_type TEXT, sub_type TEXT);
    CREATE TABLE legacy_ids (legacy_id INTEGER PRIMARY KEY, dialogue_id INTEGER,
      match_kind TEXT NOT NULL);
    CREATE TABLE legacy_variants (legacy_id INTEGER PRIMARY KEY, group_id INTEGER,
      source_file TEXT, source_row INTEGER, group_row INTEGER, selection_group INTEGER,
      text_jp TEXT, text_kr TEXT, speaker_jp TEXT, speaker_kr TEXT, speaker_resolution TEXT);
    CREATE TABLE source_variants (group_id INTEGER, operation TEXT,
      aggregate_records TEXT, canonical_records TEXT);
    CREATE TABLE build_info (key TEXT PRIMARY KEY, value TEXT NOT NULL);
    """)
    paths = defaultdict(list)
    new_groups = defaultdict(list)
    unknowns = Counter()
    statuses = Counter()
    text_kinds = Counter()
    new_id = 0
    for gid, rows in groups.items():
        metas = locations.get(gid, [{"category": "その他_シナリオ", "volume": f"Group_{gid}",
            "chapter": "未分類", "episode": f"Ep_{gid}", "mode_type": "Unknown", "sub_type": ""}])
        for meta in metas:
            conn.execute("INSERT INTO group_locations VALUES (?,?,?,?,?,?,?)",
                         (gid, *(meta[k] for k in ("category", "volume", "chapter", "episode", "mode_type", "sub_type"))))
        meta = metas[0]
        rel = Path("02_corpus/stories") / meta["category"] / meta["volume"] / meta["chapter"] / (meta["episode"] + ".md")
        group_records = []
        for ordinal, (filename, source_row, row) in enumerate(rows, 1):
            txt = row.get("TextJp", "").strip()
            if not txt:
                continue
            script = row.get("ScriptKr", "")
            names = speaker_commands(script)
            if len(names) == 1:
                kr = names[0]
                jp, status = resolve_speaker(kr, mapping)
                if status == "unresolved": unknowns[kr] += 1
            else:
                jp = kr = ""
                status = "ambiguous" if names else "no_named_speaker"
            statuses[status] += 1
            kind = "hidden_label_text" if names and not jp else classify_text(script, names)
            text_kinds[kind] += 1
            new_id += 1
            conn.execute("INSERT INTO dialogues VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (new_id, gid, *(meta[k] for k in ("category", "volume", "chapter", "episode")),
                 jp, kr, txt, script, row.get("SelectionGroup", 0), filename, source_row,
                 ordinal, status, rel.as_posix(), kind, xxh32(kr.encode("utf-8")) if kr else None))
            new_groups[gid].append((txt, row.get("SelectionGroup", 0), new_id))
            group_records.append((new_id, jp, txt, filename, source_row, ordinal, status))
        if group_records:
            for loc in metas:
                path = Path(loc["category"]) / loc["volume"] / loc["chapter"] / (loc["episode"] + ".md")
                paths[path].append((gid, group_records))
    for path, scene_groups in paths.items():
        target = stories_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        content = ["<!-- Generated raw Japanese corpus; translations belong in evidence notes. -->",
                   "<!-- IDs refer to schema v2. See legacy_ids for pre-repair citations. -->", "",
                   "# " + str(path.with_suffix("")).replace("\\", " / "), ""]
        for gid, records in scene_groups:
            content.extend([f"## Group {gid}", ""])
            for did, jp, txt, filename, source_row, ordinal, status in records:
                content.extend([f"<!-- id={did}; group_row={ordinal}; source={filename}:{source_row}; speaker={status} -->",
                                f"**{jp}**: {txt}" if jp else txt, ""])
        target.write_text("\n".join(content), encoding="utf-8")
    # Preserve every differing aggregate/canonical Japanese block as a versioned source.
    variant_blocks = 0
    for gid in sorted(aggregate_groups.keys() & groups.keys()):
        old = [(i,r) for _,i,r in aggregate_groups[gid] if r.get("TextJp", "").strip()]
        new = [(f,i,r) for f,i,r in groups[gid] if r.get("TextJp", "").strip()]
        matcher = SequenceMatcher(None, [(r["TextJp"].strip(),r.get("SelectionGroup",0)) for _,r in old],
            [(r["TextJp"].strip(),r.get("SelectionGroup",0)) for _,_,r in new], autojunk=False)
        for op,a,b,x,y in matcher.get_opcodes():
            if op == "equal": continue
            before=[{"source_file":aggregate_path.name,"source_row":i,"text_jp":r["TextJp"],"script_kr":r["ScriptKr"]} for i,r in old[a:b]]
            after=[{"source_file":f,"source_row":i,"text_jp":r["TextJp"],"script_kr":r["ScriptKr"]} for f,i,r in new[x:y]]
            conn.execute("INSERT INTO source_variants VALUES (?,?,?,?)",(gid,op,json.dumps(before,ensure_ascii=False),json.dumps(after,ensure_ascii=False)))
            variant_blocks += 1
    # Reproduce old sequential IDs from its original three-table ingestion order.
    # Align whole group sequences, so legitimate repeated utterances stay distinct.
    legacy_id = 0
    legacy_matched = 0
    legacy_unmatched = 0
    for path in [aggregate_path, *shards]:
        old_groups = defaultdict(list)
        group_positions = Counter()
        for source_row, row in enumerate(read_rows(path), 1):
            group_positions[row["GroupId"]] += 1
            txt = row.get("TextJp", "").strip()
            if txt:
                legacy_id += 1
                old_groups[row["GroupId"]].append((txt, row.get("SelectionGroup", 0), legacy_id, source_row, group_positions[row["GroupId"]], row.get("ScriptKr", "")))
        for gid, old in old_groups.items():
            new = new_groups.get(gid, [])
            lookup = {}
            matcher = SequenceMatcher(None, [(r[0], r[1]) for r in old],
                                      [(r[0], r[1]) for r in new], autojunk=False)
            for a, b, length in matcher.get_matching_blocks():
                for offset in range(length): lookup[a + offset] = new[b + offset][2]
            for index, (old_txt, old_sel, old_id, source_row, group_row, old_script) in enumerate(old):
                matched = lookup.get(index)
                conn.execute("INSERT INTO legacy_ids VALUES (?,?,?)",
                             (old_id, matched, "sequence_text_selection" if matched else "unmatched_variant"))
                legacy_matched += matched is not None
                legacy_unmatched += matched is None
                if matched is None:
                    jp, kr = extract_speaker(old_script, mapping)
                    resolution = resolve_speaker(kr, mapping)[1] if kr else "no_named_speaker"
                    conn.execute("INSERT INTO legacy_variants VALUES (?,?,?,?,?,?,?,?,?,?,?)",(old_id,gid,path.name,source_row,group_row,old_sel,old_txt,old_script,jp,kr,resolution))
    conn.executescript("""
    CREATE INDEX idx_text_jp ON dialogues(text_jp);
    CREATE INDEX idx_speaker_jp ON dialogues(speaker_jp);
    CREATE INDEX idx_group_id ON dialogues(group_id,group_row);
    CREATE INDEX idx_volume ON dialogues(volume);
    CREATE INDEX idx_locations ON group_locations(volume,chapter,episode,group_id);
    """)
    commit = subprocess.check_output(["git", "-C", str(BA_DATA_DIR), "rev-parse", "HEAD"], text=True).strip()
    manifest = {"schema_version": 2, "raw_commit": commit,
        "source_policy": "Numbered shards in numeric order; aggregate only for otherwise absent groups",
        "sources": source_manifest, "aggregate_sha256": hashlib.sha256(aggregate_path.read_bytes()).hexdigest(),
        "aggregate_fallback_groups": fallback_groups, "aggregate_differences": differences,
        "indexed_text_records": new_id, "groups_with_text": len(new_groups),
        "markdown_files": len(paths), "speaker_resolution": dict(statuses), "text_kinds": dict(text_kinds),
        "unresolved_speakers": dict(unknowns.most_common()),
        "legacy_ids": legacy_id, "legacy_matched": legacy_matched, "legacy_unmatched": legacy_unmatched, "legacy_variants_preserved": legacy_unmatched, "source_variant_blocks": variant_blocks, "legacy_retrievable": legacy_matched + legacy_unmatched, "legacy_unavailable": 0,
        "limitations": ["Snapshot coverage, not proof of all released game content",
            "Speaker internal keys resolve by XXH32 to official display labels; unknown keys remain raw",
            "Unnamed text is explicitly classified by script syntax, without inventing a speaker identity",
            "Primary location is first metadata entry; all explicit aliases are preserved in group_locations"]}
    for key, value in manifest.items():
        conn.execute("INSERT INTO build_info VALUES (?,?)", (key, json.dumps(value, ensure_ascii=False)))
    conn.commit()
    if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise RuntimeError("SQLite integrity check failed")
    conn.close()
    (output_dir / "build_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k not in ("aggregate_differences", "unresolved_speakers")}, ensure_ascii=False, indent=2))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="Empty staging directory; active corpus is never overwritten")
    args = parser.parse_args()
    build_database_and_markdown(args.output_dir)
