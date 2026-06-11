# Hugo PaperMod Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前 Jekyll + Minimal Mistakes 博客迁移为 Hugo + PaperMod，并保留现有文章、页面、图片、自定义域名和基础 SEO 能力。

**Architecture:** 迁移采用独立分支完成：先创建 Jekyll 归档分支，再在迁移分支建立标准 Hugo 项目结构。内容转换由一个仓库内 Python 脚本完成，Hugo 配置和 PaperMod 主题负责页面结构、导航、taxonomy、RSS、sitemap、robots 和 Open Graph 等站点级能力。

**Tech Stack:** Hugo Extended、PaperMod、GitHub Pages Actions、Python 3 标准库、Markdown/TOML/YAML front matter。

---

## File Structure

迁移后文件职责如下：

- Create: `hugo.toml` — Hugo 站点主配置，包含 PaperMod 参数、菜单、permalink、taxonomy、outputs、SEO、robots 和 sitemap 设置。
- Create: `.gitmodules` — PaperMod git submodule 配置，由 `git submodule add` 生成。
- Create: `themes/PaperMod/` — PaperMod 主题 submodule。
- Create: `content/posts/` — 迁移后的 21 篇文章。
- Create: `content/about.md` — 从 `_pages/about.md` 迁移的关于页面。
- Create: `content/privacy.md` — 从 `_pages/term-and-privacy.md` 迁移的隐私/条款页面。
- Create: `content/archives.md` — PaperMod archive 页面。
- Create: `content/search.md` — PaperMod search 页面。
- Create: `static/CNAME` — GitHub Pages 自定义域名。
- Create: `static/favorite.ico` — 站点图标。
- Create: `static/images/avatar.jpg` — 作者头像。
- Create: `static/posts/images/` — 文章图片。
- Create: `.github/workflows/hugo.yml` — GitHub Pages 部署工作流。
- Create: `scripts/migrate_jekyll_to_hugo.py` — 一次性迁移脚本，负责转换 front matter、复制页面和静态资源。
- Create: `scripts/validate_hugo_migration.py` — 验证迁移结果，检查文章数量、关键文件、front matter 和构建产物。
- Modify: `CLAUDE.md` — 从 Jekyll 指南更新为 Hugo + PaperMod 指南。
- Delete: `Gemfile`, `Rakefile`, `_config.yml`, `_data/`, `_pages/`, `_posts/`, `assets/`, `favorite.ico`, root `CNAME`, `README` 保留或改写为 Hugo 简介。

## Task 1: Branch preparation

**Files:**
- Branch: `archive/jekyll-before-hugo`
- Branch: `migration/hugo-papermod`

- [ ] **Step 1: Confirm working tree state before branching**

Run:

```bash
git status --short
```

Expected: only untracked planning files may appear, such as:

```text
?? CLAUDE.md
?? docs/
```

- [ ] **Step 2: Create archive branch from current master without switching**

Run:

```bash
git branch archive/jekyll-before-hugo master
```

Expected: no output. If the branch already exists, run:

```bash
git branch --list archive/jekyll-before-hugo
```

Expected:

```text
  archive/jekyll-before-hugo
```

- [ ] **Step 3: Create and switch to migration branch**

Run:

```bash
git switch -c migration/hugo-papermod master
```

Expected:

```text
Switched to a new branch 'migration/hugo-papermod'
```

If the branch already exists, run:

```bash
git switch migration/hugo-papermod
```

- [ ] **Step 4: Verify active branch**

Run:

```bash
git branch --show-current
```

Expected:

```text
migration/hugo-papermod
```

- [ ] **Step 5: Commit approved spec and plan on migration branch**

Run:

```bash
git add CLAUDE.md docs/superpowers/specs/2026-06-11-hugo-papermod-migration-design.md docs/superpowers/plans/2026-06-11-hugo-papermod-migration.md
git commit -m "docs: plan Hugo PaperMod migration"
```

Expected: commit succeeds. Do not include `Co-Authored-By` in the commit message.

