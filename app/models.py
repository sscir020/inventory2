from .__init__ import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id=db.Column(db.Integer,nullable=False,primary_key=True)
    user_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    user_pass = db.Column(db.String(64),nullable=False)

    # def __init__(self,**kwargs):
    #     # self.user_name=username
    #     # self.user_pass=userpass
    #     super(User, self).__init__(**kwargs)
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    def verify_pass(self,password):
        return self.user_pass==password

    def change_pass(self,newpass):
        self.user_pass=newpass
        db.session.add(self)
        db.session.commit()

    def prt(self):
        print(self.user_id,self.user_name,self.user_pass)

class Material(db.Model):
    __tablename__ = 'materials'
    material_id=db.Column(db.Integer,nullable=False,primary_key=True)
    material_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    countnum=db.Column(db.Integer,nullable=False)

    def change_countnum(self,diff):
        self.countnum+=diff
        if(self.countnum<0):
            return False
        db.session.add(self)
        db.session.commit()
        return True
    def prt(self):
        print(self.material_id, self.material_name, self.countnum)

class Opr(db.Model):
    __tablename__ = 'oprs'
    opr_id = db.Column(db.Integer,nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diff=db.Column(db.Integer,nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    # timestamp =db.Column(db.DateTime,index=True,nullable=False)

    def prt(self):
        print(self.opr_id,self.user_id, self.diff, self.material_id)


