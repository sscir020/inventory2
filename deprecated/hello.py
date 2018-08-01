# FileName:hello.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

    # @ctr.route("/text_color_change", methods=['GET', 'POST'])
    # @loggedin_required
    # def change_text_color():
    #     if request.method=="POST":
    #         alarm_level=convert_str_num(request.form['input_change_color'])
    #         if alarm_level>0:
    #             return redirect(url_for('ctr.show_materials',page=1,alarm_level=alarm_level))
    #         flash("警戒值应大于0")
    #     flash("提交错误")
    #     return redirect(url_for('ctr.show_materials',page= 1, alarm_level=0))


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

    # form1 = ColorForm()
    # if form1.validate_on_submit:
    #     alarm_level = form1.alarm_level.data
    #     if alarm_level==None or  alarm_level <0:
    #         alarm_level = 0
    #         flash("警戒值错误")
    # flash("提交错误")

    # params = {
    #     Param.PARAM_8.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name,
    #                          Sensorname.WINDSPEED.name,
    #                          Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name, Sensorname.PRESSURE.name],
    #     Param.PARAM_7.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name,
    #                          Sensorname.WINDSPEED.name,
    #                          Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name],
    #     Param.PARAM_5.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name,
    #                          Sensorname.WINDSPEED.name],
    #     Param.PARAM_3.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name]
    # }
    # paramnums = {
    #     Param.PARAM_8.name: [1, 1, 1, 1, 1, 1, 1, 1],
    #     Param.PARAM_7.name: [1, 1, 1, 1, 1, 1, 1],
    #     Param.PARAM_5.name: [1, 1, 1, 1, 1],
    #     Param.PARAM_3.name: [1, 1, 1]
    # }
    #
    # paramdict = {
    #     Param.PARAM_8.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name,
    #                          Sensorname.WINDSPEED.name,
    #                          Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name, Sensorname.PRESSURE.name],
    #     Param.PARAM_7.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name,
    #                          Sensorname.WINDSPEED.name,
    #                          Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name],
    #     Param.PARAM_5.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name,
    #                          Sensorname.WINDSPEED.name],
    #     Param.PARAM_3.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name]
    # }

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
#                 m=dbsession.query(Material).filter_by(materialid=materialid).first()
#                 comments_dict=json.loads(m.buy_comments)
#                 comments_dict[batch]=comment
#                 m.buy_comments = json.dump(comments_dict)
#                 dbsession.add(m)
#                 dbsession.commit()
#             else:
#                 flash("每条备注不超过20个中文字")
#         else:
#             flash("请勾选购买备注")
#     return redirect(url_for('ctr.show_buy_materials'))

