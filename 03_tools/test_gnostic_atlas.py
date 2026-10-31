"""Regression checks for the semantic and rendering failures in the external review."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent.parent

class AtlasReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'06_comparative_analysis/gnostic_atlas/atlas_data.json').read_text(encoding='utf-8'))
        cls.nodes={n['id']:n for n in cls.data['nodes']}
        cls.edges=cls.data['edges']

    def relation(self, source, target, kind=None):
        return any(e['from_id']==source and e['to_id']==target and (kind is None or e['type']==kind) for e in self.edges)

    def test_identifiers_sources_and_endpoints(self):
        self.assertEqual(len(self.nodes),len(self.data['nodes']))
        self.assertEqual(len({e['id'] for e in self.edges}),len(self.edges))
        for e in self.edges:
            self.assertIn(e['from_id'],self.nodes)
            self.assertIn(e['to_id'],self.nodes)
            self.assertIn(e['source'],self.data['sources'])
            self.assertTrue(e['label'] and e['locator'])

    def test_only_one_original_sophia_and_twelve_attendants(self):
        self.assertNotIn('aj-eleleth2',self.nodes)
        self.assertIn('Wisdom',self.nodes['aj-sophia']['aliases'])
        lights={'aj-'+x for x in ['harmozel','oroiael','daveithe','eleleth']}
        membership=[e for e in self.edges if e['from_id'] in lights and e['type']=='membership']
        self.assertEqual(len(membership),12)
        self.assertTrue(self.relation('aj-eleleth','aj-sophia','membership'))
        self.assertLess(self.nodes['aj-sophia']['tier'],self.nodes['aj-repentant']['tier'])
        self.assertTrue(self.relation('aj-sophia','aj-ninth','state'))

    def test_joint_sources_of_autogenes_and_attributes(self):
        for origin in ['aj-monad','aj-barbelo']:
            self.assertTrue(self.relation(origin,'aj-autogenes','generation'))
        for key in ['foreknow','incorrupt','life','truth']:
            self.assertTrue(self.relation('aj-monad','aj-'+key,'emanation'))
            self.assertTrue(self.relation('aj-barbelo','aj-'+key,'request'))

    def test_genealogy_is_not_replaced_by_residence(self):
        self.assertTrue(self.relation('aj-adamas','aj-seth','generation'))
        self.assertTrue(self.relation('aj-seth','aj-seed','descent'))
        for a,b in [('harmozel','adamas'),('oroiael','seth'),('daveithe','seed'),('eleleth','repentant')]:
            self.assertTrue(self.relation('aj-'+a,'aj-'+b,'location'))

    def test_adam_has_model_material_power_and_help(self):
        for a,b,kind in [('adamas','adam','image'),('body','adam','formation'),('yald','adam','power'),('epinoia','adam','assistance')]:
            self.assertTrue(self.relation('aj-'+a,'aj-'+b,kind))
        self.assertTrue(self.relation('aj-sophia','aj-yald','power'))
        self.assertTrue(self.relation('aj-five-lights','aj-yald','assistance'))

    def test_adam_does_not_generate_his_constraints_or_upper_spirit(self):
        for key in ['spirit','counterfeit','fate']:
            self.assertFalse(self.relation('aj-adam','aj-'+key))
        self.assertTrue(self.relation('aj-yald','aj-counterfeit','control'))
        self.assertTrue(self.relation('aj-yald','aj-fate','control'))
        self.assertTrue(self.relation('aj-monad','aj-spirit','source'))

    def test_eve_has_distinct_sources_and_five_seals_has_correct_actor(self):
        self.assertTrue(self.relation('aj-yald','aj-eve','formation'))
        self.assertTrue(self.relation('aj-adam','aj-eve','material'))
        self.assertTrue(self.relation('aj-epinoia','aj-eve','image'))
        self.assertTrue(self.relation('aj-barbelo','aj-return','action'))
        self.assertFalse(self.relation('aj-epinoia','aj-return'))

    def test_lists_keep_distinct_membership_and_no_forced_identity(self):
        self.assertEqual(self.nodes['aj-twelve']['tier'],self.nodes['aj-seven']['tier'])
        for group,count in [('aj-twelve',12),('aj-seven',7)]:
            entries=[e for e in self.edges if e['from_id']==group and e['type']=='membership']
            self.assertEqual(len(entries),count)
            for e in entries:self.assertGreater(self.nodes[e['to_id']]['tier'],self.nodes[group]['tier'])
        self.assertFalse(any(e['type']=='identity' and e['system']=='aj' for e in self.edges))

if __name__=='__main__':unittest.main()
