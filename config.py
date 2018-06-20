from flask_sqlalchemy import SQLAlchemy

from app import app
from app.ctr import ctr

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql://root:1234@localhost:3306/testdb1?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'hard to guess string'

db=SQLAlchemy()
db.init_app(app)

app.register_blueprint(ctr)
app.register_blueprint(ctr,url_prefix='/ctr')
