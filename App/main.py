from flask import Blueprint, render_template
from . import db
from flask_login import login_required,current_user
main = Blueprint('main', __name__)

@main.route('/')
def index():
    #return render_template('index.html')
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/bad')
def bad_request():
    return "Internal Server Error",500

@main.route('/help')
def help_page():
    return render_template('help_page.html', name=current_user.name)
