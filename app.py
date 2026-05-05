from app import create_app
from app.models.record import init_db

app = create_app()

if __name__ == '__main__':
    # 在啟動伺服器之前，先確保資料庫與資料表已經建立
    init_db()
    # 啟動 Flask 開發伺服器
    app.run(debug=True)
