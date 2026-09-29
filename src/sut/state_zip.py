"""Patton Ch.5 SUT: 10-char ZIP text box + dirty-document flag + FSM."""
import re

ZIP5 = re.compile(r"^\d{5}$")
ZIP9 = re.compile(r"^\d{5}-\d{4}$")

def classify_zip(s: str) -> str:
    """Return partition label for equivalence-class benchmark."""
    if ZIP5.match(s):
        return "valid-5"
    if ZIP9.match(s):
        return "valid-9"
    if len(s) == 0:
        return "empty"
    if len(s) > 10:
        return "too-long"
    if "-" in s:
        parts = s.split("-")
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            return "bad-dash"
        return "bad-9-shape"
    if not s.replace("-", "").isdigit():
        return "non-digit"
    return "bad-5-shape"

class DirtyDoc:
    """Patton Ch.5 dirty-document flag."""
    def __init__(self):
        self.text = ""
        self._saved = ""
        self.dirty = False
    def edit(self, new_text: str):
        self.text = new_text
        self.dirty = (self.text != self._saved)
    def save(self):
        self._saved = self.text
        self.dirty = False
    def try_close(self) -> str:
        return "prompt-save" if self.dirty else "close-ok"

class PasswordFSM:
    """Patton Fig.5.10 mini-FSM: Idle -> Waiting -> Destruct/Idle."""
    IDLE, WAITING, DESTRUCT = "idle", "waiting", "destruct"
    def __init__(self, password="joshua"):
        self.state = self.IDLE
        self._pw = password
    def press_esc(self):
        self.state = self.IDLE
    def request(self):
        if self.state == self.IDLE:
            self.state = self.WAITING
    def enter(self, pw: str):
        if self.state != self.WAITING:
            return self.state
        if pw == self._pw:
            self.state = self.DESTRUCT
        else:
            self.state = self.IDLE  # clear field, back to idle
        return self.state
