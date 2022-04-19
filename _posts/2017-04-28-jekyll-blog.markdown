---
layout: posts
title:  "使用GitHub搭建Jekyll博客"
date:   2017-04-28 13:57:32 +0800
categories: jekyll
comments: true
---

[GitHub](https://github.com/) 是一个代码托管网站，现在很多开源项目都放在GitHub上。 利用GitHub，可以让全球各地的程序员们一起协作开发。GitHub 提供了一种功能，叫 [GitHub Pages](https://help.github.com/categories/20/articles) , 利用这个功能，我 们可以为项目建立网站，当然，这也意味着我们可以通过 GitHub Pages 建立自己的网站。

[Jekyll](http://jekyllrb.com/) 是一个简单的，针对博客设计的静态网站生成器。使用 GitHub 和 Jekyll，我们可以打造自己的独立博客，你可以自由地定制网站的风格，并且这 一切都是免费的。

我在GitHub上自己建立的 [博客](http://francissoung.github.io) 及 [源代码](https://github.com/FrancisSoung/francissoung.github.io) ，下文是分享给第一次搭建和对原理感兴趣的朋友看的，如果你急切的想使用，直接fork以上链接直接可用，后面再去研究原理。

网站截图：

![](http://img1.tuicool.com/AFbQVnU.jpg!web)

### 入门指引

GitHub Pages 的 [主页](http://pages.github.com/) 提供了一个简单的入门指引，阅读并 操作一下，会有一个直观简单的认识。

阮一峰前辈的文章《 [搭建一个免费的，无限流量的Blog—-github Pages和Jekyll入门](http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html) 》是使用 GitHub 和 Jekyll 搭建独立博客非常好的入门文章，强烈建议先阅读并操作一遍。

### 建立自己的博客

在学习完阮一峰前辈的文章后，你就已经有能力搭建自己的独立博客了，但是这个博客 只有最基本的功能，并且也不好看。这时候，你面临几个选择:

1.  完全自己定制博客
2.  找一份框架，修改后使用
3.  从GitHub上fork别人的博客代码，在其中添加自己的文章

如果选择 2, 那么 [jekyll-bootstrap](http://jekyllbootstrap.com/) 是一个选择。

如果选择 3, 那么自己Google一下 github.io 博客 能找到不少博客,去fork,然后修改一下就好。

如果选择 1, 那么可以好好看看后文的内容。

### GitHub + Jekyll 工作机制

#### 机制一

简单地说，你在 GitHub 上有一个账号，名为username(任意)， 有一个项目，名为 `username.github.io` (固定格式，username与账号名一致)， 项目分支名为 `master` (固定)，这个分支有着类似下面的 目录结构:



这样，当你访问 `http://username.github.io/` 时，GitHub 会使用 Jekyll 解析 用户 username名下的username.github.io项目中，分支为master 的源代码，为你构建一个静态网站，并将生成的 index.html 展示给你。

关于这个目录更多的内容，我们还不需要关心，如果你好奇心比较重，可以先看后文源代码一节。

看完上面的解释，你可能会有一些疑问，因为按照上面的说法，一个用户只能有一个网站，那我有很多项目，每个项目都需要一个项目网站，该怎么办呢？另外，在阮一峰前辈的文章中，特别提到，分支名应该为 `gh-pages` ，这又是怎么回事呢？

原来，GitHub认为，一个GitHub账号对应一个用户或者一个组织，GitHub会 给这个用户分配一个域名： `username.github.io` ，当用户访问这个域名时， GitHub会去解析username用户下， `username.github.io` 项目的master分支， 这与我们之前的描述一致。

另外，GitHub还为每个项目提供了域名，例如，你有一个项目名为blog， GitHub为这个项目提供的域名为 `username.github.io/blog` ， 当你访问这个域名时，GitHub会去解析username用户下，blog项目的gh-pages 分支。

所以，要搭建自己的博客，你可以选择建立名为 `username.github.io` 的项目， 在 `master` 分支下存放网站源代码，也可以选择建立名为 `blog` 的项目，在 `gh-pages` 分支下存放网站源代码。

GitHub 的 Help 文档中的 [User, Organization and Project Pages](https://help.github.com/articles/user-organization-and-project-pages) 对此有 详细的描述。

#### 机制二

Jekyll 提供了插件功能，在网站源代码目录下，有一个名为 _plugins的目录，你可以将一些插件放进去，这样，Jekyll在解析网站源代码时，就会运行你的插件，这样插件是 Ruby 写成的。可以为Jekyll添加功能，例如，Jekyll默认是不提供分类页面的，你可以写一个插件，根据文章内容生成分类页面。如果没有插件，你只能每次写文章添加分类时为每个分类手动写HTML页面。

在本地运行 Jekyll 时，这些插件会自动被调用，但是GitHub在解析网站源代码时，出于安全考虑，会开启安全模式，禁用这些插件。我们既想用这些插件，又想用 GitHub，怎么办呢怎么办呢？

GitHub还为我们提供了更一种解析网站的方式，那就是直接上传最终的静态网页，这样，我们可以在本地使用 Jeklly 把网站解析出来，然后再上传到 GitHub上， 这就使得我们既使用了插件，又使用了 GitHub。在上文的目录结构中，有一个 名为 _site 的目录，这个就是Jeklly在本地解析时最终生成的静态网站，我们把其中的内容上传到 GitHub 的项目中就可以了。

### 工作流

关于 git 和 jekyll 的安装与基本使用，这里就不多说了。

#### 工作流一

如果你不使用插件，那么只需要维护一个分支就好:

其中 username 是你的 GitHub 帐号。

你需要在本地维护一份网站源代码，添加新文章后，使用 jekyll 在本地测试一下，没有问题后，commit 到 GitHub 上的相应分支中就可以了。

#### 工作流二

如果你需要使用插件，那么需要维护两个分支，一个是网站的源代码分支，另一个 是 Jeklly 解析源代码后生成的静态网站。

例如，我的源代码分支名为 `master` ，静态网站分支名为 `gh-pages` 。平时写博客时， 首先在 `master` 分支下，添加新文章，然后本地使用 `jekyll build` 将添加文章后的网站 解析一次，这时 `_site` 目录下就有新网站的静态代码了。然后把这个目录下的所有内容 复制到 `gh-pages` 分支下。这个过程，可以写一个 `Makefile` ，每次添加文章后 `make` 一下， 就自动将文章发布到 GitHub 上。

Makefile 内容如下：

deploy:



下面的内容涉及源代码，如果需要进一步学习，或者有问题，可以在 [Jeklly](http://jekyllrb.com/) 官网上找到更详细的解释，或者在评论中留言。

### 源代码

再来看一下这个目录结构：

#### _config.yml

这是针对 Jekyll 的 [配置文件](http://jekyllrb.com/docs/configuration/) ， 决定了 Jekyll 如何解析网站的源代码,下面是一个示例：


我的网站建立在 StrayBirds 项目中，所以 baseurl 设置成 StrayBirds， 我的文章采用 Markdown 格式写成，可以指定 Markdown 的解析器 redcarpet。 另外，安全模式需要关闭，以便 Jekyll 解析时会运行插件。 pygments 可以使得Jekyll解析文章中源代码时加入特殊标记，例如指定代码类型， 这可以被很多 javascript 代码高度库使用。 excerpt_separator 指定了一个摘要分割符号，这样 Jekyll 可以在解析文章时， 将文章的提要提取出来。 paginate 指定了一页有几篇文章，页数太多时，我们可以将文章列表分页，我们在 后文还会提到。

#### _layouts

这个目录存放着一些网页模板文件，为网站所有网页提供一个基本模板，这样 每个网页只需要关心自己的内容就好，其它的都由模板决定。例如，这个目录下的 default.html 文件：



来引用这个文件的内容，方便代码模块化和重用。

#### _plugins

这个文件中存放一些Ruby插件, 例如 gen_categories.rb，这些文件会在 Jekyll 解析网站源代码时被执行。下一节讲述的就是插件。

#### _site

Jekyll 解析整个网站源代码后，会将最终的静态网站源代码放在这里。

### 插件

插件使用 Ruby 写成，放在 _plugins 目录下，有些 Jekyll 没有的功能，又不能 手动添加，因为页面的内容会随着文章日期类别的不同而不同，例如分类功能和归档功能， 这时，就需要使用插件自动生成一些页面和目录。

#### 分类

分类插件推荐使用 [jekyll-category-archive-plugin](https://github.com/shigeya/jekyll-category-archive-plugin/tree/master/_plugins) , 它会根据网站文章的分类信息，为每个类别生成一个页面。

使用方法是，把 `plugins/categoryarchive_plugin.rb` 放在 `plugins` 目录下， 把 `_layouts/categoryarchive.html` 放在 `layouts` 目录下， 这样，这个插件会在Jekyll解析网站时，生成相应categories目录，目录下是各个分类， 每个分类下都有一个 `index.html` 文件，这个文件是根据模板文件 `categoryarchive.html` 生成的，例如：

然后，你就可以通过 `http://username.github.io/blog/categories/工具/` 访问 工具类下的 `index.html` 文件。

#### 归档

归档插件推荐使用 [jekyll-monthly-archive-plugin](https://github.com/shigeya/jekyll-monthly-archive-plugin) ,它会根据网站 _posts目录下的文章日期，为每个月生成一个页面。

使用方法同上。注意，这个插件在 jekyll-1.4.2 中可能会出错，在 jekyll-1.2.0 中没有错误。

### 组件

#### 分页

当文章很多时，就需要使用分页功能，在 Jekyll 官网上提供了一种 [实现](http://jekyllrb.com/docs/pagination/) ，把相应代码放在 主页上，然后在 `_config.yml` 中设置 `paginate` 值就行了。

#### 评论

评论功能需要使用社会化评论系统，我使用的是 [DISQUS](http://disqus.com/) , 注册 之后，将评论区的一段代码放在你需要使用评论功能的页面上, 然后，通过在页面的 front-matter 部分使用



启用评论。

评论区截图：

![](http://img0.tuicool.com/r6rQrin.jpg!web)

### 自定义域名解析

这里很简单了，在你的网站根目录中新建一个 `CNAME` 的文件， **注：一定要大写** 。

![](http://img1.tuicool.com/YzmuIfa.jpg!web)

在CNAME文件中添加你要解析的域名。

![](http://img1.tuicool.com/aYV32y7.jpg!web)

获取GitHub Page的IP地址，最好的方法就是ping一下你的 `username.github.io` 域名。

最后在你的域名提供商域名管理系统中添加对应的解析。我这里做了一个CNAME，可直接解析到A记录到IP即可。

![](http://img0.tuicool.com/BvYbuyV.jpg!web)

基本的内容就介绍到这里，任何问题，欢迎留言。
