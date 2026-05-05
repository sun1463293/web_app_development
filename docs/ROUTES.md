# 路由設計文件 (ROUTES)

這份文件基於前面的 PRD、系統架構與資料庫設計，詳細規劃了個人記帳系統的網址路徑 (URL)、HTTP 方法與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 總覽儀表板 (首頁) | GET | `/` | `templates/index.html` | 顯示當前可用餘額與當月收支摘要 |
| 歷史紀錄列表 | GET | `/records` | `templates/records/list.html` | 列出所有收支紀錄 |
| 新增紀錄頁面 | GET | `/records/new` | `templates/records/new.html` | 顯示填寫收支/儲蓄的表單 |
| 建立紀錄 | POST | `/records` | — | 接收表單資料，寫入資料庫後重導向 |
| 分類花費圖表 | GET | `/analytics` | `templates/analytics.html` | 顯示各類別支出比例的圖表 |
| 刪除單筆紀錄 | POST | `/records/<id>/delete` | — | 刪除特定紀錄後重導向 |

## 2. 每個路由的詳細說明

### `GET /` (總覽儀表板)
- **輸入**：無
- **處理邏輯**：呼叫 `get_summary()` 取得收入、支出、儲蓄與可用餘額。呼叫 `get_all_records()` 取得最近幾筆紀錄（可限制筆數）。
- **輸出**：渲染 `index.html`
- **錯誤處理**：若資料庫連線失敗，顯示友好錯誤訊息。

### `GET /records` (歷史紀錄列表)
- **輸入**：(未來可擴充 GET 參數如 `?month=2024-05`)
- **處理邏輯**：呼叫 `get_all_records()` 取出所有歷史紀錄。
- **輸出**：渲染 `records/list.html`
- **錯誤處理**：無特殊錯誤，若無資料顯示「目前無紀錄」。

### `GET /records/new` (新增紀錄頁面)
- **輸入**：無
- **處理邏輯**：無特殊邏輯，單純準備表單。
- **輸出**：渲染 `records/new.html`
- **錯誤處理**：無。

### `POST /records` (建立紀錄)
- **輸入**：表單欄位 `type`, `category`, `amount`, `date`, `description`
- **處理邏輯**：驗證 `amount` 是否為正整數、必填欄位是否皆有值。通過後呼叫 `create_record(...)` 寫入資料庫。
- **輸出**：成功後重導向至 `GET /` 或 `GET /records`。
- **錯誤處理**：若驗證失敗，將錯誤訊息帶回並重新渲染 `records/new.html`。

### `GET /analytics` (分類花費圖表)
- **輸入**：無
- **處理邏輯**：從資料庫中取得支出 (expense) 紀錄，並依據 `category` 加總，整理成圖表所需格式。
- **輸出**：渲染 `analytics.html`
- **錯誤處理**：若完全無支出紀錄，需在畫面上提示「目前尚無支出資料」。

### `POST /records/<id>/delete` (刪除單筆紀錄)
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `delete_record(id)` 刪除該筆資料。
- **輸出**：成功後重導向至 `GET /records`。
- **錯誤處理**：若找不到該 ID，可忽略或回傳 404 Not Found。

## 3. Jinja2 模板清單

所有的模板都應繼承自 `base.html`，以維持導覽列與樣式的一致性。

- `templates/base.html`：共用版型，包含 `<head>`、導覽列 (Navbar)、引入 CSS/JS 與主要內容區塊 `{% block content %}`。
- `templates/index.html`：首頁儀表板，繼承 `base.html`。
- `templates/records/list.html`：紀錄列表頁，繼承 `base.html`。
- `templates/records/new.html`：新增紀錄表單頁，繼承 `base.html`。
- `templates/analytics.html`：圖表分析頁，繼承 `base.html`。
