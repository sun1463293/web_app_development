from flask import Blueprint, render_template, request, redirect, url_for

# 建立 Blueprint，後續在 app.py 中註冊
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    總覽儀表板 (首頁)
    輸入：無
    處理：呼叫 Model 取得摘要資訊與最近幾筆紀錄
    輸出：渲染 index.html
    """
    pass

@main_bp.route('/records', methods=['GET'])
def list_records():
    """
    歷史紀錄列表
    輸入：無 (未來可擴充條件篩選)
    處理：呼叫 Model 取得所有歷史紀錄
    輸出：渲染 records/list.html
    """
    pass

@main_bp.route('/records/new', methods=['GET'])
def new_record_page():
    """
    新增紀錄頁面
    輸入：無
    處理：單純準備表單供使用者填寫
    輸出：渲染 records/new.html
    """
    pass

@main_bp.route('/records', methods=['POST'])
def create_record():
    """
    建立紀錄
    輸入：表單欄位 (type, category, amount, date, description)
    處理：驗證資料並呼叫 Model 寫入資料庫
    輸出：成功後重導向至首頁或列表頁；失敗則重新渲染 new.html 並顯示錯誤訊息
    """
    pass

@main_bp.route('/analytics', methods=['GET'])
def analytics():
    """
    分類花費圖表
    輸入：無
    處理：從 Model 取得支出分類資料並彙整給圖表使用
    輸出：渲染 analytics.html
    """
    pass

@main_bp.route('/records/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    刪除單筆紀錄
    輸入：URL 中的 record_id
    處理：呼叫 Model 刪除指定紀錄
    輸出：成功後重導向至歷史紀錄列表
    """
    pass
