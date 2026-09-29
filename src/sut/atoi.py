"""Patton Fig.7.6 SUT: atoi() - ASCII to integer."""
import re

def atoi(s: str):
    """Spec: [whitespace][sign]digits; stop at first non-digit; 0 if no conversion."""
    i = 0
    n = len(s)
    while i < n and s[i] in (" ", "\t"):
        i += 1
    sign = 1
    if i < n and s[i] in ("+", "-"):
        sign = -1 if s[i] == "-" else 1
        i += 1
    start = i
    while i < n and s[i].isdigit():
        i += 1
    digits = s[start:i]
    if not digits:
        return 0
    return sign * int(digits)

def atoi_undefined_overflow(s: str):
    """Variant documenting 'undefined on overflow' - clamps to 32-bit for test."""
    v = atoi(s)
    INT_MAX, INT_MIN = 2**31 - 1, -(2**31)
    if v > INT_MAX:
        return INT_MAX
    if v < INT_MIN:
        return INT_MIN
    return v
