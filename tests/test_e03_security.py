"""E03: Patton Ch.13 security - buffer overrun vs safe copy + JPEG length bug."""
from sut.buffer import vulnerable_copy, safe_copy, jpeg_comment_length_field

def test_vulnerable_overflows():
    r = vulnerable_copy(100, b"A"*50)
    assert not r.overflowed and r.dest == b"A"*50
    r = vulnerable_copy(100, b"A"*150)
    assert r.overflowed and r.overflow_bytes == 50

def test_safe_never_overflows():
    for n in [0, 1, 50, 100, 150, 1000]:
        r = safe_copy(100, b"A"*n)
        assert not r.overflowed
        assert len(r.dest) <= 99
    r = safe_copy(100, b"A"*150)
    assert r.truncated and len(r.dest) == 99

def test_jpeg_length_unsigned_wrap():
    # spec: field>=2 valid; 0/1 are illegal and wrap to ~4GB (the 2004 JPEG virus root cause)
    assert jpeg_comment_length_field(2) == 0
    assert jpeg_comment_length_field(100) == 98
    assert jpeg_comment_length_field(1) == 4294967295
    assert jpeg_comment_length_field(0) == 4294967294

def test_hidden_pattern_lengths_cluster():
    # Hidden-pattern probe: overflow risk jumps exactly at dest_size boundary
    sizes = [98, 99, 100, 101, 102]
    flags = [vulnerable_copy(100, b"X"*s).overflowed for s in sizes]
    assert flags == [False, False, False, True, True]
