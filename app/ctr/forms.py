from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired,EqualTo

class EditOprForm(FlaskForm):
    diff=IntegerField("change +/- amount,eg. -10",  validators=[DataRequired()])
    submit=SubmitField('Submit')

class AddOprForm(FlaskForm):
    materialname=StringField("type material name",validators=[DataRequired()])
    countnum=IntegerField("type material amount",  validators=[DataRequired()])
    submit=SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username=StringField("type your eng_name",validators=[DataRequired()])
    userpass=StringField("type your password",validators=[DataRequired(),EqualTo('userpass2',message='password must be the same')])
    userpass2 = StringField("confirm your password", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('type your eng_name',validators=[DataRequired()])
    userpass = StringField('type your password', validators=[DataRequired()])
    submit = SubmitField('Submit')

