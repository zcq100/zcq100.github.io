---
title: "如何安全备份数据"
description: "使用rclone加密备份数据"
headline:
modified: 2023-11-18 15:20
category: personal
tags: [rclone,linux]
image:
  feature:
comments: true
mathjax:
---

# 如何安全的备份数据

比如我有1T的数据想备份到云服务上，考虑到隐私保护，决定先加密再上传。

一般我们会选择使用zip，7z之类的工具，进行对称加密，最终文件会打包成一个，这个文件会非常的大，传输过程也可能出现问题。即便当时校验通过，也不能保证以后取回的数据也绝对的一致。像rar这样带容错机制和恢复日志的工具，也存在数据无法解密的风险。

单独给每个文件加密可能是个更好的选择。

这里可以写脚本，遍历所有的文件，逐一加密，但是在不解密的情况下，查看又是个问题。

经过一番折腾，发现rclone能有效的解决这个问题。可以通过挂载一个加密的来源，来实现文件的自动加密和解密。

首先定义一个 远程的目标，比如这里名称为remote:
然后再定义一个加密的目标，比如叫做target:
```
[secret]
type = crypt
remote = target:C:\Users\user1\Downloads\rclone_secret
directory_name_encryption = false
password = pkmdv-7HX4..............EGFZfS0

[target]
type = local
```

然后secret的类型选择crypt，并指向target：
所有写入secret:的数据都会被AES加密后保存在target上。
可以通过目录挂载的方式来访问数据。

```
rclone mount secret: ./mount_dir
```

比如我们想把50G的数据写入BD-R蓝光光盘，如果整体打包加密，那么数据损坏一点都可能导致整个文件无法解密。

通过这种方式单独给每个文件加密，即便部分文件顺坏也不会影响到其他的数据。在需要读取的时候，只需要插入光盘，并通过之前加密的密码挂载，就能访问原始的内容。