# def change_outbound_num(m,materialid,diff,oprtype):
#     oprbatch=m.material_change_num(diff=diff,oprtype=oprtype,batch='')
#     o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=True,oprbatch=oprbatch, \
#             momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     dbsession.add(o)
#     dbsession.commit()
#
#     if m.acces_id!= None and m.acces_id!=0:
#         a=dbsession.query(Accessory).filter_by(acces_id=m.acces_id).first()
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
#         dbsession.add(o)
#         dbsession.commit()

        # if m.acces_id != None and m.acces_id != 0:
        #     a = dbsession.query(Accessory).filter_by(acces_id=m.acces_id).first()
        #     data = json.loads(a.param_acces)
        #     for materialid in data:
        #         # num = int(data[materialid])
        #         # num = num * m.countnum
        #         m1 = dbsession.query(Material).filter_by(material_id=materialid).first()
        #         # m1.material_change_num(diff=num,oprtype=Oprenum.INITADD.name,batch='')
        #         o = Opr(material_id=m1.material_id, diff=0, user_id=session['userid'], oprtype=Oprenum.INITADD.name,isgroup=False,oprbatch='',\
        #                 momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #         dbsession.add(o)
        #         dbsession.commit()

    # @ctr.route('/form_device_prepare_act', methods=['', 'POST'])
    # @loggedin_required
    # def form_device_prepare():
    #     device_id = 0
    #     if request.method == "POST":
    #         diff = 0
    #         for key in request.form:
    #             if "input_number_" in key and request.form[key] != '':
    #                 diff = convert_str_num(request.form[key])
    #                 if diff > 0:
    #                     device_id = key[20:]  # input_number_prepare_
    #                     break
    #         if diff > 0:
    #             d = dbsession.query(Device).filter(Device.device_id == device_id).first()
    #             if d != None:
    #                 if diff <= d.countnum:
    #                     d.countnum -= diff
    #                     d.preparenum += diff
    #                     dbsession.add(d)
    #                     dbsession.commit()
    #                 else:
    #                     flash("要备货数量大于库存数量")
    #             else:
    #                 flash("设备不存在")
    #         else:
    #             flash("请正确填写修好数量")
    #     return redirect(url_for('ctr.show_device_table'))

        # @ctr.route('/add_client1_post',methods=['GET','POST'])
        # def add_client1():
        #     if request.method=='POST':
        #         clientname=request.form['input_text_client_name']
        #         mn_id=request.form['input_number_MN']
        #         comment=request.form['input_text_comment']
        #         if dbsession.query(Client).filter_by(client_name=clientname).first() == None:
        #             c=Client(client_name=clientname,mn_id=int(mn_id),comment=comment)
        #             dbsession.add(c)
        #             dbsession.commit()
        #             flash("客户创建成功")
        #             return redirect(url_for('ctr.show_client_table'))
        #         else:
        #             flash("客户已存在")
        #     else:
        #         flash("需要填写")
        #     return render_template('add_client_form1.html')

    # @ctr.route('/form_chang_scrap_act', methods=['', 'POST'])
    # @loggedin_required
    # def form_change_scrap():
    #     if request.method=="POST":
    #         diff=0
    #         for key in request.form:
    #             if "input_restore_num_" in key and request.form[key]!='':
    #                 diff = convert_str_num(request.form[key])
    #                 if diff > 0:
    #                     string=key[18:]
    #                     # string = request.form["input_hidden_" + str(index)]
    #                     break
    #         if diff > 0:
    #             comment=request.form['input_comment_'+string]
    #             list = string.split('_')
    #             materialid = list[0]
    #             batch = list[1]
    #             change_materials_oprs_db(oprtype=Oprenum.SCRAP.name, materialid=materialid, diff=diff, isgroup=True, batch=batch, comment=comment)
    #         else:
    #             flash("请正确填写修好数量")
    #     return redirect(url_for('ctr.show_rework_materials'))

    #
    # @ctr.route('/form_change_device_outbound_act',methods=['','POST'])
    # @loggedin_required
    # def form_device_outbound():
    #     device_id=0
    #     if request.method=="POST":
    #         diff=0
    #         for key in request.form:
    #             if "input_number_" in key and request.form[key]!='':
    #                 diff = convert_str_num(request.form[key])
    #                 if diff > 0:
    #                     string=key[13:]#input_number_
    #                     break
    #         if diff > 0:
    #             comment=request.form['input_comment_'+string]
    #             list = string.split('_')
    #             device_id = list[0]
    #             MN_id = list[1]
    #             d=dbsession.query(Device).filter(Device.device_id==device_id).first()
    #             if d!= None:
    #                 if diff <= d.preparenum:
    #                     if d.acces_id != None and d.acces_id != 0:
    #                         a = dbsession.query(Accessory).filter_by(acces_id=d.acces_id).first()
    #                         if a!=None:
    #                             data = json.loads(a.param_acces)
    #                             for materialid in data:
    #                                 num = int(data[materialid])
    #                                 num = num * diff
    #                                 m=dbsession.query(Material).filter_by(material_id=materialid).first()
    #                                 if material_isvalid_num(m=m,diff=num, oprtype=Oprenum.DOUTBOUND, batch='') ==False:
    #                                     flash("配件数量不足")
    #                                     return redirect(url_for('ctr.show_device_table'))
    #                             for materialid in data:
    #                                 num = int(data[materialid])
    #                                 num = num * diff
    #                                 change_materials_oprs_db(oprtype=Oprenum.DOUTBOUND, materialid=materialid, diff=num, isgroup=False,batch='', comment='')
    #                             d.preparenum -= diff
    #                             d.salenum += diff
    #                             # d.preparenum += diff
    #                             o = Opr(device_id=device_id, diff=diff, user_id=session['userid'],oprtype=Oprenum.DOUTBOUND.name, isgroup=True, oprbatch='', comment=d.comment, \
    #                                     MN_id=d.MN_id,momentary=datetime.datetime.now())  # .strftime("%Y-%m-%d %H:%M:%S")
    #                             dbsession.add_all([d,o])
    #                             dbsession.commit()
    #                             dbsession.flush()
    #                             flash("设备出库更新成功")
    #                         else:
    #                             flash("设备参数不存在")
    #                     else:
    #                         flash("设备参数等于空或0")
    #                 else:
    #                     flash("出货数量大于备货数量")
    #             else:
    #                 flash("设备不存在")
    #         else:
    #             flash("请正确填写修好数量")
    #     return redirect(url_for('ctr.show_device_table'))

    #
    # @ctr.route('/form_cancel_buy_act', methods=['', 'POST'])
    # @loggedin_required
    # def form_cancel_buy():
    #     if request.method=="POST":
    #         # print(request.form)
    #         if "input_checkbox_cancel" in request.form:
    #             list=request.form["input_checkbox_cancel"].split('_')
    #             materialid=list[0]
    #             batch=list[1]
    #             b = dbsession.query(Buy).filter(Buy.batch==batch).first()
    #             diff=b.num
    #             o = Opr(material_id=materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CANCELBUY.name, isgroup=True,oprbatch=batch,comment=b.comment, \
    #                     momentary=datetime.datetime.now())#.strftime("%Y-%m-%d %H:%M:%S")
    #             dbsession.query(Buy).filter(Buy.batch==batch).delete()
    #             # dbsession.commit()
    #             dbsession.add(o)
    #             dbsession.commit()
    #             dbsession.flush()
    #             flash("订单取消成功")
    #         else:
    #             flash("请勾选订单并提交")
    #     return redirect(url_for('ctr.show_buy_materials'))
    # @ctr.route('/add_material_act', methods=['', 'POST'])
    # @loggedin_required
    # def add_material():
    #     if request.method == "POST":
    #         materialname=request.form['input_text_material_name']
    #         storenum=convert_str_num(request.form['input_number_countnum'])
    #         alarm_level=convert_str_num(request.form['input_number_alarm_level'])
    #         if materialname!=None and materialname!=''and alarm_level>0 :
    #         # if 'input_accessory_list' in request.form:
    #         #     list=request.form['input_accessory_list']
    #         # list1 = request.form
    #         # print(list1)
    #             if dbsession.query(Material).filter_by(material_name=materialname).first() == None:
    #                 m = Material(material_name=materialname, storenum=storenum, acces_id=0,alarm_level=alarm_level)
    #                 dbsession.add(m)
    #                 dbsession.commit()
    #                 dbsession.flush()
    #                 m=dbsession.query(Material).filter_by(material_name=materialname).first()
    #                 o=Opr(material_id=m.material_id,diff=storenum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch='', \
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

    # @ctr.route('/form_change_dresale_act', methods=['', 'POST'])
    # @loggedin_required
    # def form_change_dresale():
    #     if request.method=="POST":
    #         diff=0
    #         for key in request.form:
    #             if "input_number_" in key and request.form[key]!='':
    #                 diff = convert_str_num(request.form[key])
    #                 if diff > 0:
    #                     string=key[13:]
    #                     # string = request.form["input_hidden_" + str(index)]
    #                     break
    #         if diff > 0:
    #             comment=request.form['input_comment_'+string]
    #             list = string.split('_')
    #             device_id = list[0]
    #             MN_id = list[1]
    #             c=dbsession.query(Customerservice).filter(Customerservice.MN_id==MN_id).first()
    #             d=dbsession.query(Device).filter(Device.MN_id==MN_id).first()
    #             if c==None:
    #                 flash("售后不存在")
    #             elif d==None:
    #                 flash("设备不存在")
    #             else:
    #                 if diff>c.recyclenum:
    #                     flash("售后带出数量大于售后带回数量")
    #                 else:
    #                     c.recyclenum-=diff
    #                     d.resalenum+=diff
    #                     o = Opr(device_id=d.device_id, diff=diff, user_id=session['userid'], oprtype=Oprenum.DRESALE.name,
    #                             isgroup=True, oprbatch='', MN_id=MN_id,comment=c.comment, momentary=datetime.datetime.now())
    #                     if c.recyclenum==0:
    #                         dbsession.query(Customerservice).filter(Customerservice.MN_id==MN_id).delete()
    #                         dbsession.add_all([d,o])
    #                         dbsession.commit()
    #                         dbsession.flush()
    #                     else:
    #                         dbsession.add_all([c,d,o])
    #                         dbsession.commit()
    #                         dbsession.flush()
    #         else:
    #             flash("请正确填写修好数量")
    #     return redirect(url_for('ctr.show_device_table'))


    # @ctr.route('/form_change_crework_act', methods=['', 'POST'])
    # @loggedin_required
    # def form_change_crework():
    #     if request.method=="POST":
    #         diff=0
    #         for key in request.form:
    #             if "input_number_" in key and request.form[key]!='':
    #                 diff = convert_str_num(request.form[key])
    #                 if diff > 0:
    #                     string=key[13:]
    #                     # string = request.form["input_hidden_" + str(index)]
    #                     break
    #         if diff > 0:
    #             comment=request.form['input_comment_'+string]
    #             list = string.split('_')
    #             service_id = list[0]
    #             MN_id = list[1]
    #             c = dbsession.query(Customerservice).filter(Customerservice.MN_id == MN_id).first()
    #             batch=datetime.datetime.now()
    #             b = dbsession.query(Rework).filter(Rework.batch == batch).first()
    #             while b!=None:
    #                 c.sleep(1)
    #                 batch = datetime.datetime.now()
    #                 b = dbsession.query(Rework).filter(Rework.batch == batch).first()
    #             b=Rework(batch=batch,material_id=c.material_id,num=diff,MN_id=MN_id)
    #             c.recyclenum -= diff
    #             o = Opr(materialid=c.materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CSREWORK.name,
    #                     isgroup=True, oprbatch='', MN_id=MN_id, comment=c.comment, \
    #                     momentary=datetime.datetime.now())
    #
    #             dbsession.add_all([b,c,o])
    #             dbsession.commit()
    #             dbsession.flush()
    #         else:
    #             flash("请正确填写返修数量")
    #     return redirect(url_for('ctr.show_customerservice'))

    # @ctr.route('/form_change_cinbound_act', methods=['', 'POST'])
    # @loggedin_required
    # def form_change_cinbound():
    #     if request.method=="POST":
    #         diff=0
    #         for key in request.form:
    #             if "input_number_" in key and request.form[key]!='':
    #                 diff = convert_str_num(request.form[key])
    #                 if diff > 0:
    #                     string=key[13:]
    #                     # string = request.form["input_hidden_" + str(index)]
    #                     break
    #         if diff > 0:
    #             comment=request.form['input_comment_'+string]
    #             list = string.split('_')
    #             service_id = list[0]
    #             MN_id = list[1]
    #             c=dbsession.query(Customerservice).filter(Customerservice.MN_id==MN_id).first()
    #             m=dbsession.query(Material).filter(Material.material_id==c.materialid).first()
    #             if c==None:
    #                 flash("售后不存在")
    #             elif m==None:
    #                 flash("材料不存在")
    #             else:
    #                 if diff>c.recyclenum:
    #                     flash("入库数量大于售后带回数量")
    #                 else:
    #                     c.recyclenum-=diff
    #                     m.storenum+=diff
    #                     o = Opr(materialid=c.materialid, diff=diff, user_id=session['userid'], oprtype=Oprenum.CSINBOUND.name,
    #                             isgroup=True, oprbatch='', MN_id=MN_id,comment=c.comment, \
    #                             momentary=datetime.datetime.now())
    #                     if c.recyclenum==0:
    #                         dbsession.query(Customerservice).filter(Customerservice.MN_id==MN_id).delete()
    #                         dbsession.add_all([m,o])
    #                         dbsession.commit()
    #                         dbsession.flush()
    #                     else:
    #                         dbsession.add_all([c, m, o])
    #                         dbsession.commit()
    #                         dbsession.flush()
    #         else:
    #             flash("请正确填写修好数量")
    #     return redirect(url_for('ctr.show_customerservice'))

