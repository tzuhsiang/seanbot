# 使用 Python 3.9 作為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade line-bot-sdk \
    && pip install --no-cache-dir -r requirements.txt

# 複製所有應用程式文件
COPY . .

# 啟動 Flask，綁定 5050 端口
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app"]
