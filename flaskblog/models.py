# 導入 datetime 模組，用來處理日期與時間
from datetime import datetime
# 從 flaskblog 模組中導入資料庫對象 db 和登入管理器 login_manager
from flaskblog import db, login_manager
# 從 flask_login 模組中導入 UserMixin，用來提供用戶模型的基礎功能
from flask_login import UserMixin


# 定義一個用戶加載器函數，用來加載指定 ID 的用戶
@login_manager.user_loader
def load_user(user_id):
    # 使用資料庫查詢用戶 ID，並返回對應的用戶對象
    return User.query.get(int(user_id))


# 定義 User 類別，繼承資料庫模型類 db.Model 和用戶功能基類 UserMixin
class User(db.Model, UserMixin):
    # 定義用戶的 ID 欄位，主鍵，整數類型
    id = db.Column(db.Integer, primary_key=True)
    # 定義用戶名欄位，字串類型，最大長度 20，唯一且不允許為空
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 定義用戶電子郵件欄位，字串類型，最大長度 120，唯一且不允許為空
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 定義用戶圖片文件欄位，字串類型，最大長度 20，不允許為空，預設為 'default.jpg'
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # 定義用戶密碼欄位，字串類型，最大長度 60，不允許為空
    password = db.Column(db.String(60), nullable=False)
    # 定義與 Post 模型的關聯，backref 為 'author'，lazy 為 True 表示延遲加載
    posts = db.relationship('Post', backref='author', lazy=True)

    # 定義用戶模型的字符串表示，用於調試
    def __repr__(self):
        # 返回用戶名、電子郵件與圖片文件名稱的格式化字串
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# 定義 Post 類別，繼承資料庫模型類 db.Model
class Post(db.Model):
    # 定義文章的 ID 欄位，主鍵，整數類型
    id = db.Column(db.Integer, primary_key=True)
    # 定義文章標題欄位，字串類型，最大長度 100，不允許為空
    title = db.Column(db.String(100), nullable=False)
    # 定義文章發布日期欄位，日期時間類型，不允許為空，預設為當前 UTC 時間
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 定義文章內容欄位，文本類型，不允許為空
    content = db.Column(db.Text, nullable=False)
    # 定義文章的作者 ID 欄位，整數類型，外鍵關聯到用戶表的 ID 欄位，不允許為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 定義文章模型的字符串表示，用於調試
    def __repr__(self):
        # 返回文章標題與發布日期的格式化字串
        return f"Post('{self.title}', '{self.date_posted}')"