## Task 2: Install PaperMod and create base Hugo config

**Files:**
- Create: `.gitmodules`
- Create: `themes/PaperMod/`
- Create: `hugo.toml`

- [ ] **Step 1: Check Hugo availability**

Run:

```bash
hugo version
```

Expected: command prints a Hugo version. If it fails with `command not found`, stop implementation and ask the user to install Hugo Extended, for example on Arch Linux:

```bash
sudo pacman -S hugo
```

- [ ] **Step 2: Add PaperMod as a submodule**

Run:

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

Expected: `.gitmodules` and `themes/PaperMod` are created.

- [ ] **Step 3: Write Hugo configuration**

Create `hugo.toml` with this content:

```toml
baseURL = "https://blog.zcq100.com/"
languageCode = "zh-CN"
title = "zcq100技术博客"
theme = "PaperMod"
timeZone = "Asia/Shanghai"
defaultContentLanguage = "zh-cn"
hasCJKLanguage = true
enableRobotsTXT = true
enableEmoji = true
summaryLength = 120
paginate = 10

[permalinks]
  posts = "/:year/:month/:day/:slug/"

[taxonomies]
  category = "categories"
  tag = "tags"

[outputs]
  home = ["HTML", "RSS", "JSON"]

[params]
  env = "production"
  title = "zcq100技术博客"
  description = "Python、Linux、Docker、AI开发、网络与自动化运维实践"
  keywords = ["Python", "Linux", "Docker", "AI开发", "自动化运维", "技术博客"]
  author = "zcq100"
  DateFormat = "2006-01-02"
  defaultTheme = "auto"
  ShowReadingTime = true
  ShowShareButtons = true
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowWordCount = true
  ShowRssButtonInSectionTermList = true
  ShowToc = true
  TocOpen = false
  UseHugoToc = true
  comments = false
  images = ["/images/avatar.jpg"]

[params.assets]
  favicon = "/favorite.ico"
  favicon16x16 = "/favorite.ico"
  favicon32x32 = "/favorite.ico"
  apple_touch_icon = "/favorite.ico"

[params.homeInfoParams]
  Title = "zcq100技术博客"
  Content = "Python、Linux、Docker、AI开发、网络与自动化运维实践。"

[[params.socialIcons]]
  name = "github"
  url = "https://github.com/zcq100"

[[menu.main]]
  identifier = "archives"
  name = "归档"
  url = "/archives/"
  weight = 10

[[menu.main]]
  identifier = "categories"
  name = "分类"
  url = "/categories/"
  weight = 20

[[menu.main]]
  identifier = "tags"
  name = "标签"
  url = "/tags/"
  weight = 30

[[menu.main]]
  identifier = "search"
  name = "搜索"
  url = "/search/"
  weight = 40

[[menu.main]]
  identifier = "about"
  name = "关于"
  url = "/about/"
  weight = 50

[markup]
  [markup.highlight]
    noClasses = false
    codeFences = true
    guessSyntax = true
    lineNos = false
    style = "github"
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true

[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5
```

- [ ] **Step 4: Verify Hugo sees the theme**

Run:

```bash
hugo config | grep -E 'theme|baseURL|title'
```

Expected output includes `PaperMod`, `https://blog.zcq100.com/`, and `zcq100技术博客`.

- [ ] **Step 5: Commit base Hugo setup**

Run:

```bash
git add .gitmodules themes/PaperMod hugo.toml
git commit -m "chore: add Hugo PaperMod base config"
```

Expected: commit succeeds. Do not include `Co-Authored-By`.

## Task 3: Create migration and validation scripts

**Files:**
- Create: `scripts/migrate_jekyll_to_hugo.py`
- Create: `scripts/validate_hugo_migration.py`

- [ ] **Step 1: Create migration script**

Create `scripts/migrate_jekyll_to_hugo.py` with this content:

