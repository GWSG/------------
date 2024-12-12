from datetime import datetime
from flaskblog import db


class User(db.Model): #建立User使用者的資料庫,使用SQLAlchemy的物件,類別的關鍵字:class
    id = db.Column(db.Integer, primary_key=True) # Integer:整數的意思,primary_key=True:負責主要欄位,意思是讓ID只能有唯一的且不能重複的整數數字
    username = db.Column(db.String(20), unique =True, nullable=False) # 這一段的意思是使用者的名稱不能是相同的,然後nullable的flase的功能是不能是空白的,一定要輸入姓名
    email = db.Column(db.String(120), unique =True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')# 頭貼的部分,如果使用者沒有頭貼的話,預設就是用指定圖片
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self): # 這段是特殊的函式用法,主要定義回傳使用者的名字,帳號,頭貼
         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):  # 定義 Post 類別，繼承自 SQLAlchemy 的 Model
    id = db.Column(db.Integer, primary_key=True)  # id 欄位：整數型，為主鍵，唯一識別每篇文章
    title = db.Column(db.String(100), nullable=False)  # title 欄位：字串型，長度限制 100，不能為空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # date_posted 欄位：儲存文章發布時間，預設為當前時間
    content = db.Column(db.Text, nullable=False)  # content 欄位：儲存文章內容，為長文本，不能為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # user_id 欄位：儲存作者的 ID，外鍵關聯 User 類別中的 id

    def __repr__(self):  # 定義特殊方法，用於返回對象的描述信息
        return f"Post('{self.title}', '{self.date_posted}')"  # 返回文章標題和發布日期
