---
title: 使用Photoprism管理照片
tags: ['docker','NAS']
category: personal
---

Emby可以管理电影和视频，那么在NAS上管理照片用什么好呢? 

如果是群晖，可以选择DS Photo 和 moments，其他NAS和linux用户，可以试试开源的*photoprism*。

![Photoprism](https://docs.photoprism.app/img/preview.jpg)

+ [官方演示](https://try.photoprism.app/)
+ [安装使用](https://docs.photoprism.app/)

## 功能介绍¶

- 浏览照片和视频，无需操心 RAW转换、视频格式和文件重复
- 使用强大的搜索过滤器，轻松查找特定图片
- 隐私保护：除非您明确选择上传，否则不会向 Google、Amazon、Facebook 或 Apple 发送任何数据🔐
- 自动识别 家人 和 朋友 的面孔，根据 内容 和 位置 自动归类图片
- 通过将鼠标悬停在相册和搜索结果中来播放实况照片
- 由于用户界面是一个 Progressive Web App，提供原生应用般的体验，您可以方便地将其 安装在所有主流操作系统和移动设备的主屏幕上
- 自带 4 张高分辨率世界地图，给您带来最美好的旅行的回忆
- 从 Exif、XMP 和其他来源（例如 Google 照片）中提取和合并 元数据
- 还可以搜索更多图像属性，例如Colors、Chroma和Quality
- 在 iOS 和 Android 上采用 PhotoSync 在后台安全备份
- 支持 WebDAV 客户端（例如 Microsoft 的 Windows Explorer 和 Apple 的 Finder）可以直接连接到 PhotoPrism，让您可以像在本地一样打开、编辑和删除计算机中的文件



## 安装部署

这里介绍在 Docker 上的部署。使用的 [官方镜像](https://hub.docker.com/r/photoprism/photoprism) 

```shell
docker pull photoprism/photoprism
```
### 注意事项

+ /photoprism/originals， 是存放照片的根目录，所有添加的 相册 和 上传的文件 都会挂载这个目录下。
+ /photoprism/storage，是存放检索的数据库，各种缓存。如果不希望每次更新容器，进去相册都是一片空白的话，请记得挂载这两个目录。

+ 项目自带 sqlite 数据库，照片不多的情况下可以勉强使用，正式环境建议使用独立的数据库，比如 mysql 和 mariadb(官方推荐)。

### 直接以命令方式部署

```shell
docker run -d \
  --name photoprism \
  --security-opt seccomp=unconfined \
  --security-opt apparmor=unconfined \
  -p 2342:2342 \
  -e PHOTOPRISM_UPLOAD_NSFW="true" \
  -e PHOTOPRISM_ADMIN_PASSWORD="insecure" \
  -v /photoprism/storage \
  -v ~/Pictures:/photoprism/originals \
  photoprism/photoprism
```

### 使用docker-compose

```shell
wget https://dl.photoprism.app/docker/docker-compose.yml
```


```dockerfile
version: '3.5'

services:
  photoprism:
    ## Use photoprism/photoprism:preview for testing preview builds:
    image: photoprism/photoprism:latest
    depends_on:
      - mariadb
    ## Don't enable automatic restarts until PhotoPrism has been properly configured and tested!
    ## If the service gets stuck in a restart loop, this points to a memory, filesystem, network, or database issue:
    ## https://docs.photoprism.app/getting-started/troubleshooting/#fatal-server-errors
    # restart: unless-stopped
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    ports:
      - "2342:2342" # HTTP port (host:container)
    environment:
      PHOTOPRISM_ADMIN_PASSWORD: "insecure"          # !!! PLEASE CHANGE YOUR INITIAL "admin" PASSWORD !!!
      PHOTOPRISM_SITE_URL: "http://localhost:2342/"  # public server URL incl http:// or https:// and /path, :port is optional
      PHOTOPRISM_ORIGINALS_LIMIT: 5000               # file size limit for originals in MB (increase for high-res video)
      PHOTOPRISM_HTTP_COMPRESSION: "gzip"            # improves transfer speed and bandwidth utilization (none or gzip)
      PHOTOPRISM_DEBUG: "false"                      # run in debug mode (shows additional log messages)
      PHOTOPRISM_PUBLIC: "false"                     # no authentication required (disables password protection)
      PHOTOPRISM_READONLY: "false"                   # don't modify originals directory (reduced functionality)
      PHOTOPRISM_EXPERIMENTAL: "false"               # enables experimental features
      PHOTOPRISM_DISABLE_CHOWN: "false"              # disables storage permission updates on startup
      PHOTOPRISM_DISABLE_WEBDAV: "false"             # disables built-in WebDAV server
      PHOTOPRISM_DISABLE_SETTINGS: "false"           # disables Settings in Web UI
      PHOTOPRISM_DISABLE_TENSORFLOW: "false"         # disables all features depending on TensorFlow
      PHOTOPRISM_DISABLE_FACES: "false"              # disables facial recognition
      PHOTOPRISM_DISABLE_CLASSIFICATION: "false"     # disables image classification
      PHOTOPRISM_DARKTABLE_PRESETS: "false"          # enables Darktable presets and disables concurrent RAW conversion
      PHOTOPRISM_DETECT_NSFW: "false"                # flag photos as private that MAY be offensive (requires TensorFlow)
      PHOTOPRISM_UPLOAD_NSFW: "true"                 # allows uploads that MAY be offensive
      # PHOTOPRISM_DATABASE_DRIVER: "sqlite"         # SQLite is an embedded database that doesn't require a server
      PHOTOPRISM_DATABASE_DRIVER: "mysql"            # use MariaDB 10.5+ or MySQL 8+ instead of SQLite for improved performance
      PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"     # MariaDB or MySQL database server (hostname:port)
      PHOTOPRISM_DATABASE_NAME: "photoprism"         # MariaDB or MySQL database schema name
      PHOTOPRISM_DATABASE_USER: "photoprism"         # MariaDB or MySQL database user name
      PHOTOPRISM_DATABASE_PASSWORD: "insecure"       # MariaDB or MySQL database user password
      PHOTOPRISM_SITE_TITLE: "PhotoPrism"
      PHOTOPRISM_SITE_CAPTION: "AI-Powered Photos App"
      PHOTOPRISM_SITE_DESCRIPTION: ""
      PHOTOPRISM_SITE_AUTHOR: ""
      ## Run/install on first startup (options: update, gpu, tensorflow, davfs, nano, clean):
      # PHOTOPRISM_INIT: "gpu tensorflow"
      ## Hardware video transcoding config (optional)
      # PHOTOPRISM_FFMPEG_BUFFERS: "64"              # FFmpeg capture buffers (default: 32)
      # PHOTOPRISM_FFMPEG_BITRATE: "32"              # FFmpeg encoding bitrate limit in Mbit/s (default: 50)
      # PHOTOPRISM_FFMPEG_ENCODER: "h264_v4l2m2m"    # use Video4Linux for AVC transcoding (default: libx264)
      # PHOTOPRISM_FFMPEG_ENCODER: "h264_qsv"        # use Intel Quick Sync Video for AVC transcoding (default: libx264)
      ## Run as a specific user, group, or with a custom umask (does not work together with "user:")
      # PHOTOPRISM_UID: 1000
      # PHOTOPRISM_GID: 1000
      # PHOTOPRISM_UMASK: 0000
      HOME: "/photoprism"
    ## Start as a non-root user (see https://docs.docker.com/engine/reference/run/#user)
    # user: "1000:1000"
    ## Share hardware devices with FFmpeg and TensorFlow (optional):
    # devices:
    #  - "/dev/dri:/dev/dri"
    #  - "/dev/nvidia0:/dev/nvidia0"
    #  - "/dev/nvidiactl:/dev/nvidiactl"
    #  - "/dev/video11:/dev/video11" # Video4Linux (h264_v4l2m2m)
    working_dir: "/photoprism"
    ## Storage Folders: "~" is a shortcut for your home directory, "." for the current directory
    volumes:
      # "/host/folder:/photoprism/folder"                # example
      - "~/Pictures:/photoprism/originals"               # original media files (photos and videos)
      # - "/example/family:/photoprism/originals/family" # *additional* media folders can be mounted like this
      # - "~/Import:/photoprism/import"                  # *optional* base folder from which files can be imported to originals
      - "./storage:/photoprism/storage"                  # *writable* storage folder for cache, database, and sidecar files (never remove)

  ## Database Server (recommended)
  ## see https://docs.photoprism.app/getting-started/faq/#should-i-use-sqlite-mariadb-or-mysql
  mariadb:
    ## If MariaDB gets stuck in a restart loop, this points to a memory or filesystem issue:
    ## https://docs.photoprism.app/getting-started/troubleshooting/#fatal-server-errors
    restart: unless-stopped
    image: mariadb:10.6
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    command: mysqld --innodb-buffer-pool-size=128M --transaction-isolation=READ-COMMITTED --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=512 --innodb-rollback-on-timeout=OFF --innodb-lock-wait-timeout=120
    ## Never store database files on an unreliable device such as a USB flash drive, an SD card, or a shared network folder:
    volumes:
      - "./database:/var/lib/mysql" # important, don't remove
    environment:
      MYSQL_ROOT_PASSWORD: insecure
      MYSQL_DATABASE: photoprism
      MYSQL_USER: photoprism
      MYSQL_PASSWORD: insecure

  ## Watchtower upgrades services automatically (optional)
  ## see https://docs.photoprism.app/getting-started/updates/#watchtower
  #
  # watchtower:
  #   restart: unless-stopped
  #   image: containrrr/watchtower
  #   environment:
  #     WATCHTOWER_CLEANUP: "true"
  #     WATCHTOWER_POLL_INTERVAL: 7200 # checks for updates every two hours
  #   volumes:
  #     - "/var/run/docker.sock:/var/run/docker.sock"
  #     - "~/.docker/config.json:/config.json" # optional, for authentication if you have a Docker Hub account
```

## 使用体验

整体操作还是不错。导入时需要处理的步骤比较多，又是生成缩略图又是图片识别的，非常慢，对性能和内存要求高。我一次性导入几百个G的手机照片和视频，没有限制cpu和内存配额，服务器直接干得没有响应。

AI识别的准确率有点低，分类和人脸很多错乱。

不支持多用户，只能自己一个人用，分享控制不方便。但是数据库里面的表看上去是准备搞多用户的，社区版不知道是否会得到支持。

缺少2FA，authy的支持。

没有官方的手机同步软件，依赖第三方的PhotoSync(收费)。
