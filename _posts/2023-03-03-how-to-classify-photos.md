---
title: "如何使用快速整理照片？"
description: "用用exiftool快速将照片按照日期目录分类"
headline:
modified: 2023-03-03 10:34
category: personal
tags: [python]
image:
  feature:
comments: true
mathjax:
---

# 快速整理照片

如何按照 照片拍摄日期，按月建立目录，归类照片
这里需要用到的工具 `exiftool` ，支持全平台。

一般照片的话，exif信息里面有个 拍摄日期：

```shell
exiftool -d "%Y/%m" "-directory<createdate" -r .
```
其他的图片，比如截图，APP里保存的，被去除exif信息的图片，就没有createdate属性，那么可以根据文件的修改日期来整理。

```shell
exiftool -d "%Y/%m" "-directory<filemodifydate" -r .
```
