from flask import render_template,url_for,redirect,flash,session,request,current_app
# from flask_login import login_user,logout_user,login_required,current_user
from ..models import Opr,Material,User,Accessory
from . import ctr
from ..__init__ import db
from ..decorators import loggedin_required
from main_config import oprenumCH,Param,Oprenum,Sensorname
# from .forms import ColorForm
import json

@ctr.route('/')
@ctr.route('/welcome')
def welcome_user():
    # return "welcome_user"
    return render_template('welcome.html')


@ctr.route('/logout')
@loggedin_required
def log_user_out():
    # logout_user()
    # print(session)
    session.pop('userid',None)
    session.pop('username', None)
    session.pop('userpass', None)
    flash("登出成功")
    return redirect(url_for('ctr.welcome_user'))


@ctr.route('/materials_table/<page>/<alarm_level>')
@loggedin_required
def show_materials(page,alarm_level):
    # print(session)
    # flash('库存列表')
    page=int(page)
    if page==None:
        page=1
    if alarm_level==None:
        alarm_level=-1
    page = request.args.get('page',page,type=int)
    pagination = Material.query.order_by(Material.material_id.desc()).\
        paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    materials=pagination.items

    # form1 = ColorForm()
    # if form1.validate_on_submit:
    #     alarm_level = form1.alarm_level.data
    #     if alarm_level==None or  alarm_level <0:
    #         alarm_level = 0
    #         flash("警戒值错误")
    # flash("提交错误")

    # print(pagination==None)
    return render_template('material_table.html',materials=materials,pagination=pagination,Param=Param,page=page,alarm_level=alarm_level )
    # return render_template('material_table.html',materials=Material.query.all())

@ctr.route('/rework_materials_table')
@loggedin_required
def show_rework_materials():
    # flash('返修列表')
    page = request.args.get('page',1,type=int)
    pagination = Material.query.filter(Material.reworknum>0).order_by(Material.material_id.desc()).\
        paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    materials=pagination.items
    return render_template('rework_material_table.html',materials=materials,pagination=pagination )


@ctr.route('/buy_materials_table')
@loggedin_required
def show_buy_materials():
    # flash('购买列表')
    page = request.args.get('page',1,type=int)
    pagination = Material.query.filter(Material.buynum>0).order_by(Material.material_id.desc()).\
        paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    materials=pagination.items
    return render_template('buy_material_table.html',materials=materials,pagination=pagination )

@ctr.route('/param_accessory_table')
@loggedin_required
def show_param_accessory():
    # flash('购买列表')
    page = request.args.get('page',1,type=int)
    pagination = Accessory.query.order_by(Accessory.acces_id).\
        paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    accessories=pagination.items
    return render_template('param_accessory_table.html',accessories=accessories,pagination=pagination,json=json,Sensorname=Sensorname )

@ctr.route('/join_oprs_table')
@loggedin_required
def show_join_oprs():
    # flash('操作记录')
    # sql1=db.session.query(Opr.opr_id,Opr.diff,User.user_name).join(User,User.user_id==Opr.user_id).all()
    sql = db.session.query(Opr.opr_id, Opr.diff, User.user_name,Material.material_name,Material.material_id,Opr.oprtype,Opr.ismain,Opr.momentary).join(User, User.user_id == Opr.user_id)\
        .join(Material,Material.material_id==Opr.material_id).order_by(Opr.opr_id.desc())
    page = request.args.get('page', 1, type=int)
    pagination = sql.paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
    join_oprs=pagination.items
    # print(sql[0])
    return render_template('join_oprs_table.html',join_oprs=join_oprs,pagination=pagination,oprenumCH=oprenumCH)

@ctr.route('/join_oprs_main_table')
@loggedin_required
def show_join_oprs_main():
    # flash('操作记录')
    # sql1=db.session.query(Opr.opr_id,Opr.diff,User.user_name).join(User,User.user_id==Opr.user_id).all()
    sql = db.session.query(Opr.opr_id, Opr.diff, User.user_name,Material.material_name,Material.material_id,Opr.oprtype,Opr.ismain,Opr.momentary).join(User, User.user_id == Opr.user_id)\
        .join(Material,Material.material_id==Opr.material_id).filter(Opr.ismain==True).order_by(Opr.opr_id.desc())
    page = request.args.get('page', 1, type=int)
    pagination = sql.paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
    join_oprs=pagination.items
    # print(sql[0])
    return render_template('join_oprs_main_table.html',join_oprs=join_oprs,pagination=pagination,oprenumCH=oprenumCH)

@ctr.route('/rollback')
@loggedin_required
def rollback_opr():
    opr= Opr.query.order_by(Opr.opr_id.desc()).first()
    while opr.ismain == False:
        m = Material.query.filter_by(material_id=opr.material_id).first()
        if opr.oprtype==Oprenum.INBOUND.name or opr.oprtype==Oprenum.OUTBOUND.name:
            m.material_change_buycountnum_rev(-opr.diff)
            db.session.add(m)
        elif  opr.oprtype==Oprenum.REWORK.name or opr.oprtype==Oprenum.RESTORE.name:
            m.material_change_reworknum(-opr.diff)
            db.session.add(m)
        elif opr.oprtype==Oprenum.BUYING.name:
            m.material_change_buynum(-opr.diff)
            db.session.add(m)
        elif opr.oprtype==Oprenum.INITADD.name:
            m.material_change_countnum(-opr.diff)
            db.session.add(m)
        else:
            flash("操作类型错误")
            return redirect(url_for('ctr.show_join_oprs'))
        Opr.query.filter_by(opr_id=opr.opr_id).delete()
        db.session.commit()
        opr = Opr.query.order_by(Opr.opr_id.desc()).first()
    m = Material.query.filter_by(material_id=opr.material_id).first()
    if opr.oprtype == Oprenum.INBOUND.name or opr.oprtype == Oprenum.OUTBOUND.name:
        m.material_change_buycountnum_rev(-opr.diff)
        db.session.add(m)
    elif opr.oprtype == Oprenum.REWORK.name or opr.oprtype == Oprenum.RESTORE.name:
        m.material_change_reworknum(-opr.diff)
        db.session.add(m)
    elif opr.oprtype == Oprenum.BUYING.name:
        m.material_change_buynum(-opr.diff)
        db.session.add(m)
    elif opr.oprtype == Oprenum.INITADD.name:
        Opr.query.filter_by(opr_id=opr.opr_id).delete()
        Material.query.filter_by(material_id=opr.material_id).delete()
        db.session.commit()
        flash("回滚成功")
        return redirect(url_for('ctr.show_join_oprs_main'))
    else:
        flash("操作类型错误")
        return redirect(url_for('ctr.show_join_oprs_main'))
    Opr.query.filter_by(opr_id=opr.opr_id).delete()
    db.session.commit()
    flash("回滚成功")
    return redirect(url_for('ctr.show_join_oprs_main'))



@ctr.route('/_add_opr_get')
@loggedin_required
def show_add_material():
    m=Material.query.filter_by(acces_id=0).order_by(Material.material_id).all()
    return render_template("_add_opr_form.html",materials=m)


