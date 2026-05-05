from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import record

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
    summary = record.get_summary()
    recent_records = record.get_all_records()[:5]  # 只取前 5 筆作為摘要
    return render_template('index.html', summary=summary, records=recent_records)

@main_bp.route('/records', methods=['GET'])
def list_records():
    """
    歷史紀錄列表
    輸入：無 (未來可擴充條件篩選)
    處理：呼叫 Model 取得所有歷史紀錄
    輸出：渲染 records/list.html
    """
    all_records = record.get_all_records()
    return render_template('records/list.html', records=all_records)

@main_bp.route('/records/new', methods=['GET'])
def new_record_page():
    """
    新增紀錄頁面
    輸入：無
    處理：單純準備表單供使用者填寫
    輸出：渲染 records/new.html
    """
    return render_template('records/new.html')

@main_bp.route('/records', methods=['POST'])
def create_record():
    """
    建立紀錄
    輸入：表單欄位 (type, category, amount, date, description)
    處理：驗證資料並呼叫 Model 寫入資料庫
    輸出：成功後重導向至首頁或列表頁；失敗則重新渲染 new.html 並顯示錯誤訊息
    """
    record_type = request.form.get('type')
    category = request.form.get('category')
    amount_str = request.form.get('amount')
    date = request.form.get('date')
    description = request.form.get('description', '')

    # 簡單驗證必填欄位
    if not all([record_type, category, amount_str, date]):
        flash('請填寫所有必填欄位 (類型、分類、金額、日期)', 'danger')
        return redirect(url_for('main.new_record_page'))

    # 驗證金額是否為正整數
    try:
        amount = int(amount_str)
        if amount < 0:
            flash('金額必須為大於等於零的正數', 'danger')
            return redirect(url_for('main.new_record_page'))
    except ValueError:
        flash('金額必須為有效的數字', 'danger')
        return redirect(url_for('main.new_record_page'))

    # 寫入資料庫
    record_id = record.create_record(record_type, category, amount, date, description)
    
    if record_id:
        flash('紀錄新增成功！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('新增失敗，資料庫發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('main.new_record_page'))

@main_bp.route('/analytics', methods=['GET'])
def analytics():
    """
    分類花費圖表
    輸入：無
    處理：從 Model 取得支出分類資料並彙整給圖表使用
    輸出：渲染 analytics.html
    """
    all_records = record.get_all_records()
    
    # 統計各分類的支出總和
    expenses = {}
    for r in all_records:
        if r['type'] == 'expense':
            cat = r['category']
            expenses[cat] = expenses.get(cat, 0) + r['amount']
            
    return render_template('analytics.html', expenses=expenses)

@main_bp.route('/records/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    刪除單筆紀錄
    輸入：URL 中的 record_id
    處理：呼叫 Model 刪除指定紀錄
    輸出：成功後重導向至歷史紀錄列表
    """
    success = record.delete_record(record_id)
    if success:
        flash('紀錄刪除成功！', 'success')
    else:
        flash('紀錄刪除失敗，找不到該筆資料。', 'danger')
        
    return redirect(url_for('main.list_records'))
