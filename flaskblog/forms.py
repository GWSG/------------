from flask_wtf import FlaskForm  # 從 flask_wtf 模組中導入 FlaskForm，作為所有表單類的基類
from flask_wtf.file import FileField, FileAllowed  # 用於處理文件上傳並限制文件類型
from flask_login import current_user  # 獲取當前登入的用戶
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  # 定義各種表單欄位類型
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # 定義表單驗證器
from flaskblog.models import User  # 導入用戶模型，用於驗證表單數據


# 用戶註冊表單
class RegistrationForm(FlaskForm):
    username = StringField('Username',  # 用戶名輸入框
                           validators=[DataRequired(), Length(min=2, max=20)])  # 必填，長度在 2 到 20 字元之間
    email = StringField('Email',  # 電子郵件輸入框
                        validators=[DataRequired(), Email()])  # 必填，且需符合電子郵件格式
    password = PasswordField('Password', validators=[DataRequired()])  # 密碼輸入框，必填
    confirm_password = PasswordField('Confirm Password',  # 確認密碼輸入框
                                     validators=[DataRequired(), EqualTo('password')])  # 必填，且需與密碼欄位一致
    submit = SubmitField('Sign Up')  # 提交按鈕

    def validate_username(self, username):  # 驗證用戶名是否已存在
        user = User.query.filter_by(username=username.data).first()  # 查詢資料庫
        if user:  # 如果用戶已存在
            raise ValidationError('That username is taken. Please choose a different one.')  # 拋出錯誤訊息

    def validate_email(self, email):  # 驗證電子郵件是否已存在
        user = User.query.filter_by(email=email.data).first()  # 查詢資料庫
        if user:  # 如果電子郵件已存在
            raise ValidationError('That email is taken. Please choose a different one.')  # 拋出錯誤訊息


# 用戶登入表單
class LoginForm(FlaskForm):
    email = StringField('Email',  # 電子郵件輸入框
                        validators=[DataRequired(), Email()])  # 必填，且需符合電子郵件格式
    password = PasswordField('Password', validators=[DataRequired()])  # 密碼輸入框，必填
    remember = BooleanField('Remember Me')  # 記住登入選框
    submit = SubmitField('Login')  # 提交按鈕


# 更新帳戶資訊表單
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])  # 用戶名輸入框
    email = StringField('Email', validators=[DataRequired(), Email()])  # 電子郵件輸入框
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])  
    # 文件上傳框，僅允許上傳 jpg 和 png 文件
    submit = SubmitField('Update')  # 提交按鈕

    def validate_username(self, username):  # 驗證更新的用戶名是否已存在
        if username.data != current_user.username:  # 如果輸入的用戶名與當前用戶名不同
            user = User.query.filter_by(username=username.data).first()  # 查詢資料庫
            if user:  # 如果用戶已存在
                raise ValidationError('That username is taken. Please choose a different one.')  # 拋出錯誤訊息

    def validate_email(self, email):  # 驗證更新的電子郵件是否已存在
        if email.data != current_user.email:  # 如果輸入的電子郵件與當前用戶電子郵件不同
            user = User.query.filter_by(email=email.data).first()  # 查詢資料庫
            if user:  # 如果電子郵件已存在
                raise ValidationError('That email is taken. Please choose a different one.')  # 拋出錯誤訊息


# 新文章表單
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  # 標題輸入框，必填
    content = TextAreaField('Content', validators=[DataRequired()])  # 內容輸入框，多行文字，必填
    submit = SubmitField('Post')  # 提交按鈕


# 重設密碼請求表單
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # 電子郵件輸入框
    submit = SubmitField('Request Password Reset')  # 提交按鈕

    def validate_email(self, email):  # 驗證電子郵件是否存在於資料庫
        user = User.query.filter_by(email=email.data).first()  # 查詢資料庫
        if user is None:  # 如果未找到用戶
            raise ValidationError('There is no account with that email. You must register first.')  # 拋出錯誤訊息


# 重設密碼表單
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])  # 新密碼輸入框，必填
    confirm_password = PasswordField('Confirm Password',  # 確認密碼輸入框
                                     validators=[DataRequired(), EqualTo('password')])  # 必填，且需與密碼欄位一致
    submit = SubmitField('Reset Password')  # 提交按鈕
