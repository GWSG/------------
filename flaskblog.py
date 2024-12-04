from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) 
#如果找不到db,就先輸入from flaskblog import db,再輸入from flaskblog import db,app
#再輸入app.app_context().push(),最後再輸入db.create_all()

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



posts = [
    {
        'author': 'Corey Schafer',      #作者姓名
        'title': 'Blog Post 1',         #貼文標題
        'content': 'First post content',#貼文內容
        'date_posted': 'April 20, 2018' #貼文張貼時間
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    },
    {
        'author': 'Henry Lao-Yang',
        'title': 'Blog Post 3',
        'content': 'Hello World',
        'date_posted': 'November 20, 2024'
    },
    {
        'author': 'Kai',
        'title': 'Blog Post 4',
        'content': 'HAHAHAHAHAHAHAHAHAHA',
        'date_posted': 'November 27, 2024'
    }
]


@app.route("/") # 定義路由，當訪問根目錄 '/' 時執行該函式
@app.route("/home")  # 定義另一個路徑 '/home'，與根路徑執行相同的函式
def home():# 定義函式 hello，用於處理上述兩個路徑的請求
    # 使用 render_template 函式，返回 home.html 的模板內容
    # 並將 posts 資料傳遞給模板（假設 posts 是一個已定義的變數，內含要顯示的資料）
    return render_template('home.html', posts=posts)


@app.route("/about") # 定義一個路徑 '/about'，與根路徑執行相同的函式
def about(): # 定義函式 photo，接受可選參數 name（此範例未使用該參數）
    # 使用 render_template 函式，返回 about.html 的模板內容
    # 同時將 title 參數（值為 'About'）傳遞給模板
    return render_template('about.html', title='About')


# 設定 /register 路由，允許 GET 和 POST 方法
@app.route("/register", methods=['GET', 'POST'])
def register():
    # 初始化註冊表單
    form = RegistrationForm()
    
    # 如果表單驗證通過（例如：所有必填欄位都正確填寫）
    if form.validate_on_submit():
        # 顯示成功建立帳號的提示訊息，使用 flash 傳遞訊息
        flash(f'Account created for {form.username.data}!', 'success')
        
        # 導向到 home 頁面
        return redirect(url_for('home'))
    
    # 顯示註冊頁面，並傳遞標題和表單給前端
    return render_template('register.html', title='Register', form=form)


# 設定 /login 路由，允許 GET 和 POST 方法
@app.route("/login", methods=['GET', 'POST'])
def login():
    # 初始化登入表單
    form = LoginForm()
    
    # 如果表單驗證通過
    if form.validate_on_submit():
        # 檢查表單輸入的 email 和 password 是否為預設的管理員帳號
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            # 登入成功，顯示成功訊息
            flash('You have been logged in!', 'success')
            
            # 導向到 home 頁面
            return redirect(url_for('home'))
        else:
            # 登入失敗，顯示失敗訊息
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    # 顯示登入頁面，並傳遞標題和表單給前端
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
     with app.app_context():  # 自動建立應用上下文
        db.create_all()  # 創建資料表
        app.run(debug=True)