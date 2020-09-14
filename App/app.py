




'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


class NameForm(FlaskForm):
 name = StringField('What is your name?')
 submit = SubmitField('Submit')

db.init_app(app)

@app.route('/')
def index():
 form = NameForm(csrf_enabled=False)
 user_agent = request.headers.get('User-Agent')
 return render_template('index.html',user_agent=user_agent, form=form)

@app.route('/bad')
def bad_500():
 return '<p>Internal server error....</p>',500

@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404


#@app.route('/user/<name>') def user(name):    return '<h1>Hello, {}!</h1>'.format(name)

'''    

