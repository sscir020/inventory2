from flask import render_template,url_for,redirect,flash,session
from ..models import Opr,Material,User
from . import ctr
from ..__init__ import db



@ctr.route('/')
@ctr.route('/welcome1')
def welcome_user():
    # return "welcome_user"
    return render_template('welcome.html')


@ctr.route('/material_list')
def show_materials():
    return render_template('material_table.html',materials=Material.query.all())

@ctr.route('/logout')
def log_user_out():
    # logout_user()
    flash("You are logged out")
    return redirect(url_for('ctr.welcome_user'))

@ctr.route('/join_oprs_list')
# @login_required
def show_join_oprs():
    # if session['userid']!=None:
    sql1=db.session.query(Opr).join(User,User.user_id==Opr.user_id).all()
    print(sql1[0].opr_id)
    return render_template('join_oprs_table.html',join_oprs=sql1)
    # return url_for('ctr.log_user_in')
#
# @ctr.route('/logout')
# def log_user_out():
#     if session['userid']!=None:
#         session.pop('userid',None)
#         session.pop('username', None)
#         flash("You logged out")
#         return render_template('welcome.html')
