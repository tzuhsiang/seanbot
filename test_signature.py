#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import os

def generate_signature(channel_secret, body):
    hash = hmac.new(channel_secret.encode('utf-8'),
        body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    return signature

# 測試訊息
body = '''{
  "destination": "xxxxxxxxxx",
  "events": [{
    "type": "message",
    "message": {
      "type": "text",
      "id": "test_id",
      "text": "測試訊息"
    },
    "timestamp": 1462629479859,
    "source": {
      "type": "user",
      "userId": "test_user"
    },
    "replyToken": "test_reply_token",
    "mode": "active"
  }]
}'''

# 從環境變數讀取 Channel Secret
channel_secret = os.getenv("CHANNEL_SECRET", "your_channel_secret")
signature = generate_signature(channel_secret, body)
print(f"Generated signature: {signature}")
print(f"\nTest command:")
print(f"""curl -X POST http://localhost:5050/callback \\
-H "Content-Type: application/json" \\
-H "X-Line-Signature: {signature}" \\
-d '{body}'""")
