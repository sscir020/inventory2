#coding:utf-8
from flask import render_template,url_for,redirect,flash,session,request,current_app
# from flask_login import login_user,logout_user,login_required,current_user
from ..models import Opr,Material,User,Accessory,Buy,Rework
from . import ctr
# from ..__init__ import db
from ..decorators import loggedin_required
from main_config import oprenumCH,Param,Oprenum,Sensorname
# from .forms import ColorForm
import json

from ..__init__ import dbsession

@ctr.route('/welcome',methods=['GET',''])
def welcome_user():
    # return "welcome_user"
    return render_template('welcome.html')

@ctr.route('/about',methods=['GET',''])
def about_app():
    return render_template('about.html')

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

@ctr.route('/user_table',methods=['GET',''])
@loggedin_required
def show_users():
    # flash('购买列表')
    # db.session.flush()
    # page = request.args.get('page',1,type=int)
    # pagination = Accessory.query.order_by(Accessory.acces_id).\
    #     paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    # accessories=pagination.items
    return render_template('user_table.html',users=dbsession.query(User).all() )
# @ctr.route('/materials_table_normal2')
# @loggedin_required
# def show_material_table_normal2():
#     # flash('库存列表')
#     # page=int(page)
#     # if page==None:
#     #     page=1
#     page = request.args.get('page',1,type=int)
#     pagination =dbsession.query(Material).order_by(Material.material_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
#     materials=pagination.items
#     return render_template('material_table_normal2.html',materials=materials,pagination=pagination,Param=Param,page=page,json=json )


@ctr.route('/materials_table',methods=['GET',''])
@loggedin_required
def show_material_table():
    print(request.url)
    # print(session)
    # flash('库存列表')
    # page=int(page)
    # if page==None:
    #     page=1
    # db.session.flush()
    # page = request.args.get('page',1,type=int)
    # pagination =dbsession.query(Material).order_by(Material.material_id.desc()).\
    #     paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    # materials=pagination.items
    # print(pagination==None)
    materials= dbsession.query(Material).order_by(Material.material_id.desc()).all()
    return render_template('material_table.html',materials=materials,Param=Param,json=json )
    # return render_template('material_table.html',materials=Material.query.all())

@ctr.route('/rework_materials_table',methods=['GET',''])
@loggedin_required
def show_rework_materials():
    print(request)
    # flash('返修列表')
    # db.session.flush()
    # page = request.args.get('page',1,type=int)
    # pagination = dbsession.query(Rework).order_by(Rework.batch.desc()).\
    #     paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE_LIST'],error_out=False)
    # reworkbatches=pagination.items
    reworkbatches = dbsession.query(Rework).order_by(Rework.batch.desc()).all()
    return render_template('rework_material_table.html',reworkbatches=reworkbatches,json=json,Oprenum=Oprenum )


@ctr.route('/buy_materials_table',methods=['GET',''])
@loggedin_required
def show_buy_materials():
    print(request)
    # flash('购买列表')
    # db.session.flush()
    # page = request.args.get('page',1,type=int)
    # pagination = dbsession.query(Buy).order_by(Buy.batch.desc()).\
    #     paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE_LIST'],error_out=False)
    # buybatches=pagination.items
    buybatches=dbsession.query(Buy).order_by(Buy.batch.desc()).all()
    return render_template('buy_material_table.html',buybatches=buybatches,json=json,Oprenum=Oprenum )

@ctr.route('/param_accessory_table',methods=['GET',''])
@loggedin_required
def show_param_accessory():
    # flash('购买列表')
    # db.session.flush()
    # page = request.args.get('page',1,type=int)
    # pagination = Accessory.query.order_by(Accessory.acces_id).\
    #     paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    # accessories=pagination.items
    accessories=dbsession.query(Accessory).order_by(Accessory.acces_id).all()
    return render_template('param_accessory_table.html',accessories=accessories,json=json,Material=Material,dbsession=dbsession )

