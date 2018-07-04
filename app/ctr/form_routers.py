from flask import render_template,url_for,redirect,flash,session,request
# from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,AddOprForm#ColorForm#ListForm,OprForm #EditOprForm,EditReworkOprForm #RegistrationForm
from ..models import Opr,Material,User,Accessory
from . import ctr
from ..__init__ import db
from ..decorators import loggedin_required
from main_config import Oprenum,Config,Param,params,paramnums,oprenumNum

import datetime
import json

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
        materialnum= int(request.form['input_material_num'])
        if materialname!=None and materialname!='' and materialnum!='' and int(materialnum)>0:
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
                    m=Material(material_name=materialname, countnum=materialnum,acces_id=a.acces_id)
                else:
                    m = Material(material_name=materialname, countnum=materialnum, acces_id=0)
                db.session.add(m)
                db.session.commit()
                m=Material.query.filter_by(material_name=materialname).first()
                o=Opr(material_id=m.material_id,diff=m.countnum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, ismain=True,\
                        momentary = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
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
                        m1.material_change_countnum(diff=num)
                        o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=Oprenum.INITADD.name,ismain=False, \
                                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        db.session.add(o)
                db.session.commit()
                flash('新材料添加成功')
                return redirect(url_for('ctr.show_materials',page=1,alarm_level=0))
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

def change_countnum(materialid,diff):
    m = Material.query.filter_by(material_id=materialid).first()
    if m==None:
        flash("材料名不存在")
    elif m.isvalid_opr(diff)==False:
        flash("数量超标")
    else:
        oprtype = Oprenum.INBOUND.name if diff > 0 else Oprenum.OUTBOUND.name
        m.material_change_buycountnum(diff)
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, ismain=True,\
                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(o)

        if m.acces_id!= None and m.acces_id!=0:
            a=Accessory.query.filter_by(acces_id=m.acces_id).first()
            data=json.loads(a.param_acces)
            for materialid in data:
                num=int(data[materialid])
                num=num*diff
                m1=Material.query.filter_by(material_id=materialid).first()
                if m1.isvalid_opr(num):
                    m1.material_change_buycountnum(diff=num)
                    o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=oprtype,ismain=False, \
                            momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    db.session.add(o)
                else:
                    flash("配件数量不足")
                    return False
        db.session.commit()
        return True
    return False

def change_reworknum(materialid,diff):
    m = Material.query.filter_by(material_id=materialid).first()
    if m==None:
        flash("材料名不存在")
    elif m.isvalid_rework_opr(diff)==False:
        flash("数量超标")
    else:
        m.material_change_reworknum(diff)
        oprtype = Oprenum.RESTORE.name if diff > 0 else Oprenum.REWORK.name
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, ismain=True,\
                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(o)

        if m.acces_id!= None and m.acces_id!=0:
            a=Accessory.query.filter_by(acces_id=m.acces_id).first()
            data=json.loads(a.param_acces)
            for materialid in data:
                num=int(data[materialid])
                num=num*diff
                m1=Material.query.filter_by(material_id=materialid).first()
                if m1.isvalid_rework_opr(num):
                    m1.material_change_reworknum(diff=num)
                    o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=oprtype, ismain=False,\
                            momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    db.session.add(o)
                else:
                    flash("配件数量不足")
                    return False
        db.session.commit()
        return True
    return False

def change_buynum(materialid,diff):
    m = Material.query.filter_by(material_id=materialid).first()
    if m==None:
        flash("材料名不存在")
    else:
        m.material_change_buynum(diff)
        oprtype = Oprenum.BUYING.name
        o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, ismain=True,\
                momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(o)

        if m.acces_id!= None and m.acces_id!=0:
            a=Accessory.query.filter_by(acces_id=m.acces_id).first()
            # print(a.param_acces)
            # data = json.dumps(a.param_acces)
            data=json.loads(a.param_acces)
            # print(data)
            # print(type(data))
            for materialid in data:
                num=int(data[materialid])
                # print(materialid,num)
                num=num*diff
                m1=Material.query.filter_by(material_id=materialid).first()
                m1.material_change_buynum(diff=num)
                o = Opr(material_id=m1.material_id, diff=num, user_id=session['userid'], oprtype=oprtype,ismain=False, \
                        momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                db.session.add(o)
        db.session.commit()
        return True
    return False

@ctr.route('/_change_num_opr/<page>/<alarm_level>', methods=['GET', 'POST'])
@loggedin_required
def form_change_num(page,alarm_level):
    diff=0
    materialid=0
    if request.method=="POST":
        for i in range(1,Config.FLASK_NUM_PER_PAGE+1):
            diff=convert_str_num(request.form["input_text_"+str(i)])
            if diff > 0:
                materialid=request.form["input_hidden_" + str(i)]
                break
        if diff > 0:
            bool=[False,False,False,False,False]
            # input_list={"入库":1,"出库":2,"修好":3,"返修":4,"购买":5}
            if(request.form["input_list_" + str(i)]!='') and request.form["input_list_" + str(i)] in oprenumNum.keys():
                # print(request.form["input_list_" + str(i)])
                # print (oprenumNum[request.form["input_list_" + str(i)]].value)
                bool[oprenumNum[request.form["input_list_" + str(i)]].value-2]=True
                # print( bool)
                if bool[1]==True or bool[3]==True:
                    diff=-diff;
                if bool[0]== True or bool[1] == True:
                    if change_countnum(materialid,diff):
                        flash('库存数量更新成功')
                elif bool[2]==True or bool[3]==True:
                    if change_reworknum(materialid,diff):
                        flash('返修数量更新成功')
                elif bool[4]==True:
                    if change_buynum(materialid,diff):
                        flash("购买数量更新成功")
                else:
                    flash("错误的操作类型")
            else:
                flash("需要选择操作类型")
        else:
            flash('需要填写一个正数')
    return redirect(url_for('ctr.show_materials',page=page,alarm_level=alarm_level))


@ctr.route("/text_color_change", methods=['GET', 'POST'])
@loggedin_required
def change_text_color():
    if request.method=="POST":
        alarm_level=convert_str_num(request.form['input_change_color'])
        if alarm_level>0:
            return redirect(url_for('ctr.show_materials',page=1,alarm_level=alarm_level))
        flash("警戒值应大于0")
    flash("提交错误")
    return redirect(url_for('ctr.show_materials',page= 1, alarm_level=0))

# @ctr.route('/forms_list', methods=['GET', ''])
# def list_forms():
#     form=ListForm()
#     if len(form.listopr)==0:
#         for i in range(0,Config.FLASK_NUM_PER_PAGE):
#             oneopr=OprForm()
#             oneopr.diff=0
#             form.listopr.append_entry(oneopr)
#         # for i in range(3, 5):
#         #     form.listopr[i].diff=i
#     return render_template("form_list.html",form=form)
#
# @ctr.route('/get_opr',methods=['', 'POST'])
# def get_opr():
#     form=ListForm()
#     # if form.validate_on_submit():
#     diff=form.listopr[0].diff.data
#     operation=form.listopr[0].operation.data
#     hide=form.listopr[0].hide.data
#     print("********************")
#     print(diff)
#     print(operation)
#     print(hide)
#     return redirect(url_for("ctr.list_forms"))
# @ctr.route('/_change_num_opr', methods=['GET', 'POST'])
# @loggedin_required
# def form_change_num():
#     materialid=0
#     if request.method=="POST":
#         for i in range(1,Config.FLASK_NUM_PER_PAGE+1):
#             diff=convert_str_num(request.form["input_text_"+str(i)])
#             if diff > 0:
#                 materialid=request.form["input_hidden_" + str(i)]
#                 break
#         if diff > 0:
#             # print(request.form["radio"])
#             bool=[False,False,False,False]
#             # print("radio" in request.form)
#             if("radio" in request.form):
#                 bool[int(request.form["radio"])]=True
#                 # print( bool)
#                 if bool[1]==True or bool[3]==True:
#                     diff=-diff;
#                 if bool[0]== True or bool[1] == True:
#                     if change_countnum(materialid,diff):
#                         flash('库存数量更新成功')
#                 elif bool[2]==True or bool[3]==True:
#                     if change_reworknum(materialid,diff):
#                         flash('返修数量更新成功')
#                 else:
#                     flash("需要选择操作类型")
#             else:
#                 flash("需要选择操作类型")
#         else:
#             flash('需要填写一个正数')
#     return redirect(url_for('ctr.show_materials'))

# if "input_inbound" in request.form:
#     bool[0]= request.form["input_inbound"]
# if "input_outbound" in request.form:
#     bool[1]= request.form["input_outbound"]
# if "input_rework" in request.form:
#     bool[2]= request.form["input_rework"]
# if "input_restore" in request.form:
#     bool[3]= request.form["input_restore"]

# @ctr.route('/_edit_opr/<materialid>', methods=['GET', 'POST'])
# @loggedin_required
# def form_change_countnum(materialid):
#     if request.method=="POST":
#         diff1=convert_str_num(request.form["input_inbound"])
#         diff2=convert_str_num(request.form["input_outbound"])
#         if diff1<0 or diff2>0:
#             flash("入库为正数，出库为负数")
#         else:
#             diff=diff1+diff2
#             if diff!=0:
#                 if change_countnum(materialid,diff):
#                     flash('材料数量更新成功')
#                 else:
#                     flash("减少的数量超标")
#             else:
#                 flash('需要填写数量')
#     return redirect(url_for('ctr.show_materials'))
#
# @ctr.route('/_edit_rework_opr/<materialid>', methods=['GET', 'POST'])
# @loggedin_required
# def form_change_reworknum(materialid):
#     if request.method=="POST":
#         diff1=convert_str_num(request.form["input_rework"])
#         diff2=convert_str_num(request.form["input_restore"])
#         if diff1<0 or diff2>0:
#             flash("修好为正数，返修为负数")
#         else:
#             diff=diff1+diff2
#             if diff!=0:
#                 if change_reworknum(materialid,diff):
#                     flash('返修数量更新成功')
#                 else:
#                     flash("减少或增加的数量超标")
#             else:
#                  flash('需要填写数量')
#     return redirect(url_for('ctr.show_materials'))
#
# @ctr.route('/_edit_opr/<materialid>', methods=['GET', 'POST'])
# @loggedin_required
# def change_countnum(materialid):
#     form = EditOprForm()
#     if form.validate_on_submit():
#         m = Material.query.filter_by(material_id=materialid).first()
#         if m.isvalid_opr(form.diff.data):
#             oprtype = oprenum[Oprenum.INBOUND] if form.diff.data > 0 else oprenum[Oprenum.OUTBOUND]
#             o = Opr(material_id=materialid, diff=form.diff.data, user_id=session['userid'], oprtype=oprtype, \
#                     momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             db.session.add(o)
#             db.session.commit()
#             m.material_change_countnum(form.diff.data)
#             flash('材料数量更新成功')
#
#         else:
#             flash("减少的数量超标")
#     else:
#         flash('需要填写数量')
#     return render_template("_edit_opr_form.html", form=form)
#
#
# @ctr.route('/_edit_rework_opr/<materialid>', methods=['GET', 'POST'])
# @loggedin_required
# def change_reworknum(materialid):
#     form = EditReworkOprForm()
#     if form.validate_on_submit():
#         m = Material.query.filter_by(material_id=materialid).first()
#         if m.isvalid_rework_opr(form.diff.data):
#             oprtype = oprenum[Oprenum.RESTORE] if form.diff.data > 0 else oprenum[Oprenum.REWORK]
#             o = Opr(material_id=materialid, diff=form.diff.data, user_id=session['userid'], oprtype=oprtype, \
#                     momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             db.session.add(o)
#             db.session.commit()
#             m.material_change_reworknum(form.diff.data)
#             flash('返修数量更新成功')
#             return redirect(url_for('ctr.show_materials'))
#         else:
#             flash("减少或增加的数量超标")
#     else:
#         flash('需要填写数量')
#     return render_template("_edit_opr_form.html", form=form)

# @ctr.route('/registration', methods=['GET', 'POST'])
# def register():
#     form=RegistrationForm()
#     if form.validate_on_submit():
#         if User.query.filter_by(user_name=form.username.data).first() == None:
#             u=User(user_name=form.username.data,user_pass=form.userpass.data)
#             db.session.add(u)
#             db.session.commit()
#             flash('账户创建成功')
#             return redirect(url_for('ctr.log_user_in'))
#         else:
#             flash('账户已存在')
#     else:
#         flash('需要注册')
#     return render_template('registration_form.html',form=form)

# @ctr.route('/change_password', methods=['GET', 'POST'])
# @loggedin_required
# def change_password():
#     form = ChangePasswordForm()
#     if form.validate_on_submit():
#         if current_user.verify_password(form.old_password.data):
#             current_user.password = form.password.data
#             db.session.add(current_user)
#             db.session.commit()
#             flash('Your password has been updated.')
#             return redirect(url_for('main.index'))
#         else:
#             flash('Invalid password.')
#     return render_template("auth/change_password.html", form=form)

