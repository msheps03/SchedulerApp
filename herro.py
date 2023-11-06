from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, DateTimeField
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
# old SQLite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'

# New MySQL db 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Shep:1max2well3@localhost/our_users'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Shep:1max2well3@localhost/conflicts'
# create a Form Class
app.config['SECRET_KEY'] = "Key"

#init database
db = SQLAlchemy(app)
app.app_context().push()

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name
    

# Create Model
class Conflicts(db.Model):
    conflictNumber = db.Column(db.Integer, primary_key = True)
    id = db.Column(db.Integer)
    dt = db.Column(db.DateTime)
    name = db.Column(db.String(100), nullable=False)
    conflictStart = db.Column(db.String(100), nullable=False)
    conflictEnd = db.Column(db.String(100), nullable=False) 
    frequency = db.Column(db.String(100), nullable=False)
    endDate = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name

    

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AvailabilityForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    date = DateField("Date of Conflict", validators=[DataRequired()], format='%Y-%m-%d')
    startTime1 = StringField("Start Time", validators=[DataRequired()])
    endTime1 = StringField("End Time", validators=[DataRequired()])
    frequency = SelectField("How Often", choices = ['Once', 'Daily', 'Daily--Weekdays', 'Daily--Weekends', 'Weekly'], validators=[DataRequired()])
    endDate = DateField("Last Day of Conflict (Optional)", format='%Y-%m-%d')
    submit = SubmitField("Submit")

# Update Database
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form = form, name_to_update = name_to_update)
        
        except:
            flash("Error! Looks like an issue, please try again")
            return render_template("update.html", form = form, name_to_update = name_to_update)

    else:
        return render_template("update.html", form = form, name_to_update = name_to_update)

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

@app.route('/availability', methods = ['GET', 'POST'])
def availability():
    # get info from logged in person
    # display that info on screen, begin with hardcoded variables
    # for side by side fillables: https://getbootstrap.com/docs/3.4/css/

    name = ''
    form = AvailabilityForm()
    
    if form.validate_on_submit():
        # no data for daily, just add a new conflict for each potential date
        '''
        if form.frequency.data == 'Daily':
            while not (form.endDate.data == tempDate):
                conflict = Conflicts(name=form.name.data, dt=form.date.data, conflictStart=form.startTime1.data,
                         conflictEnd=form.endTime1.data, frequency=form.frequency.data, endDate = form.endDate.data)
                tempDate.next() # everyday
                db.session.add(conflict)
        
        elif form.frequency.data == 'Weekly':
            while not (form.endDate.data == tempDate):
                conflict = Conflicts(name=form.name.data, dt=form.date.data, conflictStart=form.startTime1.data,
                         conflictEnd=form.endTime1.data, frequency=form.frequency.data, endDate = form.endDate.data)
                tempDate.next() # once a week on that day
                db.session.add(conflict)
            
        elif form.frequency.data == 'Daily--Weekdays':
            while not (form.endDate.data == tempDate):
                conflict = Conflicts(name=form.name.data, dt=form.date.data, conflictStart=form.startTime1.data,
                         conflictEnd=form.endTime1.data, frequency=form.frequency.data, endDate = form.endDate.data)
                tempDate.next() # once a week on that day
                db.session.add(conflict)
        
        elif form.frequency.data == 'Daily--Weekends':
            while not (form.endDate.data == tempDate):
                conflict = Conflicts(name=form.name.data, dt=form.date.data, conflictStart=form.startTime1.data,
                         conflictEnd=form.endTime1.data, frequency=form.frequency.data, endDate = form.endDate.data)
                tempDate.next() # once a week on that day
                db.session.add(conflict)
        
        else:
            conflict = Conflicts(name=form.name.data, dt=form.date.data, conflictStart=form.startTime1.data,
                    conflictEnd=form.endTime1.data, frequency=form.frequency.data, endDate = form.endDate.data)
            db.session.add(conflict)
            
        db.session.commit()
        '''
        conflict = Conflicts(name=form.name.data, dt=form.date.data, conflictStart=form.startTime1.data,
                         conflictEnd=form.endTime1.data, frequency=form.frequency.data, endDate = form.endDate.data)
        db.session.add(conflict)
        db.session.commit()
        
        form.startTime1.data = ''
        form.endTime1.data = ''
        form.date.data = ''
        form.endDate.data = ''
        form.frequency.data = ''
        
        flash("Conflict Added")

    current_Conflicts = Conflicts.query.order_by(Conflicts.conflictNumber)

    return render_template("availability.html", name = name, form = form, current_Conflicts = current_Conflicts)


# custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


