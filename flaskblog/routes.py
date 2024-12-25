import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
        'author': 'Henry ',
        'title': 'Blog Post 3',
        'content': 'Hello World',
        'date_posted': 'November 20, 2024'
    },
    {
        'author': 'Kai',
        'title': 'Blog Post 4',
        'content': 'HAHAHAHAHAHAHAHAHAHA',
        'date_posted': 'November 27, 2024'
    },
    {
        'author': 'Lao-Yang',
        'title': 'Blog Post 5',
        'content': 'OOOOOOOOOOOOOOOO',
        'date_posted': 'December 11, 2024'
    },
    {
        'author': 'Kyle',
        'title': 'Blog Post 6',
        'content': 'I am Kyle',
        'date_posted': 'December 18, 2024'
    },
    {
        'author': 'PiPP',
        'title': 'Blog Post 7',
        'content': 'User Account and Profile Picture',
        'date_posted': 'December 25, 2024'
    }
]


# 註冊一個路由，當訪問 "/" 或 "/home" 時，會執行以下函數
@app.route("/")
@app.route("/home")
# 定義 home 函數，用來處理 "/" 和 "/home" 路徑的請求
def home():
    # 回傳 home.html 的模板，並將變數 posts 傳遞給模板
    return render_template('home.html', posts=posts)

# 註冊一個路由，當訪問 "/about" 時，會執行以下函數
@app.route("/about")
# 定義 about 函數，用來處理 "/about" 路徑的請求
def about():
    # 回傳 about.html 的模板，並傳遞 title 參數為 'About'
    return render_template('about.html', title='About')

# 註冊一個路由，當訪問 "/register" 並使用 GET 或 POST 方法時，會執行以下函數
@app.route("/register", methods=['GET', 'POST'])
# 定義 register 函數，用來處理註冊邏輯
def register():
    # 如果當前用戶已經驗證，則重定向到 home 路徑
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # 建立一個註冊表單實例
    form = RegistrationForm()
    # 如果表單驗證通過
    if form.validate_on_submit():
        # 將用戶密碼加密並進行 UTF-8 解碼
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 建立一個新的用戶對象
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # 將用戶數據添加到資料庫會話中
        db.session.add(user)
        # 提交資料庫會話
        db.session.commit()
        # 顯示一個成功創建帳號的訊息
        flash('Your account has been created! You are now able to log in', 'success')
        # 重定向到登錄頁面
        return redirect(url_for('login'))
    # 如果表單驗證失敗，返回 register.html 模板，並傳遞表單數據
    return render_template('register.html', title='Register', form=form)

# 註冊一個路由，當訪問 "/login" 並使用 GET 或 POST 方法時，會執行以下函數
@app.route("/login", methods=['GET', 'POST'])
# 定義 login 函數，用來處理登入邏輯
def login():
    # 如果當前用戶已經驗證，則重定向到 home 路徑
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # 建立一個登入表單實例
    form = LoginForm()
    # 如果表單驗證通過
    if form.validate_on_submit():
        # 從資料庫查找與表單輸入 email 匹配的用戶
        user = User.query.filter_by(email=form.email.data).first()
        # 如果用戶存在且密碼正確
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # 登錄用戶，根據用戶選擇是否記住
            login_user(user, remember=form.remember.data)
            # 嘗試從請求中獲取重定向的下一個頁面
            next_page = request.args.get('next')
            # 如果存在下一頁，則重定向；否則重定向到 home 路徑
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # 如果登入失敗，顯示錯誤訊息
            flash('Login Unsuccessful. Please check email and password', 'danger')
    # 返回 login.html 模板，並傳遞表單數據
    return render_template('login.html', title='Login', form=form)

# 註冊一個路由，當訪問 "/logout" 時，會執行以下函數
@app.route("/logout")
# 定義 logout 函數，用來處理登出邏輯
def logout():
    # 執行登出操作
    logout_user()
    # 重定向到 home 路徑
    return redirect(url_for('home'))

# 定義一個函數 save_picture，用來保存用戶上傳的圖片
def save_picture(form_picture):
    # 生成一個隨機的 16 進制字串，作為文件名稱
    random_hex = secrets.token_hex(8)
    # 分離上傳文件的名稱與副檔名
    _, f_ext = os.path.splitext(form_picture.filename)
    # 組合新的文件名稱
    picture_fn = random_hex + f_ext
    # 設定文件的保存路徑
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # 定義圖片的輸出大小
    output_size = (125, 125)
    # 打開圖片
    i = Image.open(form_picture)
    # 調整圖片大小
    i.thumbnail(output_size)
    # 保存圖片到指定路徑
    i.save(picture_path)

    # 返回文件名稱
    return picture_fn

# 註冊一個路由，當訪問 "/account" 並使用 GET 或 POST 方法時，會執行以下函數
@app.route("/account", methods=['GET', 'POST'])
# 定義 account 函數，用來處理帳戶資訊更新邏輯
@login_required
def account():
    # 建立一個更新帳戶表單實例
    form = UpdateAccountForm()
    # 如果表單驗證通過
    if form.validate_on_submit():
        # 如果用戶有上傳新圖片
        if form.picture.data:
            # 保存圖片並獲取新文件名稱
            picture_file = save_picture(form.picture.data)
            # 更新當前用戶的圖片文件名稱
            current_user.image_file = picture_file
        # 更新用戶的用戶名和電子郵件
        current_user.username = form.username.data
        current_user.email = form.email.data
        # 提交資料庫更新
        db.session.commit()
        # 顯示帳戶更新成功的訊息
        flash('Your account has been updated!', 'success')
        # 重定向到帳戶頁面
        return redirect(url_for('account'))
    # 如果請求是 GET 方法，則預填充用戶數據到表單中
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # 設定用戶的圖片文件路徑
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 返回 account.html 模板，並傳遞數據
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)
