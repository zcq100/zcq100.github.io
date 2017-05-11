---
layout: post
title: "Shadowsocks用户规则设置"
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

## Windows

最新版本的shadowsocks支持用户自定义代理规则，更新到最新的版本的shadowsocks后， 在shadowsocks文件夹内会有一个user-rule.txt文档，如果用户需要添加自定义代理规则，只需要编辑user-rule.txt文件。

自定义代理规则的设置语法与GFWlist相同，即adblockplus过滤规则。

简要描述如下：

* 通配符支持，如 *.example.com/* 实际书写时可省略* 如.example.com/ 意即*.example.com/*
* 正则表达式支持，以\开始和结束， 如 \[\w]+:\/\/example.com\
* 例外规则 @@，如 @@*.example.com/* 满足@@后规则的地址不使用代理
* 匹配地址开始和结尾 |，如 |http://example.com、example.com|分别表示以http://example.com开始和以example.com结束的地址
* || 标记，如 ||example.com 则http://example.com、https://example.com、ftp://example.com等地址均满足条件
* 注释 ! 如 ! Comment

例如你要添加www.domain.com、ipaddress 两个网站到自定义代理规则，编辑user-rule.txt文件，在文件最后加入：

```
!测试user-rule生效
||domain.com
||ipaddress
```

备注：user-rule.txt一行只能有一条代理规则。

user-rule.txt中的规则并不能直接被shadowsocks使用，如要添加到user-rule.txt中的规则生效，你还要执行下面重要的一步：更新本地的PAC，更新后user-rule.txt中的自定义规则会添加到PAC.txt文件内。

（备注：每次编辑完user-rule.txt后，均需执行“从GFWList更新本地PAC”，使本次规则也生效。）


## Linux
Linux下设置代理稍微麻烦点。火狐浏览器建议安装FoxyPoxy插件，Chrome安装Proxy SwitchyOmega插件。
终端命令建议安装proxychains。

浏览器插件默认是全局代理，需要局部代理的话可以指定pac文件。

这个pac文件建议用pacgen来生成，这样可以自定义user-rule。

- archlinux安装pacgen： ```sudo pacman -S pacgen```
- ubuntu   安装pacgen： ```sudo apt install pacgen```
- centos   安装pacgen： ```sudo yum install pacgen```


{% highlight shell %}
#! /bin/bash
genpac --pac-proxy "SOCKS 127.0.0.1:1080" --user-rule-from ./user-rule -o ./gwflist.pac
echo "gwflist.pac 生成成功"
{% endhighlight %}
