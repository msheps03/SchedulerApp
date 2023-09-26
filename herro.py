from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


"""
JINJA Shortys
safe
capitalize
lower
upper
title
trim
striptags
"""


# Create a Flask Instance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
# create a Form Class
app.config['SECRET_KEY'] = "Key"

#init database
db = SQLAlchemy(app)
app.app_context().push()
#db.init_app(app)
# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name
    

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/useradd', methods=['POST', 'GET'])
def addUser():
    name= None
    form = UserForm()
    
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        
        flash("User Added")
    
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", name = name, form = form, our_users=our_users)
# Create a route decorator
@app.route('/')

def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)


@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Name Submitted Successfully")
    
    return render_template("name.html", name = name, form = form)

# custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


