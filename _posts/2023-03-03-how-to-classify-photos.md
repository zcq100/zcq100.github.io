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

这边文章主要将如何通过文件属性，比如拍摄日期，设备类型，来自动归类整理照片。

本期需要用到的工具有 `exiftool` ，支持全平台。

```shell
 -> exiftool -g 4944107950309404_02.jpg

通常根据文件类型的不同，能看到的Exif信息也不同
---- ExifTool ----
ExifTool Version Number         : 12.70
---- File ----
File Name                       : 4944107950309404_02.jpg
Directory                       : .
File Size                       : 2.8 MB
File Modification Date/Time     : 2013:07:09 02:06:40+08:00
File Access Date/Time           : 2023:11:22 13:16:36+08:00
File Inode Change Date/Time     : 2023:11:22 12:21:59+08:00
File Permissions                : -rwxr--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
Image Width                     : 4032
Image Height                    : 3024
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
---- JFIF ----
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
---- Composite ----
Image Size                      : 4032x3024
Megapixels                      : 12.2
```

从上面的图片exif信息，可以找到拍摄日期：

```shell
exiftool -d "%Y/%m" "-directory<createdate" -r .
```
其他的图片，比如截图，APP转存的，会被剔除部分exif信息，可能没有createdate属性，那么可以根据文件的修改日期再整理一遍。

```shell
exiftool -d "%Y/%m" "-directory<filemodifydate" -r .
```

## 通过元素据检索文件

```
找出所有苹果手机拍摄的照片
exiftool -FileName -if '$LensId =~ /iphone/i' -r .
找出所有苹果手机拍摄的照片，并将元素据写入txt
exiftool -if '$LensId =~ /iphone/i' -r . > info.txt
遍历子目录，找出所有 有GPS信息的,文件扩展名是jpg的照片，并将元素据写入txt
exiftool -if '$GPSPosition =~ /.*/' -ext jpg -r . > info.txt
```

+ Date/Time Original  照片的原始时间
+ Create Date  照片的创建时间
+ GPSPosition  GPS信息
+ ...

# 参考

+ [ExifTool filename 更多信息](!https://exiftool.org/filename.html)