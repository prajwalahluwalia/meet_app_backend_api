from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, widgets
from wtforms import validators
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.users import UserModel

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("First Name", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user_name = UserModel.find_by_username(username = username.data).first()
        if user_name:
            raise ValidationError("Username is already in use. Pick another one.")

    def validate_email(self, email):
        user_email = UserModel.find_by_email(email = email.data).first()
        if user_email:
            raise ValidationError("Email is already in use. Pick another one.")
        

class MeetigForm(FlaskForm):
    scheduled_on = DateField("Schedule On", validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    attendes = IntegerField("Attendes", validators=[DataRequired()])