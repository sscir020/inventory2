from .__init__ import db
from flask import flash
from main_config import Oprenum
import json,datetime
# from datetime import datetime
# from flask_login import UserMixin, AnonymousUserMixin

class User(db.Model):
    __tablename__ = 'users'
    user_id=db.Column(db.Integer,nullable=False,primary_key=True)
    user_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    user_pass = db.Column(db.String(64),nullable=False)
    oprs = db.relationship('Opr', backref='users', lazy='dynamic')
    # def __init__(self,**kwargs):
    #     # self.user_name=username
    #     # self.user_pass=userpass
    #     super(User, self).__init__(**kwargs)
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    def verify_pass(self,password):
        return self.user_pass==password

    # def change_pass(self,newpass):
    #     self.user_pass=newpass
    #     db.session.add(self)
    #     db.session.commitAA()

    def prt(self):
        print(self.user_id,self.user_name,self.user_pass)

class Material(db.Model):
    __tablename__ = 'materials'
    material_id=db.Column(db.Integer,nullable=False,primary_key=True)
    material_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    countnum=db.Column(db.Integer,nullable=False,default=0)
    reworknum=db.Column(db.String(256),nullable=False,default='{}')
    buynum = db.Column(db.String(256), nullable=False, default='{}')
    alarm_level=db.Column(db.Integer,nullable=False,default=0)
    acces_id=db.Column(db.Integer, db.ForeignKey('accessories.acces_id'),default=0)
    oprs = db.relationship('Opr', backref='materials', lazy='dynamic')

    def material_isvalid_num(self,diff,oprtype,batch):
        if oprtype==Oprenum.INITADD.name:
            if diff<=0:
                flash("新入库数量小于等于0")
                return False
        elif oprtype == Oprenum.OUTBOUND.name:
            if self.countnum<diff:
                flash("出库数量大于库存数量")
                return False
        elif oprtype == Oprenum.BUYING.name:
            if diff<=0:
                flash("购买数量小于等于0")
                return False
        elif oprtype == Oprenum.REWORK.name:
            if self.countnum<diff:
                flash("返修数量大于库存数量")
                return False
        elif oprtype==Oprenum.INBOUND.name:
            buydict = json.loads(self.buynum)
            # print(buydict)
            if batch not in buydict.keys():
                flash("批次不存在")
                return False
            if buydict[batch]<diff:
                flash("入库数量大于购买数量")
                return False
        elif oprtype == Oprenum.RESTORE.name:
            reworkdict = json.loads(self.reworknum)
            if batch not in reworkdict.keys():
                flash("批次不存在")
                return False
            if reworkdict[batch]<diff:
                flash("修好数量大于返修数量")
                return False
        return True

    def material_change_num(self,diff,oprtype,batch):
        if oprtype==Oprenum.INITADD.name:#****
            self.countnum += diff
        elif oprtype == Oprenum.OUTBOUND.name:#****
            self.countnum-=diff
        elif oprtype == Oprenum.BUYING.name:#-->
            buydict=json.loads(self.buynum)
            batch=len(buydict.keys())+1
            buydict[batch]=diff
            self.buynum=json.dumps(buydict)
        elif oprtype == Oprenum.REWORK.name:#-->
            reworkdict = json.loads(self.reworknum)
            batch = len(reworkdict.keys()) + 1
            reworkdict[batch]=diff
            self.reworknum = json.dumps(reworkdict)
            self.countnum-=diff
        elif oprtype==Oprenum.INBOUND.name:####
            buydict = json.loads(self.buynum)
            buydict[batch]-=diff
            if buydict[batch]==0:
                buydict.pop(batch)
            self.buynum = json.dumps(buydict)
            self.countnum+=diff
        elif oprtype == Oprenum.RESTORE.name:####
            reworkdict=json.loads(self.reworknum)
            reworkdict[batch]-=diff
            if reworkdict[batch]==0:
                reworkdict.pop(batch)
            self.reworknum=json.dumps(reworkdict)
            self.countnum+=diff
        elif oprtype == Oprenum.CANCELBUY.name:
            buydict = json.loads(self.buynum)
            value=buydict.pop(batch)
            batch=value
            self.buynum = json.dumps(buydict)
        else:
            flash("操作类型错误")
            batch=-1
        db.session.add(self)
        # db.session.commit()
        return batch

    def material_isvalid_num_rev (self,diff,oprtype,batch):
        if oprtype==Oprenum.INITADD.name:
            if diff> self.countnum:
                flash("取消新入库数量大于库存数量")##
                return False
        elif oprtype == Oprenum.OUTBOUND.name:
            if diff<=0:
                flash("取消出库数量小于等于0")##
                return False
        elif oprtype == Oprenum.BUYING.name:
            buydict = json.loads(self.buynum)
            if batch not in buydict.keys():
                flash("批次不存在")
                return False
            if diff> buydict[batch]:
                flash("取消购买数量大于购买批次数量")##
                return False
        elif oprtype == Oprenum.REWORK.name:
            reworkdict = json.loads(self.reworknum)
            if batch not in reworkdict.keys():
                flash("批次不存在")
                return False
            if diff>reworkdict[batch]:
                flash("取消返修数量大于返修批次数量")##
                return False
        elif oprtype==Oprenum.INBOUND.name:
            if diff>self.countnum:# 5 2  -> 7 0
                flash("取消入库数量大于库存数量")
                return False
        elif oprtype == Oprenum.RESTORE.name:
            if diff>self.countnum:
                flash("取消修好数量大于库存数量")
                return False
        return True


    def material_change_num_rev(self,diff,oprtype,batch):
        if oprtype==Oprenum.INITADD.name:
            self.countnum -= diff
        elif oprtype == Oprenum.OUTBOUND.name:
            self.countnum+=diff
        elif oprtype == Oprenum.BUYING.name:
            # batch=len(self.buynum.keys())+1
            buydict = json.loads(self.buynum)
            # print(buydict)
            buydict[batch]-=diff
            if buydict[batch]==0:
                buydict.pop(batch)
            self.buynum = json.dumps(buydict)
        elif oprtype == Oprenum.REWORK.name:
            reworkdict = json.loads(self.reworknum)
            reworkdict[batch]-=diff
            if reworkdict[batch] == 0:
                reworkdict.pop(batch)
            self.reworknum = json.dumps(reworkdict)
            self.countnum+=diff
        elif oprtype==Oprenum.INBOUND.name:
            buydict = json.loads(self.buynum)
            if batch not in buydict.keys():
                buydict[batch] = diff
            else:
                buydict[batch]+=diff
            self.buynum = json.dumps(buydict)
            self.countnum-=diff
        elif oprtype == Oprenum.RESTORE.name:
            reworkdict = json.loads(self.reworknum)
            if batch not in reworkdict.keys():
                reworkdict[batch] = diff
            else:#  if self.reworknum[batch]==0:
                reworkdict[batch] += diff
            self.reworknum = json.dumps(reworkdict)
            self.countnum-=diff
        elif oprtype == Oprenum.CANCELBUY.name:
            buydict = json.loads(self.buynum)
            buydict[batch]=diff
            self.buynum = json.dumps(buydict)
        else:
            flash("操作类型错误")
            batch=-1
        db.session.add(self)
        # db.session.commit()
        return batch

    def prt(self):
        print(self.material_id, self.material_name, self.countnum,self.reworknum,self.buynum)


