# SmartFridge 系統架構設計

## 1. 技術架構說明

### 選用技術與原因
- **後端框架：Flask (Python)**
  - 原因：輕量級且易於上手，適合快速開發 MVP，並且 Python 擁有豐富的 AI 和資料處理套件，有利於未來整合影像辨識與 AI 推薦功能。
- **模板引擎：Jinja2**
  - 原因：內建於 Flask 中，能夠無縫將後端資料渲染至 HTML 頁面，不需額外建置複雜的前端框架（如 React 或 Vue），降低初期開發門檻。
- **資料庫：SQLite**
  - 原因：輕量級的關聯式資料庫，無需額外安裝資料庫伺服器，資料儲存於單一檔案中，非常適合單機或初期小型應用的開發與測試。
- **前端技術：HTML / CSS / JavaScript (原生或輕量級框架)**
  - 原因：搭配 Jinja2 處理基本互動與畫面呈現。

### Flask MVC 模式說明
在我們的專案中，Flask 將採用類似 MVC (Model-View-Controller) 的架構來組織：
- **Model (資料模型)**：負責定義資料庫的表格結構與資料操作邏輯。例如：定義 `Ingredient` (食材) 資料表，包含名稱、數量、到期日等欄位。
- **View (視圖)**：負責呈現使用者介面。在這裡主要由 Jinja2 模板（`.html` 檔案）組成，接收從 Controller 傳來的資料並渲染成最終的網頁。
- **Controller (控制器)**：在 Flask 中主要由 **Routes (路由)** 擔任。負責接收使用者的請求 (HTTP Requests)，呼叫相應的 Model 取得或更新資料，然後將結果傳遞給 View 進行渲染。

---

## 2. 專案資料夾結構

以下為 SmartFridge 系統的建議資料夾結構：

```text
smartfridge/
│
├── app/                      # 應用程式主要邏輯目錄
│   ├── __init__.py           # 初始化 Flask 應用程式與擴充套件
│   ├── models.py             # 資料庫模型 (定義 SQLite 的 Table 結構)
│   ├── routes.py             # Flask 路由控制器 (處理所有的 URL 請求)
│   ├── templates/            # Jinja2 HTML 模板檔案目錄 (View)
│   │   ├── base.html         # 共用版型 (Header, Footer, Navigation)
│   │   ├── index.html        # 首頁 (庫存狀態與過期預警)
│   │   ├── add_item.html     # 新增食材頁面
│   │   └── recipes.html      # AI 食譜推薦結果頁面
│   └── static/               # 靜態資源目錄
│       ├── css/              # 樣式表檔案 (style.css)
│       ├── js/               # 客製化 JavaScript 檔案 (main.js)
│       └── images/           # 網站圖片與使用者上傳的食材圖片
│
├── instance/                 # 存放執行實例專屬的檔案 (例如本機資料庫、密鑰)
│   └── database.db           # SQLite 資料庫檔案
│
├── .env                      # 環境變數設定檔 (如 API Keys、Secret Key)
├── requirements.txt          # Python 依賴套件清單
└── app.py                    # 專案啟動入口點
```

---

## 3. 元件關係圖

以下是系統運作時各元件的互動關係圖：

```mermaid
graph TD
    %% 使用者介面
    Browser[瀏覽器 / 使用者]
    
    %% Flask 控制與處理
    Route[Flask Route (Controller)]
    Template[Jinja2 Template (View)]
    Model[Model (資料邏輯)]
    
    %% 儲存與外部服務
    DB[(SQLite 資料庫)]
    AI_API[外部 AI / 影像辨識 API]

    %% 流程關係
    Browser -- "1. 發送請求 (GET / POST)" --> Route
    Route -- "2. 查詢/更新資料" --> Model
    Model -- "3. 讀寫資料" --> DB
    DB -- "4. 回傳資料" --> Model
    Model -- "5. 將資料回傳給路由" --> Route
    Route -- "6a. 呼叫外部 API (如推薦食譜)" --> AI_API
    AI_API -- "6b. 回傳 AI 結果" --> Route
    Route -- "7. 傳送資料與渲染指令" --> Template
    Template -- "8. 回傳渲染後的 HTML" --> Route
    Route -- "9. 回應結果" --> Browser
```

*(純文字說明版)*：
1. **瀏覽器 → Flask Route**：使用者透過瀏覽器發送請求（例如：查看庫存清單）。
2. **Flask Route → Model → SQLite**：Route 接收請求後，向 Model 請求資料，Model 負責與 SQLite 溝通讀取庫存紀錄。
3. **Flask Route ↔ 外部 API**：若為食譜推薦功能，Route 會將取得的庫存資料發送至 AI API，並接收推薦結果。
4. **Flask Route → Jinja2 Template → 瀏覽器**：Route 將所有準備好的資料傳給 Jinja2 Template 進行畫面渲染，最後將完整的 HTML 頁面回傳給使用者的瀏覽器顯示。

---

## 4. 關鍵設計決策

1. **單一資料庫 (SQLite)**：
   - **原因**：考量到此專案目前為 MVP 階段，主要需求是快速驗證概念。SQLite 不需要繁瑣的配置，可隨專案程式碼一起移動，大幅降低開發初期的基礎設施維護成本。

2. **伺服器端渲染 (SSR) 搭配 Jinja2**：
   - **原因**：為減少開發複雜度並加快開發速度，不採用前後端分離（如 React/Vue + API）的架構。由 Flask 直接負責路由與畫面渲染，能更快實現「庫存狀態監控」與「新增食材」等核心表單操作。

3. **統一的路由控制器 (`routes.py`)**：
   - **原因**：考量到 MVP 功能數量有限（約 5 個主要功能），初期將所有路由邏輯集中於一個 `routes.py` 檔案中，便於檢視與維護。未來若專案規模擴大，可再重構為 Flask Blueprints 以模組化管理。

4. **將 AI/API 呼叫與核心邏輯分離**：
   - **原因**：「影像辨識」與「AI 食譜推薦」涉及外部網路請求，可能會影響系統回應時間。架構上應允許這些功能獨立處理（甚至在未來改為非同步執行），確保首頁與庫存管理等核心操作的流暢性。
