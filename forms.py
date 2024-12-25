from flask_wtf import FlaskForm  # 引入 FlaskForm，Flask-WTF 提供的表單類型基礎類
from wtforms import StringField, PasswordField, SubmitField, BooleanField  # 引入表單欄位類型
from wtforms.validators import DataRequired, Length, Email, EqualTo  # 引入表單驗證器

# 註冊表單類別
class RegistrationForm(FlaskForm):  # 定義一個繼承自 FlaskForm 的註冊表單
    username = StringField('Username',  # 定義一個字串輸入欄位，標籤為 'Username'
                           validators=[DataRequired(), Length(min=2, max=20)])  
                           # 驗證規則：必填，長度需在 2 到 20 字元之間
    email = StringField('Email',  # 定義一個字串輸入欄位，標籤為 'Email'
                        validators=[DataRequired(), Email()])  
                        # 驗證規則：必填，且需符合 Email 格式
    password = PasswordField('Password', validators=[DataRequired()])  
    # 定義密碼輸入欄位，驗證規則：必填
    confirm_password = PasswordField('Confirm Password',  
                                     validators=[DataRequired(), EqualTo('password')])  
                                     # 確認密碼輸入欄位，驗證規則：必填，需與密碼欄位相等
    submit = SubmitField('Sign Up')  # 定義提交按鈕，標籤為 'Sign Up'

# 登入表單類別
class LoginForm(FlaskForm):  # 定義一個繼承自 FlaskForm 的登入表單
    email = StringField('Email',  # 定義一個字串輸入欄位，標籤為 'Email'
                        validators=[DataRequired(), Email()])  
                        # 驗證規則：必填，且需符合 Email 格式
    password = PasswordField('Password', validators=[DataRequired()])  
    # 定義密碼輸入欄位，驗證規則：必填
    remember = BooleanField('Remember Me')  # 定義一個布林選框，標籤為 'Remember Me'
    submit = SubmitField('Login')  # 定義提交按鈕，標籤為 'Login'

