from flask import render_template,url_for,redirect,flash,session
from ..models import Opr,Material,User
from .forms import EditOprForm,AddOprForm,LoginForm,RegistrationForm
from .__init__ import ctr

@ctr.route('/login')
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(user_name=form.username)
        if user is not None and user.verify_pass(user_pass=form.userpass):
            session.username=user.user_name
            session.userpass=user.user_pass
            return redirect(url_for('materials'))
        else:
            flash("invalid user")
    else:
        flash("invalid login")
    return render_template('login_form.html')

@ctr.route('/registration')
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(user_name=form.username).first() is None:
            User(user_name=form.username,user_pass=form.userpass)
            flash('account created')
            return redirect(url_for('login'))
        else:
            flash('account existed')
    else:
        flash('invalid registration')
    return render_template('registration_form.html')

@ctr.route('/_edit_opr/<material_id>', method=['', 'POST'])
# @login_required
def change_amout(material_id):
    form=EditOprForm()
    if form.validate_on_submit():
        current_material=Material.query.filer_by(material_id=material_id).first()
        current_material.change_countnum(form.diff)
        Opr(material_id=material_id, diff=form.diff, user_id=session.user_id)
        flash('Your material amount has been updated')
        return redirect(url_for('materials'))
    else:
        flash('Invalid amount')
    return render_template("_edit_opr.html", form=form)


@ctr.route('/_add_opr>', method=['', 'POST'])
# @login_required
def add_material():
    form=AddOprForm()
    if form.validate_on_submit():
        curren_material = Material(material_name=form.material_name, countnum=form.countnum)
        Opr(material_id=curren_material.material_id,diff=form.countnum,user_id=session.user_id)
        flash('Your material has been added')
        return redirect(url_for('materials'))
    else:
        flash('Invalid add')
    return render_template("_edit_opr.html", form=form)



# @auth.route('/change-password', methods=['GET', 'POST'])
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