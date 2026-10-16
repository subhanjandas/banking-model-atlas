"""Mutation tests prove malformed metadata is rejected, without pretending to test banking data."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_model import validate

class ModelContractTests(unittest.TestCase):
    def setUp(self):self.m=json.loads((ROOT/'model/banking.model.json').read_text())
    def rejects(self,needle):self.assertTrue(any(needle in e for e in validate(self.m)),validate(self.m))
    def test_baseline(self):self.assertEqual(validate(self.m),[])
    def test_duplicate_entity(self):self.m['entities'].append(copy.deepcopy(self.m['entities'][0]));self.rejects('duplicate ID')
    def test_unknown_domain(self):self.m['entities'][0]['domain']='missing';self.rejects('unknown domain')
    def test_missing_grain(self):del self.m['entities'][0]['grain'];self.rejects('missing grain')
    def test_nullable_primary_key(self):self.m['entities'][0]['columns'][0]['nullable']=True;self.rejects('nullable primary key')
    def test_dangling_fk(self):self.m['relationships'][0]['target_entity']='missing';self.rejects('broken relationship')
    def test_bad_key_type(self):self.m['entities'][0]['columns'][0]['type']='integer';self.rejects('mismatched key types')
    def test_optional_cardinality(self):self.m['relationships'][0]['source_to_target']='zero_or_one';self.rejects('nullability/cardinality')
    def test_reverse_cardinality(self):self.m['relationships'][0]['target_to_source']='zero_or_one';self.rejects('reverse cardinality')
    def test_missing_fk(self):self.m['relationships'].pop(0);self.rejects('identifier has no relationship')
    def test_unknown_journey_entity(self):self.m['journeys'][0]['steps'][0]['entity']='missing';self.rejects('invalid journey step')
    def test_disconnected_journey(self):self.m['journeys'][0]['relationship_ids'].pop(0);self.rejects('disconnected journey')
    def test_unjustified_enforcement_claim(self):self.m['rules'][0]['implementation_status']='enforced';self.rejects('must not claim')
    def test_rule_backlink(self):self.m['rules'][0]['entities'].append('customer');self.rejects('backlink')
    def test_bad_type(self):self.m['entities'][0]['columns'][0]['type']='money';self.rejects('unsupported type')
    def test_bad_unique_key(self):self.m['entities'][0]['unique_keys']=[['missing']];self.rejects('invalid unique key')
    def test_unsupported_schema(self):self.m['schema_version']='9';self.rejects('Unsupported metadata')
    def test_nonobject_model(self):self.assertEqual(validate([]),['Model must be an object'])

if __name__=='__main__':unittest.main()
