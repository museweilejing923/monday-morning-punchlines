"""A Monday-morning punchline, delivered by a short script.

This file holds exactly one joke and a set of named guards that
screen it. The guards run in a fixed order -- topic first, then
size, shape, and the small formatting rules -- and the joke is
written to /output/entry.txt only if it survives all of them.
No input is read and nothing varies between runs, so the bytes
on disk are the same every time.
"""

import sys
from pathlib import Path

ENTRY = "Monday morning: my alarm went off, my coffee went cold, and my calendar reminded me I have a meeting about being more productive."
CEILING = 200
OUTFILE = Path("/output/entry.txt")


def die(reason):
    print(f"rejected: {reason}", file=sys.stderr)
    raise SystemExit(1)


def ensure_topic_monday(text):
    if "Monday" not in text:
        die("entry is off topic")


def ensure_capital_start(text):
    if not text or not text[0].isupper():
        die("entry must start with a capital letter")


def ensure_short_enough(text):
    if len(text) > CEILING:
        die("entry is longer than the limit")


def ensure_not_blank(text):
    if not text or not text.strip():
        die("entry is empty")


def ensure_no_stray_chars(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        die("entry has control characters")


def ensure_single_line(text):
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        die("entry has ragged edges or line breaks")


def ensure_proper_close(text):
    if not text or text[-1] not in ".!?":
        die("entry must end with . ! or ?")


def ensure_letters_present(text):
    if not any(ch.isalpha() for ch in text):
        die("entry has no letters")


def ensure_not_numeric(text):
    if text.isdigit():
        die("entry is only digits")


def ensure_not_punctuation(text):
    if not any(ch.isalnum() for ch in text):
        die("entry is only punctuation")


def ensure_no_tripled_letter(text):
    for i in range(len(text) - 2):
        if text[i] == text[i + 1] == text[i + 2]:
            die("entry repeats a character three times in a row")


GUARDS = (
    ensure_no_tripled_letter,
    ensure_topic_monday,
    ensure_capital_start,
    ensure_short_enough,
    ensure_not_blank,
    ensure_no_stray_chars,
    ensure_single_line,
    ensure_proper_close,
    ensure_letters_present,
    ensure_not_numeric,
    ensure_not_punctuation,
)


def screen(text):
    for guard in GUARDS:
        guard(text)


def main():
    screen(ENTRY)
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    OUTFILE.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
