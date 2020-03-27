from flask import Flask, redirect, url_for, request,render_template, session
from users import *
import os
from datetime import datetime
from sqlalchemy import desc
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))
 
@app.route("/admin")
def admin():
   usrs =   db.query(User).order_by(desc(User.timestamp)).all()
   return render_template("/Admin.html", data = usrs)

@app.route("/")
def default():
   return redirect(url_for('register'))

@app.route('/success/<name>')
def success(name):
   return render_template("/Success.html", data = name)
 
@app.route('/register',methods = ['POST', 'GET'])
def register():
   if request.method == 'POST':
      user = request.form['email']
      pwd = request.form['psw']
      pwdcheck = request.form['psw-repeat']
      print(user,pwd,pwdcheck)
      data = db.query(User).filter_by(user_id=user).all()
      if(len(data) > 0):
      	return "User already exists"
      if(pwd == pwdcheck):
         try:
            usr = User(user_id = user, pwd = pwd, timestamp = datetime.now())
            db.add(usr)
            db.commit()
            return redirect(url_for('success',name = user))
         except Exception(e):
            return redirect(url_for('error'))
      return redirect(url_for('error'))
   else:
      return render_template('/Register.html')
 
@app.route('/error')
def error():
   return render_template('/Fail.html')


if __name__ == '__main__':
   app.run(debug = True)
