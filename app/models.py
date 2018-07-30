# from .__init__ import db
from flask import flash
from main_config import Oprenum
import json,datetime,time
# from datetime import datetime
# from flask_login import UserMixin, AnonymousUserMixin

from sqlalchemy import Column,String,Integer,ForeignKey,Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base=declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id=Column(Integer,nullable=False,primary_key=True)
    user_name=Column(String(64),nullable=False, unique=True, index=True)
    user_pass = Column(String(64),nullable=False)
    role = Column(Integer,nullable=False,default=1)
    oprs = relationship('Opr', backref='users', lazy='dynamic')
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
    #     session.add(self)
    #     session.commitAA()

    def prt(self):
        print(self.user_id,self.user_name,self.user_pass)

class Material(Base):
    __tablename__ = 'materials'
    material_id=Column(Integer,nullable=False,primary_key=True)
    material_name=Column(String(64),nullable=False, unique=True, index=True)##### no defalut
    storenum=Column(Integer,nullable=False,default=0)
    restorenum=Column(Integer,nullable=False,default=0)
    scrapnum=Column(Integer,nullable=False,default=0)
    preparenum=Column(Integer,nullable=False,default=0)
    salenum=Column(Integer,nullable=False,default=0)
    resalenum=Column(Integer,nullable=False,default=0)
    alarm_level=Column(Integer,nullable=False,default=0)
    acces_id=Column(Integer, ForeignKey('accessories.acces_id'))
    oprs = relationship('Opr', backref='materials', lazy='dynamic')
    buybatches = relationship('Buy', backref='materials', lazy='dynamic')
    reworkbatches = relationship('Rework', backref='materials', lazy='dynamic')
    customerservices= relationship('Customerservice', backref='materials', lazy='dynamic')

    def prt(self):
        print(self.material_id, self.material_name, self.countnum,self.reworknum,self.buynum)

class Buy(Base):
    __tablename__='buys'
    buy_id=Column(Integer,nullable=False,primary_key=True)
    material_id = Column(Integer,ForeignKey('materials.material_id'), nullable=False)
    batch=Column(String(32),nullable=False,unique=True,index=True)
    num=Column(Integer,nullable=False,default=0)
    comment=Column(String(64),nullable=True,default='')

class Rework(Base):
    __tablename__='reworks'
    rework_id=Column(Integer,nullable=False,primary_key=True)
    material_id = Column(Integer,ForeignKey('materials.material_id'))
    device_id = Column(Integer,ForeignKey('devices.device_id'))
    MN_id = Column(String(32), nullable=True, default='')
    batch=Column(String(32),nullable=False,unique=True,index=True,default='')
    num=Column(Integer,nullable=False,default=0)
    comment=Column(String(64),nullable=True,default='')

class Opr(Base):
    __tablename__ = 'oprs'
    opr_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    diff = Column(Integer, nullable=False)
    MN_id = Column(String(32), nullable=True,default='')
    material_id = Column(Integer, ForeignKey('materials.material_id'))
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    oprtype = Column(String(32), nullable=False)
    oprbatch = Column(String(32), nullable=False,default='')
    isgroup =Column(Boolean,nullable=False,default=0)
    comment = Column(String(64), nullable=True, default='')
    momentary = Column(DateTime, index=True,default=datetime.datetime.now())#.strftime("%Y-%m-%d %H:%M:%S")

    def prt(self):
        print(self.opr_id, self.user_id, self.diff, self.material_id)

class Accessory(Base):
    __tablename__='accessories'
    acces_id = Column(Integer, nullable=False, primary_key=True)
    param_num = Column(Integer, nullable=False)
    param_acces = Column(String(2048), nullable=False)
    devices = relationship('Device', backref='accessories', lazy='dynamic')

class Device(Base):
    __tablename__='devices'
    device_id = Column(Integer, nullable=False, primary_key=True)
    MN_id = Column(String(32), nullable=False,default='')
    device_type = Column(String(32), nullable=False,default='')
    device_name = Column(String(32), nullable=False, default='')
    storenum = Column(Integer, nullable=False,default=0)
    preparenum = Column(Integer, nullable=False,default=0)
    salenum = Column(Integer, nullable=False,default=0)
    resalenum = Column(Integer, nullable=False,default=0)
    acces_id = Column(Integer, ForeignKey('accessories.acces_id'), nullable=False)
    comment = Column(String(64), nullable=True,default='')
    oprs = relationship('Opr', backref='devices', lazy='dynamic')

class Client(Base):
    __tablename__='clients'
    client_id = Column(Integer, nullable=False, primary_key=True)
    client_name = Column(String(32), nullable=False)
    MN_id = Column(String(32),nullable=False,default='')
    credit=Column(Integer,nullable=True,default=0)
    comment = Column(String(64), nullable=True,default='')

class Customerservice(Base):
    __tablename__='customerservice'
    service_id= Column(Integer, nullable=False, primary_key=True)
    MN_id=Column(String(32), nullable=False,default='')
    material_id=Column(Integer,ForeignKey('materials.material_id'))
    device_id=Column(Integer,ForeignKey('devices.device_id'))
    originnum= Column(Integer, nullable=True,default=0)
    goodnum= Column(Integer, nullable=True,default=0)
    brokennum= Column(Integer, nullable=True,default=0)
    restorenum= Column(Integer, nullable=True,default=0)
    scrapnum= Column(Integer, nullable=True,default=0)
    inboundnum= Column(Integer, nullable=True,default=0)
    resalenum= Column(Integer, nullable=True,default=0)
    comment= Column(String(64), nullable=True,default='')

class Customerservice_his(Base):
    __tablename__='customerservice_his'
    service_id= Column(Integer, nullable=False, primary_key=True)
    MN_id=Column(String(32), nullable=False)
    material_id=Column(Integer,ForeignKey('materials.material_id'))
    device_id=Column(Integer,ForeignKey('devices.device_id'))
    originnum= Column(Integer, nullable=False,default=0)
    goodnum= Column(Integer, nullable=False,default=0)
    brokennum= Column(Integer, nullable=False,default=0)
    restorenum= Column(Integer, nullable=False,default=0)
    scrapnum= Column(Integer, nullable=False,default=0)
    inboundnum= Column(Integer, nullable=False,default=0)
    resalenum= Column(Integer, nullable=False,default=0)
    comment= Column(String(64), nullable=True,default='')
# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False
#
#     def is_administrator(self):pytho
#         return False
#
# login_manager.anonymous_user = AnonymousUser
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# def material_change_countnum(self, diff):
#     self.countnum += diff
#     session.add(self)
#     # session.commit()
#     return True
#
#
# def material_change_buycountnum_rev(self, diff, batch):
#     if diff < 0:
#         self.buynum[batch] -= diff
#     self.countnum += diff
#     session.add(self)
#     # session.commit()
#     return True
#
#
# def material_change_buycountnum(self, diff, batch):
#     if diff > 0:
#         self.buynum -= diff
#     self.countnum += diff
#     session.add(self)
#     # session.commit()
#     return True
#
#
# def material_change_reworknum(self, diff):
#     self.countnum += diff
#     self.reworknum -= diff
#     session.add(self)
#     # session.commit()
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