@ctr.route('/join_oprs_table',methods=['GET',''])
@loggedin_required
def show_join_oprs():
    # flash('操作记录')
    # db.session.flush()
    # sql1=db.session.query(Opr.opr_id,Opr.diff,User.user_name).join(User,User.user_id==Opr.user_id).all()
    sql = dbsession.query(Opr.opr_id, Opr.diff, User.user_name,Material.material_name,Material.material_id,Opr.oprtype,\
                           Opr.isgroup,Opr.oprbatch,Opr.comment,Opr.momentary).join(User, User.user_id == Opr.user_id)\
        .join(Material,Material.material_id==Opr.material_id).order_by(Opr.opr_id.desc()).all()
    # print(sql)
    # page = request.args.get('page', 1, type=int)
    # pagination = sql.paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
    # join_oprs=pagination.items
    # print(sql[0])
    return render_template('join_oprs_table.html',join_oprs=sql,oprenumCH=oprenumCH)

@ctr.route('/join_oprs_main_table',methods=['GET',''])
@loggedin_required
def show_join_oprs_main():
    # flash('操作记录')
    # db.session.flush()
    # sql1=db.session.query(Opr.opr_id,Opr.diff,User.user_name).join(User,User.user_id==Opr.user_id).all()
    sql = dbsession.query(Opr.opr_id, Opr.diff, User.user_name,Material.material_name,Material.material_id,Opr.oprtype,\
                           Opr.isgroup,Opr.oprbatch,Opr.comment, Opr.momentary).join(User, User.user_id == Opr.user_id)\
        .join(Material,Material.material_id==Opr.material_id).filter(Opr.isgroup==True).order_by(Opr.opr_id.desc()).all()
    # print(sql)
    # page = request.args.get('page', 1, type=int)
    # pagination = sql.paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
    # join_oprs=pagination.items
    # print(sql[0])
    return render_template('join_oprs_main_table.html',join_oprs=sql,oprenumCH=oprenumCH)

def material_isvalid_num_rev (m,diff,oprtype,batch):
    if diff<0:
        flash("数量小于等于0")##
        return False
    if oprtype==Oprenum.INITADD.name:
        pass
        # if diff> self.countnum:
        #     flash("取消新添加数量大于库存数量")##
        #     return False
    # elif oprtype == Oprenum.OUTBOUND.name:
    #     if diff<=0:
    #         flash("取消出库数量小于等于0")##
    #         return False
    elif oprtype == Oprenum.BUYING.name:
        b = dbsession.query(Buy).filter(Buy.batch == batch).first()
        if b==None:
            flash("批次不存在")
            return False
        if diff!= b.num:
            flash("取消购买数量不等于购买批次数量")##
            return False
    elif oprtype == Oprenum.REWORK.name:
        b=dbsession.query(Rework).filter(Rework.batch == batch).fist()
        if b==None:
            flash("批次不存在")
            return False
        if diff!=b.num:
            flash("取消返修数量不等于返修批次数量")
            return False
    elif oprtype==Oprenum.INBOUND.name:
        if diff>m.countnum:# 5 2  -> 7 0
            flash("取消入库数量大于库存数量")
            return False
    elif oprtype == Oprenum.RESTORE.name:#返修
        if diff>m.countnum:
            flash("取消修好数量大于库存数量")
            return False
    # elif oprtype == Oprenum.SCRAP.name:
    #     if diff<=0:
    #         flash("报废数量小于等于0")
    #         return False
    else:
        if oprtype != Oprenum.OUTBOUND.name and oprtype != Oprenum.CANCELBUY.name and oprtype != Oprenum.SCRAP.name:
            flash("操作类型错误")
            return False
    return True


def material_change_num_rev(m,diff,oprtype,batch):
    value=0
    if oprtype==Oprenum.OUTBOUND.name:####
        m.countnum += diff
        dbsession.add_all([m])
    elif oprtype == Oprenum.INITADD.name:####
        pass
    #     self.countnum -= diff
    elif oprtype == Oprenum.BUYING.name:#++++
        dbsession.query(Buy).filter(Buy.batch == batch).delete()
    elif oprtype == Oprenum.REWORK.name:#++++
        m.countnum += diff
        dbsession.query(Rework).filter(Rework.batch == batch).delete()
        dbsession.add_all([m])
    elif oprtype==Oprenum.INBOUND.name:#----
        m.countnum -= diff
        b = dbsession.query(Buy).filter(Buy.batch == batch).first()
        if b==None:
            b=Buy(batch=batch,material_id=m.material_id,num=diff)
        else:
            b.num+=diff
        dbsession.add_all([m,b])
    elif oprtype == Oprenum.RESTORE.name:#----
        m.countnum -= diff
        b = dbsession.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            b = Buy(batch=batch, material_id=m.material_id, num=diff)
        else:
            b.num += diff
        dbsession.add_all([m,b])
    elif oprtype == Oprenum.CANCELBUY.name:#>>>>
        b = Buy(batch=batch, material_id=m.material_id, num=diff)
        dbsession.add_all([b])
    elif oprtype == Oprenum.SCRAP.name:#>>>>
        b = dbsession.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            b = Rework(batch=batch, material_id=m.material_id, num=diff)
        else:
            b.num += diff
        dbsession.add_all([b])
    else:
        flash("操作类型错误")
        value='-1'
    # if value!='-1':
    #     db.session.add(self)
    #     db.session.commit()
    return value
