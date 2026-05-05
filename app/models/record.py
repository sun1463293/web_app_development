import sqlite3
import os
from contextlib import contextmanager

# 預設資料庫路徑：指向 /Users/peggy/Desktop/web_app_development/instance/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

@contextmanager
def get_db_connection():
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以使用 dict 的方式存取
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    os.makedirs(os.path.dirname(schema_path), exist_ok=True)
    
    # 如果 schema.sql 尚未建立，提供一個預設的建表語句
    if not os.path.exists(schema_path):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount INTEGER NOT NULL CHECK(amount >= 0),
            date TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    else:
        with open(schema_path, 'r', encoding='utf-8') as f:
            create_table_sql = f.read()

    with get_db_connection() as conn:
        conn.executescript(create_table_sql)
        conn.commit()

def create_record(record_type, category, amount, date, description=""):
    """新增一筆紀錄"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (type, category, amount, date, description) VALUES (?, ?, ?, ?, ?)",
            (record_type, category, amount, date, description)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_records(order_by="date DESC"):
    """取得所有紀錄"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 簡單的防呆，確保 order_by 格式正確
        safe_order_by = "date DESC" if "DESC" in order_by.upper() else "date ASC"
        cursor.execute(f"SELECT * FROM records ORDER BY {safe_order_by}")
        return [dict(row) for row in cursor.fetchall()]

def get_record_by_id(record_id):
    """根據 ID 取得單筆紀錄"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_record(record_id, record_type, category, amount, date, description=""):
    """更新單筆紀錄"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE records SET type = ?, category = ?, amount = ?, date = ?, description = ? WHERE id = ?",
            (record_type, category, amount, date, description, record_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_record(record_id):
    """刪除單筆紀錄"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_summary():
    """計算目前的總收入、總支出、總儲蓄與可用餘額"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT type, SUM(amount) as total FROM records GROUP BY type")
        results = cursor.fetchall()
        
        summary = {"income": 0, "expense": 0, "saving": 0}
        for row in results:
            if row["type"] in summary:
                summary[row["type"]] = row["total"] or 0
            
        summary["balance"] = summary["income"] - summary["expense"] - summary["saving"]
        return summary
