#!/usr/bin/env python3
"""Verify PascalCase tracked paths and local Markdown links without external packages."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
FILE_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*$")
EXTENSION = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9]+)*$")
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
PLATFORM_PARTS = {".github", "workflows", ".gitignore"}
# The ECPP loaders address these generated certificates by a truncated SHA-256
# of the decimal prime. The lowercase hash stem is part of the on-disk format.
ECPP_CERTIFICATE = re.compile(r"Research/(?:NightOrder|NightMerge)/ECPP/[0-9a-f]{24}\.json\.gz")


def tracked_files() -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return sorted(p.decode("utf-8") for p in proc.stdout.split(b"\x00") if p)


def resolve_href(source: str, href: str) -> Path | None:
    href = href.strip()
    if href.startswith("<") and ">" in href:
        href = href[1:href.index(">")]
    else:
        href = href.split(maxsplit=1)[0]
    if not href or href.startswith(("#", "//")):
        return None
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return None
    relative = unquote(parsed.path)
    if not relative:
        return None
    return (ROOT / source).parent.joinpath(relative).resolve()


def main() -> int:
    failures: list[str] = []
    paths = tracked_files()
    for rel in paths:
        segments = rel.split("/")
        for idx, segment in enumerate(segments):
            if segment in PLATFORM_PARTS and (
                segment != "workflows" or (idx > 0 and segments[idx - 1] == ".github")
            ):
                continue
            if segment.startswith("."):
                failures.append(f"noncanonical dot path: {rel}")
                break
            if idx == len(segments) - 1:
                base, separator, ext = segment.partition(".")
                if not separator or not EXTENSION.fullmatch(ext):
                    failures.append(f"invalid file suffix: {rel}")
                    break
                if not FILE_NAME.fullmatch(base) and not ECPP_CERTIFICATE.fullmatch(rel):
                    failures.append(f"non-PascalCase file: {rel}")
                    break
            elif not FILE_NAME.fullmatch(segment):
                failures.append(f"non-PascalCase folder: {rel}")
                break
        if rel.startswith("Research/2026-11-22/"):
            failures.append(f"retired research directory: {rel}")

    for rel in paths:
        if not rel.endswith(".md"):
            continue
        content = (ROOT / rel).read_text(encoding="utf-8")
        refs = [m.group(1) for m in INLINE_LINK.finditer(content)]
        refs += [m.group(1) for m in REFERENCE_LINK.finditer(content)]
        for href in refs:
            target = resolve_href(rel, href)
            if target is None:
                continue
            if not target.is_relative_to(ROOT):
                failures.append(f"link escapes repository: {rel}: {href}")
            elif not target.exists():
                failures.append(f"missing local link: {rel}: {href}")

    if failures:
        for item in failures:
            print("FAIL:", item)
        print(f"REPOSITORY_STRUCTURE_FAILED issues={len(failures)} files={len(paths)}")
        return 1
    print(f"REPOSITORY_STRUCTURE_OK files={len(paths)} markdown_links_verified=YES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
