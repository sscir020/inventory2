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