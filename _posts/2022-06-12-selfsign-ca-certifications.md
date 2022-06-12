---
title: "如何生成自签名证书"
description: "生成和使用自签名证书"
headline:
modified: 2022-06-12 15:34
category: personal
tags: [安全]
image:
  feature:
comments: true
mathjax:
---


# 自签名证书

### 生成CA key
```shell
openssl genrsa -des3 -out myCA.key 2048
```

### 生成CA 公钥
```shell
openssl req -utf8 -x509 -new -nodes -key myCA.key -sha256 -days 825 -out myCA.pem
```

### 生成服务器证书 key
```shell
openssl genrsa -out server.key 2048
```

### 生成服务器签名请求 csr
```shell
openssl req -new -key server.key -out server.csr
```

### 用CA Key 签名 server.csr，得到server.crt

这里签名的时候要指定: *subjectAltName*
```shell
openssl x509 -req -in server.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out server.crt -days 3650 -sha256 -extfile <(printf "subjectAltName=DNS:your.domain.com,DNS:*.domain2.com")
```

### 如何使用
将的 server.crt和 server.key, 部署到服务器。比如nginx:
```nginx
server {
    listen       443 ssl;
    server_name  your.domain.com;
    ssl_certificate     /usr/local/nginx/cert/server.crt;  
    ssl_certificate_key  /usr/local/nginx/cert/server.key; # 
}
```
把CA.pem下发给客户端,导入到系统受信任的根证书里面.