class Opr(db.Model):
    __tablename__ = 'oprs'
    opr_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diff = db.Column(db.Integer, nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    oprtype = db.Column(db.String(32), nullable=False)
    oprbatch = db.Column(db.Integer, nullable=False,default=0)
    isgroup =db.Column(db.Boolean,nullable=False,default=0)
    momentary = db.Column(db.DateTime, index=True,default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def prt(self):
        print(self.opr_id, self.user_id, self.diff, self.material_id)

class Accessory(db.Model):
    __tablename__='accessories'
    acces_id = db.Column(db.Integer, nullable=False, primary_key=True)
    param_num = db.Column(db.Integer, nullable=False)
    param_acces = db.Column(db.String(2048), nullable=False)


# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False
#
#     def is_administrator(self):
#         return False
#
# login_manager.anonymous_user = AnonymousUser
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# def material_change_countnum(self, diff):
#     self.countnum += diff
#     db.session.add(self)
#     # db.session.commit()
#     return True
#
#
# def material_change_buycountnum_rev(self, diff, batch):
#     if diff < 0:
#         self.buynum[batch] -= diff
#     self.countnum += diff
#     db.session.add(self)
#     # db.session.commit()
#     return True
#
#
# def material_change_buycountnum(self, diff, batch):
#     if diff > 0:
#         self.buynum -= diff
#     self.countnum += diff
#     db.session.add(self)
#     # db.session.commit()
#     return True
#
#
# def material_change_reworknum(self, diff):
#     self.countnum += diff
#     self.reworknum -= diff
#     db.session.add(self)
#     # db.session.commit()
#     return True


# def isvalid_opr(self, diff):
#     if diff == 0:
#         return False
#     if self.buynum < diff:  # 入库
#         flash("入库数量大于购买数量")
#         return False
#     if self.countnum < -diff:  # 出库
#         flash("出库数量大于库存数量")
#         return False
#     return True
#
#
# def isvalid_rework_opr(self, diff):
#     # print("********************")
#     # print(diff)
#     # print("=====================")
#     if diff == 0:
#         return False
#     if self.reworknum < diff:  # 修好
#         flash("修好数量大于返修数量")
#         return False
#     if self.countnum < -diff:  # 返修
#         flash("返修数量大于库存数量")
#         return False
#     return True
