"""Patton Ch.13 SUT: buffer overrun (strcpy) vs safe copy + JPEG comment length bug."""
from dataclasses import dataclass

@dataclass
class CopyResult:
    dest: bytes
    truncated: bool
    overflowed: bool
    overflow_bytes: int = 0

def vulnerable_copy(dest_size: int, src: bytes) -> CopyResult:
    """Simulates C strcpy with no bounds check. overflowed=True if len(src) > dest_size."""
    if len(src) <= dest_size:
        return CopyResult(dest=src, truncated=False, overflowed=False)
    # in C this would smash stack/return address; we model it explicitly
    return CopyResult(dest=src[:dest_size], truncated=False, overflowed=True,
                      overflow_bytes=len(src) - dest_size)

def safe_copy(dest_size: int, src: bytes) -> CopyResult:
    """Simulates RtlStringCbCopy: size-aware, null-terminates, truncates safely."""
    if dest_size <= 0:
        return CopyResult(dest=b"", truncated=True, overflowed=False)
    if len(src) < dest_size:
        return CopyResult(dest=src, truncated=False, overflowed=False)
    # reserve 1 byte for null terminator
    return CopyResult(dest=src[:dest_size-1], truncated=True, overflowed=False)

def jpeg_comment_length_field(raw_len: int) -> int:
    """Patton Ch.13 JPEG bug: code does raw_len-2 then treats as unsigned.
    raw_len is the 2-byte field value (should be >=2). Returns bytes-to-read as unsigned 32-bit.
    """
    signed = raw_len - 2
    if signed < 0:
        # C unsigned wrap: -2 -> 4294967294, -1 -> 4294967295
        return (1 << 32) + signed
    return signed
