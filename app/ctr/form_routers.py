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

@ctr.route('/add_material_act', methods=['GET', 'POST'])
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
                # print (acces)
                if(len(dict)>0 ):
                    if Accessory.query.filter_by(param_acces=acces).first()==None:
                        a = Accessory(param_num=len(dict),param_acces=acces)
                        db.session.add(a)
                        db.session.commit()
                    a = Accessory.query.filter_by(param_acces=acces).first()
                    m = Material(material_name=materialname, countnum=0,acces_id=a.acces_id,alarm_level=alarm_level)
                else:
                    m = Material(material_name=materialname, countnum=0, acces_id=0,alarm_level=alarm_level)
                db.session.add(m)
                db.session.commit()

                m=Material.query.filter_by(material_name=materialname).first()
                o=Opr(material_id=m.material_id,diff=m.countnum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch='', \
                      momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                        m1.material_change_num(diff=num,oprtype=Oprenum.INITADD.name,batch='')
                        o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=Oprenum.INITADD.name,isgroup=False,oprbatch='',\
                                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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

def change_outbound_num(m,materialid,diff,oprtype):
    oprbatch=m.material_change_num(diff=diff,oprtype=oprtype,batch='')
    o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True,oprbatch=oprbatch, \
            momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(o)
    db.session.commit()

    if m.acces_id!= None and m.acces_id!=0:
        a=Accessory.query.filter_by(acces_id=m.acces_id).first()
        data=json.loads(a.param_acces)
        for materialid in data:
            num=int(data[materialid])
            num=num*diff
            m1=Material.query.filter_by(material_id=materialid).first()
            if m1.material_isvalid_num(diff=diff,oprtype=oprtype,batch=''):
                m1.material_change_num(diff=num,oprtype=oprtype,batch='')
                o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=oprtype,isgroup=False, \
                        momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                db.session.add(o)
                db.session.commit()
            else:
                flash("配件数量不足")
                return False



def change_rework_buying_num(m,materialid,diff,oprtype):#outbound,rework,buying
        m.material_change_num(diff=diff,oprtype=oprtype,batch='')
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True, \
                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(o)
        db.session.commit()



@ctr.route('/change_buy_rework_outbound_act/<page>', methods=['GET', 'POST'])
@loggedin_required
def form_change_num(page):
    materialid=0
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    materialid=key[13:]
                    # materialid = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            print(request.form)
            # input_list={"入库":1,"出库":2,"修好":3,"返修":4,"购买":5},入库,修好
            if(request.form["input_oprlist_" + str(materialid)]!='') and request.form["input_oprlist_" + str(materialid)] in oprenumNum.keys():
                # print(request.form["input_list_" + str(i)])
                # print (oprenumNum[request.form["input_list_" + str(i)]].value)
                index=oprenumNum[request.form["input_oprlist_" + str(materialid)]].value
                # print(index)
                oprtype=Oprenum(index).name
                # print(oprtype)
                m = Material.query.filter_by(material_id=materialid).first()
                if m == None:
                    flash("材料名不存在")
                elif m.material_isvalid_num(diff=diff, oprtype=oprtype, batch='') == False:
                    flash("数量超标")
                else:
                    if oprtype==Oprenum.BUYING.name:
                        change_rework_buying_num(m=m,materialid=materialid,diff=diff,oprtype=oprtype)
                        flash("购买列表数量更新成功")
                    elif oprtype == Oprenum.REWORK.name:
                        change_rework_buying_num(m=m,materialid=materialid,diff=diff,oprtype=oprtype)
                        flash("返修列表数量更新成功")
                    elif oprtype==Oprenum.OUTBOUND.name:
                        change_outbound_num(m=m,materialid=materialid,diff=diff,oprtype=oprtype)
                        flash("出库数量更新成功")
                    else:
                        flash("错误的操作类型")
            else:
                flash("请选择操作类型")
        else:
            flash('请填写数量')
    return redirect(url_for('ctr.show_materials',page=page))

@ctr.route('/form_change_inbound_num_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_inbound_num():
    if request.method=="POST":
        print(request.form)
        diff=0
        for key in request.form:
            if "input_inbound_num_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[18:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            comment = request.form['input_comment_' + string]
            list=string.split('_')
            materialid=list[0]
            batch=list[1]
            m = Material.query.filter_by(material_id=materialid).first()
            if m == None:
                flash("材料名不存在")
            elif m.material_isvalid_num(diff=diff, oprtype=Oprenum.INBOUND.name, batch=batch) == False:
                flash("数量超标")
            else:
                batch=m.material_change_num(diff=diff,oprtype=Oprenum.INBOUND.name,batch=batch)
                if batch!='-1':
                    o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.INBOUND.name, isgroup=True,oprbatch=batch,comment=comment, \
                            momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    db.session.add(o)
                    db.session.commit()
        else:
            flash("请选择填写到货数量并提交")
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
            comments_dict=json.loads(m.buy_comments)
            diff=buydict.pop(batch)
            comment =''
            if batch in comments_dict:
                comment=comments_dict.pop(batch)
                m.buy_comments=json.dumps(comments_dict)
            m.buynum = json.dumps(buydict)
            db.session.add(m)
            db.session.commit()
            o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CANCELBUY.name, isgroup=True,oprbatch=batch,comment=comment, \
                    momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(o)
            db.session.commit()
            flash("订单取消成功")
        else:
            flash("请勾选订单并提交")
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
                    string=key[18:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            comment = request.form['input_comment_' + string]
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
                o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.RESTORE.name, isgroup=True,oprbatch=batch, comment=comment,\
                        momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                db.session.add(o)
                db.session.commit()
        else:
            flash("请填写修好数量")

    return redirect(url_for('ctr.show_rework_materials'))


@ctr.route('/form_chang_scrap_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_scrap():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_restore_num_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[18:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            comment=request.form['input_comment_'+string]
            list = string.split('_')
            materialid = list[0]
            batch = list[1]
            m = Material.query.filter_by(material_id=materialid).first()
            if m == None:
                flash("材料名不存在")
            elif m.material_isvalid_num(diff=diff, oprtype=Oprenum.SCRAP.name, batch=batch) == False:
                flash("数量超标")
            else:
                m.material_change_num(diff=diff, oprtype=Oprenum.SCRAP.name, batch=batch,comment=comment)
                o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.SCRAP.name, isgroup=True,oprbatch=batch, comment=comment,\
                        momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                db.session.add(o)
                db.session.commit()
        else:
            flash("请填写修好数量")

@ctr.route('/form_cahnge_rework_comment_act',methods=['GET','POST'])
@loggedin_required
def form_change_rework_comment():
    if request.method == 'POST':
        if 'input_checkbox_comment' in request.form:
            string=request.form['input_checkbox_comment']
            list = string.split('_')
            materialid = list[0]
            batch = list[1]
            comment=request.form['input_comment_'+string]
            m=Material.query.filter_by(materialid=materialid).first()
            comments_dict=json.loads(m.buy_comments)
            comments_dict[batch]=comment
        else:
            flash("请勾选备注")