from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

#import db
from app import db

#import models
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # check hashed password
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # reload if incorrect credentials

        login_user(user, remember=remember)
        
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # validate and add to database
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # cast username to lower (user names are case sensitive)
        username_lwr = username.lower()

        user = User.query.filter_by(email=email).first() # check if email exsists
        name = User.query.filter_by(username=username_lwr).first() # check if the username exsists

        if user or name: # if a user is found, we want to redirect back to signup page so user can try again
            if user:
                flash('"%s"' % (email), '1')

            if name:
                flash('"%s"' % (username), '2')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
