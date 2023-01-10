---
title: "如何使用python从智能卡中读取证书？"
description: "使用python读取智能卡"
headline:
modified: 2022-08-12 15:34
category: personal
tags: [python]
image:
  feature:
comments: true
mathjax:
---

通常智能卡制造商会提供一个库（.so或.dll）实现PKCS#11标准。  
您可以使用多种解决方案通过此库与您的智能卡进行通信。如：pkcs11-tool（CLI接口）、PyKCS11（python包装器）。

这是一个如何使用 PyKCS11 实现的示例：

```python
from asn1crypto import x509
from PyKCS11 import *

pkcs11 = PyKCS11Lib()
pkcs11.load('<MANUFACTURER_LIBRARY_PATH>')
# get slot value via pkcs11.getSlotList(tokenPresent=False). Usually it's 0
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
session.login('<SMART_CARD_PIN_CODE>')
result = []
certs = session.findObjects([(CKA_CLASS, CKO_CERTIFICATE)])
for cert in certs:
    cka_value, cka_id = session.getAttributeValue(cert, [CKA_VALUE, CKA_ID])
    cert_der = bytes(cka_value)
    cert = x509.Certificate.load(cert_der)
    result.append(cert)
print(result)
```

这样就能够在 Linux 和 Windows 上列出智能卡上的证书
