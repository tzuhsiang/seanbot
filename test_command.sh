Generated signature: IzcAQRsce9T6OehY9mAa2dZiaI//n40u/gaFOG7oTOo=

Test command:
curl -X POST http://localhost:5050/callback \
-H "Content-Type: application/json" \
-H "X-Line-Signature: IzcAQRsce9T6OehY9mAa2dZiaI//n40u/gaFOG7oTOo=" \
-d '{
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
}'
