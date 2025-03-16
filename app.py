from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import os
import json
import logging

import requests

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 讀取環境變數
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

# Langchain API 設定
langchain_api_url = os.getenv("LANGCHAIN_API_URL")
api_key = os.getenv("API_KEY")


if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    logger.error("未設置 LINE Bot 憑證！")
    raise ValueError("CHANNEL_ACCESS_TOKEN 和 CHANNEL_SECRET 是必需的")

logger.info("LINE Bot 憑證已載入")

# 初始化 API
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/", methods=['GET'])
def health_check():
    """健康檢查端點"""
    logger.info("收到健康檢查請求")
    return "OK", 200

@app.route("/test", methods=['GET'])
def test_bot():
    """測試 LINE Bot 端點"""
    logger.info("開始測試 LINE Bot")
    try:
        test_message = TextMessage(text="測試訊息")
        logger.info("測試訊息建立成功")
        return "測試成功：訊息物件創建正確", 200
    except Exception as e:
        logger.error(f"測試失敗：{str(e)}", exc_info=True)
        return f"測試失敗：{str(e)}", 500

@app.route("/callback", methods=['POST'])
def callback():
    """處理 LINE Webhook 請求"""
    try:
        signature = request.headers.get('X-Line-Signature', '')

        body = request.get_data(as_text=True)
        logger.info(f"收到的請求: {body}")

        try:
            json_data = json.loads(body)
            logger.info(f"解析後的 JSON: {json.dumps(json_data, indent=2)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析錯誤: {e}")
            return "Invalid JSON", 400

        handler.handle(body, signature)
        return "OK", 200
    except InvalidSignatureError:
        logger.error("驗證失敗！可能是 Signature 錯誤")
        abort(400)
    except Exception as e:
        logger.error(f"發生錯誤: {e}", exc_info=True)
        return "Internal Server Error", 500


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """回應 LINE 訊息"""
    logger.info(f"收到訊息事件: {event}")
    user_text = event.message.text

    #呼叫Langflow的AI API
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "input_value": user_text
    }

    # 發送請求
    response = requests.post(langchain_api_url, headers=headers, json=data)
    try:
        response.raise_for_status()  # 若發生錯誤會觸發例外
        result = response.json()
        reply_text = result['outputs'][0]['outputs'][0]['results']['message'].get('text', '無法獲取對話')
    except Exception as e:
        logger.error(f"Langflow API 錯誤: {e}")
        reply_text = "抱歉，我現在無法正確處理您的訊息"


    try:
        if event.reply_token == "test_reply_token":
            # 測試模式：只記錄不實際發送
            logger.info(f"測試模式：將回覆訊息「{reply_text}」")
            return
            
        # 實際發送回覆
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        logger.info("成功回覆訊息")
    except Exception as e:
        logger.error(f"回覆訊息時發生錯誤: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
