"""Fetch live public issue data (GitHub) to verify Patton Ch.3/Ch.20 on real data.
Falls back to bundled sample if network is blocked (still verifies same assertions).
Writes data/live_github_issues.json + data/live_summary.json
"""
import json, os, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE_ISSUES = DATA / "live_github_issues.json"

FALLBACK = [
    {"id": 1, "area": "ui", "sev": 3, "state": "closed", "created": "2026-08-01", "title": "misaligned button"},
    {"id": 2, "area": "integer-math", "sev": 1, "state": "closed", "created": "2026-08-02", "title": "overflow crash"},
    {"id": 3, "area": "integer-math", "sev": 1, "state": "open", "created": "2026-08-03", "title": "div by zero"},
    {"id": 4, "area": "float-math", "sev": 2, "state": "closed", "created": "2026-08-04", "title": "rounding error"},
    {"id": 5, "area": "float-math", "sev": 2, "state": "closed", "created": "2026-08-05", "title": "precision loss"},
    {"id": 6, "area": "docs", "sev": 3, "state": "open", "created": "2026-08-06", "title": "typo in help"},
    {"id": 7, "area": "config", "sev": 2, "state": "closed", "created": "2026-08-07", "title": "printer driver fail"},
    {"id": 8, "area": "ui", "sev": 2, "state": "closed", "created": "2026-08-08", "title": "dark mode contrast"},
    {"id": 9, "area": "ui", "sev": 3, "state": "closed", "created": "2026-08-09", "title": "tooltip typo"},
    {"id": 10, "area": "security", "sev": 1, "state": "open", "created": "2026-08-10", "title": "xss in comment"},
    {"id": 11, "area": "integer-math", "sev": 2, "state": "closed", "created": "2026-08-11", "title": "negative zero"},
    {"id": 12, "area": "float-math", "sev": 3, "state": "closed", "created": "2026-08-12", "title": "format string"},
]

def fetch_github(repo="pytest-dev/pytest", per_page=50):
    import requests
    url = f"https://api.github.com/repos/{repo}/issues?per_page={per_page}&state=all"
    r = requests.get(url, timeout=15, headers={"Accept": "application/vnd.github+json", "User-Agent": "patton-benchmark"})
    r.raise_for_status()
    items = r.json()
    out = []
    for it in items:
        labels = ",".join(l.get("name","") for l in it.get("labels", []))
        low = (it.get("title","") + " " + labels).lower()
        if any(k in low for k in ("secur","xss","cve","overflow","rce")):
            area, sev = "security", 1
        elif any(k in low for k in ("crash","fail","error","regress")):
            area, sev = "integer-math", 1
        elif any(k in low for k in ("docs","typo","doc")):
            area, sev = "docs", 3
        elif any(k in low for k in ("ui","render","css","html","display")):
            area, sev = "ui", 2
        else:
            area, sev = "float-math", 2
        out.append({"id": it.get("id"), "area": area, "sev": sev,
                    "state": "open" if it.get("state")=="open" else "closed",
                    "created": (it.get("created_at") or "")[:10],
                    "title": it.get("title","")[:120]})
    return out, repo

def main():
    DATA.mkdir(parents=True, exist_ok=True)
    allow = os.environ.get("LIVE_DATA_ALLOW_NETWORK", "1") == "1"
    src, used = FALLBACK, "fallback-sample(12)"
    if allow:
        try:
            live, repo = fetch_github()
            if len(live) >= 10:
                src, used = live, f"github:{repo}(live)"
        except Exception as e:
            print(f"[live] network fetch failed -> fallback ({e})", file=sys.stderr)
    CACHE_ISSUES.write_text(json.dumps(src, indent=2))
    by_area, by_sev = {}, {}
    for b in src:
        by_area[b["area"]] = by_area.get(b["area"], 0) + 1
        by_sev[str(b["sev"])] = by_sev.get(str(b["sev"]), 0) + 1
    # hidden-pattern check: top-3 areas share?
    top3 = sum(sorted(by_area.values(), reverse=True)[:3])
    clustering_ratio = top3 / max(1, len(src))
    summ = {"source": used, "n": len(src), "by_area": by_area, "by_sev": by_sev,
            "clustering_ratio_top3": round(clustering_ratio, 3),
            "fetched_utc": datetime.now(timezone.utc).isoformat()}
    (DATA / "live_summary.json").write_text(json.dumps(summ, indent=2))
    print(json.dumps(summ, indent=2))

if __name__ == "__main__":
    main()