```python
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
    _fm, body = split_front_matter(source.read_text(encoding="utf-8"))
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
        "title: \"归档\"\n"
        "layout: \"archives\"\n"
        "url: \"/archives/\"\n"
        "summary: \"archives\"\n"
        "---\n",
        encoding="utf-8",
    )
    (content / "search.md").write_text(
        "---\n"
        "title: \"搜索\"\n"
        "layout: \"search\"\n"
        "url: \"/search/\"\n"
        "summary: \"search\"\n"
        "placeholder: \"搜索文章\"\n"
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
```

- [ ] **Step 2: Create validation script**

Create `scripts/validate_hugo_migration.py` with this content:

```python
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
```

- [ ] **Step 3: Make scripts executable**

Run:

```bash
chmod +x scripts/migrate_jekyll_to_hugo.py scripts/validate_hugo_migration.py
```

Expected: no output.

- [ ] **Step 4: Run validation before migration to verify expected failure**

Run:

```bash
python scripts/validate_hugo_migration.py
```

Expected: FAIL because `content/posts` and other Hugo files do not exist yet, with output similar to:

```text
validation failed: expected 21 migrated posts, got 0
```

- [ ] **Step 5: Commit scripts**

Run:

```bash
git add scripts/migrate_jekyll_to_hugo.py scripts/validate_hugo_migration.py
git commit -m "chore: add Jekyll to Hugo migration scripts"
```

Expected: commit succeeds. Do not include `Co-Authored-By`.

## Task 4: Migrate content and static assets

**Files:**
- Create: `content/posts/*.md`
- Create: `content/about.md`
- Create: `content/privacy.md`
- Create: `content/archives.md`
- Create: `content/search.md`
- Create: `static/CNAME`
- Create: `static/favorite.ico`
- Create: `static/images/avatar.jpg`
- Create: `static/posts/images/*`

- [ ] **Step 1: Run migration script**

Run:

```bash
python scripts/migrate_jekyll_to_hugo.py
```

Expected: no output and Hugo content/static directories are created.

- [ ] **Step 2: Verify migrated article count**

Run:

```bash
find content/posts -maxdepth 1 -type f -name '*.md' | wc -l
```

Expected:

```text
21
```

- [ ] **Step 3: Run validation after migration**

Run:

```bash
python scripts/validate_hugo_migration.py
```

Expected:

```text
migration validation passed: 21 posts
```

- [ ] **Step 4: Inspect one migrated post front matter**

Run:

```bash
python - <<'PY'
from pathlib import Path
post = sorted(Path('content/posts').glob('*.md'))[-1]
text = post.read_text(encoding='utf-8')
print(post)
print(text.split('---', 2)[1].strip())
PY
```

Expected: output contains `title`, `date`, `lastmod`, optional `description`, optional `categories`, optional `tags`, and `draft: false`.

- [ ] **Step 5: Commit migrated content**

Run:

```bash
git add content static
git commit -m "feat: migrate blog content to Hugo"
```

Expected: commit succeeds. Do not include `Co-Authored-By`.

## Task 5: Remove Jekyll-specific files after migration

**Files:**
- Delete: `Gemfile`
- Delete: `Rakefile`
- Delete: `_config.yml`
- Delete: `_data/`
- Delete: `_pages/`
- Delete: `_posts/`
- Delete: `assets/`
- Delete: `favorite.ico`
- Delete: `CNAME`
- Modify: `.gitignore`

- [ ] **Step 1: Verify migrated files exist before deleting source files**

Run:

```bash
python scripts/validate_hugo_migration.py
```

Expected:

```text
migration validation passed: 21 posts
```

- [ ] **Step 2: Remove Jekyll files**

Run:

```bash
git rm -r Gemfile Rakefile _config.yml _data _pages _posts assets favorite.ico CNAME
```

Expected: git reports removed files.

- [ ] **Step 3: Update `.gitignore` for Hugo**

Replace `.gitignore` with:

```gitignore
public/
resources/_gen/
.hugo_build.lock
.DS_Store
.vscode
```

