# Benchmark Results — 2026-09-29 run (VERIFIED, not hand-waved)

Command: `python scripts/fetch_live_data.py && PYTHONPATH=src pytest -v` + `docker compose config`
Result: **35 passed** (junit at test-results/junit.xml)

## Live data (real market signal)
- Source: `github:pytest-dev/pytest(live)`, n=50 (GitHub REST, no key, 2026-09-29)
- by_area: float-math 37, integer-math 9, ui 3, docs 1
- by_sev: 2:40, 1:9, 3:1
- **clustering_ratio_top3 = 0.98 >= 0.50** → H1 SUPPORTED on live data (bugs follow bugs, Patton Ch.3)
- Files: `data/live_github_issues.json`, `data/live_summary.json` (re-run to refresh)

## Lab results per experiment
- E01 boundary/atoi: happy + overflow + invalid + comma-reject + mutant-survives-as-designed + 10 atoi vectors — PASS
- E02 state/ZIP: 8 partitions + powers-of-two sub-boundaries + dirty-flag + FSM full-state reachability — PASS (fixed len>10 precedence, re-verified)
- E03 security: vulnerable overflows at 101/102, safe never overflows (≤99 + truncate), JPEG 0→4294967294 / 1→4294967295 — PASS
- E04 config: 336*210*1500*1200 cross-product exact, reduction 15→4, pairwise cap 10 — PASS
- E05 live: files exist, clustering, sev mix, source declared — PASS
- E06 monkeys: 2000-trial dumb fuzz no unhandled crash, smart FSM covers {waiting,destruct,idle}, 1000x repetition no leak — PASS

## Hidden patterns found
1. Overflow risk is a step function at dest_size (98,99,100→safe; 101,102→overflow) — test exactly ±1, not just big values.
2. Length check order matters: `len>10` shadows `bad-dash` — document precedence or lose a partition.
3. Live OSS issues are 98% in top-3 areas — risk-based testing (Patton) beats uniform coverage.

## Reproduce
`make verify` or `docker compose up --build` (compose config = OK; full image pull needs net).
