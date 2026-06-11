# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a Hugo + PaperMod personal blog published at `https://pages.zcq100.com/`. The site uses the PaperMod theme as a git submodule. Content is primarily Markdown posts and pages.

## Common commands

```bash
git submodule update --init --recursive  # Initialize PaperMod theme
hugo server -D                            # Local preview with draft content
hugo --gc --minify                        # Production build
python scripts/validate_hugo_migration.py # Validate migration
```

## Site structure and architecture

- `hugo.toml` is the central site configuration: site metadata, URL/baseurl, locale, author profile, menu, and PaperMod theme settings.
- `content/posts/` contains blog posts.
- `content/about/`, `content/privacy/`, `content/archives/`, `content/search/` contain standalone pages.
- `static/` stores static assets such as images, CNAME file, etc.
- `themes/PaperMod/` is the PaperMod theme as a git submodule.
- `.github/workflows/hugo.yml` is the GitHub Actions workflow for CI/CD.
- `scripts/` contains utility scripts like `validate_hugo_migration.py`.

## Content conventions

Posts use YAML front matter with fields such as `title`, `description`, `date`, `lastmod`, `tags`, `categories`, etc. Keep existing Chinese-language content style unless editing a post that is already in another language.

Generated build artifacts are ignored (`public/`, `resources/_gen/`).

## URL/SEO notes

- Site URL: `https://pages.zcq100.com/`
- Canonical URLs should use this domain
- The `static/CNAME` file contains the production domain
