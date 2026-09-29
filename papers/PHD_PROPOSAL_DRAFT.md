# PhD Proposal Draft — Verifying Patton (2006) in 2026: A Live-Data Benchmark of Classic Testing Heuristics

## 1. Problem
Classic heuristics (equivalence partitioning, boundary analysis, state coverage, config reduction, buffer-overrun vigilance, monkey fuzzing, opened/resolved/closed tracking) are taught as timeless but rarely benchmarked jointly on live 2026 data with modern gates (mutation, escape-rate).

## 2. Hypotheses (falsifiable)
- H1 Boundary-State-Security clustering: ≥50% of defects fall in top-3 areas (numeric boundary / state / string-handling). Tested in E01/E02/E03/E05.
- H2 Pesticide paradox: fixed suite's new-mutant kill-rate decays without diversification (E01 mutant + E06 monkeys).
- H3 Shift-left dividend: spec/design-phase fixes dominate cost saving; validated via lit + severity mix in live data (E05).

## 3. Method (Runeson case-study + Elbaum prioritization + Karhu mapping)
Within-lab replication (this repo) + live mining (GitHub issues, n≥10, declared source) + mutation probes + negative controls (mutants that must survive/fail as specified). Expected values pinned in `data/expected_values.json`.

## 4. Threats
Single-repo live sample; label→severity proxy; fallback sample if offline (explicitly declared, never silent).

## 5. Next
Scale to Defects4J + NASA MDP + 3 OSS repos; add Stryker/Mutmut mutation + flaky-rate + escape-rate dashboards; pre-register thresholds before scaling.