- [ ] **Step 4: Adjust validation script for post-migration source removal**

Modify `scripts/validate_hugo_migration.py` so `main()` uses a fixed expected post count after `_posts` is removed. Replace the beginning of `main()` with:

```python
def main() -> int:
    source_dir = ROOT / "_posts"
    source_count = count_posts(source_dir) if source_dir.exists() else 21
    migrated_count = count_posts(ROOT / "content" / "posts")
    if source_count != 21:
        raise AssertionError(f"expected 21 source posts, got {source_count}")
    if migrated_count != source_count:
        raise AssertionError(f"expected {source_count} migrated posts, got {migrated_count}")
```

Leave the rest of the function unchanged.

- [ ] **Step 5: Run validation after deleting Jekyll files**

Run:

```bash
python scripts/validate_hugo_migration.py
```

Expected:

```text
migration validation passed: 21 posts
```

- [ ] **Step 6: Commit Jekyll removal**

Run:

```bash
git add .gitignore scripts/validate_hugo_migration.py
git commit -m "chore: remove Jekyll project files"
```

Expected: commit succeeds. Do not include `Co-Authored-By`.

## Task 6: Add GitHub Pages deployment workflow

**Files:**
- Create: `.github/workflows/hugo.yml`

- [ ] **Step 1: Create workflow directory**

Run:

```bash
mkdir -p .github/workflows
```

Expected: no output.

- [ ] **Step 2: Create Hugo deployment workflow**

Create `.github/workflows/hugo.yml` with this content:

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - master
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.148.2
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        run: |
          wget -O "$RUNNER_TEMP/hugo.deb" "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb"
          sudo dpkg -i "$RUNNER_TEMP/hugo.deb"

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build with Hugo
        env:
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Commit workflow**

Run:

```bash
git add .github/workflows/hugo.yml
git commit -m "ci: deploy Hugo site to GitHub Pages"
```

Expected: commit succeeds. Do not include `Co-Authored-By`.

## Task 7: Update project documentation for Hugo

**Files:**
- Modify: `CLAUDE.md`
- Modify or Create: `README.md`
- Delete or leave removed: `README` after replacing with `README.md`

- [ ] **Step 1: Replace `CLAUDE.md` with Hugo guidance**

Write `CLAUDE.md` with:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a Hugo-powered personal technical blog using the PaperMod theme. The site is published at `https://blog.zcq100.com/` and uses Chinese locale (`zh-CN`). Content is primarily Markdown posts under `content/posts/`, with PaperMod providing homepage, taxonomy, archive, search, RSS, sitemap, and SEO behavior.

## Common commands

```bash
git submodule update --init --recursive
hugo server -D
hugo --gc --minify
python scripts/validate_hugo_migration.py
```

Use `hugo server -D` for local preview. Use `hugo --gc --minify` to validate the production build. There is no separate unit test suite; migration and generated-site checks are handled by `scripts/validate_hugo_migration.py`.

## Site structure

- `hugo.toml` is the central Hugo configuration: site metadata, base URL, language, PaperMod parameters, menus, permalinks, taxonomies, outputs, sitemap, and Markdown rendering.
- `content/posts/` contains blog posts. Filenames retain the original date-prefixed Jekyll names. Posts use Hugo front matter with `title`, `date`, `lastmod`, `description`, `categories`, `tags`, and `draft`.
- `content/about.md`, `content/privacy.md`, `content/archives.md`, and `content/search.md` define standalone pages.
- `static/` contains files copied verbatim to the generated site, including `CNAME`, `favorite.ico`, `images/avatar.jpg`, and post images.
- `themes/PaperMod/` is a git submodule. Initialize it before building after a fresh clone.
- `.github/workflows/hugo.yml` builds the site with Hugo Extended and deploys `public/` to GitHub Pages.

## Content conventions

Keep Chinese-language writing style unless editing a post that is already in another language. For new posts, create files under `content/posts/` with date-prefixed filenames and Hugo front matter. Use `categories` and `tags` arrays for taxonomy. Avoid adding Jekyll-specific fields such as `layout`, `headline`, `comments`, or `image.feature` unless a Hugo layout explicitly uses them.

