from datetime import datetime
from sixfoods import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	user_type = db.Column(db.String(20), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(120), nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	phone = db.Column(db.String(14), nullable=True)
	location = db.Column(db.String(200), nullable=True)
	content = db.Column(db.Text, nullable=True, default='Enter information you wish to share. (what you offer, prices, how they are made, etc.)')

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}','{self.user_type}')"