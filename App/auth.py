from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from .models import User
from . import db
from .main import active_required

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(login=login).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    _superAdmin = current_user.isSuperAdmin
    
    if _superAdmin:
        return redirect(url_for('main.reset_page'))
    else:
        return redirect(url_for('docPages.documents'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    login = request.form.get('login')
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    isAsker = 1 if request.form.get('isAsker') else 0
    isConfirmer =  1 if request.form.get('isConfirmer') else 0
    password = request.form.get('password')
    isSuperAdmin = 0


    user = User.query.filter_by(login=login).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Login already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(login=login, name=name, password=generate_password_hash(password, method='sha256'),lastname=lastname, \
                   isAsker=isAsker,isConfirmer=isConfirmer, isSuperAdmin=isSuperAdmin)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))