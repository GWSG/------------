import os  # 導入 os 模組，用於處理環境變數
from flask import Flask  # 從 Flask 模組中導入 Flask 類，用於創建應用
from flask_sqlalchemy import SQLAlchemy  # 導入 SQLAlchemy，用於處理資料庫
from flask_bcrypt import Bcrypt  # 導入 Bcrypt，用於加密處理
from flask_login import LoginManager  # 導入 LoginManager，用於管理用戶登入狀態
from flask_mail import Mail  # 導入 Mail，用於處理電子郵件功能

app = Flask(__name__)  # 創建 Flask 應用實例
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'  
# 設定應用的密鑰，用於保護數據，例如 CSRF 保護或簽名驗證

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
# 設定資料庫 URI，指定使用 SQLite 作為資料庫，資料庫文件名為 site.db

db = SQLAlchemy(app)  # 初始化 SQLAlchemy 並綁定到應用，用於處理資料庫操作
bcrypt = Bcrypt(app)  # 初始化 Bcrypt，提供密碼加密功能
login_manager = LoginManager(app)  # 初始化 LoginManager，管理用戶登入和登出
#如果找不到db,就先輸入from flaskblog import db,再輸入from flaskblog import db,app
#再輸入app.app_context().push(),最後再輸入db.create_all()


login_manager.login_view = 'login'  
# 設定未登入用戶訪問需要登入的路由時，重定向的登入頁面
login_manager.login_message_category = 'info'  
# 設定閃存消息的分類，這裡設為 'info' 類別

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'  
# 設定電子郵件服務器，這裡使用 Google 的 SMTP 服務器
app.config['MAIL_PORT'] = 587  
# 設定電子郵件服務器的端口號，587 是使用 TLS 的 SMTP 預設端口
app.config['MAIL_USE_TLS'] = True  
# 啟用傳輸層安全性 (TLS) 來加密電子郵件
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  
# 從環境變數中獲取電子郵件地址，用於登入電子郵件服務器
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  
# 從環境變數中獲取電子郵件密碼，用於登入電子郵件服務器

mail = Mail(app)  # 初始化 Flask-Mail 並綁定到應用，用於處理電子郵件發送功能

from flaskblog import routes  
# 從 flaskblog 模組中導入 routes 模組，這是應用的路由邏輯，需放在最後避免循環導入
