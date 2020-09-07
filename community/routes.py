# Manikishore Medam, mm5224@drexel.edu
# CS 530: DUI , Final Project

from flask import Flask, render_template, url_for, flash, redirect,request,abort
from community import app,db
from community.models import User,Post,PostLike,Comment
from community.forms import RegistrationForm, LoginForm, UpdateAccountForm,Newpostform,Newcommentform
from flask_bcrypt import Bcrypt
from flask_login import login_user,current_user,logout_user,login_required
import os
from flask import g
import sqlite3


bcrypt = Bcrypt(app)

DATABASE = '/community/community.db'

# Function that handles save and updating of profile pictures
def save_picture(form_picture):
	picture_name = form_picture.filename
	picture_path = os.path.join(app.root_path, 'static/Profile_pics', picture_name)
	form_picture.save(picture_path)
	return picture_name

# Home page route
@app.route('/home')
@login_required
def Home(): 
	try:
		posts = Post.query.order_by(Post.date_posted.desc()) #quering posts
	except NameError: 
		posts = Post.query.order_by(Post.date_posted.desc())
	return render_template('home.html', posts=posts)

# About page Route
@app.route('/about')
def About():
	return render_template('about.html',title='About')

# Register page Route
@app.route("/register", methods =['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('Home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8') #hashing passwords before storing in db 
		user = User(username = form.username.data, email = form.email.data, password = encrypted_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created, Please try to log in','success')  
		return redirect(url_for('login'))
	return render_template('register.html',title='register', form = form)

# Login page Route
@app.route('/', methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('Home'))
	form = LoginForm()
	if form.validate_on_submit():   
		user = User.query.filter_by(email = form.email.data).first() 
		if (user is not None):
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user,remember= form.remember.data)
				flash('Welcome back!','success')
				return redirect(url_for('Home'))
			else:
				flash("Please check your Email and password",'danger')
				return redirect(request.referrer)
		else:
			flash("You have not signed up with us, please register","danger")
	return render_template('login.html',title='login', form = form)


# Route that handles logout
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

# Account page Route
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.profile_pic.data:
			picture_file = save_picture(form.profile_pic.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.bio = form.bio.data
		db.session.commit()
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.bio.data = current_user.bio
	image_file = url_for('static', filename='Profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account',
						   image_file=image_file, form=form)

# Route that handles new post creation page
@app.route("/newpost", methods=['GET', 'POST'])
@login_required
def new_post():
	form = Newpostform()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author =current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('Home'))
	return render_template('newpost.html', title='New Post',
						   form=form, legend = 'New Post')
	
# Route that handles view post page
@app.route("/post/<int:post_id>")
@login_required
def view_post(post_id):
	post = Post.query.get_or_404(post_id) 
	comments = Comment.query.filter_by(post_id =post_id).order_by(Comment.timestamp.desc())
	return render_template('view_post.html',title = post.title, post = post, comments = comments)

# Route that handles edit post functionality
@app.route("/post/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def editpost(id):
	form = Newpostform()
	post = db.session.query(Post).filter(Post.id==id).first()
	if post.author != current_user:
		abort(403)
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!!','success')
		return redirect(url_for('view_post',post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('newpost.html', post = post, title = post.title, legend = 'Edit Post', form = form)

# Route that handles delete post functionality
@app.route("/post/<int:id>/delete", methods=['POST'])
@login_required
def deletepost(id):
	post = db.session.query(Post).filter(Post.id==id).first()
	comments = Comment.query.filter_by(post_id =id)
	if post.author != current_user:
		abort(403)
	for comment in comments:
		db.session.delete(comment)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted','success')
	return redirect(url_for('Home'))

# Route that handles like and unlike functionality of posts 
@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
	post = Post.query.filter_by(id=post_id).first_or_404()
	if action == 'like':
		current_user.like_post(post)
		db.session.commit()
	if action == 'unlike':
		current_user.unlike_post(post)
		db.session.commit()
	return redirect(request.referrer)

#Route that handles newcomment functionality 
@app.route("/newcomment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
	form = Newcommentform() 
	post = Post.query.filter_by(id = post_id).first_or_404()
	if form.validate_on_submit():
		comment = Comment(body = form.body.data, post = post, author = current_user)
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for('view_post', post_id = post.id))
	return render_template('newcomment.html', title='New comment',
						   form=form, legend = 'New comment')









