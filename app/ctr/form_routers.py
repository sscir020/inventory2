#coding:utf-8
from flask import render_template,url_for,redirect,flash,session,request
# from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,AddOprForm#ColorForm#ListForm,OprForm #EditOprForm,EditReworkOprForm #RegistrationForm
from ..models import Opr,Material,User,Accessory
from . import ctr
from ..__init__ import db
from ..decorators import loggedin_required
from main_config import Oprenum,Config,Param,params,paramnums,oprenumNum,oprenumCH

import datetime
import json

@ctr.route('/', methods=['GET', 'POST'])
@ctr.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(user_name=form.username.data).first()
        if user == None:
            flash("用户不存在")
            return redirect(url_for('ctr.log_user_in'))
        elif not user.verify_pass(password=form.userpass.data):
            flash("密码不正确")
            return redirect(url_for('ctr.log_user_in'))
        else:
            # login_user(user)
            # next = request.args.get('next')
            # if next is None or not next.startswith('/'):
            #     return redirect(url_for('ctr.welcome_user'))
            # print(session)
            session['userid'] = user.user_id
            session['username'] = user.user_name
            session['userpass'] = user.user_pass
            flash("登录成功")
            return redirect(url_for('ctr.welcome_user'))
    else:
        flash("需要登录")
    return render_template('login_form.html',form=form)

@ctr.route('/_add_opr_post', methods=['GET', 'POST'])
@loggedin_required
def add_material():
    if request.method == "POST":
        materialname=request.form['input_material_name']
        alarm_level=request.form['input_alarm_level']
        if materialname!=None and materialname!='' :
        # if 'input_accessory_list' in request.form:
        #     list=request.form['input_accessory_list']
        # list1 = request.form
        # print(list1)
            if Material.query.filter_by(material_name=materialname).first() == None:
                dict={}
                for keyid in request.form.keys():
                    if keyid[0:21]=='input_accessory_check':
                        # print(key1)
                        keynum='input_accessory_num_'+keyid[22:]
                        if( request.form[keynum]=='' or int(request.form[keynum])<=0 ):
                            flash("数值应是一个正数")
                            return redirect(url_for('ctr.show_add_material'))
                        else:
                            dict[request.form[keyid]]=request.form[keynum]
                acces=json.dumps(dict)
                print (acces)
                if(len(dict)>0 ):
                    if Accessory.query.filter_by(param_acces=acces).first()==None:
                        a = Accessory(param_num=len(dict),param_acces=acces)
                        db.session.add(a)
                        db.session.commit()
                    a = Accessory.query.filter_by(param_acces=acces).first()
                    m=Material(material_name=materialname, countnum=0,acces_id=a.acces_id,alarm_level=alarm_level)
                else:
                    m = Material(material_name=materialname, countnum=0, acces_id=0,alarm_level=alarm_level)
                db.session.add(m)
                db.session.commit()
                m=Material.query.filter_by(material_name=materialname).first()
                o=Opr(material_id=m.material_id,diff=m.countnum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch=0 )
                db.session.add(o)

                if m.acces_id != None and m.acces_id != 0:
                    a = Accessory.query.filter_by(acces_id=m.acces_id).first()
                    data = json.loads(a.param_acces)
                    for materialid in data:
                        num = int(data[materialid])
                        num = num * m.countnum
                        # print('*************************')
                        # print(num)
                        m1 = Material.query.filter_by(material_id=materialid).first()
                        m1.material_change_num(diff=num,oprtype=Oprenum.INITADD.name,batch=0)
                        o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=Oprenum.INITADD.name,isgroup=False,oprbatch=0)
                        db.session.add(o)
                db.session.commit()
                flash('新材料添加成功')
                return redirect(url_for('ctr.show_materials',page=1))
            else:
                flash('材料名已存在')
        else:
            flash('需要填写材料名称和数量')
    else:
        flash('需要添加新材料')
    return redirect(url_for('ctr.show_add_material'))


def convert_str_num(num):
    if num=='' or num =="":
        return 0
    return int(num)

def change_outbound_num(m,materialid,diff,oprtype,batch):
    m.material_change_num(diff=diff,oprtype=oprtype,batch=0)
    o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True)
    db.session.add(o)

    if m.acces_id!= None and m.acces_id!=0:
        a=Accessory.query.filter_by(acces_id=m.acces_id).first()
        data=json.loads(a.param_acces)
        for materialid in data:
            num=int(data[materialid])
            num=num*diff
            m1=Material.query.filter_by(material_id=materialid).first()
            if m1.material_isvalid_num(diff=diff,oprtype=oprtype,batch=0):
                m1.material_change_num(diff=num,oprtype=oprtype,batch=0)
                o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=oprtype,isgroup=False,oprbatch=batch)
                db.session.add(o)
            else:
                flash("配件数量不足")
                return False
    db.session.commit()


