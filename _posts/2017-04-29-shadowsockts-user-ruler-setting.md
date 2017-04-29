---
layout: post
title: "shadowsockts user-ruler setting"
description: 
headline: 
modified: 2017-04-29
category: personal
tags: []
image: 
  feature: 
comments: true
mathjax: 
---

最新版本的shadowsocks支持用户自定义代理规则，更新到最新的版本的shadowsocks后， 在shadowsocks文件夹内会有一个user-rule.txt文档，如果用户需要添加自定义代理规则，只需要编辑user-rule.txt文件。
自定义代理规则的设置语法与GFWlist相同，即adblockplus过滤规则。简要描述如下：
```
1. 通配符支持，如 *.example.com/* 实际书写时可省略* 如.example.com/ 意即*.example.com/*
2. 正则表达式支持，以\开始和结束， 如 \[\w]+:\/\/example.com\
3. 例外规则 @@，如 @@*.example.com/* 满足@@后规则的地址不使用代理
4. 匹配地址开始和结尾 |，如 |http://example.com、example.com|分别表示以http://example.com开始和以example.com结束的地址
5. || 标记，如 ||example.com 则http://example.com、https://example.com、ftp://example.com等地址均满足条件
6. 注释 ! 如 ! Comment
```

例如你要添加www.domain.com、ipaddress 两个网站到自定义代理规则，编辑user-rule.txt文件，在文件最后加入：

```
!测试user-rule生效
||domain.com
||ipaddress
```
备注：user-rule.txt一行只能有一条代理规则。
user-rule.txt中的规则并不能直接被shadowsocks使用，如要添加到user-rule.txt中的规则生效，你还要执行下面重要的一步：更新本地的PAC，更新后user-rule.txt中的自定义规则会添加到PAC.txt文件内。（备注：每次编辑完user-rule.txt后，均需执行“从GFWList更新本地PAC”，使本次规则也生效。）
更新PAC

