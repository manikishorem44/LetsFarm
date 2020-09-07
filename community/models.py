# Manikishore Medam, mm5224@drexel.edu
# CS 530: DUI , Final Project

from community import db,login
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

#function to load user during login
@login.user_loader
def load_user(usr_id):
	return User.query.get(int(usr_id))

#class for creating User table
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
	password = db.Column(db.String(60), nullable = False, unique= False)
	bio = db.Column(db.String(200), nullable = True)
	posts = db.relationship('Post', backref = 'author', lazy = True)
	liked = db.relationship('PostLike', foreign_keys = 'PostLike.user_id', backref='user',lazy = 'dynamic')
	comments = db.relationship('Comment', backref= 'author', lazy = 'dynamic')

	#function that handles like post functionality
	def like_post(self, post):
		if not self.has_liked_post(post):
			like = PostLike(user_id = self.id, post_id = post.id)
			db.session.add(like)
	#function that handles unlike post functionality
	def unlike_post(self,post):
		if self.has_liked_post(post):
			PostLike.query.filter_by(user_id = self.id, post_id = post.id).delete()

	#function that checks whether user liked post
	def has_liked_post(self,post):
		return PostLike.query.filter(PostLike.user_id ==self.id, PostLike.post_id == post.id).count() > 0

#class for creating Post table
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(150), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	likes = db.relationship('PostLike', backref = 'post', lazy = 'dynamic')
	comments = db.relationship('Comment', backref= 'post', lazy = 'dynamic')

#Class for creating PostLike table
class PostLike(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

#Class for creating comment table
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	post_id = db.Column(db.Integer,db.ForeignKey('post.id'), nullable = False)








