"""E06: Patton Ch.15 monkeys - dumb fuzzer finds crash; smart FSM monkey covers all states."""
import random
from sut.state_zip import PasswordFSM, classify_zip
from sut.calculator import calc_add

def dumb_fuzz_calculator(seed=0, trials=2000):
    rnd = random.Random(seed)
    crashes = 0
    for _ in range(trials):
        s = "".join(rnd.choice("012ab+-,\x00 ") for _ in range(rnd.randint(0, 12)))
        try:
            calc_add(s, "1")
        except (ValueError, OverflowError):
            crashes += 1  # handled = good; unhandled exception would be bug
        except Exception:
            return True  # unexpected crash = monkey win (should not happen)
    return False

def test_dumb_monkey_no_unhandled_crash():
    assert dumb_fuzz_calculator(seed=42) is False

def test_smart_monkey_covers_fsm():
    # smart monkey knows state map: idle->waiting->{destruct,idle}
    seen = set()
    for pw in ["joshua", "wrong", "", "JOSHUA", "joshua "]:
        f = PasswordFSM("joshua")
        f.request(); seen.add("waiting")
        seen.add(f.enter(pw))
    assert {"waiting", "destruct", "idle"} <= seen

def test_repetition_no_leak():
    from sut.state_zip import DirtyDoc
    d = DirtyDoc()
    for i in range(1000):
        d.edit(f"v{i}"); d.save()
    assert d.try_close() == "close-ok"
