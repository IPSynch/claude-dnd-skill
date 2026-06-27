"""
test_import_statblocks.py — statblock import into the supplemental library.

Exercises the pure helpers (CR→XP, record normalisation) and the file-mutating
commands (add / dedup-vs-SRD / update / list / remove / remove-book) against a
throwaway data dir, so the real bundled data files are never touched.

Run from repo root:
    python3 -m unittest tests.test_import_statblocks -v
"""
import importlib.util
import io
import json
import os
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

REPO = pathlib.Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "dnd" if (REPO / "skills" / "dnd").is_dir() else REPO
SCRIPTS = SKILL / "scripts"


def _import(name, filename):
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, str(SCRIPTS / filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


isb = _import("import_statblocks", "import_statblocks.py")
# Patch the SAME lookup instance that import_statblocks imported internally,
# not a fresh copy — otherwise path redirection in tests wouldn't take effect.
lk = isb.lk


class TestPureHelpers(unittest.TestCase):
    def test_cr_key_fractions(self):
        self.assertEqual(isb._cr_key("1/4"), "1/4")
        self.assertEqual(isb._cr_key(0.25), "1/4")
        self.assertEqual(isb._cr_key(0.5), "1/2")
        self.assertEqual(isb._cr_key(0.125), "1/8")
        self.assertEqual(isb._cr_key(5), "5")
        self.assertEqual(isb._cr_key(5.0), "5")

    def test_normalise_derives_index_and_xp(self):
        rec, warns = isb._normalise_record({"name": "Clockwork Dragon", "cr": 5}, "Tome of Beasts")
        self.assertEqual(rec["index"], "clockwork-dragon")
        self.assertEqual(rec["xp"], 1800)          # CR 5 → 1800 XP
        self.assertEqual(rec["cr"], 5)             # integer CR stored as int
        self.assertEqual(rec["_source"], "Tome of Beasts")
        # abilities defaulted to 10
        for ab in isb.ABILITIES:
            self.assertEqual(rec[ab], 10)

    def test_normalise_fractional_cr_kept_as_string(self):
        rec, _ = isb._normalise_record({"name": "Imp Spawn", "cr": "1/4"}, "Book")
        self.assertEqual(rec["cr"], "1/4")
        self.assertEqual(rec["xp"], 50)

    def test_normalise_explicit_xp_wins(self):
        rec, _ = isb._normalise_record({"name": "X", "cr": 5, "xp": 9999}, "Book")
        self.assertEqual(rec["xp"], 9999)

    def test_normalise_requires_name(self):
        with self.assertRaises(ValueError):
            isb._normalise_record({"cr": 1}, "Book")

    def test_parse_records_forms(self):
        self.assertEqual(len(isb._parse_records('{"name":"A"}')), 1)
        self.assertEqual(len(isb._parse_records('[{"name":"A"},{"name":"B"}]')), 2)
        self.assertEqual(len(isb._parse_records('{"monsters":[{"name":"A"}]}')), 1)


class TestFileCommands(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.supp = os.path.join(self.tmp, "supp.json")
        self.srd = os.path.join(self.tmp, "srd.json")
        # A minimal SRD with one monster, to test dedup-vs-SRD.
        with open(self.srd, "w") as f:
            json.dump({"_meta": {}, "monsters": [{"name": "Goblin", "index": "goblin", "cr": "1/4"}]}, f)
        # Redirect lookup's path resolution at the module-global level.
        self._orig_supp = lk.SUPPLEMENTAL_FILE_2014
        self._orig_srd = lk.DATA_FILE_2014
        lk.SUPPLEMENTAL_FILE_2014 = self.supp
        lk.DATA_FILE_2014 = self.srd

    def tearDown(self):
        lk.SUPPLEMENTAL_FILE_2014 = self._orig_supp
        lk.DATA_FILE_2014 = self._orig_srd

    def _add(self, records, book="Tome of Beasts"):
        buf, err = io.StringIO(), io.StringIO()
        with redirect_stdout(buf), redirect_stderr(err):
            rc = isb.cmd_add(records, book, "2014")
        return rc, buf.getvalue(), err.getvalue()

    def _read_supp(self):
        with open(self.supp) as f:
            return json.load(f)

    def test_add_new_monster(self):
        rc, out, _ = self._add([{"name": "Clockwork Dragon", "cr": 5, "hp": 195, "ac": 19}])
        self.assertEqual(rc, 0)
        data = self._read_supp()
        self.assertEqual(len(data["monsters"]), 1)
        m = data["monsters"][0]
        self.assertEqual(m["name"], "Clockwork Dragon")
        self.assertEqual(m["xp"], 1800)
        self.assertEqual(m["_source"], "Tome of Beasts")
        self.assertIn("Tome of Beasts", data["_meta"]["sources"])

    def test_dedup_against_srd(self):
        rc, out, err = self._add([{"name": "Goblin", "cr": "1/4"}])
        self.assertEqual(rc, 0)
        # Goblin is in the SRD, so it must be skipped, not written.
        self.assertEqual(self._read_supp().get("monsters", []), [])
        self.assertIn("already in the bundled SRD", err)

    def test_reimport_updates_not_duplicates(self):
        self._add([{"name": "Clockwork Dragon", "cr": 5, "hp": 195}])
        self._add([{"name": "Clockwork Dragon", "cr": 6, "hp": 200}])
        monsters = self._read_supp()["monsters"]
        self.assertEqual(len(monsters), 1)          # updated, not duplicated
        self.assertEqual(monsters[0]["cr"], 6)
        self.assertEqual(monsters[0]["hp"], 200)

    def test_add_requires_source_book(self):
        rc, _, err = self._add([{"name": "X"}], book="")
        self.assertEqual(rc, 1)
        self.assertIn("--source-book is required", err)

    def test_remove_by_name(self):
        self._add([{"name": "Clockwork Dragon", "cr": 5}, {"name": "Gearforged", "cr": 1}])
        rc = isb.cmd_remove("Clockwork Dragon", "2014")
        self.assertEqual(rc, 0)
        names = [m["name"] for m in self._read_supp()["monsters"]]
        self.assertEqual(names, ["Gearforged"])

    def test_remove_book(self):
        self._add([{"name": "A", "cr": 1}], book="Tome of Beasts")
        self._add([{"name": "B", "cr": 1}], book="Creature Codex")
        rc = isb.cmd_remove_book("Tome of Beasts", "2014")
        self.assertEqual(rc, 0)
        data = self._read_supp()
        self.assertEqual([m["name"] for m in data["monsters"]], ["B"])
        self.assertNotIn("Tome of Beasts", data["_meta"]["sources"])

    def test_list_runs(self):
        self._add([{"name": "Clockwork Dragon", "cr": 5}])
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = isb.cmd_list("2014")
        self.assertEqual(rc, 0)
        self.assertIn("Clockwork Dragon", buf.getvalue())

    def test_imported_monster_is_findable_via_lookup(self):
        """End-to-end: an imported statblock resolves through lookup.py's merge."""
        self._add([{"name": "Clockwork Dragon", "cr": 5, "hp": 195, "ac": 19}])
        # Clear lookup caches so it re-reads our redirected files.
        lk._data_by_rs.clear()
        lk._index_by_rs.clear()
        rec = lk.lookup_record("Clockwork Dragon", "monster", "2014")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["name"], "Clockwork Dragon")


if __name__ == "__main__":
    unittest.main()
