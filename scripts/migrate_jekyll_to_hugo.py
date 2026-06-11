#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_IN = ROOT / "_posts"
POSTS_OUT = ROOT / "content" / "posts"
STATIC_OUT = ROOT / "static"


def split_front_matter(text: str) -> tuple[dict[str, object], str]:
    # Normalize line endings to LF
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    return parse_simple_yaml(raw), body


def parse_simple_yaml(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None
    nested: dict[str, object] | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and nested is not None and current_key:
            child = line.strip()
            if ":" in child:
                key, value = child.split(":", 1)
                nested[key.strip()] = parse_scalar(value.strip())
            continue
        nested = None
        current_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            nested = {}
            current_key = key
            data[key] = nested
        else:
            data[key] = parse_scalar(value)
    return data


def parse_scalar(value: str) -> object:
    if value in {"", "~", "null", "None"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            inside = value[1:-1].strip()
            if not inside:
                return []
            return [part.strip().strip('"\'') for part in inside.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def quote(value: object) -> str:
    text = "" if value is None else str(value)
    return '"' + text.replace('"', '\\"') + '"'


def list_value(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def post_date_from_name(path: Path) -> str:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})-", path.name)
    if not match:
        return ""
    return "-".join(match.groups())


def normalize_date(value: object, fallback: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        raw = fallback
    if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
        return f"{raw}T00:00:00+08:00"
    if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", raw):
        return raw.replace(" ", "T") + ":00+08:00"
    if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", raw):
        return raw.replace(" ", "T") + "+08:00"
    if "T" in raw:
        return raw
    return f"{fallback}T00:00:00+08:00"


def convert_post(path: Path) -> None:
    fm, body = split_front_matter(path.read_text(encoding="utf-8"))
    fallback_date = post_date_from_name(path)
    date = normalize_date(fm.get("modified"), fallback_date)
    title = fm.get("title") or path.stem[11:].replace("-", " ")
    description = fm.get("description")
    categories = list_value(fm.get("categories") or fm.get("category"))
    tags = list_value(fm.get("tags"))
    math_value = fm.get("mathjax")

    lines = ["---"]
    lines.append(f"title: {quote(title)}")
    lines.append(f"date: {quote(date)}")
    lines.append(f"lastmod: {quote(date)}")
    if description:
        lines.append(f"description: {quote(description)}")
    if categories:
        lines.append("categories: [" + ", ".join(quote(item) for item in categories) + "]")
    if tags:
        lines.append("tags: [" + ", ".join(quote(item) for item in tags) + "]")
    if math_value is True or str(math_value).lower() == "true":
        lines.append("math: true")
    lines.append("draft: false")
    lines.append("---")
    lines.append("")

    POSTS_OUT.mkdir(parents=True, exist_ok=True)
    output_path = POSTS_OUT / path.name.replace(".markdown", ".md")
    output_path.write_text("\n".join(lines) + body, encoding="utf-8")


def convert_page(source: Path, dest: Path, title: str, url: str) -> None:
    _, body = split_front_matter(source.read_text(encoding="utf-8"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        "---\n"
        f"title: {quote(title)}\n"
        f"url: {quote(url)}\n"
        "draft: false\n"
        "---\n\n"
        + body,
        encoding="utf-8",
    )


def write_builtin_pages() -> None:
    content = ROOT / "content"
    content.mkdir(parents=True, exist_ok=True)
    (content / "archives.md").write_text(
        "---\n"
        'title: "归档"\n'
        'layout: "archives"\n'
        'url: "/archives/"\n'
        'summary: "archives"\n'
        "---\n",
        encoding="utf-8",
    )
    (content / "search.md").write_text(
        "---\n"
        'title: "搜索"\n'
        'layout: "search"\n'
        'url: "/search/"\n'
        'summary: "search"\n'
        'placeholder: "搜索文章"\n'
        "---\n",
        encoding="utf-8",
    )


def copy_if_exists(source: Path, dest: Path) -> None:
    if not source.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source, dest)
    else:
        shutil.copy2(source, dest)


def main() -> None:
    if POSTS_OUT.exists():
        shutil.rmtree(POSTS_OUT)
    for post in sorted(POSTS_IN.glob("*.md")) + sorted(POSTS_IN.glob("*.markdown")):
        convert_post(post)

    convert_page(ROOT / "_pages" / "about.md", ROOT / "content" / "about.md", "关于", "/about/")
    convert_page(ROOT / "_pages" / "term-and-privacy.md", ROOT / "content" / "privacy.md", "条款与隐私", "/privacy/")
    write_builtin_pages()

    copy_if_exists(ROOT / "assets" / "images" / "avatar.jpg", STATIC_OUT / "images" / "avatar.jpg")
    copy_if_exists(ROOT / "_posts" / "images", STATIC_OUT / "posts" / "images")
    copy_if_exists(ROOT / "favorite.ico", STATIC_OUT / "favorite.ico")
    copy_if_exists(ROOT / "CNAME", STATIC_OUT / "CNAME")


if __name__ == "__main__":
    main()
