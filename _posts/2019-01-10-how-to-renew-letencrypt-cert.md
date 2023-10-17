---
title: "使用dns挑战续签letsencrtpt证书"
description: "使用dns挑战续签let'sencrtpt证书"
headline:
modified: 2019-01-10 09:34
category: personal
tags: [linux,安全]
image:
  feature:
comments: true
mathjax:
---

#  Letsencrypt 证书续签

一般letsencrypt证书续签可以通过文件验证，在/.well-knows目录下放置指定的文件，certbot工具就能自动验证并下发证书。

有的时候我们没有80端口权限，或者是想获得一个泛域名的证书，这时候通过dns方式验证就能排上用场。

过程也非常的简单：

1. `certbot certonly -d *.dmian.com --manual --preferred-challenges dns`，然后会提醒设置域名记录。

```
 -> sudo certbot certonly -d *.domain.com --manual --preferred-challenges dns
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Renewing an existing certificate for *.domain.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name:

_acme-challenge.domain.com.

with the following value:

0-ghIseVhCR3ygYuh5QtAUpVQM2T1EzPYdD5puA3ZRc
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue

```

2. 按照要求在dns商的后台设置好解析后，就可以确认下一步。

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/domain.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/domain.com/privkey.pem
This certificate expires on 2024-01-15.
These files will be updated when the certificate renews.

NEXT STEPS:
- This certificate will not be renewed automatically. Autorenewal of --manual certificates requires the use of an authentication hook script (--manual-auth-hook) but one was not provided. To renew this certificate, repeat this same certbot command before the certificate's expiry date.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

3. 将上面路径中的证书链接到需要的地方，就完成了证书的更新。不要忘记重启服务应用新证书。


## 参考

+ [Letsencrypt 验证方式](https://letsencrypt.org/zh-cn/docs/challenge-types/)
