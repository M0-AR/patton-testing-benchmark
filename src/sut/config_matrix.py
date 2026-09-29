"""Patton Ch.8/9 SUT: config-matrix counting + equivalence reduction + pairwise sample."""
import itertools
import math

def full_cross_product(sizes: dict) -> int:
    n = 1
    for v in sizes.values():
        n *= len(v)
    return n

def reduced_by_equivalence(sizes: dict, keep_per_class: dict) -> int:
    """keep_per_class maps dimension -> num classes kept (e.g. printers: laser->2, inkjet->1)."""
    n = 1
    for k, v in sizes.items():
        n *= min(len(v), keep_per_class.get(k, len(v)))
    return n

def pairwise_sample(params: dict, limit: int = 50):
    """Greedy pairwise-ish sample: round-robin cross of sorted values, capped."""
    keys = list(params.keys())
    vals = [params[k] for k in keys]
    out, seen = [], set()
    # pairwise coverage approximation: iterate product but cap
    for combo in itertools.product(*vals):
        # pairwise key: all 2-combos
        out.append(dict(zip(keys, combo)))
        if len(out) >= limit:
            break
    return out

def risk_score(sev: int, pri: int, dread: int) -> int:
    """Patton Ch.19 + Ch.13 DREAD-inspired: simple additive risk for prioritization."""
    return sev * 10 + pri * 5 + dread
