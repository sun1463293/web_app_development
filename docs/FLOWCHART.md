# 流程圖文件 (Flowchart)

這份文件基於 PRD 的需求與系統架構，視覺化了個人記帳系統的使用者操作路徑與系統內部的資料流動。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者在網站上的各種操作路徑，包含新增收支、查看歷史紀錄以及瀏覽圖表分析。

```mermaid
flowchart LR
    Start(["使用者開啟網頁"]) --> Home["首頁 (儀表板)"]
    
    Home --> Action{"選擇操作？"}
    
    Action -->|查看總覽| Dashboard["顯示當前可用餘額與當月收支摘要"]
    Action -->|新增紀錄| AddForm["填寫收支/儲蓄表單"]
    Action -->|查看歷史| HistoryList["瀏覽歷史紀錄清單"]
    Action -->|查看圖表| ChartView["查看每月分類花費比例圖表"]
    
    AddForm --> AddSubmit{"選擇類別並送出"}
    AddSubmit -->|新增收入| SaveIncome["儲存收入紀錄"]
    AddSubmit -->|新增支出| SaveExpense["儲存支出紀錄 (含食衣住行育樂)"]
    AddSubmit -->|新增儲蓄| SaveSaving["儲存儲蓄紀錄"]
    
    SaveIncome --> ReturnHome["重新計算餘額並返回首頁/列表"]
    SaveExpense --> ReturnHome
    SaveSaving --> ReturnHome
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖詳細描述了當使用者「新增一筆支出紀錄」時，系統前後端及資料庫的完整互動流程。

```mermaid
sequenceDiagram
    actor User as "使用者"
    participant Browser as "瀏覽器"
    participant Flask as "Flask Route (app.py / routes)"
    participant Model as "Model (record.py)"
    participant DB as "SQLite"

    User->>Browser: 在首頁點擊「新增支出」，填寫金額與分類後送出表單
    Browser->>Flask: POST /record (帶有金額、日期、分類等資料)
    Flask->>Model: 呼叫新增紀錄的函式 create_record(data)
    Model->>DB: 執行 SQL: INSERT INTO records ...
    DB-->>Model: 回傳執行成功
    Model-->>Flask: 紀錄新增完成
    Flask-->>Browser: 重新導向 (Redirect) 至首頁或歷史清單頁面 (GET /)
    Browser->>User: 顯示更新後的可用餘額與最新紀錄
```

## 3. 功能清單對照表

以下整理了系統中的主要功能，以及預計對應的 URL 路徑與 HTTP 方法：

| 功能名稱 | 對應 URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 總覽儀表板 (首頁) | `/` | GET | 顯示當前可用餘額、最近幾筆紀錄與當月摘要 |
| 顯示新增紀錄表單 | `/record/new` | GET | 顯示填寫收入/支出/儲蓄的 HTML 表單 |
| 送出新增紀錄 | `/record` | POST | 接收表單資料並寫入資料庫 |
| 查看歷史紀錄列表 | `/records` | GET | 列出所有歷史收支紀錄 (可支援分頁或月份篩選) |
| 查看分類花費圖表 | `/analytics` | GET | 顯示各類別支出比例的圓餅圖或長條圖 |
| 刪除單筆紀錄 (擴充功能) | `/record/<id>/delete` | POST | 刪除特定 ID 的收支紀錄 |
