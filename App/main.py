from flask import Blueprint, render_template,redirect
from .models import Document
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

@main.route('/reset')
def reset_page():
    return render_template('reset_page.html')

@main.route('/reset_full')
def reset_full():
	db.session.query(Document).delete()
	db.session.commit()
	return redirect("/")
