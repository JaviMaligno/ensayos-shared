#!/usr/bin/env python3
"""Inject LaTeX \\index{} commands into Markdown chapters for PDF index generation.

Usage: generate_indexed_sources.py <file1> <file2> ...

Reads indice_terminos.txt from the parent directory of the script's working directory.
Outputs indexed versions to .tmp/indexed/.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path


def find_terms_file() -> Path:
    """Look for indice_terminos.txt in cwd or parent."""
    for candidate in [Path.cwd() / "indice_terminos.txt", Path.cwd().parent / "indice_terminos.txt"]:
        if candidate.exists():
            return candidate
    return Path.cwd() / "indice_terminos.txt"


TERMS_FILE = find_terms_file()


def strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text) if unicodedata.category(ch) != "Mn"
    )


def latex_escape(text: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "%": r"\%",
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "$": r"\$",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = []
    for ch in text:
        out.append(repl.get(ch, ch))
    return "".join(out)


def parse_terms(text: str) -> list[tuple[str, str]]:
    terms: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            continue
        term, desc = parts[0], parts[1]
        if not term:
            continue
        terms.append((term, desc))
    return terms


def make_pattern(term: str) -> re.Pattern[str]:
    parts: list[str] = []
    token: list[str] = []

    def flush_token() -> None:
        if not token:
            return
        text = "".join(token)
        parts.append(r"(?:[*_]+)?" + re.escape(text) + r"(?:[*_]+)?")
        token.clear()

    for ch in term:
        if ch.isalnum():
            token.append(ch)
            continue
        flush_token()
        if ch.isspace():
            parts.append(r"\s+")
        else:
            parts.append(re.escape(ch))
    flush_token()

    escaped = "".join(parts) if parts else re.escape(term)
    prefix = r"(?<!\w)" if term[:1].isalnum() else ""
    suffix = r"(?!\w)" if term[-1:].isalnum() else ""
    return re.compile(prefix + escaped + suffix, re.IGNORECASE)


def term_variants(term: str) -> list[str]:
    variants: list[str] = [term]
    no_paren = re.sub(r"\s*\([^)]*\)", "", term).strip()
    if no_paren and no_paren not in variants:
        variants.append(no_paren)
    split_variants: list[str] = []
    for candidate in list(variants):
        parts = [p.strip() for p in candidate.split("/") if p.strip()]
        if len(parts) > 1:
            split_variants.extend(parts)
    variants.extend(split_variants)
    deduped: list[str] = []
    seen: set[str] = set()
    for variant in variants:
        if variant and variant not in seen:
            seen.add(variant)
            deduped.append(variant)
    return deduped


def inject_indexes(text: str, terms: list[tuple[str, str]], inserted: set[str]) -> str:
    lines = text.splitlines(keepends=True)
    out_lines: list[str] = []
    in_code = False
    patterns = {
        term: [make_pattern(strip_accents(variant)) for variant in term_variants(term)]
        for term, _ in terms
    }

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code or stripped.startswith("#"):
            out_lines.append(line)
            continue

        base = line
        base_stripped = strip_accents(base)
        inserts: list[tuple[int, str, str]] = []
        for term, desc in terms:
            if term in inserted:
                continue
            match = None
            for pattern in patterns[term]:
                candidate = pattern.search(base_stripped)
                if candidate and (match is None or candidate.start() < match.start()):
                    match = candidate
            if not match:
                continue
            sort_key = strip_accents(term)
            display = f"{term} - {desc}"
            index_entry = f"\\index{{{latex_escape(sort_key)}@{latex_escape(display)}}}"
            inserts.append((match.end(), index_entry, term))

        if not inserts:
            out_lines.append(line)
            continue

        updated = base
        for pos, index_entry, term in sorted(inserts, key=lambda x: x[0], reverse=True):
            updated = updated[:pos] + index_entry + updated[pos:]
            inserted.add(term)

        out_lines.append(updated)

    return "".join(out_lines)


def main() -> int:
    if not TERMS_FILE.exists():
        print(f"Missing {TERMS_FILE}", file=sys.stderr)
        return 1
    terms = parse_terms(TERMS_FILE.read_text(encoding="utf-8"))

    if len(sys.argv) < 2:
        print("Usage: generate_indexed_sources.py <file1> <file2> ...", file=sys.stderr)
        return 1

    out_dir = Path.cwd() / ".tmp" / "indexed"
    out_dir.mkdir(parents=True, exist_ok=True)

    inserted: set[str] = set()
    not_found = set(term for term, _ in terms)

    for rel in sys.argv[1:]:
        src = Path.cwd() / rel
        if not src.exists():
            print(f"Missing source: {rel}", file=sys.stderr)
            return 1
        content = src.read_text(encoding="utf-8")
        updated = inject_indexes(content, terms, inserted)
        (out_dir / Path(rel).name).write_text(updated, encoding="utf-8")

    not_found -= inserted
    if not_found:
        print("Terms not found:", ", ".join(sorted(not_found)), file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
