#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_tools/build_index.py - Build fast SQLite database index for Blue Archive story corpus.
"""

import os
import re
import sqlite3
import time
from pathlib import Path

CORPUS_ROOT = Path(__file__).resolve().parent.parent / "02_corpus" / "ba-storybook" / "ba-stories"
DB_PATH = Path(__file__).resolve().parent.parent / "02_corpus" / "story_index.db"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SPEAKER_RE = re.compile(r'^\*\*([^*]+)\*\*:\s*(.*)$')
PAREN_SPEAKER_RE = re.compile(r'^\*（([^）]+)）\s*(.*)\*$')

def build_index():
    print(f"Building SQLite database index from: {CORPUS_ROOT}")
    start_t = time.time()
    
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE dialogues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT NOT NULL,
        category TEXT NOT NULL,
        volume TEXT NOT NULL,
        chapter TEXT NOT NULL,
        line_no INTEGER NOT NULL,
        speaker TEXT,
        text TEXT NOT NULL
    )
    """)

    cur.execute("CREATE INDEX idx_text ON dialogues(text)")
    cur.execute("CREATE INDEX idx_speaker ON dialogues(speaker)")
    cur.execute("CREATE INDEX idx_category ON dialogues(category)")
    cur.execute("CREATE INDEX idx_volume ON dialogues(volume)")

    total_files = 0
    total_lines = 0
    records = []

    for root, _, files in os.walk(CORPUS_ROOT):
        rel_dir = os.path.relpath(root, CORPUS_ROOT)
        cat = rel_dir.split(os.sep)[0]
        vol = rel_dir.split(os.sep)[1] if os.sep in rel_dir else cat

        for fname in sorted(files):
            if not fname.endswith(".md") or fname in ("README.md", "CLAUDE.md", "PLAN.md"):
                continue

            file_path = Path(root) / fname
            rel_file = file_path.relative_to(PROJECT_ROOT).as_posix()
            
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            total_files += 1

            # Extract chapter title from frontmatter
            chapter_title = fname
            lines = content.splitlines()
            body_start = 0
            if lines and lines[0].strip().startswith("---"):
                for i in range(1, len(lines)):
                    if lines[i].strip() == "---":
                        body_start = i + 1
                        break
                    if lines[i].strip().startswith("chapter:"):
                        chapter_title = lines[i].split(":", 1)[1].strip().strip('"\'')

            for l_idx in range(body_start, len(lines)):
                raw_line = lines[l_idx].strip()
                if not raw_line or raw_line.startswith("#"):
                    continue

                line_no = l_idx + 1
                speaker = ""
                dialogue_text = raw_line

                # Check speaker patterns
                m1 = SPEAKER_RE.match(raw_line)
                if m1:
                    speaker = m1.group(1).strip()
                    dialogue_text = m1.group(2).strip()
                else:
                    m2 = PAREN_SPEAKER_RE.match(raw_line)
                    if m2:
                        speaker = m2.group(1).strip()
                        dialogue_text = m2.group(2).strip()

                records.append((rel_file, cat, vol, chapter_title, line_no, speaker, dialogue_text))
                total_lines += 1

                if len(records) >= 10000:
                    cur.executemany("""
                    INSERT INTO dialogues (file_path, category, volume, chapter, line_no, speaker, text)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, records)
                    records = []

    if records:
        cur.executemany("""
        INSERT INTO dialogues (file_path, category, volume, chapter, line_no, speaker, text)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, records)

    conn.commit()
    conn.close()

    elapsed = time.time() - start_t
    db_size = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] Indexed {total_files} files, {total_lines} dialogue lines in {elapsed:.2f}s.")
    print(f"Database saved to: {DB_PATH} ({db_size:.2f} MB)")

if __name__ == "__main__":
    build_index()
