# Hugo + PaperMod 博客迁移设计

## 背景

当前仓库是 Jekyll + Minimal Mistakes 的中文技术博客。用户希望将博客引擎迁移为 Hugo，并使用 PaperMod 主题，同时保留现有文章内容和博客发布能力。迁移前需要基于当前分支创建一个归档分支，便于以后回看 Jekyll 版本。

## 目标

- 创建归档分支保存迁移前 Jekyll 版本。
- 创建独立迁移分支执行 Hugo + PaperMod 改造。
- 将现有 `_posts/` 文章迁移到 Hugo `content/posts/`。
- 将必要页面、图片、站点配置、域名配置迁移到 Hugo 结构。
- 使用 PaperMod 提供更现代、适合技术博客的样式。
- 保留或尽量兼容旧文章链接，降低 SEO 损失。
- 配置基础 SEO，包括 sitemap、RSS、robots、canonical、Open Graph 和站点元信息。
- 使用 GitHub Actions 构建并部署 Hugo 站点到 GitHub Pages。

## 非目标

- 不大规模重写文章正文内容。
- 不引入复杂前端应用或自定义交互系统。
- 不在迁移阶段设计完整个人品牌视觉系统。
- 不承诺完全复刻 Minimal Mistakes 的每个页面和组件。

## 分支策略

采用方案 A：

1. 从当前 `master` 创建归档分支：`archive/jekyll-before-hugo`。
2. 从当前 `master` 创建迁移分支：`migration/hugo-papermod`。
3. 在迁移分支上执行 Hugo 改造。

当前仓库存在未提交的 `CLAUDE.md`。归档分支应表示迁移前的博客代码状态，不强制包含未提交文件。迁移分支会根据 Hugo 项目结构更新 `CLAUDE.md`。

## 目标结构

迁移后采用标准 Hugo 项目结构：

```text
.
├── hugo.toml
├── content/
│   ├── posts/
│   ├── about.md
│   ├── archives.md
│   ├── search.md
│   └── privacy.md
├── static/
│   ├── CNAME
│   ├── favorite.ico
│   ├── images/
│   └── posts/images/
├── themes/
│   └── PaperMod/
├── .github/
│   └── workflows/
│       └── hugo.yml
└── CLAUDE.md
```

`themes/PaperMod` 可以使用 git submodule 引入，便于跟随上游更新。若当前环境不适合使用 submodule，可改为 Hugo Modules 或 vendor 主题，但默认优先 submodule。

## 内容迁移规则

### 文章

- `_posts/*.md` 迁移到 `content/posts/*.md`。
- 文件名保留日期和 slug，便于追踪来源。
- 将 Jekyll front matter 转换为 Hugo front matter。

字段转换：

| Jekyll 字段 | Hugo 字段 |
| --- | --- |
| `title` | `title` |
| `description` | `description` |
| `modified` | `date` 和 `lastmod`，如果无法区分发布时间与修改时间则两者一致 |
| `category` | `categories` 数组 |
| `tags` | `tags` 数组 |
| `comments` | `comments` 或 `params.comments`，视 PaperMod 配置决定 |
| `mathjax` | `math: true`，仅在原文明确需要时设置 |

Jekyll/Minimal Mistakes 专用字段如 `layout`、`headline`、`image.feature` 默认移除，除非迁移时发现某篇文章依赖这些字段。

### 页面

- `_pages/about.md` 迁移为 `content/about.md`。
- `_pages/term-and-privacy.md` 迁移为 `content/privacy.md`。
- 归档、分类、标签页面优先使用 Hugo taxonomy 和 PaperMod 内置能力生成。
- 首页由 PaperMod 配置驱动，不迁移 `_pages/index.md` 的 Jekyll home layout。

### 静态资源

- `assets/images/avatar.jpg` 迁移到 `static/images/avatar.jpg`。
- `_posts/images/` 迁移到 `static/posts/images/`。
- `favorite.ico` 迁移到 `static/favorite.ico`。
- `CNAME` 迁移到 `static/CNAME`。

正文中的图片路径需要根据迁移后的静态资源路径检查并修正。

## URL 与 SEO 设计

Hugo 配置应尽量保留旧文章 URL。实现前需要确认当前 Jekyll 实际生成的文章 URL。如果无法构建 Jekyll，则根据默认 Jekyll 行为和现有 front matter 推断，并在 Hugo 中设置 permalink。

候选 permalink：

```toml
[permalinks]
  posts = "/:year/:month/:day/:slug/"
```

基础 SEO 配置：

- `baseURL = "https://blog.zcq100.com/"`
- `languageCode = "zh-CN"`
- 设置站点标题和描述。
- 启用 sitemap、RSS、robots.txt。
- 配置 canonical URL。
- 配置 Open Graph / Twitter Card 所需的 title、description、images。
- 配置 taxonomy 页面和归档页标题。
- 保留自定义域名 `CNAME`。

## PaperMod 配置

PaperMod 应配置为技术博客阅读优先：

- 首页展示文章列表和简短个人简介。
- 顶部导航包含归档、分类、标签、关于、搜索。
- 启用搜索页面。
- 启用代码高亮、目录、阅读时间、面包屑或返回顶部等阅读辅助功能。
- 使用头像和 GitHub 链接延续当前作者信息。
- 默认不开启复杂封面图布局，避免迁移时需要为每篇文章补图。

## 部署设计

新增 GitHub Actions 工作流：

1. checkout 仓库并拉取主题 submodule。
2. 安装 Hugo extended。
3. 运行 `hugo --gc --minify`。
4. 将 `public/` 部署到 GitHub Pages。

这样部署不依赖 GitHub Pages 的 Jekyll 构建环境。

## 验证计划

迁移完成后执行：

```bash
hugo version
hugo --gc --minify
```

如果环境允许，再运行：

```bash
hugo server -D
```

检查项：

- Hugo 构建成功。
- 迁移后文章数量与原 `_posts/` 数量一致。
- 首页、文章页、关于页、归档页、分类页、标签页、搜索页可生成。
- 图片路径可用。
- `public/sitemap.xml`、`public/index.xml`、`public/robots.txt` 存在。
- `public/CNAME` 存在。
- 关键旧 URL 尽量兼容。
- `CLAUDE.md` 更新为 Hugo 项目说明。

## 风险与处理

- **旧 URL 不完全一致**：优先用 Hugo permalink 复刻旧文章路径；必要时为重要页面添加 aliases。
- **front matter 格式差异**：使用脚本批量转换，再抽样检查。
- **图片路径断裂**：迁移静态资源后使用 grep 检查旧路径引用，并针对性替换。
- **主题更新方式选择**：默认 submodule；如果 submodule 在当前环境受限，再改用 Hugo Modules 或直接 vendor。
- **本地环境缺少 Hugo**：实现时先检查 `hugo version`，没有则提示安装或使用包管理器安装。