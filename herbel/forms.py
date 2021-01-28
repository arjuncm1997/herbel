from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from herbel.models import  Login, Shippingdetails
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    add = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Login.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
            
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Shipform(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
   
    add = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')


class Shipdetailsform(FlaskForm):
    fromplace = StringField('From',
                           validators=[DataRequired(), Length(min=2, max=20)])
    to = StringField('To',
                        validators=[DataRequired()])
   
    date = DateField('Date',format='%m/%d/%Y',render_kw={"placeholder":"dd/mm/yyyy"})
    time = TimeField('Time - 24 hour format',render_kw={"placeholder":"hrs:mins"})
    desc = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')


class Productaddform(FlaskForm):
    product = StringField('Product Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    weight = StringField('Weight',
                        validators=[DataRequired()])

    name = StringField('Delivery Name',validators=[DataRequired()])
    address = StringField('Delivery Address',validators=[DataRequired()])
    
    submit = SubmitField('Submit')

class Delivery(FlaskForm):
    status = StringField('Delivery Status',validators=[DataRequired()])
    
    submit = SubmitField('Submit')

class Imageadd(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=40)])
    pic = FileField('Upload Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')

class Changepassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[ EqualTo('password')])
    submit = SubmitField('Reset Password')
