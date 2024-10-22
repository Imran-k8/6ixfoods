import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from sixfoods import db, app, bcrypt
from sixfoods.models import User
from sixfoods.forms import RegistrationForm, RegistrationCatererForm, LoginForm, UpdateAccountForm, SearchUserForm

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html", title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type='client')
		db.session.add(user)
		db.session.commit()
		flash(f"Your account has been created! You are now able to log in", "success")
		return redirect(url_for("login"))
	return render_template("register.html", title="Register", form=form)

@app.route("/register_caterer", methods=["GET", "POST"])
def register_caterer():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RegistrationCatererForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, location=form.location.data, user_type="caterer", phone=form.phone.data)
		db.session.add(user)
		db.session.commit()
		flash(f"Your account has been created! You are now able to log in", "success")
		return redirect(url_for("login"))
	return render_template("register_caterer.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get("next")
			flash(f"Successfully logged in!", "success")

			return redirect(next_page) if next_page else redirect(url_for("home"))
		else:
			flash("Login Unsuccessful! Please check email and password", "danger")
	return render_template("login.html", title="login", form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		print("hello")
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file 
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your account has been updated!", "success")
		return redirect(url_for("account"))
	elif request.method =='GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
	return render_template("account.html", title="account", image_file=image_file, form=form)



@app.route("/account_caterer", methods=['GET', 'POST'])
@login_required
def account_caterer():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.location = form.location.data
		current_user.phone = form.phone.data
		current_user.content = form.content.data
		db.session.commit()
		flash("Your account has been updated!", "success")
		return redirect(url_for("account_caterer"))
	elif request.method =='GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.location.data = current_user.location
		form.phone.data = current_user.phone
		form.content.data = current_user.content
	image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
	return render_template("account_caterer.html", title="account", image_file=image_file, form=form)


@app.route("/user/<string:username>", methods=['GET', 'POST'])
def user_profile(username):
	image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
	user = User.query.filter_by(username=username).first_or_404()
	return render_template("user_profile.html", user=user, image_file=image_file)


@app.route("/search", methods=['GET', 'POST'])
def search():
	form = SearchUserForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.search.data).first()
		if user is None:
			flash(f"No user with username {form.search.data} found!", "warning")
			return redirect(url_for('home'))
		elif user.user_type == "caterer":
			flash(f"User {user.username} found!", "success")
			return redirect(url_for('user_profile', username=user.username))
		else:
			flash(f"Not authorized to visit {user.username}'s profile!", "warning")
			return redirect(url_for('home'))
	return render_template("search_user.html", titel='Search', form=form)

@app.route("/search_location", methods=['GET', 'POST'])
def search_location():
	form = SearchUserForm()
	if form.validate_on_submit():
		users = User.query.filter_by(location=form.location.data).all()
		print(users)
		if users == []:
			flash(f"No current users in {form.location.data}", "warning")
			return redirect(url_for('home'))
		else:
			flash(f"Users in {form.location.data}:", "success")
			return render_template('user_list.html', users=users)
	return render_template("search_location.html", titel='Search', form=form)