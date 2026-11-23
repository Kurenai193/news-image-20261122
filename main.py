"""Entry program for the 22 November 2026 news-image competition.

The repository holds one finished front page, entry.png, which sums up
Sunday 22 November 2026 in thirty-five dated stories: COP31 closing in
Antalya with no deal, 186 drones over Ukraine, Iran's claimed radar
strikes in Bahrain, and thirty-two further stories with a map, a
numbers band and a date check. This program validates that image and
places an identical copy where the grader expects it, at
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Only the Python standard library is used and no network is touched.
"""

import hashlib
import os
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
ONE_MEBIBYTE = 1_048_576


def load_entry_bytes() -> bytes:
    """Read the bundled front page and check it obeys the size rules."""
    source = Path(__file__).resolve().parent / "entry.png"
    payload = source.read_bytes()
    if not payload.startswith(PNG_MAGIC):
        raise ValueError("entry.png does not start with the PNG signature")
    if len(payload) > ONE_MEBIBYTE:
        raise ValueError("entry.png is larger than one mebibyte")
    return payload


def publish(payload: bytes) -> Path:
    """Write the payload to the output directory and return its path."""
    target_dir = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    target.write_bytes(payload)
    return target


def digest(data: bytes) -> str:
    """Return the SHA-256 hex digest used to verify the copy."""
    return hashlib.sha256(data).hexdigest()


def run() -> None:
    payload = load_entry_bytes()
    target = publish(payload)
    written = target.read_bytes()
    if digest(written) != digest(payload):
        raise IOError("the written file differs from the bundled image")
    print(f"wrote {target} ({len(written)} bytes, sha256 {digest(written)[:16]}...)")


if __name__ == "__main__":
    run()
