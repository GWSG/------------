from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) 
#如果找不到db,就先輸入from flaskblog import db,再輸入from flaskblog import db,app
#再輸入app.app_context().push(),最後再輸入db.create_all()


from flaskblog import routes