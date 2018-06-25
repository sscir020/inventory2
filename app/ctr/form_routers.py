from flask import render_template,url_for,redirect,flash,session
from .forms import EditOprForm,AddOprForm,LoginForm,RegistrationForm
from ..models import Opr,Material,User
from . import ctr
from app import db

@ctr.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(user_name=form.username.data).first()
        if user == None:
            flash("no such user ")
            return redirect(url_for('ctr.log_user_in'))
        elif not user.verify_pass(password=form.userpass.data):
            flash("incorrect password")
            return redirect(url_for('ctr.log_user_in'))
        else:
            session['userid'] = user.user_id
            session['username'] = user.user_name
            session['userpass'] = user.user_pass
            return redirect(url_for('ctr.show_materials'))
    else:
        flash("invalid login")
    return render_template('login_form.html',form=form)

@ctr.route('/registration', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(user_name=form.username.data).first() == None:
            User(user_name=form.username.data,user_pass=form.userpass.data)
            flash('account created')
            return redirect(url_for('ctr.login_user_in'))
        else:
            flash('account existed')
    else:
        flash('invalid registration')
    return render_template('registration_form.html',form=form)

@ctr.route('/_edit_opr/<materialid>', methods=['GET', 'POST'])
# @login_required
def change_countnum(materialid):
    form=EditOprForm()
    if form.validate_on_submit():
        # if session.userid != None:
        m=Material.query.filter_by(material_id=materialid).first()
        m.change_countnum(form.diff.data)
        o=Opr(material_id=materialid, diff=form.diff.data, user_id=session['userid'])
        db.session.add(o)
        db.session.commit()
        flash('Your material amount has been updated')
        return redirect(url_for('ctr.show_materials'))
        # else:
        #     return redirect(url_for('ctr.login_user_in'))
    else:
        flash('Invalid amount')
    return render_template("_edit_opr_form.html", form=form)


@ctr.route('/_add_opr', methods=['GET', 'POST'])
# @login_required
def add_material():
    form=AddOprForm()
    if form.validate_on_submit():
        # if session.userid != None:
        m = Material(material_name=form.materialname.data, countnum=form.countnum.data)
        db.session.add(m)
        db.session.commit()
        m = Material.query.filter_by(material_name=form.materialname.data).first()
        o=Opr(material_id=m.material_id,diff=form.countnum.data,user_id=session['userid'])
        db.session.add(o)
        db.session.commit()
        flash('Your material has been added')
        return redirect(url_for('ctr.show_materials'))
        # else:
        #     return redirect(url_for('ctr.login_user_in'))
    else:
        flash('Invalid add')
    return render_template("_edit_opr_form.html", form=form)



# @ctr.route('/change-password', methods=['GET', 'POST'])
# @login_required
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

