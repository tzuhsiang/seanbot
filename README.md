# LINE Bot 專案

這是一個使用 Python Flask 和 LINE Messaging API 建立的 LINE Bot 專案。

## 功能特點

- 使用 Flask 框架處理 webhook 請求
- 整合 LINE Messaging API v3
- Docker 容器化部署
- 完整的錯誤處理和日誌記錄
- 健康檢查端點

## 環境要求

- Python 3.9+
- Docker
- Docker Compose

## 快速開始

1. 複製專案
```bash
git clone [你的專案URL]
cd seanbot
```

2. 設定環境變數
```bash
# 複製範例配置檔
cp .env.example .env

# 編輯 .env 檔案，填入你的 LINE Bot 憑證
# CHANNEL_ACCESS_TOKEN=你的token
# CHANNEL_SECRET=你的secret
```

3. 啟動服務
```bash
docker-compose up -d
```

4. 確認服務狀態
```bash
docker-compose logs
```

## LINE Platform 設定

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立/選擇你的 Provider
3. 建立一個 Messaging API Channel
4. 在 Basic Settings 中取得 Channel Secret
5. 在 Messaging API 中取得 Channel Access Token
6. 設定 Webhook URL: `https://你的網域/callback`
7. 開啟 Use webhook

## 專案結構

```
seanbot/
├── app.py              # 主應用程式
├── requirements.txt    # Python 依賴
├── Dockerfile         # Docker 建構檔
├── docker-compose.yml # Docker Compose 配置
├── .env              # 環境變數（需自行建立）
└── .gitignore        # Git 忽略檔案
```

## API 端點

- `GET /`: 健康檢查
- `GET /test`: 測試 LINE Bot 功能
- `POST /callback`: LINE Webhook 接收端點

## 開發指南

### 本地開發

1. 建立虛擬環境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

2. 安裝依賴
```bash
pip install -r requirements.txt
```

3. 設定環境變數並執行
```bash
export FLASK_ENV=development
python app.py
```

### 使用 Docker

1. 建構映像
```bash
docker-compose build
```

2. 啟動服務
```bash
docker-compose up -d
```

3. 查看日誌
```bash
docker-compose logs -f
```

## 問題排解

1. Webhook 驗證失敗
- 確認 Channel Secret 正確
- 確認請求使用 HTTPS
- 檢查 Signature 是否正確生成

2. 無法接收訊息
- 確認 Webhook URL 設定正確
- 確認 Channel Access Token 有效
- 檢查 LINE Platform 的 webhook 狀態

## 安全性注意事項

- 永遠不要提交 .env 檔案到版本控制
- 定期更新 Channel Access Token
- 使用 HTTPS 進行所有的 API 通訊
- 謹慎處理使用者資料和訊息

## 貢獻指南

1. Fork 本專案
2. 建立特性分支
3. 提交變更
4. 發送 Pull Request

## 授權條款

[你的授權條款]

## 連絡方式

[你的連絡資訊]
