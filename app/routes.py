# app/routes.py
# 此檔案為路由骨架，集中管理所有的 Flask 路由 (依據架構文件設計)

def register_routes(app):
    """
    將所有路由註冊到 Flask 應用程式中。
    在 app.py 裡會呼叫此函式並傳入 app 實例。
    """

    @app.route('/', methods=['GET'])
    def index():
        """
        首頁：顯示所有食材清單與庫存狀態，並高亮即將過期的項目。
        """
        pass

    @app.route('/ingredient/add', methods=['GET', 'POST'])
    def add_ingredient():
        """
        新增食材：
        - GET: 顯示新增食材的表單
        - POST: 接收表單資料，寫入資料庫並重導向回首頁
        """
        pass

    @app.route('/ingredient/edit/<int:id>', methods=['GET', 'POST'])
    def edit_ingredient(id):
        """
        編輯食材：
        - GET: 讀取指定 ID 的食材資料，並顯示在編輯表單中
        - POST: 接收修改後的資料，更新至資料庫並重導向回首頁
        """
        pass

    @app.route('/ingredient/delete/<int:id>', methods=['POST'])
    def delete_ingredient(id):
        """
        刪除食材：
        - 接收刪除請求，從資料庫移除指定 ID 的食材並重導向回首頁
        """
        pass

    @app.route('/recipes', methods=['POST'])
    def generate_recipes():
        """
        AI 食譜推薦：
        - 接收使用者勾選的食材清單 (IDs)
        - 呼叫外部 AI API 生成對應的食譜建議
        - 將結果渲染至 recipes.html
        """
        pass
