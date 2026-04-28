# SmartFridge 路由與頁面設計

本文件詳細規劃了 SmartFridge 的所有 API 路由、URL 路徑設計，以及前端 Jinja2 模板的對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (庫存列表) | GET | `/` | `index.html` | 讀取資料庫顯示所有食材，標示即將過期者 |
| 新增食材頁面 | GET | `/ingredient/add` | `add_item.html` | 顯示新增食材的空白表單 |
| 建立食材 | POST | `/ingredient/add` | — | 接收表單資料，寫入 DB 後重導向至首頁 |
| 編輯食材頁面 | GET | `/ingredient/edit/<int:id>` | `edit_item.html` | 讀取特定食材資料並填入表單 |
| 更新食材 | POST | `/ingredient/edit/<int:id>` | — | 接收修改後的表單資料，更新 DB 後重導向 |
| 刪除食材 | POST | `/ingredient/delete/<int:id>` | — | 從 DB 中刪除指定食材，完成後重導向 |
| AI 剩食食譜推薦 | POST | `/recipes` | `recipes.html` | 接收使用者勾選的食材，呼叫 AI 並顯示食譜 |

## 2. 每個路由的詳細說明

### 首頁 (庫存列表)
- **輸入**：無
- **處理邏輯**：呼叫 `IngredientModel.get_all()` 取得所有食材資料。可以透過 Python 邏輯計算是否距離 `expiry_date` 小於 3 天，加上過期警告標記。
- **輸出**：渲染 `index.html`，傳入 `ingredients` 變數。
- **錯誤處理**：若資料庫為空，顯示「目前無庫存」提示。

### 新增/建立食材
- **輸入**：表單欄位 (`name`, `quantity`, `unit`, `category`, `expiry_date`)
- **處理邏輯**：如果是 GET，直接顯示表單。如果是 POST，接收欄位值，呼叫 `IngredientModel.create(...)` 存入資料庫。
- **輸出**：GET 渲染 `add_item.html`。POST 成功後重導向至 `/` (首頁)。
- **錯誤處理**：若必填欄位缺失，可回傳錯誤訊息重新渲染表單。

### 編輯/更新食材
- **輸入**：URL 參數 `id`，表單欄位 (`name`, `quantity`, ...)
- **處理邏輯**：
  - GET：呼叫 `IngredientModel.get_by_id(id)` 取出舊資料並填入表單。
  - POST：呼叫 `IngredientModel.update(id, ...)` 更新資料。
- **輸出**：GET 渲染 `edit_item.html`。POST 成功後重導向至 `/`。
- **錯誤處理**：若 `id` 不存在回傳 404 Not Found。

### 刪除食材
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `IngredientModel.delete(id)`。
- **輸出**：成功後重導向至 `/`。
- **錯誤處理**：若 `id` 不存在可忽略或提示錯誤。

### AI 剩食食譜推薦
- **輸入**：表單中的多選 Checkbox，傳遞勾選的 `ingredient_ids` 清單。
- **處理邏輯**：根據勾選的 ids 查詢出對應的食材名稱，組成 prompt字串，呼叫外部 AI API (如 OpenAI/Gemini) 請求生成食譜。
- **輸出**：渲染 `recipes.html`，傳入 AI 回傳的食譜字串或結構化資料。
- **錯誤處理**：若 AI API 呼叫失敗或超時，顯示友善的錯誤提示並提供「重試」按鈕。

## 3. Jinja2 模板清單

所有模板皆位於 `app/templates/` 目錄下：

1. **`base.html`**：共用版型（Header, 導覽列, Footer, 載入共用 CSS/JS）。所有其他頁面都繼承此模板。
2. **`index.html`**：首頁，繼承 `base.html`。顯示食材表格或卡片，並包含「勾選食材產生食譜」的表單。
3. **`add_item.html`**：新增食材頁面，繼承 `base.html`。
4. **`edit_item.html`**：編輯食材頁面，繼承 `base.html`。
5. **`recipes.html`**：食譜展示頁面，繼承 `base.html`。顯示 AI 回傳的結果，並提供「回首頁」按鈕。

*(註：因架構文件決定採用集中式路由管理，故不建立 `app/routes/` 目錄，而是將路由骨架集中撰寫於 `app/routes.py` 內。)*
