#!/usr/bin/env python3
"""Wrap bare URLs with angle brackets for ePub/Pandoc compatibility."""
from __future__ import annotations

import re
import sys
from pathlib import Path


URL_RE = re.compile(r"(?<!<)https?://\S+")
TRAILING_PUNCT = ".,;:!?)]}\"'—–"


def wrap_urls(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(0)
        trimmed = raw.rstrip(TRAILING_PUNCT)
        trailing = raw[len(trimmed) :]
        if not trimmed:
            return raw
        return f"<{trimmed}>{trailing}"

    return URL_RE.sub(repl, text)


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: prepare_bibliography.py <input> <output>", file=sys.stderr)
        return 1

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    if not src.exists():
        print(f"Missing source: {src}", file=sys.stderr)
        return 1

    content = src.read_text(encoding="utf-8")
    updated = wrap_urls(content)
    dst.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
