#coding:utf-8
from flask import render_template,url_for,redirect,flash,session,request
# from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,AddOprForm#ColorForm#ListForm,OprForm #EditOprForm,EditReworkOprForm #RegistrationForm
from ..models import Opr,Material,User,Accessory,Buy,Rework
from . import ctr
from ..__init__ import db
from ..decorators import loggedin_required
from main_config import Oprenum,Config,Param,params,paramnums,oprenumNum,oprenumCH,Oprenum

import datetime,time
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
        alarm_level=convert_str_num(request.form['input_alarm_level'])
        if materialname!=None and materialname!=''and alarm_level>0 :
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
                        if(request.form[keynum]==''or  int(request.form[keynum])<=0 ):
                            flash("数量应是一个正数")
                            return redirect(url_for('ctr.show_add_material'))
                        else:
                            dict[request.form[keyid]]=request.form[keynum]
                acces=json.dumps(dict)
                if(len(dict)>0 ):
                    if Accessory.query.filter(Accessory.param_acces==acces).first()==None:
                        a = Accessory(param_num=len(dict),param_acces=acces)
                        db.session.add(a)
                        db.session.commit()
                    else:
                        a=Accessory.query.filter(Accessory.param_acces==acces).first()
                    m = Material(material_name=materialname, countnum=0,acces_id=a.acces_id,alarm_level=alarm_level)

                    for materialid in dict:
                        o = Opr(material_id=materialid, diff=0, user_id=session['userid'], oprtype=Oprenum.INITADD.name,isgroup=False,oprbatch='',\
                                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        db.session.add(o)
                        db.session.commit()
                else:
                    m = Material(material_name=materialname, countnum=0, acces_id=0,alarm_level=alarm_level)
                db.session.add(m)
                db.session.commit()
                m=Material.query.filter_by(material_name=materialname).first()
                o=Opr(material_id=m.material_id,diff=0,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch='', \
                      momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                db.session.add(o)
                db.session.commit()

                flash('新材料添加成功')
                return redirect(url_for('ctr.show_material_table',page=1))
            else:
                flash('材料名已存在')
        else:
            flash('请正确填写材料名称和数量')
    return redirect(url_for('ctr.show_add_material'))


def convert_str_num(num):
    if num=='' or num =="":
        return 0
    return int(num)
def material_isvalid_num(self,diff,oprtype,batch):
    if diff <= 0:
        flash("数量小于等于0")
        return False
    if oprtype == Oprenum.OUTBOUND.name:
        if self.countnum<diff:
            flash("出库数量大于库存数量")
            return False
    # elif oprtype==Oprenum.INITADD.name:
    #     if diff<=0:
    #         flash("新入库数量小于等于0")
    #         return False
    # elif oprtype == Oprenum.BUYING.name:
    #     if diff<=0:
    #         flash("购买数量小于等于0")
    #         return False
    elif oprtype == Oprenum.REWORK.name:
        if diff>self.countnum:
            flash("返修数量大于库存数量")
            return False
    elif oprtype==Oprenum.INBOUND.name:
        b=Buy.query.filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在")
            return False
        if diff>b.num:
            flash("入库数量大于购买批次数量")
            return False
    elif oprtype == Oprenum.RESTORE.name:
        b = Rework.query.filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在")
            return False
        if diff>b.bum:
            flash("修好数量大于返修批次数量")
            return False
    elif oprtype == Oprenum.CANCELBUY.name:
        b=Buy.query.filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在")
            return False
    elif oprtype == Oprenum.SCRAP.name:
        b = Rework.query.filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在")
            return False
        if diff>b.bum:
            flash("报废数量大于返修数量")
            return False
    else:
        if oprtype!=Oprenum.INITADD.name and oprtype!=Oprenum.BUYING.name:
            flash("操作类型错误")
            return False
    return True

def material_change_num(m,diff,oprtype,batch):
        value=batch
        if oprtype==Oprenum.INITADD.name:#****
            m.countnum += diff
        elif oprtype == Oprenum.OUTBOUND.name:#****
            m.countnum -= diff
        elif oprtype == Oprenum.BUYING.name:#-->
            batch = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            b = Buy.query.filter(Buy.batch == batch).first()
            while b!=None:
                time.sleep(1)
                batch = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                b = Buy.query.filter(Buy.batch == batch).first()
            b=Buy(batch=batch,material_id=m.material_id,num=diff)
            db.session.add(b)
            value = batch
        elif oprtype == Oprenum.REWORK.name:#-->
            batch=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            b = Rework.query.filter(Rework.batch == batch).first()
            while b!=None:
                m.sleep(1)
                batch = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                b = Rework.query.filter(Rework.batch == batch).first()
            b=Rework(batch=batch,material_id=m.material_id,num=diff)
            m.countnum -= diff
            db.session.add(b)
            value = batch
        elif oprtype==Oprenum.INBOUND.name:####
            b = Buy.query.filter(Buy.batch == batch).first()
            b.num-=diff
            m.countnum += diff
            db.session.add(b)
            if b.num==0:
                Buy.query.filter(Buy.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        elif oprtype == Oprenum.RESTORE.name:####
            b = Rework.query.filter(Rework.batch == batch).first()
            b.num -= diff
            m.countnum += diff
            if b.num == 0:
                Rework.query.filter(Rework.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        elif oprtype == Oprenum.CANCELBUY.name:
            b = Buy.query.filter(Buy.batch == batch).first()
            value=b.num
            Buy.query.filter(Buy.batch == batch).delete()
            # db.session.commit()
        elif oprtype == Oprenum.SCRAP.name:
            b = Rework.query.filter(Rework.batch == batch).first()
            b.num -= diff
            if b.num == 0:
                Rework.query.filter(Rework.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        else:
            flash("操作类型错误")
            value='-1'
        # if value!='-1':
        #     db.session.add(self)
        #     db.session.commit()
        return value


def change_materials_oprs_db(oprtype,materialid,diff,isgroup,batch,comment):#BUYING,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
    print('materialid:' + str(materialid) + ",diff:" + str(diff) + ",oprtype:" + str(oprtype) + ",batch:" + str(batch))
    m = Material.query.filter_by(material_id=materialid).first()
    if m == None:
        flash("材料名不存在")
        return False
    elif material_isvalid_num(m=m,diff=diff, oprtype=oprtype, batch=batch) == False:
        flash("数量超标")
        return False
    else:
        value=material_change_num(m=m,diff=diff, oprtype=oprtype, batch=batch)
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                oprbatch=value, comment=comment, momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add_all([m,o])
        db.session.commit()
        db.session.flush()
        db.session.close()
    return True


@ctr.route('/form_rollback_act',methods=['GET','POST'])
@loggedin_required
def form_rollback():
    db.session.rollback()


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
                if oprtype==Oprenum.BUYING.name:
                    if change_materials_oprs_db(oprtype=Oprenum.BUYING.name, materialid=materialid, diff=diff,isgroup=True, batch='', comment='')==True:
                        flash("购买列表数量更新成功")
                    else:
                        flash("购买列表数量更新失败")
                elif oprtype == Oprenum.REWORK.name:
                    if change_materials_oprs_db(oprtype=Oprenum.REWORK.name, materialid=materialid, diff=diff,isgroup=True, batch='', comment='')==True:
                        flash("返修列表数量更新成功")
                    else:
                        flash("返修列表数量更新失败")
                elif oprtype==Oprenum.OUTBOUND.name:
                    m = Material.query.filter_by(material_id=materialid).first()
                    if m.acces_id != None and m.acces_id != 0:
                        a = Accessory.query.filter_by(acces_id=m.acces_id).first()
                        data = json.loads(a.param_acces)
                        for acces_materialid in data:
                            num = int(data[acces_materialid])
                            num = num * diff
                            if change_materials_oprs_db(oprtype=Oprenum.OUTBOUND.name, materialid=acces_materialid, diff=num, isgroup=False,batch='', comment='') == False:
                                flash("配件数量不足")
                                return redirect(url_for('ctr.show_material_table', page=page))
                    if change_materials_oprs_db(oprtype=Oprenum.OUTBOUND.name, materialid=materialid, diff=diff,isgroup=True, batch='', comment='') == True:
                        flash("出库数量更新成功")
                    else:
                        flash("出库数量更新失败")
                else:
                    flash("错误的操作类型")
            else:
                flash("请选择操作类型")
        else:
            flash('请填写数量')
    return redirect(url_for('ctr.show_material_table', page=page))


@ctr.route('/form_cancel_buy_act', methods=['GET', 'POST'])
@loggedin_required
def form_cancel_buy():
    if request.method=="POST":
        # print(request.form)
        if "input_checkbox_cancel" in request.form:
            list=request.form["input_checkbox_cancel"].split('_')
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
            change_materials_oprs_db(oprtype=Oprenum.INBOUND.name, materialid=materialid, diff=diff, isgroup=True,batch=batch, comment=comment)
        else:
            flash("请正确填写到货数量并提交")
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
            change_materials_oprs_db(oprtype=Oprenum.RESTORE.name, materialid=materialid, diff=diff, isgroup=True,batch=batch, comment=comment)
        else:
            flash("请正确填写修好数量")
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
            change_materials_oprs_db(oprtype=Oprenum.SCRAP.name, materialid=materialid, diff=diff, isgroup=True, batch=batch, comment=comment)
        else:
            flash("请正确填写修好数量")
    return redirect(url_for('ctr.show_rework_materials'))



@ctr.route('/form_change_comment_act/<oprtype>',methods=['GET','POST'])
@loggedin_required
def form_change_comment(oprtype):
    if request.method == 'POST':
        if 'input_checkbox_comment' in request.form:
            string=request.form['input_checkbox_comment']
            list = string.split('_')
            materialid = list[0]
            batch = list[1]
            comment=str(request.form['input_comment_'+string])
            if len(comment)<=Config.MAX_CHAR_PER_COMMENT:
                m=Material.query.filter_by(material_id=materialid).first()
                if oprtype==Oprenum.REWORK.name:
                    comments_dict=json.loads(m.rework_comments)
                    comments_dict[batch]=comment
                    m.rework_comments = json.dumps(comments_dict)
                    db.session.add(m)
                    db.session.commit()
                    flash("返修备注修改成功")
                elif oprtype==Oprenum.BUYING.name:
                    comments_dict = json.loads(m.buy_comments)
                    comments_dict[batch] = comment
                    m.buy_comments = json.dumps(comments_dict)
                    db.session.add(m)
                    db.session.commit()
                    flash("购买备注修改成功")
                else:
                    flash("备注类型错误")
            else:
                flash("每条备注不超过20个中文字")
        else:
            flash("请勾选返修备注")
    if oprtype == Oprenum.REWORK.name:
        return redirect(url_for('ctr.show_rework_materials'))
    elif oprtype == Oprenum.BUYING.name:
        return redirect(url_for('ctr.show_buy_materials'))
    else:
        flash("备注类型错误")

# @ctr.route('/form_change_buy_comment_act',methods=['GET','POST'])
# @loggedin_required
# def form_change_buy_comment():
#     if request.method == 'POST':
#         if 'input_checkbox_comment' in request.form:
#             string=request.form['input_checkbox_comment']
#             list = string.split('_')
#             materialid = list[0]
#             batch = list[1]
#             comment=str(request.form['input_comment_'+string])
#             if len(comment)<=40:
#                 m=Material.query.filter_by(materialid=materialid).first()
#                 comments_dict=json.loads(m.buy_comments)
#                 comments_dict[batch]=comment
#                 m.buy_comments = json.dump(comments_dict)
#                 db.session.add(m)
#                 db.session.commit()
#             else:
#                 flash("每条备注不超过20个中文字")
#         else:
#             flash("请勾选购买备注")
#     return redirect(url_for('ctr.show_buy_materials'))

# def change_outbound_num(m,materialid,diff,oprtype):
#     oprbatch=m.material_change_num(diff=diff,oprtype=oprtype,batch='')
#     o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True,oprbatch=oprbatch, \
#             momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     db.session.add(o)
#     db.session.commit()
#
#     if m.acces_id!= None and m.acces_id!=0:
#         a=Accessory.query.filter_by(acces_id=m.acces_id).first()
#         data=json.loads(a.param_acces)
#         for acces_materialid in data:
#             num=int(data[acces_materialid])
#             num=num*diff
#             if change_materials_oprs_db(oprtype=Oprenum.OUTBOUND.name, materialid=acces_materialid, diff=num, isgroup=False,
#                                      batch='', comment='')==False:
#                 flash("配件数量不足")
#                 return False
#
#
#
# def change_rework_buying_num(m,materialid,diff,oprtype):#outbound,rework,buying
#         m.material_change_num(diff=diff,oprtype=oprtype,batch='')
#         o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True, \
#                 momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         db.session.add(o)
#         db.session.commit()

        # if m.acces_id != None and m.acces_id != 0:
        #     a = Accessory.query.filter_by(acces_id=m.acces_id).first()
        #     data = json.loads(a.param_acces)
        #     for materialid in data:
        #         # num = int(data[materialid])
        #         # num = num * m.countnum
        #         m1 = Material.query.filter_by(material_id=materialid).first()
        #         # m1.material_change_num(diff=num,oprtype=Oprenum.INITADD.name,batch='')
        #         o = Opr(material_id=m1.material_id, diff=0, user_id=session['userid'], oprtype=Oprenum.INITADD.name,isgroup=False,oprbatch='',\
        #                 momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #         db.session.add(o)
        #         db.session.commit()