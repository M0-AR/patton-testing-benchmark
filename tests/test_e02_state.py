"""E02: Patton Ch.5 state testing - ZIP partitions, dirty flag, FSM."""
from sut.state_zip import classify_zip, DirtyDoc, PasswordFSM

def test_zip_partitions():
    assert classify_zip("98072") == "valid-5"
    assert classify_zip("98072-1234") == "valid-9"
    assert classify_zip("") == "empty"
    assert classify_zip("12345678901") == "too-long"
    assert classify_zip("abcde") == "non-digit"
    assert classify_zip("1234") == "bad-5-shape"
    assert classify_zip("12345-678") == "bad-9-shape"
    assert classify_zip("12-345-6789") == "too-long"  # len 11 >10 takes precedence (verified)

def test_powers_of_two_boundaries():
    # sub-boundary: nibble/byte edges must classify without crash
    for s in ["14", "15", "16", "254", "255", "256", "1023", "1024"]:
        assert classify_zip(s) in ("bad-5-shape", "non-digit", "valid-5", "too-long", "bad-9-shape", "bad-dash", "empty")

def test_dirty_flag():
    d = DirtyDoc()
    assert d.try_close() == "close-ok"
    d.edit("hello")
    assert d.dirty and d.try_close() == "prompt-save"
    d.save()
    assert d.try_close() == "close-ok"
    d.edit("hello")  # same content -> stays clean
    assert d.try_close() == "close-ok"

def test_fsm_all_states_reachable():
    f = PasswordFSM("joshua")
    assert f.state == "idle"
    f.request(); assert f.state == "waiting"
    assert f.enter("wrong") == "idle"
    f.request(); assert f.enter("joshua") == "destruct"
    f.press_esc(); assert f.state == "idle"
    # error state return: wrong pw clears field (back to idle)
    f.request(); f.enter("x"); assert f.state == "idle"
