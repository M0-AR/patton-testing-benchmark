"""Generate demo charts + video frames (verified, no hand art)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
DOCS = ROOT / "docs"
ASSETS.mkdir(exist_ok=True); DOCS.mkdir(exist_ok=True)

s = json.loads((DATA/"live_summary.json").read_text())
areas = s["by_area"]; sevs = s["by_sev"]

# bar: bugs by area
plt.figure(figsize=(7,3.5))
plt.bar(list(areas.keys()), list(areas.values()))
plt.title(f"Live bugs by area (n={s['n']}, src={s['source'][:24]})")
plt.xticks(rotation=20, ha="right"); plt.tight_layout()
plt.savefig(ASSETS/"chart-areas.png", dpi=150); plt.close()

# pie: severity
plt.figure(figsize=(4,4))
plt.pie([int(sevs.get(k,0)) for k in sorted(sevs)], labels=[f"sev{k}" for k in sorted(sevs)], autopct="%1.0f%%")
plt.title("Severity mix (live)"); plt.tight_layout()
plt.savefig(ASSETS/"chart-severity.png", dpi=150); plt.close()
print("charts ok:", s)