@ctr.route('/rollback')
def rollback_opr():
    opr = dbsession.query(Opr).order_by(Opr.opr_id.desc()).first()
    m =dbsession.query(Material).filter_by(material_id=opr.material_id).first()

    if opr.isgroup == True:
        if m != None:
            if opr.oprtype == Oprenum.INITADD.name:
                dbsession.query(Opr).filter_by(opr_id=opr.opr_id).delete()
                dbsession.query(Material).filter_by(material_id=opr.material_id).delete()
                dbsession.commit()
                flash("回滚成功_主件")
            else:
                if m.material_isvalid_num_rev(diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype):
                    m.material_change_num_rev(diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype)
                    dbsession.query(Opr).filter_by(opr_id=opr.opr_id).delete()
                    dbsession.commit()
                    flash("回滚成功_主件")
                else:
                    flash("回滚操作记录错误-数量超标_main")
                    return redirect(url_for('ctr.show_join_oprs_main'))
        else:
            flash("回滚操作记录错误-材料不存在_main")
            return redirect(url_for('ctr.show_join_oprs_main'))
        opr = dbsession.query(Opr).order_by(Opr.opr_id.desc()).first()

    while opr.isgroup == False:
        m =dbsession.query(Material).filter_by(material_id=opr.material_id).first()
        if m!=None:
            if material_isvalid_num_rev(m=m,diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype):
                material_change_num_rev(m=m,diff=opr.diff,batch=opr.oprbatch,oprtype=opr.oprtype)
                dbsession.query(Opr).filter_by(opr_id=opr.opr_id).delete()
                dbsession.commit()
                flash("回滚成功_配件")
            else:
                flash("回滚操作记录错误-数量超标_配件")
                return redirect(url_for('ctr.show_join_oprs_main'))
        else:
            flash("回滚操作记录错误-材料不存在_配件")
            return redirect(url_for('ctr.show_join_oprs_main'))
        opr = dbsession.query(Opr).order_by(Opr.opr_id.desc()).first()
    # dbsession.close()
    return redirect(url_for('ctr.show_join_oprs_main'))



@ctr.route('/_add_opr_get',methods=['GET',''])
@loggedin_required
def show_add_material():
    print(request)
    # db.session.flush()
    m=dbsession.query(Material).filter_by(acces_id=0).order_by(Material.material_id).all()
    return render_template("_add_opr_form.html",materials=m)

#
# @ctr.route('/rollback')
# def rollback_opr():
#     opr= dbsession.query(Opr).order_by(Opr.opr_id.desc()).first()
#     while opr.isgroup == False:
#         m =dbsession.query(Material).filter_by(material_id=opr.material_id).first()
#         if m!=None:
#             m.material_change_num_rev(diff=opr.diff,batch=opr.oprbatch,oprtype=opr.oprtype)
#             db.session.add(m)
#         else:
#             flash("操作记录错误")
#             return redirect(url_for('ctr.show_join_oprs_main'))
#         dbsession.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#         db.session.commit()
#         opr = dbsession.query(Opr).order_by(Opr.opr_id.desc()).first()
#     m =dbsession.query(Material).filter_by(material_id=opr.material_id).first()
#     if opr.oprtype == Oprenum.INITADD.name:
#         dbsession.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#        dbsession.query(Material).filter_by(material_id=opr.material_id).delete()
#     else:
#         if m != None:
#             m.material_change_num_rev(diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype)
#             dbsession.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#             db.session.add(m)
#         else:
#             flash("操作记录错误")
#             return redirect(url_for('ctr.show_join_oprs_main'))
#     db.session.commit()
#     flash("回滚成功")
#     return redirect(url_for('ctr.show_join_oprs_main'))