# def change_materials_oprs_db(oprtype,materialid,MN_id,diff,isgroup,batch,comment):#BUY,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
#     print('materialid:' + str(materialid) +'MN_id:' + str(MN_id) +  ",diff:" + str(diff) + ",oprtype:" + str(oprtype) + ",batch:" + str(batch))
#     m = dbsession.query(Material).filter(Material.material_id==materialid).first()
#     if m == None:
#         flash("材料名不存在")
#         return False
#     elif material_isvalid_num(m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id) == False:
#         flash("数量超标")
#         return False
#     else:
#         value=material_change_num(m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id)
#         o = Opr(material_id=materialid, MN_id=MN_id, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
#                 oprbatch=value,comment=comment, momentary=datetime.datetime.now())
#         dbsession.add_all([m,o])
#         dbsession.commit()
#         dbsession.flush()
#         # dbsession.close()
#     return True

# elif oprtype == Oprenum.CSRESTORE.name:
#     b = dbsession.query(Rework).filter(Rework.batch == batch).first()
#     c = dbsession.query(Customerservice).filter(Customerservice.material_id == m.material_id).filter(
#         Customerservice.MN_id == MN_id).first()
#     b.num -= diff
#     c.reworknum -= diff
#     c.restorenum += diff
#     if b.num == 0:
#         dbsession.query(Rework).filter(Rework.batch == batch).delete()
#     else:
#         dbsession.add_all([b, c])
# elif oprtype == Oprenum.CSSCRAP.name:
#     b = dbsession.query(Rework).filter(Rework.batch == batch).first()
#     c = dbsession.query(Customerservice).filter(Customerservice.material_id == m.material_id).filter(
#         Customerservice.MN_id == MN_id).first()
#     b.num -= diff
#     c.reworknum -= diff
#     c.scrapnum += diff
#     if b.num == 0:
#         dbsession.query(Rework).filter(Rework.batch == batch).delete()
#     else:
#         dbsession.add_all([b, c])
# elif oprtype == Oprenum.CSGINBOUND.name:
#     c = dbsession.query(Customerservice).filter(Customerservice.material_id == m.material_id).filter(
#         Customerservice.MN_id == MN_id).first()
#     c.goodnum -= diff
#     c.inboundnum += diff
#     m.storenum += diff
#     dbsession.add_all([c])
# elif oprtype == Oprenum.CSRINBOUND.name:
#     c = dbsession.query(Customerservice).filter(Customerservice.material_id == m.material_id).filter(
#         Customerservice.MN_id == MN_id).first()
#     c.restorenum -= diff
#     c.inboundnum += diff
#     m.storenum += diff
#     dbsession.add_all([c])
    #     # hiscs = Customerservice_his(MN_id=cs.MN_id,material_id=cs.material_id,device_id=cs.device_id,
    #     #                             originnum=cs.originnum,goodnum=cs.goodnum, brokennum=cs.brokennum,reworknum=cs.reworknum,
    #     #                             restorenum=cs.restorenum,scrapnum=cs.scrapnum,inboundnum=cs.inboundnum, resalenum=cs.resalenum,
    #     #                             comment=cs.comment)
