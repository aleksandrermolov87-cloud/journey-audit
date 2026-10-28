"""Smoke tests for skills/journey-audit/scripts/journey_check.py (standard library only)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "journey-audit", "scripts", "journey_check.py")
EXAMPLE = os.path.join(ROOT, "examples", "card-reissue", "journey.json")


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


class CheckTests(unittest.TestCase):
    def test_check_finds_expected_codes(self):
        res = json.loads(run("check", EXAMPLE, "--json").stdout)
        codes = {f["id"] for f in res}
        for code in ("L04", "L05", "L10", "L12", "L13", "L14", "L17", "L19"):
            self.assertIn(code, codes)

    def test_branch_ids_are_not_double_prefixed(self):
        res = json.loads(run("check", EXAMPLE, "--json").stdout)
        self.assertFalse([f for f in res if str(f["step"]).startswith("b1.b1.")])

    def test_russian_output(self):
        out = run("check", EXAMPLE, "--lang", "ru").stdout
        self.assertIn("Находок", out)


class LoadTests(unittest.TestCase):
    def test_system_steps_do_not_raise_exit_risk_by_index(self):
        res = json.loads(run("load", EXAMPLE, "--json").stdout)
        system = [r for r in res["rows"] if r["actor"] != "user"]
        for r in system:
            self.assertFalse([x for x in r["exit_risk"] if "index" in x])

    def test_low_profile_is_heavier(self):
        low = json.loads(run("load", EXAMPLE, "--json", "--persona-tech", "low").stdout)
        high = json.loads(run("load", EXAMPLE, "--json", "--persona-tech", "high").stdout)
        self.assertGreater(low["peak"]["index"], high["peak"]["index"])
        self.assertGreater(low["total_klm_s"], high["total_klm_s"])


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp()
        shutil.copy(EXAMPLE, os.path.join(self.work, "journey.json"))
        for fam in ("cjm", "edge", "load"):
            os.makedirs(os.path.join(self.work, fam))
        base = {"severity": "high", "title": "t", "evidence_class": "interpretation", "confidence": "med"}
        self.write("cjm", [dict(base, id="CJM-01", family="cjm", check="L05", steps=["s3"], root_cause="dead-end-failure")])
        self.write("edge", [dict(base, id="EDGE-01", family="edge", check="E07", steps=["s3", "s4"], frequency=2, impact=3,
                                 root_cause="dead-end-failure")])
        self.write("load", [dict(base, id="LOAD-01", family="load", check="C-s7", steps=["s7"], root_cause="mobile-context",
                                 report=None)])

    def tearDown(self):
        shutil.rmtree(self.work)

    def write(self, fam, items, report_md="# Report\n"):
        with open(os.path.join(self.work, fam, "findings.json"), "w", encoding="utf-8") as f:
            json.dump({"family": fam, "findings": items, "report_md": report_md}, f)

    def test_contract_ok_and_merge_clusters_same_cause(self):
        self.assertEqual(run("findings", self.work).returncode, 0)
        merged = json.loads(run("merge", self.work).stdout)
        self.assertEqual(merged["total_findings"], 3)
        self.assertEqual(len(merged["clusters"]), 2)

    def test_contract_rejects_unknown_step(self):
        self.write("load", [{"id": "LOAD-01", "family": "load", "check": "C-x", "severity": "high", "steps": ["zz"],
                             "title": "t", "evidence_class": "hypothesis", "confidence": "low"}])
        res = run("findings", self.work)
        self.assertEqual(res.returncode, 1)
        self.assertIn("zz", res.stdout)

    def test_render_writes_reports(self):
        run("render", self.work)
        self.assertTrue(os.path.exists(os.path.join(self.work, "cjm", "report.md")))


if __name__ == "__main__":
    unittest.main()
