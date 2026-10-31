"""Regression tests for real corpus corruption found during handover."""
import sqlite3
import unittest
from pathlib import Path
import build_complete_corpus as builder
import search

DATABASE_PATH = search.DB_PATH

class SpeakerParserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping, _ = builder.load_character_mappings()

    def test_pose_before_actual_unnamed_voice(self):
        script = "3;아리스 결전 비무장;03\n#na;부드러운 목소리;실제 발언"
        self.assertEqual(builder.extract_speaker(script, self.mapping), ("柔らかい声", "부드러운 목소리"))

    def test_pose_before_actual_visible_speaker(self):
        self.assertEqual(builder.extract_speaker("2;케이;06\n3;아리스;09;발언", self.mapping)[0], "アリス")

    def test_character_substring_collision(self):
        self.assertEqual(builder.extract_speaker("3;히마리 방한복;01;발언", self.mapping)[0], "ヒマリ")

    def test_same_display_name_keeps_distinct_internal_key(self):
        self.assertEqual(builder.extract_speaker("#na;가짜 총학생회장;발언", self.mapping), ("連邦生徒会長", "가짜 총학생회장"))

    def test_commands_without_text_are_not_speakers(self):
        self.assertEqual(builder.extract_speaker("3;아리스;01\n#3;em;[반응]", self.mapping), ("", ""))

    def test_ambiguous_multi_speaker_stays_unresolved(self):
        self.assertEqual(builder.extract_speaker("3;아리스;01;하나\n2;케이;01;둘", self.mapping), ("", ""))

    def test_hash_vectors_and_missing_alias(self):
        from xxhash32 import xxh32
        for value, expected in [(b"",0x02cc5d05),(b"a",0x550d7456),(b"abc",0x32d153ff)]:
            self.assertEqual(xxh32(value), expected)
        self.assertEqual(builder.resolve_speaker("not a real script key", self.mapping)[1], "unresolved")

    def test_unnamed_text_and_choice_are_explicit(self):
        self.assertEqual(builder.classify_text("#na;unnamed dialogue", []), "unnamed_text")
        self.assertEqual(builder.classify_text('[s1] "yes"', []), "choice_text")

    def test_question_presenter_and_answers(self):
        script='#Q;쿠루미;질문\n[as1] 답변'
        self.assertEqual(builder.extract_speaker(script,self.mapping)[0],"クルミ")
        self.assertEqual(builder.classify_text(script,builder.speaker_commands(script)),"quiz_question_and_choices")

    def test_uppercase_na(self):
        self.assertEqual(builder.extract_speaker("#NA;부드러운 목소리;발언", self.mapping)[0], "柔らかい声")

class CorpusRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = search.get_db_connection(DATABASE_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_integrity(self):
        self.assertEqual(self.conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")

    def test_invitation_has_correct_speaker_and_single_occurrence(self):
        rows = search.search_db(self.conn, query="この先の彼方は", group_id=10052195)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["speaker"], "柔らかい声")

    def test_identity_line_has_correct_speaker(self):
        rows = search.search_db(self.conn, query="私の正体に気づいているケイ", group_id=10052195)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["speaker"], "柔らかい声")

    def test_series_do_not_share_special_operation_path(self):
        a = self.conn.execute("SELECT volume FROM dialogues WHERE group_id=90001020 LIMIT 1").fetchone()[0]
        b = self.conn.execute("SELECT volume FROM dialogues WHERE group_id=90101020 LIMIT 1").fetchone()[0]
        self.assertNotEqual(a, b)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM dialogues WHERE group_id=90001020").fetchone()[0], 179)

    def test_speaker_filter_does_not_search_text(self):
        self.assertFalse(search.search_db(self.conn, query="私の正体に気づいているケイ", speaker="ケイ", speaker_exact=True))

    def test_legacy_id_can_be_resolved(self):
        did = self.conn.execute("SELECT dialogue_id FROM legacy_ids WHERE legacy_id=344595").fetchone()[0]
        r = search.search_db(self.conn, dialogue_id=did)[0]
        self.assertEqual(r["speaker"], "柔らかい声")
        self.assertIn("この先の彼方は", r["text_jp"])

    def test_all_speakers_resolve_to_source_table_keys(self):
        self.assertEqual(self.conn.execute("SELECT count(*) FROM dialogues WHERE speaker_resolution='unresolved'").fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM dialogues WHERE speaker_kr!='' AND speaker_key IS NULL").fetchone()[0], 0)

    def test_every_legacy_id_has_canonical_or_preserved_variant(self):
        self.assertEqual(self.conn.execute("SELECT count(*) FROM legacy_ids l LEFT JOIN legacy_variants v ON l.legacy_id=v.legacy_id WHERE l.dialogue_id IS NULL AND v.legacy_id IS NULL").fetchone()[0],0)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM legacy_variants").fetchone()[0],151)
        old_id=self.conn.execute("SELECT legacy_id FROM legacy_variants LIMIT 1").fetchone()[0]
        result=search.legacy_variant_result(self.conn,old_id,1)
        self.assertEqual(result["source_version"],"aggregate_variant")
        self.assertEqual(result["legacy_id"],old_id)

    def test_president_core_passages_survive(self):
        rows = search.search_db(self.conn, query="私のミスでした", max_results=0)
        self.assertEqual({r["group_id"] for r in rows}, {11000, 103110})
        youngest = search.search_db(self.conn, query="史上最年少")
        self.assertEqual(len(youngest), 1)
        self.assertEqual(youngest[0]["speaker"], "アユム")

    def test_split_group_is_concatenated_without_loss(self):
        self.assertEqual(self.conn.execute("SELECT count(*) FROM dialogues WHERE group_id=10014085").fetchone()[0], 51)
        self.assertEqual(self.conn.execute("SELECT count(distinct source_file) FROM dialogues WHERE group_id=10014085").fetchone()[0], 2)

    def test_raw_provenance_and_row_uniqueness(self):
        self.assertEqual(self.conn.execute("SELECT count(*) FROM dialogues WHERE source_row<1 OR group_row<1").fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM (SELECT source_file,source_row FROM dialogues GROUP BY 1,2 HAVING count(*)>1)").fetchone()[0], 0)

    def test_context_counts_text_records_not_raw_action_gaps(self):
        r = search.search_db(self.conn, query="忘却は", group_id=10052195)[0]
        lines = search.get_dialogue_context(self.conn, r["id"], 3)
        self.assertEqual(len(lines), 7)
        self.assertEqual(sum(line.startswith(">>") for line in lines), 1)

    def test_metadata_aliases_are_searchable(self):
        rows = search.search_db(self.conn, query="私のミスでした", volume="第0篇_プロローグ")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["group_id"], 11000)

if __name__ == "__main__":
    unittest.main()
