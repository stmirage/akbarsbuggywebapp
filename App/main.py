from flask import Blueprint, render_template,redirect
from .models import Document, Setting, User
from . import db
from flask_login import login_required,current_user
from flask import g
import functools
main = Blueprint('main', __name__)




def active_required(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    # Do something with your request here
    if getSetting("active")=="False":
      return redirect("/shiba")
    return f(*args, **kwargs)
  return decorated_function


def superUserRequired(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    # Do something with your request here
    _superAdmin = current_user.isSuperAdmin
    if not _superAdmin:
      return redirect("/")
    return f(*args, **kwargs)
  return decorated_function

def getSetting(name):
    _setting = Setting.query.filter(Setting.name==name).first()
    return _setting.state

def set_setting(name,state):
    _setting = Setting.query.filter(Setting.name==name).first()
    _setting.state=state
    db.session.commit()

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
@active_required
def help_page():
    return render_template('help_page.html', name=current_user.name)


@main.route('/reset')
@login_required
@superUserRequired
def reset_page():
    
    
    return render_template('reset_page.html',data={"active_app":getSetting("active")})

@main.route('/reset_full')
@login_required
@superUserRequired
def reset_full():
	db.session.query(Document).delete()
	db.session.commit()
	return redirect("/reset")

@main.route('/activateapp')
@login_required
@superUserRequired
def activate_app():
    set_setting("active","True")
    return redirect("/reset")
    
@main.route('/deactivateapp')
@login_required
@superUserRequired
def deactivate_app():

    set_setting("active","False")
    return redirect("/reset")
    
    
@main.route('/shiba')
def deactivated_message():
    return render_template('deactivated_page.html')