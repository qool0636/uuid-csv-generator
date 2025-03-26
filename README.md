# UUID CSV 檔案生成器

這是一個簡單的網頁應用程式，可以根據輸入的 UUID 生成相關的 CSV 檔案。

## 本地開發

1. 創建虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行應用：
```bash
python app.py
```

4. 訪問 http://localhost:5000

## 部署到 Render.com

1. 在 [Render.com](https://render.com) 註冊帳號
2. 點擊 "New +" 按鈕，選擇 "Web Service"
3. 連接您的 GitHub 倉庫
4. 選擇倉庫
5. 設置以下配置：
   - Name: uuid-csv-generator
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. 點擊 "Create Web Service"

## 使用方法

1. 訪問部署後的網址
2. 在輸入框中輸入有效的 UUID
3. 點擊 "生成檔案" 按鈕
4. 下載生成的 CSV 檔案

## 注意事項

- 生成的檔案會自動保存在伺服器的 `downloads` 目錄中
- 檔案名稱包含 UUID 的前 8 位和時間戳
- 每次生成都會創建三個不同的 CSV 檔案

## 系統需求

- macOS 10.13 或更高版本
- 不需要安裝 Python 或其他依賴 