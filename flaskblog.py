from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
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
    app.run(debug=True)