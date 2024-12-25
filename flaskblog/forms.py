# 從 flask_wtf 模組中導入 FlaskForm，用於建立表單類
from flask_wtf import FlaskForm
# 從 flask_wtf.file 模組中導入 FileField 和 FileAllowed，用於處理文件上傳
from flask_wtf.file import FileField, FileAllowed
# 從 flask_login 模組中導入 current_user，用於獲取當前登入的用戶
from flask_login import current_user
# 從 wtforms 模組中導入表單欄位類別
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# 從 wtforms.validators 模組中導入表單驗證器
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# 從 flaskblog.models 模組中導入 User 模型，用於查詢資料庫
from flaskblog.models import User


# 註冊表單類別
class RegistrationForm(FlaskForm):  # 定義一個繼承自 FlaskForm 的註冊表單
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # 定義用戶名驗證方法，檢查用戶名是否已存在於資料庫
    def validate_username(self, username):
        # 查詢資料庫中是否有相同用戶名的記錄
        user = User.query.filter_by(username=username.data).first()
        if user:
            # 如果用戶名已存在，拋出驗證錯誤
            raise ValidationError('That username is taken. Please choose a different one.')

    # 定義電子郵件驗證方法，檢查電子郵件是否已存在於資料庫
    def validate_email(self, email):
        # 查詢資料庫中是否有相同電子郵件的記錄
        user = User.query.filter_by(email=email.data).first()
        if user:
            # 如果電子郵件已存在，拋出驗證錯誤
            raise ValidationError('That email is taken. Please choose a different one.')


# 登入表單類別
class LoginForm(FlaskForm):  # 定義一個繼承自 FlaskForm 的登入表單
    email = StringField('Email',  # 定義一個字串輸入欄位，標籤為 'Email'
                        validators=[DataRequired(), Email()])  
                        # 驗證規則：必填，且需符合 Email 格式
    password = PasswordField('Password', validators=[DataRequired()])  
    # 定義密碼輸入欄位，驗證規則：必填
    remember = BooleanField('Remember Me')  # 定義一個布林選框，標籤為 'Remember Me'
    submit = SubmitField('Login')  # 定義提交按鈕，標籤為 'Login'



# 定義一個更新帳戶表單類 UpdateAccountForm，繼承自 FlaskForm
class UpdateAccountForm(FlaskForm):
    # 定義用戶名欄位，要求必填且長度介於 2 到 20 字元之間
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 定義電子郵件欄位，要求必填且符合電子郵件格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 定義上傳圖片欄位，僅允許上傳 jpg 和 png 格式的文件
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # 定義提交按鈕
    submit = SubmitField('Update')

    # 定義用戶名驗證方法，檢查更新的用戶名是否已存在於資料庫
    def validate_username(self, username):
        # 如果輸入的用戶名與當前用戶名不同
        if username.data != current_user.username:
            # 查詢資料庫中是否有相同用戶名的記錄
            user = User.query.filter_by(username=username.data).first()
            if user:
                # 如果用戶名已存在，拋出驗證錯誤
                raise ValidationError('That username is taken. Please choose a different one.')

    # 定義電子郵件驗證方法，檢查更新的電子郵件是否已存在於資料庫
    def validate_email(self, email):
        # 如果輸入的電子郵件與當前用戶電子郵件不同
        if email.data != current_user.email:
            # 查詢資料庫中是否有相同電子郵件的記錄
            user = User.query.filter_by(email=email.data).first()
            if user:
                # 如果電子郵件已存在，拋出驗證錯誤
                raise ValidationError('That email is taken. Please choose a different one.')
            

class PostForm(FlaskForm):  # 繼承 FlaskForm，表示這是一個表單類
    title = StringField('Title', validators=[DataRequired()])  
    # 定義一個標題欄位（輸入框類型），標籤為 'Title'
    # 使用 `DataRequired()` 驗證器確保此欄位為必填

    content = TextAreaField('Content', validators=[DataRequired()])  
    # 定義一個內容欄位（多行文字輸入框），標籤為 'Content'
    # 使用 `DataRequired()` 驗證器確保此欄位為必填

    submit = SubmitField('Post')  
    # 定義一個提交按鈕，標籤為 'Post'

