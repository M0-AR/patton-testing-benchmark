"""Patton Ch.5/7 SUT: 32-digit calculator add (mirrors Windows Calculator example)."""
MAX_DIGITS = 32
MAX_VAL = int("9" * MAX_DIGITS)

def parse_operand(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("empty operand")
    neg = False
    if s[0] in "+-":
        neg = s[0] == "-"
        s = s[1:]
    if not s.isdigit():
        raise ValueError(f"invalid operand: {s!r}")
    if len(s) > MAX_DIGITS:
        raise OverflowError("operand exceeds 32 digits")
    v = int(s)
    return -v if neg else v

def calc_add(a: str, b: str) -> str:
    """Add two decimal strings, enforcing 32-digit boundary. Returns decimal string."""
    x, y = parse_operand(a), parse_operand(b)
    r = x + y
    if abs(r) > MAX_VAL:
        raise OverflowError("result exceeds 32 digits")
    return str(r)

# --- Mutants for benchmark (each simulates a classic Patton bug) ---
def calc_add_mut_offbyone(a: str, b: str) -> str:
    """Mutant: off-by-one on upper boundary (accepts 33 digits)."""
    x, y = parse_operand(a), parse_operand(b)
    r = x + y
    if abs(r) > int("9" * 33):
        raise OverflowError("overflow")
    return str(r)

def calc_add_mut_comma(a: str, b: str) -> str:
    """Mutant: silently converts comma to dot then truncates (Patton Ch.3 comma bug)."""
    def conv(s):
        return parse_operand(s.replace(",", ".").split(".")[0] if "," in s else s)
    return str(conv(a) + conv(b))
