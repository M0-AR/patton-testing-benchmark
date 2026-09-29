"""E05: Patton Ch.3/Ch.20 verified on LIVE public data (GitHub) + fallback.
Asserts: bugs cluster (top-3 areas >=50%), sev distribution sane, live file exists.
Run: python scripts/fetch_live_data.py before pytest (or test auto-runs fallback check).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "live_summary.json"
ISSUES = ROOT / "data" / "live_github_issues.json"

def _load():
    assert SUMMARY.exists(), "run python scripts/fetch_live_data.py first"
    assert ISSUES.exists(), "missing live issues file"
    return json.loads(SUMMARY.read_text()), json.loads(ISSUES.read_text())

def test_live_files_exist_and_sane():
    s, issues = _load()
    assert s["n"] >= 10, s
    assert 0.0 <= s["clustering_ratio_top3"] <= 1.0

def test_hidden_pattern_bug_clustering():
    """Patton axiom 'bugs follow bugs': top-3 areas hold majority of defects."""
    s, _ = _load()
    assert s["clustering_ratio_top3"] >= 0.5, f"no clustering? {s}"

def test_severity_not_all_trivial():
    s, _ = _load()
    sev1_2 = int(s["by_sev"].get("1",0)) + int(s["by_sev"].get("2",0))
    assert sev1_2 >= 1, f"expected at least one sev1/2 in live data: {s['by_sev']}"

def test_source_is_declared():
    s, _ = _load()
    assert s["source"].startswith(("github:", "fallback-sample")), s["source"]
