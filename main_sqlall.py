# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:testdb1@localhost:3306/testdb1?charset=utf8'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SECRET_KEY'] = 'hard to guess string'
#
# db=SQLAlchemy(app)
#
# class User(db.Model):
#     __tablename__ = 'users'
#     user_id=db.Column(db.Integer,nullable=False,primary_key=True)
#     user_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
#     user_pass = db.Column(db.String(64),nullable=False)
#     # def __init__(self,user_name,user_pass):
#     #     u=super(User,user_name,user_pass)
#     #     db.session.add(u)
#     #     db.commit()
#
# from flask import  render_template
#
# @app.route('/router1')
# def show_user():
#     print('router-user')
#     users=User.query.all()
#     return render_template('showusers.html',users=users)
#
# if __name__=='__main__':
#     app.run(port=6004,debug=True)