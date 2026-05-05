from flask import Flask
from dotenv import load_dotenv
import os

# 載入 .env 檔案（如果存在的話）
load_dotenv()

def create_app():
    # 初始化 Flask 應用程式
    app = Flask(__name__)
    
    # 讀取環境變數，若無則使用預設值
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 載入 Blueprint (路由)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
