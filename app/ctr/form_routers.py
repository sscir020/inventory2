#coding:utf-8
from flask import render_template,url_for,redirect,flash,session,request
# from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,RegistrationForm,AddClientForm,AddMaterialForm,SearchMNForm #AddOprForm#ColorForm#ListForm,OprForm #EditOprForm,EditReworkOprForm
from ..models import Opr,Material,User,Accessory,Buy,Rework,Device,Client,Customerservice
from . import ctr
# from ..__init__ import db
from ..decorators import loggedin_required
from main_config import Config,oprenumNum,oprenumCH,Oprenum,CommentType #Param,params,paramnums,

import datetime,time
import json

from ..__init__ import dbsession

@ctr.route('/', methods=['GET', 'POST'])
@ctr.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        user=dbsession.query(User).filter_by(user_name=form.username.data).first()
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
            session['role'] = user.role
            flash("登录成功")
            return redirect(url_for('ctr.welcome_user'))
    else:
        flash("需要登录")
    return render_template('login_form.html',form=form)

@ctr.route('/registration', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        if dbsession.query(User).filter_by(user_name=form.username.data).first() == None:
            u=User(user_name=form.username.data,user_pass=form.userpass.data,role=form.role.data)
            dbsession.add(u)
            dbsession.commit()
            dbsession.flush()
            flash('账户创建成功')
            return redirect(url_for('ctr.log_user_in'))
        else:
            flash('账户已存在')
    else:
        flash('需要注册')
    return render_template('registration_form.html',form=form)

@ctr.route('/add_client_post',methods=['GET','POST'])
def add_client():
    form=AddClientForm()
    if form.validate_on_submit():
        if dbsession.query(Client).filter_by(client_name=form.clientname.data).first() == None:
            c= dbsession.query(Client).filter(Device.MN_id==form.MN_id.data).first() == None
            if c==None:
                c=Client(client_name=form.clientname.data,MN_id=form.MN_id.data,)
                dbsession.add(c)
                dbsession.commit()
                dbsession.flush()
            else:
                flash("设备MN号已被使用")
        else:
            flash("客户已存在")
    else:
        flash("需要填写")
    return render_template('add_client_form.html',form=form)


@ctr.route('/add_material_act', methods=['GET', 'POST'])
@loggedin_required
def add_material():
    form=AddMaterialForm()
    if form.validate_on_submit():
        materialname=form.materialname.data
        countnum=form.countnum.data
        alarm_level=form.alarm_level.data
        if countnum>=0 and alarm_level>=0 :
            if dbsession.query(Material).filter_by(material_name=materialname).first() == None:
                m = Material(material_name=materialname, countnum=countnum, acces_id=0,alarm_level=alarm_level)
                dbsession.add(m)
                dbsession.commit()
                dbsession.flush()
                # m=dbsession.query(Material).filter_by(material_name=materialname).first()
                o=Opr(material_id=m.material_id,diff=countnum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch='', \
                      momentary=datetime.datetime.now())
                dbsession.add(o)
                dbsession.commit()
                dbsession.flush()
                flash('新材料添加成功')
                return redirect(url_for('ctr.show_material_table',page=1))
            else:
                flash('材料名已存在')
        else:
            flash('数量或者警戒值应大于等于0')
    else:
        flash('需要填写')
    return render_template('add_material_form.html',form=form)
# @ctr.route('/add_material_act', methods=['', 'POST'])
# @loggedin_required
# def add_material():
#     if request.method == "POST":
#         materialname=request.form['input_text_material_name']
#         countnum=convert_str_num(request.form['input_number_countnum'])
#         alarm_level=convert_str_num(request.form['input_number_alarm_level'])
#         if materialname!=None and materialname!=''and alarm_level>0 :
#         # if 'input_accessory_list' in request.form:
#         #     list=request.form['input_accessory_list']
#         # list1 = request.form
#         # print(list1)
#             if dbsession.query(Material).filter_by(material_name=materialname).first() == None:
#                 m = Material(material_name=materialname, countnum=countnum, acces_id=0,alarm_level=alarm_level)
#                 dbsession.add(m)
#                 dbsession.commit()
#                 dbsession.flush()
#                 m=dbsession.query(Material).filter_by(material_name=materialname).first()
#                 o=Opr(material_id=m.material_id,diff=countnum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch='', \
#                       momentary=datetime.datetime.now())
#                 dbsession.add(o)
#                 dbsession.commit()
#                 dbsession.flush()
#                 flash('新材料添加成功')
#                 return redirect(url_for('ctr.show_material_table',page=1))
#             else:
#                 flash('材料名已存在')
#         else:
#             flash('请正确填写材料名称和数量')
#     return redirect(url_for('ctr.show_add_material'))

@ctr.route('/add_device_act', methods=['', 'POST'])
@loggedin_required
def add_device():
    if request.method == "POST":
        devicename=request.form['input_text_device_name']
        MN_id = convert_str_num(request.form['input_number_MN'])
        devicetype=request.form['input_text_device_type']
        # countnum=convert_str_num(request.form['input_number_countnum'])
        # alarm_level=convert_str_num(request.form['input_number_alarm_level'])

        if devicename!=None and devicename!=''and devicetype!=None and devicetype!='' and  MN_id!=None and MN_id!='' :
            if dbsession.query(Device).filter_by(device_name=devicename).first() == None:
                if dbsession.query(Device).filter_by(MN_id=MN_id).first() == None:
                    dict={}
                    for keyid in request.form.keys():
                        if keyid[0:21]=='input_accessory_check':
                            # print(key1)
                            keynum='input_accessory_num_'+keyid[22:]
                            if(request.form[keynum]==''or  int(request.form[keynum])<=0 ):
                                flash("数量应是一个正数")
                                return redirect(url_for('ctr.show_add_device'))
                            else:
                                dict[request.form[keyid]]=request.form[keynum]
                    acces=json.dumps(dict)
                    if(len(dict)>0 ):
                        if dbsession.query(Accessory).filter(Accessory.param_acces==acces).first()==None:
                            a = Accessory(param_num=len(dict),param_acces=acces)
                            dbsession.add(a)
                            dbsession.commit()
                            dbsession.flush()
                        else:
                            a=dbsession.query(Accessory).filter(Accessory.param_acces==acces).first()
                        d = Device(device_name=devicename,device_type=devicetype,MN_id=MN_id, countnum=0,acces_id=a.acces_id)

                        for material_id in dict:
                            o = Opr(material_id=material_id, diff=0*int(dict[material_id]), user_id=session['userid'], oprtype=Oprenum.DINITADD.name,isgroup=False,oprbatch='',\
                                    momentary=datetime.datetime.now())
                            dbsession.add(o)
                            dbsession.commit()
                            dbsession.flush()
                    else:
                        flash("请勾选参数")
                        return redirect(url_for('ctr.show_add_device'))
                    dbsession.add(d)
                    dbsession.commit()
                    dbsession.flush()
                    d=dbsession.query(Device).filter_by(device_name=devicename).first()
                    o=Opr(device_id=d.device_id,diff=0,user_id=session['userid'],oprtype=Oprenum.DINITADD.name, isgroup=True,oprbatch='', \
                          momentary=datetime.datetime.now())
                    dbsession.add(o)
                    dbsession.commit()
                    dbsession.flush()
                    flash('新设备添加成功')
                    return redirect(url_for('ctr.show_device_table',page=1))
                else:
                    flash('MN号已存在')
            else:
                flash('设备名已存在')
        else:
            flash('请正确填写设备名称,类型,MN号，警戒值')
    return redirect(url_for('ctr.show_add_device'))

def convert_str_num(num):
    if num=='' or num =="":
        return 0
    return int(num)
def material_isvalid_num(m,diff,oprtype,batch,MN_id):
    if diff <= 0:
        flash("数量小于等于0")
        return False
    if oprtype == Oprenum.OUTBOUND.name:
        if diff>m.preparenum:
            flash("出库数量大于备货数量"+str(diff)+">"+str(m.preparenum))
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
        if diff>m.countnum:
            flash("返修数量大于库存数量"+str(diff)+">"+str(m.countnum))
            return False
    elif oprtype==Oprenum.INBOUND.name:
        b=dbsession.query(Buy).filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("入库数量大于购买批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.RESTORE.name:
        b = dbsession.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("修好数量大于返修批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.CANCELBUY.name:
        b=dbsession.query(Buy).filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在"+str(batch))
            return False
    elif oprtype == Oprenum.SCRAP.name:
        b = dbsession.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("报废数量大于返修批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.RESALE.name:
        if MN_id == '':
            flash("需要填写MN号"+str(MN_id))
            return False
        if diff>m.countnum:
            flash("售后带出数量大于库存数量"+str(diff)+">"+str(m.countnum))
            return False
    elif oprtype == Oprenum.RECYCLE.name:
        if MN_id == '':
            flash("需要填写MN号"+str(MN_id))
            return False
        # c = dbsession.query(Customerservice).filter(Customerservice.MN_id == MN_id).first()
        # if c != None:
        #     flash("售后带回设备已存在"+str(MN_id))
        #     return False
    elif oprtype == Oprenum.INITADD.name:
        pass
    elif oprtype == Oprenum.BUYING.name:
        pass
    elif oprtype == Oprenum.PREPARE.name:
        if diff>m.countnum:
            flash("备货数量大于库存数量"+str(diff)+">"+str(m.countnum))
            return False
    elif oprtype == Oprenum.DINITADD.name:
        pass
    elif oprtype == Oprenum.DOUTBOUND.name:
        if diff > m.preparenum:
            flash("设备出库数量大于备货数量"+str(diff)+">"+str(m.preparenum))
            return False
    else:
        flash("操作类型错误")
        return False
    return True

def material_change_num(m,diff,oprtype,batch,MN_id):
        value=batch
        if oprtype==Oprenum.INITADD.name:#****
            # m.countnum += diff
            pass
        elif oprtype == Oprenum.OUTBOUND.name:#****
            m.preparenum -= diff
        elif oprtype == Oprenum.BUYING.name:#-->
            batch = datetime.datetime.now()
            b = dbsession.query(Buy).filter(Buy.batch == batch).first()
            while b!=None:
                time.sleep(1)
                batch = datetime.datetime.now()
                b = dbsession.query(Buy).filter(Buy.batch == batch).first()
            b=Buy(batch=batch,material_id=m.material_id,num=diff)
            dbsession.add(b)
            value = batch
        elif oprtype == Oprenum.REWORK.name:#-->
            batch=datetime.datetime.now()
            b = dbsession.query(Rework).filter(Rework.batch == batch).first()
            while b!=None:
                m.sleep(1)
                batch = datetime.datetime.now()
                b = dbsession.query(Rework).filter(Rework.batch == batch).first()
            b=Rework(batch=batch,material_id=m.material_id,num=diff)
            m.countnum -= diff
            dbsession.add(b)
            value = batch
        elif oprtype==Oprenum.INBOUND.name:####
            b = dbsession.query(Buy).filter(Buy.batch == batch).first()
            b.num-=diff
            m.countnum += diff
            dbsession.add(b)
            if b.num==0:
                dbsession.query(Buy).filter(Buy.batch == batch).delete()
                # dbsession.commit()
            else:
                dbsession.add(b)
        elif oprtype == Oprenum.RESTORE.name:####
            b = dbsession.query(Rework).filter(Rework.batch == batch).first()
            b.num -= diff
            m.countnum += diff
            if b.num == 0:
                dbsession.query(Rework).filter(Rework.batch == batch).delete()
                # dbsession.commit()
            else:
                dbsession.add(b)
        elif oprtype == Oprenum.CANCELBUY.name:
            b = dbsession.query(Buy).filter(Buy.batch == batch).first()
            value=b.num
            Buy.query.filter(Buy.batch == batch).delete()
            # dbsession.commit()
        elif oprtype == Oprenum.SCRAP.name:
            b = dbsession.query(Rework).filter(Rework.batch == batch).first()
            b.num -= diff
            if b.num == 0:
                dbsession.query(Rework).filter(Rework.batch == batch).delete()
                # dbsession.commit()
            else:
                dbsession.add(b)
        elif oprtype == Oprenum.RECYCLE.name:
            c = Customerservice(countnum=diff, material_id=m.material_id, MN_id=MN_id)
            dbsession.add(c)
        elif oprtype == Oprenum.RESALE.name:
            m.countnum-=diff
        elif oprtype == Oprenum.PREPARE.name:
            m.countnum-=diff
            m.preparenum+=diff
        elif oprtype == Oprenum.DINITADD.name:
            # m.countnum += diff
            pass
        elif oprtype == Oprenum.DOUTBOUND.name:
            m.preparenum -= diff
        else:
            flash("操作类型错误")
            value='-1'
        # if value!='-1':
        #     dbsession.add(self)
        #     dbsession.commit()
        return value


def change_materials_oprs_db(oprtype,materialid,diff,isgroup,batch,MN_id,comment):#BUYING,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
    print('materialid:' + str(materialid) + ",diff:" + str(diff) + ",oprtype:" + str(oprtype) + ",batch:" + str(batch))
    m = dbsession.query(Material).filter(Material.material_id==materialid).first()
    if m == None:
        flash("材料名不存在")
        return False
    elif material_isvalid_num(m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id) == False:
        flash("数量超标")
        return False
    else:
        value=material_change_num(m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id)
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                oprbatch=value, MN_id=MN_id,comment=comment, momentary=datetime.datetime.now())
        dbsession.add_all([m,o])
        dbsession.commit()
        dbsession.flush()
        # dbsession.close()
    return True

@ctr.route('/form_rollback_act',methods=['','POST'])
@loggedin_required
def form_rollback():
    dbsession.rollback()
    return redirect(url_for('ctr.show_join_oprs_main'))


@ctr.route('/change_buy_rework_outbound_act', methods=['', 'POST'])
@loggedin_required
def form_change_num():
    materialid=0
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    materialid=key[13:]
                    MN_id=request.form['input_text_MN_'+materialid]
                    # materialid = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            # print(request.form)
            # input_list={"入库":1,"出库":2,"修好":3,"返修":4,"购买":5},入库,修好
            if(request.form["input_oprlist_" + str(materialid)]!='') and request.form["input_oprlist_" + str(materialid)] in oprenumNum.keys():
                # print(request.form["input_list_" + str(i)])
                # print (oprenumNum[request.form["input_list_" + str(i)]].value)
                index=oprenumNum[request.form["input_oprlist_" + str(materialid)]].value
                # print(index)
                oprtype=Oprenum(index).name
                # print(oprtype)
                if oprtype==Oprenum.BUYING.name:
                    if change_materials_oprs_db(oprtype=Oprenum.BUYING.name, materialid=materialid, diff=diff,isgroup=True, batch='',MN_id='', comment='')==True:
                        flash("购买列表数量更新成功")
                    else:
                        flash("购买列表数量更新失败")
                elif oprtype == Oprenum.REWORK.name:
                    if change_materials_oprs_db(oprtype=Oprenum.REWORK.name, materialid=materialid, diff=diff,isgroup=True, batch='',MN_id='',  comment='')==True:
                        flash("返修列表数量更新成功")
                    else:
                        flash("返修列表数量更新失败")
                elif oprtype==Oprenum.OUTBOUND.name:
                    if change_materials_oprs_db(oprtype=Oprenum.OUTBOUND.name, materialid=materialid, diff=diff,isgroup=True, batch='',MN_id='',  comment='') == True:
                        flash("出库数量更新成功")
                    else:
                        flash("出库数量更新失败")
                elif oprtype == Oprenum.RECYCLE.name:
                    if change_materials_oprs_db(oprtype=Oprenum.RECYCLE.name, materialid=materialid, diff=diff,isgroup=True, batch='',MN_id=MN_id,  comment='')==True:
                         flash("售后带回到售后列表数量更新成功")
                    else:
                        flash("售后带回到售后列表数量更新失败")
                elif oprtype == Oprenum.RESALE.name:
                    if change_materials_oprs_db(oprtype=Oprenum.RESALE.name, materialid=materialid, diff=diff,isgroup=True, batch='',MN_id=MN_id,  comment='')==True:
                        flash("售后带出列表数量更新成功")
                    else:
                        flash("售后带出列表数量更新失败")
                elif oprtype == Oprenum.PREPARE.name:
                    if change_materials_oprs_db(oprtype=Oprenum.PREPARE.name, materialid=materialid, diff=diff, isgroup=True, batch='',MN_id='',  comment='') == True:
                        flash("备货数量更新成功")
                    else:
                        flash("备货数量更新失败")
                else:
                    flash("错误的操作类型")
            else:
                flash("请选择操作类型")
        else:
            flash('请填写数量')
    return redirect(url_for('ctr.show_material_table'))


@ctr.route('/form_cancel_buy_act', methods=['', 'POST'])
@loggedin_required
def form_cancel_buy():
    if request.method=="POST":
        # print(request.form)
        if "input_checkbox_cancel" in request.form:
            list=request.form["input_checkbox_cancel"].split('_')
            materialid=list[0]
            batch=list[1]
            b = dbsession.query(Buy).filter(Buy.batch==batch).first()
            diff=b.num
            o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CANCELBUY.name, isgroup=True,oprbatch=batch,comment=b.comment, \
                    momentary=datetime.datetime.now())#.strftime("%Y-%m-%d %H:%M:%S")
            dbsession.query(Buy).filter(Buy.batch==batch).delete()
            # dbsession.commit()
            dbsession.add(o)
            dbsession.commit()
            dbsession.flush()
            flash("订单取消成功")
        else:
            flash("请勾选订单并提交")
    return redirect(url_for('ctr.show_buy_materials'))



@ctr.route('/form_device_outbound_act',methods=['','POST'])
@loggedin_required
def form_device_outbound():
    device_id=0
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    device_id=key[13:]#input_number_
                    break
        if diff > 0:
            d=dbsession.query(Device).filter(Device.device_id==device_id).first()
            if d!= None:
                # if diff <= d.preparenum:
                    if d.acces_id != None and d.acces_id != 0:
                        a = dbsession.query(Accessory).filter_by(acces_id=d.acces_id).first()
                        data = json.loads(a.param_acces)
                        for materialid in data:
                            num = int(data[materialid])
                            num = num * diff
                            m=dbsession.query(Material).filter_by(material_id=materialid).first()
                            if material_isvalid_num(m=m,diff=num, oprtype=Oprenum.DOUTBOUND.name, batch='') ==False:
                                flash("配件数量不足")
                                return redirect(url_for('ctr.show_device_table'))
                        for materialid in data:
                            num = int(data[materialid])
                            num = num * diff
                            change_materials_oprs_db(oprtype=Oprenum.DOUTBOUND.name, materialid=materialid, diff=num, isgroup=False,batch='', comment='')
                        d.countnum += diff
                        # d.preparenum += diff
                        o = Opr(device_id=device_id, diff=diff, user_id=session['userid'],oprtype=Oprenum.DOUTBOUND.name, isgroup=True, oprbatch='', comment=d.comment, \
                                momentary=datetime.datetime.now())  # .strftime("%Y-%m-%d %H:%M:%S")
                        dbsession.add_all([d,o])
                        dbsession.commit()
                        dbsession.flush()
                        flash("设备出库更新成功")
                    else:
                        flash("设备参数不存在")
                # else:
                #     flash("要备货数量大于库存数量")
            else:
                flash("设备不存在")
        else:
            flash("请正确填写修好数量")
    return redirect(url_for('ctr.show_device_table'))

@ctr.route('/form_change_inbound_num_act', methods=['', 'POST'])
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

@ctr.route('/form_change_restore_num_act', methods=['', 'POST'])
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




@ctr.route('/form_chang_scrap_act', methods=['', 'POST'])
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

@ctr.route('/form_change_cinbound_act', methods=['', 'POST'])
@loggedin_required
def form_change_cinbound():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[13:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            comment=request.form['input_comment_'+string]
            list = string.split('_')
            service_id = list[0]
            MN_id = list[1]
            c=dbsession.query(Customerservice).filter(Customerservice.MN_id==MN_id).first()
            m=dbsession.query(Material).filter(Material.material_id==c.materialid).first()
            if c==None:
                flash("售后不存在")
            elif m==None:
                flash("材料不存在")
            else:
                if diff>c.countnum:
                    flash("入库数量大于售后带回数量")
                else:
                    c.countnum-=diff
                    m.countnum+=diff
                    o = Opr(materialid=c.materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CINBOUND.name,
                            isgroup=True, oprbatch='', MN_id=MN_id,comment=c.comment, \
                            momentary=datetime.datetime.now())
                    dbsession.add_all([c, m,o])
                    dbsession.commit()
                    dbsession.flush()
        else:
            flash("请正确填写修好数量")
    return redirect(url_for('ctr.show_customerservice'))

@ctr.route('/form_change_crework_act', methods=['', 'POST'])
@loggedin_required
def form_change_crework():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[13:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            comment=request.form['input_comment_'+string]
            list = string.split('_')
            service_id = list[0]
            MN_id = list[1]
            c = dbsession.query(Customerservice).filter(Customerservice.MN_id == MN_id).first()
            batch=datetime.datetime.now()
            b = dbsession.query(Rework).filter(Rework.batch == batch).first()
            while b!=None:
                c.sleep(1)
                batch = datetime.datetime.now()
                b = dbsession.query(Rework).filter(Rework.batch == batch).first()
            b=Rework(batch=batch,material_id=c.material_id,num=diff,MN_id=MN_id)
            c.countnum -= diff
            o = Opr(materialid=c.materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CREWORK.name,
                    isgroup=True, oprbatch='', MN_id=MN_id, comment=c.comment, \
                    momentary=datetime.datetime.now())
            dbsession.add_all([b,c,o])
            dbsession.commit()
            dbsession.flush()
        else:
            flash("请正确填写修好数量")
    return redirect(url_for('ctr.show_customerservice'))

@ctr.route('/form_change_dresale_act', methods=['', 'POST'])
@loggedin_required
def form_change_dresale():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[13:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            comment=request.form['input_comment_'+string]
            list = string.split('_')
            service_id = list[0]
            MN_id = list[1]
            c=dbsession.query(Customerservice).filter(Customerservice.MN_id==MN_id).first()
            d=dbsession.query(Device).filter(Device.MN_id==MN_id).first()
            if c==None:
                flash("售后不存在")
            elif d==None:
                flash("设备不存在")
            else:
                if diff>c.countnum:
                    flash("售后带出数量大于售后带回数量")
                else:
                    c.countnum-=diff
                    o = Opr(device_id=d.device_id, diff=diff, user_id=session['userid'], oprtype=Oprenum.DRESALE.name,
                            isgroup=True, oprbatch='', MN_id=MN_id,comment=c.comment, \
                            momentary=datetime.datetime.now())
                    dbsession.add_all([c,o])
                    dbsession.commit()
                    dbsession.flush()
        else:
            flash("请正确填写修好数量")
    return redirect(url_for('ctr.show_customerservice'))

@ctr.router('/form_search_MN_act',methods=['GET','POST'])
@loggedin_required
def form_search_MN():
    form=SearchMNForm()
    sql=None
    if form.validate_on_submit():
        MN_id=form.MN_id.data
        if dbsession.query(Device).filter(Device.MN_id==MN_id).first()!=None:
            sql = dbsession.query(Opr.opr_id,Material.material_id, Material.material_name,Device.device_id,Device.device_name,Client.client_id,Client.client_name,Opr.oprtype, Opr.diff,\
                                  Opr.isgroup,Opr.oprbatch,Opr.comment, User.user_name,Opr.momentary\
                                  ).outerjoin(Material,Material.material_id==Opr.material_id).outerjoin(Device,Device.device_id==Opr.device_id).outerjoin(Client,Client.client_id==Opr.client_id).\
                                  join(User,User.user_id==Opr.user_id).order_by(Opr.opr_id.desc()).filter(Opr.MN_id==MN_id).limit(50)
    return render_template('search_MN.html',form=form,join_oprs=sql)


@ctr.route('/form_change_comment_act/<comment_type>',methods=['','POST'])
@loggedin_required
def form_change_comment(comment_type):
    if request.method == 'POST':
        if 'input_checkbox_comment' in request.form:
            string=request.form['input_checkbox_comment']
            list = string.split('_')
            id = list[0]
            batch = list[1]
            comment=str(request.form['input_comment_'+string])
            if len(comment)<=Config.MAX_CHAR_PER_COMMENT:
                if comment_type==CommentType.REWORK.name:
                    b=dbsession.query(Rework).filter_by(batch=batch).first()
                    b.comment=comment
                    dbsession.add(b)
                    dbsession.commit()
                    dbsession.flush()
                    flash("返修备注修改成功")
                elif comment_type==CommentType.BUY.name:
                    b = dbsession.query(Buy).filter_by(batch=batch).first()
                    b.comment = comment
                    dbsession.add(b)
                    dbsession.commit()
                    dbsession.flush()
                    flash("购买备注修改成功")
                elif comment_type == CommentType.DEVICE.name:
                    d = dbsession.query(Device).filter_by(device_id=id).first()
                    d.comment =comment
                    dbsession.add(d)
                    dbsession.commit()
                    dbsession.flush()
                    flash("设备备注修改成功")
                elif comment_type == CommentType.CLIENT.name:
                    c = dbsession.query(Client).filter_by(client_id=id).first()
                    c.comment =comment
                    dbsession.add(c)
                    dbsession.commit()
                    dbsession.flush()
                    flash("客户备注修改成功")
                elif comment_type == CommentType.CUSTOMERSERVICE.name:
                    c = dbsession.query(Customerservice).filter_by(service_id=id).first()
                    c.comment =comment
                    dbsession.add(c)
                    dbsession.commit()
                    dbsession.flush()
                    flash("售后备注修改成功")
                else:
                    flash("备注类型错误")
            else:
                flash("每条备注不超过20个中文字")
        else:
            flash("请勾选返修备注")
    if comment_type == CommentType.REWORK.name:
        return redirect(url_for('ctr.show_rework_materials'))
    elif comment_type == CommentType.BUY.name:
        return redirect(url_for('ctr.show_buy_materials'))
    if comment_type == CommentType.DEVICE.name:
        return redirect(url_for('ctr.show_device_table'))
    elif comment_type == CommentType.CLIENT.name:
        return redirect(url_for('ctr.show_client_table'))
    elif comment_type == CommentType.CUSTOMERSERVICE.name:
        return redirect(url_for('ctr.show_customerservice_table'))
    else:
        flash("备注类型错误")