## URL and SEO notes

`hugo.toml` configures post permalinks as `/:year/:month/:day/:slug/` to preserve the previous Jekyll-style URL shape as much as possible. PaperMod and Hugo generate canonical metadata, RSS, sitemap, taxonomy pages, and Open Graph metadata from site configuration and front matter.
```

- [ ] **Step 2: Replace old README with Hugo README**

If root `README` still exists, remove it:

```bash
git rm README
```

Create `README.md` with:

```markdown
# zcq100 技术博客

这是使用 Hugo + PaperMod 构建的个人技术博客。

访问地址：<https://blog.zcq100.com/>

## 本地预览

```bash
git submodule update --init --recursive
hugo server -D
```

## 生产构建

```bash
hugo --gc --minify
```
```
```

- [ ] **Step 3: Commit documentation updates**

Run:

```bash
git add CLAUDE.md README.md
git commit -m "docs: update project docs for Hugo"
```

Expected: commit succeeds. Do not include `Co-Authored-By`.

## Task 8: Build and validate generated Hugo site

**Files:**
- Generated: `public/`

- [ ] **Step 1: Initialize submodule**

Run:

```bash
git submodule update --init --recursive
```

Expected: PaperMod submodule is checked out.

- [ ] **Step 2: Build Hugo site**

Run:

```bash
hugo --gc --minify
```

Expected: command exits 0 and creates `public/`.

- [ ] **Step 3: Validate build artifacts**

Run:

```bash
python scripts/validate_hugo_migration.py
```

Expected:

```text
migration validation passed: 21 posts
```

- [ ] **Step 4: Check generated SEO files**

Run:

```bash
python - <<'PY'
from pathlib import Path
for path in ['public/index.html', 'public/sitemap.xml', 'public/index.xml', 'public/robots.txt', 'public/CNAME']:
    target = Path(path)
    print(path, 'OK' if target.exists() else 'MISSING')
PY
```

Expected:

```text
public/index.html OK
public/sitemap.xml OK
public/index.xml OK
public/robots.txt OK
public/CNAME OK
```

- [ ] **Step 5: Check generated post count roughly matches source count**

Run:

```bash
python - <<'PY'
from pathlib import Path
post_dirs = [p for p in Path('public').rglob('index.html') if '/posts/' in p.as_posix()]
print(len(post_dirs))
PY
```

Expected: prints at least `21`. More is acceptable if taxonomy or pagination pages are counted; investigate if less than 21.

- [ ] **Step 6: Commit final validation-related updates if any**

Run:

```bash
git status --short
```

Expected: only ignored `public/` may exist. If tracked files changed due to fixes, commit them with a focused message and no `Co-Authored-By`.

## Task 9: Final review and handoff

**Files:**
- All migration files

- [ ] **Step 1: Review git history**

Run:

```bash
git log --oneline --decorate -8
```

Expected: recent commits show documentation plan, Hugo setup, scripts, content migration, Jekyll removal, workflow, and docs updates.

- [ ] **Step 2: Review final working tree**

Run:

```bash
git status --short
```

Expected: no tracked changes. `public/` should not appear because it is ignored.

- [ ] **Step 3: Summarize branches**

Run:

```bash
git branch --list 'archive/jekyll-before-hugo' 'migration/hugo-papermod'
```

Expected:

```text
  archive/jekyll-before-hugo
* migration/hugo-papermod
```

- [ ] **Step 4: Report outcome to user**

Report:

```text
Created archive branch: archive/jekyll-before-hugo
Created migration branch: migration/hugo-papermod
Migrated 21 posts to Hugo content/posts/
Configured Hugo + PaperMod
Added GitHub Pages workflow
Verified with: hugo --gc --minify and python scripts/validate_hugo_migration.py
```

If any command failed, report the exact failing command and output instead of claiming completion.
