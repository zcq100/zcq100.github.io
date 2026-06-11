#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def count_posts(path: Path) -> int:
    return len(list(path.glob("*.md"))) + len(list(path.glob("*.markdown")))


def require(path: str) -> None:
    target = ROOT / path
    if not target.exists():
        raise AssertionError(f"missing required path: {path}")


def require_contains(path: str, text: str) -> None:
    content = (ROOT / path).read_text(encoding="utf-8")
    if text not in content:
        raise AssertionError(f"{path} does not contain {text!r}")


def main() -> int:
    source_count = count_posts(ROOT / "_posts")
    migrated_count = count_posts(ROOT / "content" / "posts")
    if source_count != 21:
        raise AssertionError(f"expected 21 source posts, got {source_count}")
    if migrated_count != source_count:
        raise AssertionError(f"expected {source_count} migrated posts, got {migrated_count}")

    for path in [
        "hugo.toml",
        "content/about.md",
        "content/privacy.md",
        "content/archives.md",
        "content/search.md",
        "static/CNAME",
        "static/favorite.ico",
        "static/images/avatar.jpg",
        "static/posts/images",
    ]:
        require(path)

    require_contains("hugo.toml", 'theme = "PaperMod"')
    require_contains("hugo.toml", 'baseURL = "https://blog.zcq100.com/"')

    public = ROOT / "public"
    if public.exists():
        for path in ["public/index.html", "public/sitemap.xml", "public/index.xml", "public/robots.txt", "public/CNAME"]:
            require(path)

    print(f"migration validation passed: {migrated_count} posts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
