# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a Jekyll-powered personal blog published at `https://zcq100.github.io` / `https://blog.zcq100.com`. The site uses the Minimal Mistakes remote theme (`mmistakes/minimal-mistakes@4.24.0`) with Chinese locale (`zh-CN`). Content is primarily Markdown posts and pages; most layout behavior comes from the remote theme rather than local templates.

## Common commands

Use Bundler so commands run with the gem versions declared in `Gemfile`:

```bash
bundle install
bundle exec jekyll serve
bundle exec jekyll build
bundle exec jekyll clean
```

Other repository-specific commands:

```bash
bundle exec rake new['Post Title']      # create a post under _posts/
bundle exec rake newquote['Quote Title']
bundle exec rake newstatus['Status Title']
bundle exec rake newpage['Page Title']
bundle exec rake rebuild                # jekyll clean && jekyll build
```

There is no test suite or lint configuration in this repository. Validate changes with `bundle exec jekyll build`; for interactive content/layout checks, run `bundle exec jekyll serve` and inspect the generated site locally.

## Site structure and architecture

- `_config.yml` is the central site configuration: site metadata, URL/baseurl, locale, author profile, pagination, comments, Minimal Mistakes skin, plugins, archive paths, and default front matter values.
- `_posts/` contains blog posts. Filenames follow Jekyll's `YYYY-MM-DD-title.md` convention. `_config.yml` applies `layout: single`, dates, read time, sharing, comments, related posts, and author profile to posts by default.
- `_pages/` contains standalone pages included by `_config.yml` via `include: ["_pages"]`. Pages define their own permalinks and commonly rely on Minimal Mistakes layouts such as `home`, `single`, and archive layouts.
- `_data/navigation.yml` defines the top navigation links for archives, categories, tags, and the about page.
- `assets/images/` stores global site assets such as the author avatar. `_posts/images/` stores images referenced by posts.
- `CNAME` configures the custom domain for GitHub Pages.

## Jekyll and theme behavior

The repository does not vendor theme layouts/includes. When changing layout, navigation, archives, pagination, comments, or author profile behavior, first check whether the behavior is controlled by `_config.yml`, front matter defaults, or Minimal Mistakes theme conventions. Add local overrides only when configuration/front matter cannot solve the change.

Category and tag archive pages are generated with `jekyll-archives` using paths configured in `_config.yml` (`/categories/:name/` and `/tags/:name/`). The visible archive landing pages live under `_pages/`.

## Content conventions

Posts use YAML front matter with fields such as `title`, `description`, `headline`, `modified`, `category`, `tags`, `image`, `comments`, and `mathjax`. Keep existing Chinese-language content style unless editing a post that is already in another language.

Generated build artifacts are ignored (`_site`, `.jekyll-cache`, `.jekyll-metadata`), and `Gemfile.lock` is also ignored in this repository.
