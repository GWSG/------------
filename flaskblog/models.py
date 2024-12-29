from datetime import datetime  # 導入 datetime 模組，用於處理日期和時間
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 用於生成和驗證加密的 JSON Web Token
from flaskblog import db, login_manager, app  # 導入資料庫實例、登入管理器和 Flask 應用實例
from flask_login import UserMixin  # 提供用戶模型的基本功能，如是否已驗證


@login_manager.user_loader  # 註冊用戶加載器函數，供登入管理器使用
def load_user(user_id):
    return User.query.get(int(user_id))  # 根據用戶 ID 從資料庫中查找並返回用戶對象


class User(db.Model, UserMixin):  # 定義 User 模型，繼承資料庫模型和用戶功能基類
    id = db.Column(db.Integer, primary_key=True)  # 定義用戶 ID 欄位，主鍵，整數類型
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名欄位，最大長度 20，必填且唯一
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件欄位，最大長度 120，必填且唯一
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 用戶頭像文件名稱，默認為 default.jpg
    password = db.Column(db.String(60), nullable=False)  # 密碼欄位，最大長度 60，必填
    posts = db.relationship('Post', backref='author', lazy=True)  # 與 Post 模型的關聯，backref 提供反向引用

    def get_reset_token(self, expires_sec=1800):  # 定義方法，用於生成密碼重設令牌，默認過期時間為 1800 秒
        s = Serializer(app.config['SECRET_KEY'], expires_sec)  # 初始化加密序列化器
        return s.dumps({'user_id': self.id}).decode('utf-8')  # 返回包含用戶 ID 的加密令牌，解碼為字符串

    @staticmethod  # 定義靜態方法，無需傳入實例
    def verify_reset_token(token):  # 用於驗證密碼重設令牌
        s = Serializer(app.config['SECRET_KEY'])  # 初始化加密序列化器
        try:
            user_id = s.loads(token)['user_id']  # 解密令牌，提取用戶 ID
        except:  # 如果解密失敗
            return None  # 返回 None 表示令牌無效
        return User.query.get(user_id)  # 根據用戶 ID 查找並返回用戶對象

    def __repr__(self):  # 定義字符串表示，用於調試
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"  # 返回用戶名、電子郵件和頭像文件名稱


class Post(db.Model):  # 定義 Post 模型，表示文章
    id = db.Column(db.Integer, primary_key=True)  # 定義文章 ID 欄位，主鍵，整數類型
    title = db.Column(db.String(100), nullable=False)  # 定義文章標題欄位，最大長度 100，必填
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 定義文章發布日期欄位，默認為當前 UTC 時間
    content = db.Column(db.Text, nullable=False)  # 定義文章內容欄位，必填
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 定義作者 ID 欄位，外鍵關聯到用戶表的 ID 欄位，必填

    def __repr__(self):  # 定義字符串表示，用於調試
        return f"Post('{self.title}', '{self.date_posted}')"  # 返回文章標題和發布日期