#
# def customerservice_isvalid_num(cs,m,diff, oprtype, batch,MN_id):
#     if oprtype == Oprenum.CSRESTORE.name:
#         b = dbsession.query(Rework).filter(Rework.batch == batch).first()
#         if b == None:
#             flash("返修批次不存在" + str(batch))
#             return False
#         if diff > b.num:
#             flash("修好数量大于返修批次数量" + str(diff) + ">" + str(b.num))
#             return False
#     elif oprtype == Oprenum.CSSCRAP.name:
#         b = dbsession.query(Rework).filter(Rework.batch == batch).first()
#         if b == None:
#             flash("返修批次不存在" + str(batch))
#             return False
#         if diff > b.num:
#             flash("报废数量大于返修批次数量" + str(diff) + ">" + str(b.num))
#             return False
#     elif oprtype == Oprenum.CSGINBOUND.name:
#         if diff > cs.goodnum:
#             flash("入库数量大于售后完好数量" + str(diff) + ">" + str(cs.goodnum))
#             return False
#         if cs.inboundnum + diff > cs.goodnum + cs.restorenum:
#             flash("入库数量大于售后带回数量" + str(diff) + str(cs.inboundnum) + ">" + str(cs.goodnum) + str(cs.restorenum))
#             return False
#     elif oprtype == Oprenum.CSRINBOUND.name:
#         if diff > cs.restorenum:
#             flash("入库数量大于售后修好数量" + str(diff) + ">" + str(cs.goodnum))
#             return False
#         if cs.inboundnum + diff > cs.goodnum + cs.restorenum:
#             flash("入库数量大于售后带回数量" + str(diff) + str(cs.inboundnum) + ">" + str(cs.goodnum) + str(cs.restorenum))
#             return False
#     else:
#         flash("操作类型错误_判断"+str(oprtype))
#         # return False
#
# def customerservice_isvalid_num(cs,m,diff, oprtype, batch,MN_id):
#     if oprtype == Oprenum.CSRESTORE.name:
#         pass
#     elif oprtype == Oprenum.CSSCRAP.name:
#         pass
#     elif oprtype == Oprenum.CSGINBOUND.name:
#         pass
#     elif oprtype == Oprenum.CSRINBOUND.name:
#         pass
#     else:
#         pass
#
# def test(q):
#     if q=='a':
#         pass
#     elif q=='b':
#         pass
#     else:
#         pass
#     return True
#
# if c.inboundnum + diff > c.goodnum + c.restorenum:
#     flash("入库数量大于总完好数量")
# elif diff > c.goodnum:
#     flash("入库数量大于完好数量")
# else:
#     c.inboundnum += diff
#     flash("入库大于完好数量")
# elif oprtype == Oprenum.CSRINBOUND.name:
# if c.inboundnum + diff > c.goodnum + c.restorenum:
#     flash("入库数量大于总修好数量")
# elif diff > c.restorenum:
#     flash("入库数量大于修好数量")
# else:
#     c.inboundnum += diff
#     flash("入库数量大于修好"
#           "量")