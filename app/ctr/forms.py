from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField
from wtforms.validators import Required,EqualTo

class EditOprForm(FlaskForm):
    diff=IntegerField("change +/- amount,eg. -10",  validators=[Required])
    submit=SubmitField('Submit')

class AddOprForm(FlaskForm):
    material_name=StringField("type aterial name",validators=[Required])
    countnum=IntegerField("type material amount",  validators=[Required])
    diff=countnum
    submit=SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username=StringField("type user name",validators=[Required])
    userpass=StringField("type user password",validators=[Required,EqualTo('userpass2',message='password must be the same')])
    userpass2 = StringField("confirm user password", validators=[Required])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username=StringField("type user name",validators=[Required])
    userpass = StringField("type user password", validators=[Required])
    submit = SubmitField('Submit')