"""E01: Patton Ch.5 boundary/equivalence on Calculator + atoi. Verifies risk-based reduction + mutation kill."""
from sut.calculator import calc_add, calc_add_mut_offbyone, MAX_VAL
from sut.atoi import atoi
import pytest

BOUNDARY_CASES = [
    ("1", "1", "2"),
    ("1", "13", "14"),
    ("0", "0", "0"),
    ("-1", "1", "0"),
    ("99999999999999999999999999999999", "0", "99999999999999999999999999999999"),
]

def test_add_happy_path():
    for a, b, exp in BOUNDARY_CASES:
        assert calc_add(a, b) == exp

def test_add_overflow_boundary():
    with pytest.raises(OverflowError):
        calc_add("99999999999999999999999999999999", "1")
    with pytest.raises(OverflowError):
        calc_add("9"*33, "0")

def test_add_invalid_partition():
    for bad in ["", "1a1", "1+2", "  "]:
        try:
            calc_add(bad, "1")
            assert False, f"should reject {bad!r}"
        except (ValueError, OverflowError):
            pass

def test_comma_bug_generalized():
    # Patton Ch.3: 5,000-5 comma handling must not silently become 5.000
    try:
        calc_add("5,000", "5")
        assert False, "comma input must be rejected, not coerced"
    except ValueError:
        pass

def test_mutant_killed_by_boundary():
    # Off-by-one mutant accepts 33-digit overflow; boundary test must kill it
    killed = False
    try:
        calc_add_mut_offbyone("99999999999999999999999999999999", "1")
    except OverflowError:
        killed = True
    # mutant does NOT raise -> survived; our correct impl DOES raise -> test kills mutant
    assert not killed, "mutant survives overflow (expected)"
    with pytest.raises(OverflowError):
        calc_add("99999999999999999999999999999999", "1")

@pytest.mark.parametrize("s,exp", [
    ("1", 1), ("-1", -1), ("+1", 1), ("0", 0), ("-0", 0),
    ("1.2", 1), ("2-3", 2), ("abc", 0), ("a123", 0),
    ("   -42xyz", -42), ("\t+7", 7),
])
def test_atoi_spec(s, exp):
    assert atoi(s) == exp
