import unittest
from engineering.benchmark import benchmark

class BenchmarkTests(unittest.TestCase):
    def test_index_preserves_results_and_changes_plan(self):
        result=benchmark(10000,2)
        self.assertEqual(result['before']['result_sha256'],result['after']['result_sha256'])
        self.assertTrue(any('SCAN activity' in p for p in result['before']['plan']))
        self.assertTrue(any('COVERING INDEX' in p for p in result['after']['plan']))
        self.assertGreater(result['indexed_bytes'],result['table_bytes'])
