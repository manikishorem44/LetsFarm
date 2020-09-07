# Manikishore Medam, mm5224@drexel.edu
# CS 530: DUI , Final Project

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField	
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from community.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

# Class for handling registration form 
class RegistrationForm(FlaskForm):
	username = StringField('Username',validators = [DataRequired(), 
		                    Length(min=2, max=20)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('password', validators = [DataRequired(), Length(min=8)])
	confirm_password = PasswordField('confirm password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	#validating username with existing accounts
	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError('Username already exist!!')
	#validating email with existing accounts
	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError('Email already exist!!')

		                                                         
		                    
# Class for handling login form and validations
class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('password', validators = [DataRequired(), Length(min=8)])
	remember = BooleanField('remember me')
	submit = SubmitField('Login')
	#validating email during login with the existing accounts during login
	def validate_username(self, username):
		user = User.query.filter_by(email = email.data).first()
		if user is None:
			raise ValidationError('Username does not exist!!')


#class for handling updating account form and it's validations
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    profile_pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Update')
    
    #validating user name while account updation with existing usernames
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already exists. Please choose a different one.')
    #validating email with existing emails during account updation
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email already exists. Please choose a different one.')

#class for handling new post form and it's validations
class Newpostform(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('Content',validators=[DataRequired()])
	submit = SubmitField('Post')

#class for handling new comment form and it's validations
class Newcommentform(FlaskForm):
	body = TextAreaField('body', validators = [DataRequired()])
	submit = SubmitField('comment')



