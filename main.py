"""Write one funny line for the One-Liner Laugh Lab to /output/entry.txt.

The bounty asks for a single short funny line, at most 200
characters. This program assembles its line from two pieces,
checks the result against the bounty's gate (single line,
length, no stray whitespace), writes it without a trailing
newline, and reads it back to confirm the bytes on disk.
"""

from pathlib import Path

DESTINATION = Path("/output/entry.txt")
LIMIT = 200

# The line is kept in pieces so a reader can see its shape:
# the tracker's proud congratulation, then the shabby truth.
SETUP = "My fitness tracker congratulated me on 10,000 steps; "
TWIST = "I was eating crisps on a vibrating washing machine."


def compose() -> str:
    return SETUP + TWIST


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("line must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("line must stay on one line")
    if len(text) > LIMIT:
        raise ValueError(f"line is {len(text)} chars, over the {LIMIT} limit")
    if text != text.strip():
        raise ValueError("line has leading or trailing whitespace")
    if not text.endswith("."):
        raise ValueError("line should end with a full stop")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("line does not survive a UTF-8 round trip")
    if not text.isascii() or len(encoded) != len(text):
        raise ValueError("line should be plain ASCII, one byte per char")
    for marker in ("fitness tracker", "10,000 steps", "vibrating washing machine"):
        if marker not in text:
            raise ValueError(f"line is missing its key phrase: {marker}")
    if compose() != text:
        raise ValueError("line does not match its assembled pieces")


def main() -> None:
    line = compose()
    validate(line)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(line.encode("utf-8"))
    on_disk = DESTINATION.read_bytes()
    if on_disk != line.encode("utf-8"):
        raise SystemExit("written bytes differ from the validated line")
    print(line)


if __name__ == "__main__":
    main()
