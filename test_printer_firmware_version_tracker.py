import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check, compare_versions, parse_version

def row(p, m, v):
    return {"printer": p, "model": m, "firmware_version": v}

class TestFirmwareVersions(unittest.TestCase):
    def test_compare_newer(self):
        self.assertEqual(compare_versions("1.10", "1.9"), 1)
    def test_compare_older(self):
        self.assertEqual(compare_versions("1.9", "1.10"), -1)
    def test_compare_equal(self):
        self.assertEqual(compare_versions("2.0.1", "2.0.1"), 0)
    def test_update_needed(self):
        self.assertEqual(check([row("HP-1", "LaserJet", "1.9")], {"LaserJet": "2.0"})[0][4], "UPDATE")
    def test_ok_at_minimum(self):
        self.assertEqual(check([row("HP-1", "LaserJet", "2.0")], {"LaserJet": "2.0"})[0][4], "OK")
    def test_unknown_model(self):
        self.assertEqual(check([row("HP-1", "Mystery", "1.0")], {"LaserJet": "2.0"})[0][4], "UNKNOWN")
    def test_updates_first(self):
        r = check([row("A", "M", "2.0"), row("B", "M", "1.0")], {"M": "2.0"})
        self.assertEqual(r[0][0], "B")
