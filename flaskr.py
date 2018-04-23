import os
import sqlite3
from flask import *
from flask_sqlalchemy import *
from datetime import datetime


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///confessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Users(db.Model):
	__tablename__='users'
	password = db.Column(db.String(255))
	email = db.Column(db.String(255),primary_key=True)
	name = db.Column(db.String(255))
	phone = db.Column(db.String(255))
	gender = db.Column(db.String(255))
	Birthday = db.Column(db.String(255))

db.create_all()


@app.route("/register",methods = ['GET','POST'])
def register():
	if request.method =='POST':
		password = request.form['password']
		password1= request.form['password1']
		email = request.form['email']
		name = request.form['name']
		gender = request.form['gender']
		Birthday = request.form['Birthday']
		phone = request.form['phone']
		if(password == password1):
			try:
				user = Users(password=password,email=email,name=name,gender=gender,Birthday=Birthday,phone=phone)
				db.session.add(user)
				db.session.commit()
				msg="registered successfully"
			except:
				db.session.rollback()
				msg="error occured"
		else:
			return render_template("layout.html",error1="password doesnot match")
	db.session.close()
	return render_template("layout.html",msg=msg)

@app.route("/loginForm")
def loginForm():
		return render_template('layout.html', error='')


@app.route('/')
def layout():	
	return render_template("layout.html")

@app.route("/registerationForm")
def registrationForm():
	return render_template("layout.html")


@app.route("/login", methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if is_valid(email, password):
			session['email'] = email
			session['logged_in'] = True
			global x
			x = email
			return redirect(url_for('index'))
		else:
			error = 'Invalid UserId / Password'
			return render_template('layout.html', error=error)
x=""		
@app.route('/index')
def index():
	if 'email' in session:
		email = session['email']
		return render_template('main.html',email=email)
	return "You are not logged in"

def is_valid(email,password):
	stmt = "SELECT email, password FROM users"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False

@app.route("/logout")
def logout():
		return render_template('layout.html', error='')

@app.route("/write")
def write():
	return render_template('post.html')

@app.route("/About")
def about():
	stmt = "SELECT * FROM users"
	data = db.engine.execute(stmt).fetchall()
	for confession1 in data:
		if(confession1.email==x):
			Name=confession1.name
			Email=confession1.email
			Birthday=confession1.Birthday
			gender=confession1.gender
			mobile=confession1.phone
			return render_template('about.html',Name=Name,Email=Email,Birthday=Birthday,gender=gender,mobile=mobile)

if __name__ =='__main__':
	
	app.run(port=5611)