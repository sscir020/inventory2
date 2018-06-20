from app import db
# from datetime import datetime
# from . import db

class Material(db.Model):
    __tablename__ = 'materials'
    material_id=db.Column(db.Integer,nullable=False,primary_key=True)
    material_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    countnum=db.Column(db.Integer,nullable=False)

    def __init__(self,material_name,countnum):
        m=super(Material,material_name,countnum)
        db.session.add(m)
        db.commit()

    def change_countnum(self,diff):
        self.countnum+=diff
        if(self.countnum<0):
            self.countnum=0

class User(db.Model):
    __tablename__ = 'users'
    user_id=db.Column(db.Integer,nullable=False,primary_key=True)
    user_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    user_pass = db.Column(db.String(64),nullable=False)
    def __init__(self,user_name,user_pass):
        u=super(User,user_name,user_pass)
        db.session.add(u)
        db.commit()

    def verify_pass(self,userpass):
        return self.user_pass==userpass

class Opr(db.Model):
    __tablename__ = 'oprs'
    opr_id = db.Column(db.Integer,nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diff=db.Column(db.Integer,nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    # timestamp =db.Column(db.DateTime, default=datetime.utcno,nullable=False)
    def __init__(self,user_id,diff,material_id):
        o=super(Opr,user_id,diff,material_id)
        db.session.add(o)
        db.commit()