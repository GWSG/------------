import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


# 註冊一個路由，當訪問 "/" 或 "/home" 時，會執行以下函數
@app.route("/")
@app.route("/home")
# 定義 home 函數，用來處理 "/" 和 "/home" 路徑的請求
def home():
    page = request.args.get('page', 1, type=int) # 從查詢參數中獲取當前頁數，默認為 1，並轉換為整數
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2) # 查詢所有文章，按發佈日期降序排列，並進行分頁，每頁顯示 2 篇文章
    return render_template('home.html', posts=posts) #返回經過處理的 home.html，並傳遞文章列表到模板中


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

@app.route("/post/new", methods=['GET', 'POST'])  # 註冊路由，允許通過 GET 和 POST 方法訪問此路徑
@login_required  # 確保只有已登入的用戶才能訪問此路由
def new_post():  # 定義 new_post 函數，用於創建新文章
    form = PostForm()  # 初始化表單，用於接受用戶的輸入
    if form.validate_on_submit():  # 如果表單驗證通過（提交時所有欄位都有效）
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  
        # 創建一個新的文章對象，包含標題、內容和當前用戶作為作者
        db.session.add(post)  # 將新文章添加到資料庫會話中
        db.session.commit()  # 提交資料庫更改
        flash('Your post has been created!', 'success')  # 顯示成功訊息
        return redirect(url_for('home'))  # 重定向到主頁
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')  
    # 渲染創建文章的模板，傳遞表單和標題到模板中

@app.route("/post/<int:post_id>")  # 定義路由，帶有文章 ID 的參數
def post(post_id):  # 定義函數，用於顯示特定文章
    post = Post.query.get_or_404(post_id)  # 從資料庫查詢文章，如果不存在則返回 404 錯誤
    return render_template('post.html', title=post.title, post=post)  
    # 渲染單篇文章的模板，傳遞文章對象和標題

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])  # 定義更新文章的路由
@login_required  # 確保只有已登入的用戶才能訪問此路由
def update_post(post_id):  # 定義更新文章的函數
    post = Post.query.get_or_404(post_id)  # 從資料庫查詢文章，確保文章存在
    if post.author != current_user:  # 如果當前用戶不是文章的作者
        abort(403)  # 返回 403 禁止訪問錯誤
    form = PostForm()  # 初始化表單
    if form.validate_on_submit():  # 如果表單驗證通過
        post.title = form.title.data  # 更新文章標題
        post.content = form.content.data  # 更新文章內容
        db.session.commit()  # 提交資料庫更改
        flash('Your post has been updated!', 'success')  # 顯示更新成功訊息
        return redirect(url_for('post', post_id=post.id))  # 重定向到文章頁面
    elif request.method == 'GET':  # 如果是 GET 方法，填充表單數據
        form.title.data = post.title  # 將現有標題填入表單
        form.content.data = post.content  # 將現有內容填入表單
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')  
    # 經過處理的模板，提供更新文章的功能

@app.route("/post/<int:post_id>/delete", methods=['POST'])  # 定義刪除文章的路由，僅允許 POST 方法
@login_required  # 確保只有已登入的用戶才能訪問此路由
def delete_post(post_id):  # 定義刪除文章的函數
    post = Post.query.get_or_404(post_id)  # 從資料庫查詢文章
    if post.author != current_user:  # 如果當前用戶不是文章的作者
        abort(403)  # 返回 403 禁止訪問錯誤
    db.session.delete(post)  # 刪除文章
    db.session.commit()  # 提交資料庫更改
    flash('Your post has been deleted!', 'success')  # 顯示刪除成功訊息
    return redirect(url_for('home'))  # 重定向到主頁

@app.route("/user/<string:username>") # 定義路由，當訪問 /user/<username> 時，執行此函數
def user_posts(username): # 接收動態 URL 中的用戶名參數
    page = request.args.get('page', 1, type=int) # 從查詢參數中獲取當前頁數，默認為 1，轉換為整數
    user = User.query.filter_by(username=username).first_or_404() # 按發佈日期降序排列,查找該用戶發表的所有文章,按發佈日期降序排列
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4) # 對結果進行分頁，每頁顯示 4 篇文章
    return render_template('user_posts.html', posts=posts, user=user) # 返回經過處理的 user_posts.html，傳遞文章和用戶信息



def send_reset_email(user):  # 定義函數，用於發送密碼重設郵件
    token = user.get_reset_token()  # 為用戶生成一個安全令牌
    msg = Message('Password Reset Request',  # 設置郵件標題
                  sender='noreply@demo.com',  # 發件人電子郵件地址
                  recipients=[user.email])  # 收件人電子郵件地址
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}  # 使用生成的令牌創建密碼重設鏈接

If you did not make this request then simply ignore this email and no changes will be made.
'''  # 郵件正文內容，包含重設密碼的鏈接和指導
    mail.send(msg)  # 發送郵件


@app.route("/reset_password", methods=['GET', 'POST'])  # 定義路由，用於請求密碼重設
def reset_request():
    if current_user.is_authenticated:  # 如果用戶已登入，無需重設密碼
        return redirect(url_for('home'))  # 重定向到主頁
    form = RequestResetForm()  # 初始化密碼重設請求表單
    if form.validate_on_submit():  # 如果表單通過驗證
        user = User.query.filter_by(email=form.email.data).first()  # 查詢電子郵件對應的用戶
        send_reset_email(user)  # 發送密碼重設郵件
        flash('An email has been sent with instructions to reset your password.', 'info')  
        # 顯示提示信息，告知郵件已發送
        return redirect(url_for('login'))  # 重定向到登入頁面
    return render_template('reset_request.html', title='Reset Password', form=form)  
    # 渲染密碼重設請求頁面，並傳遞表單數據


@app.route("/reset_password/<token>", methods=['GET', 'POST'])  # 定義路由，處理令牌驗證和密碼重設
def reset_token(token):
    if current_user.is_authenticated:  # 如果用戶已登入，無需重設密碼
        return redirect(url_for('home'))  # 重定向到主頁
    user = User.verify_reset_token(token)  # 驗證令牌，獲取對應用戶
    if user is None:  # 如果令牌無效或已過期
        flash('That is an invalid or expired token', 'warning')  # 顯示錯誤訊息
        return redirect(url_for('reset_request'))  # 重定向到密碼重設請求頁面
    form = ResetPasswordForm()  # 初始化密碼重設表單
    if form.validate_on_submit():  # 如果表單通過驗證
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  
        # 將新密碼加密並解碼為字符串
        user.password = hashed_password  # 更新用戶的密碼
        db.session.commit()  # 提交資料庫更改
        flash('Your password has been updated! You are now able to log in', 'success')  
        # 顯示成功訊息，告知用戶密碼已更新
        return redirect(url_for('login'))  # 重定向到登入頁面
    return render_template('reset_token.html', title='Reset Password', form=form)  
    # 渲染密碼重設頁面，並傳遞表單數據
