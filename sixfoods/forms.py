from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from sixfoods.models import User


class RegistrationForm(FlaskForm):
	username = StringField("Username", 
							validators = [DataRequired(), Length(min=2, max=20)])
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	password = PasswordField("Password", 
							validators=[ DataRequired()])
	confirm_password = PasswordField("Confirm Password", 
							validators=[ DataRequired(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username Taken!")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("email Taken!")

class LoginForm(FlaskForm):
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	password = PasswordField("Password", 
							validators=[ DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
	username = StringField("Username", 
							validators = [DataRequired(), Length(min=2, max=20)])
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	location = SelectField("Location", choices=[('Ajax', 'Ajax'),('Aurora', 'Aurora'),('Brampton', 'Brampton'),('Brock', 'Brock'),('Burlington', 'Burlington'),('Caledon', 'Caledon'),('carlington', 'carlington'),('East Gwillimbury', 'East Gwillimbury'),('Georgina', 'Georgina'),('Halton Hills', 'Halton Hills'),('King', 'King'),('Markham', 'Markham'),('Milton', 'Milton'),('Mississauga', 'Mississauga'),('Newmarket', 'Newmarket'),('Oakville', 'Oakville'),('Oshawa', 'Oshawa'),('Pickering', 'Pickering'),('Richmond Hill', 'Richmond Hill'),('Scugog', 'Scugog'),('Toronto', 'Toronto'),('Uxbridge', 'Uxbridge'),('Vaughan', 'Vaughan'),('Whitby', 'Whitby')],
							validators = [Optional()])
	phone = StringField("Phone", 
							validators = [Optional()])

	picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg','png'])])
	content = TextAreaField("content", validators=[DataRequired()])
	submit = SubmitField("Update")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Username Taken!")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("email Taken!")


class SearchUserForm(FlaskForm):
	search = StringField('Search for a username (exact username)', validators=[Optional()])
	location = SelectField("Search for a location", choices=[('Ajax', 'Ajax'),('Aurora', 'Aurora'),('Brampton', 'Brampton'),('Brock', 'Brock'),('Burlington', 'Burlington'),('Caledon', 'Caledon'),('carlington', 'carlington'),('East Gwillimbury', 'East Gwillimbury'),('Georgina', 'Georgina'),('Halton Hills', 'Halton Hills'),('King', 'King'),('Markham', 'Markham'),('Milton', 'Milton'),('Mississauga', 'Mississauga'),('Newmarket', 'Newmarket'),('Oakville', 'Oakville'),('Oshawa', 'Oshawa'),('Pickering', 'Pickering'),('Richmond Hill', 'Richmond Hill'),('Scugog', 'Scugog'),('Toronto', 'Toronto'),('Uxbridge', 'Uxbridge'),('Vaughan', 'Vaughan'),('Whitby', 'Whitby')],
							validators = [Optional()])
	submit = SubmitField("Search")

class RegistrationCatererForm(FlaskForm):
	username = StringField("Name", 
							validators = [DataRequired(), Length(min=2, max=20)])
	location = SelectField("Location", choices=[('Ajax', 'Ajax'),('Aurora', 'Aurora'),('Brampton', 'Brampton'),('Brock', 'Brock'),('Burlington', 'Burlington'),('Caledon', 'Caledon'),('carlington', 'carlington'),('East Gwillimbury', 'East Gwillimbury'),('Georgina', 'Georgina'),('Halton Hills', 'Halton Hills'),('King', 'King'),('Markham', 'Markham'),('Milton', 'Milton'),('Mississauga', 'Mississauga'),('Newmarket', 'Newmarket'),('Oakville', 'Oakville'),('Oshawa', 'Oshawa'),('Pickering', 'Pickering'),('Richmond Hill', 'Richmond Hill'),('Scugog', 'Scugog'),('Toronto', 'Toronto'),('Uxbridge', 'Uxbridge'),('Vaughan', 'Vaughan'),('Whitby', 'Whitby')],
							validators = [DataRequired()])
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	phone = StringField("Phone", 
							validators = [DataRequired()])
	password = PasswordField("Password", 
							validators=[ DataRequired()])
	confirm_password = PasswordField("Confirm Password", 
							validators=[ DataRequired(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username Taken!")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("email Taken!")