def change_rework_buying_num(m,materialid,diff,oprtype,batch):#outbound,rework,buying
        m.material_change_num(diff=diff,oprtype=oprtype,batch=0)
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True,oprbatch=batch)
        db.session.add(o)
        db.session.commit()



@ctr.route('/_change_num_opr/<page>', methods=['GET', 'POST'])
@loggedin_required
def form_change_num(page):
    diff=0
    materialid=0
    if request.method=="POST":
        for i in range(1,Config.FLASK_NUM_PER_PAGE+1):
            diff=convert_str_num(request.form["input_text_"+str(i)])
            if diff > 0:
                materialid=request.form["input_hidden_" + str(i)]
                break
        if diff > 0:
            # input_list={"入库":1,"出库":2,"修好":3,"返修":4,"购买":5},入库,修好
            if(request.form["input_list_" + str(i)]!='') and request.form["input_list_" + str(i)] in oprenumNum.keys():
                # print(request.form["input_list_" + str(i)])
                # print (oprenumNum[request.form["input_list_" + str(i)]].value)
                index=oprenumNum[request.form["input_list_" + str(i)]].value
                # print(index)
                oprtype=Oprenum(index).name
                # print(oprtype)
                m = Material.query.filter_by(material_id=materialid).first()
                if m == None:
                    flash("材料名不存在")
                elif m.material_isvalid_num(diff=diff, oprtype=oprtype, batch=0) == False:
                    flash("数量超标")
                else:
                    if oprtype==Oprenum.REWORK.name or oprtype==Oprenum.BUYING.name:
                        change_rework_buying_num(m=m,materialid=materialid,diff=diff,oprtype=oprtype,batch=0)
                        flash(oprenumCH[oprtype], "数量更新成功")
                    elif oprtype==Oprenum.OUTBOUND.name:
                        change_outbound_num(m=m,materialid=materialid,diff=diff,oprtype=oprtype,batch=0)
                        flash(oprenumCH[oprtype], "数量更新成功")
                    else:
                        flash("错误的操作类型")
            else:
                flash("需要选择操作类型")
        else:
            flash('需要填写一个正数')
    return redirect(url_for('ctr.show_materials',page=page))

@ctr.route('/form_change_inbound_num_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_inbound_num():
    if request.method=="POST":
        # print(request.form)
        diff=0
        for key in request.form:
            if "input_inbound_num_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    index=key[18:]
                    string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            list=string.split('_')
            materialid=list[0]
            batch=list[1]
            m = Material.query.filter_by(material_id=materialid).first()
            if m == None:
                flash("材料名不存在")
            elif m.material_isvalid_num(diff=diff, oprtype=Oprenum.INBOUND.name, batch=batch) == False:
                flash("数量超标")
            else:
                m.material_change_num(diff=diff,oprtype=Oprenum.INBOUND.name,batch=batch)
                o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.INBOUND.name, isgroup=True,oprbatch=batch)
                db.session.add(o)
                db.session.commit()
    return redirect(url_for('ctr.show_buy_materials'))


@ctr.route('/form_cancel_buy_act', methods=['GET', 'POST'])
@loggedin_required
def form_cancel_buy():
    if request.method=="POST":
        # print(request.form)
        if "input_checkbox" in request.form:
            list=request.form["input_checkbox"].split('_')
            materialid=list[0]
            batch=list[1]
            m = Material.query.filter_by(material_id=materialid).first()
            buydict=json.loads(m.buynum)
            diff=buydict.pop(batch)
            m.buynum=json.dumps(buydict)
            db.session.add(m)
            o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CANCELBUY.name, isgroup=True,oprbatch=batch)
            db.session.add(o)
            db.session.commit()
            flash("订单取消成功")
    return redirect(url_for('ctr.show_buy_materials'))

@ctr.route('/form_change_restore_num_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_restore_num():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_restore_num_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    index=key[18:]
                    string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            list = string.split('_')
            materialid = list[0]
            batch = list[1]
            m = Material.query.filter_by(material_id=materialid).first()
            if m == None:
                flash("材料名不存在")
            elif m.material_isvalid_num(diff=diff, oprtype=Oprenum.RESTORE.name, batch=batch) == False:
                flash("数量超标")
            else:
                m.material_change_num(diff=diff, oprtype=Oprenum.RESTORE.name, batch=batch)
                o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.RESTORE.name, isgroup=True,oprbatch=batch)
                db.session.add(o)
                db.session.commit()
    return redirect(url_for('ctr.show_rework_materials'))


