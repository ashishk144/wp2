from flask import Flask, redirect, url_for, request,render_template
from sqlalchemy.orm import sessionmaker
from users import *
import os
from datetime import datetime

app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Session = sessionmaker(bind = engine)
session = Session()
 
@app.route("/admin")
def admin():
   usrs =   session.query(User).all()
   # for i in usrs:
      # print(i)
   return render_template("/Admin.html", data = usrs)

@app.route("/")
def default():
   return redirect(url_for('register'))

@app.route('/success/<name>')
def success(name, pwd):
   # print("name ", name)
   # print("pwd", pwd)
   # d = {'name':name, 'pwd':pwd}
   return render_template("/Success.html", data = name)
 
@app.route('/register',methods = ['POST', 'GET'])
def register():
   if request.method == 'POST':
      user = request.form['email']
      pwd = request.form['psw']
      pwdcheck = request.form['psw-repeat']
      print(user,pwd,pwdcheck)
      # return render_template('/Register.html')
      data = session.query(User).filter_by(user_id=user).all()
      if(len(data) > 0):
      	return "User already exists"
      if(pwd == pwdcheck):
         try:
            usr = User(user_id = user, pwd = pwd, timestamp = datetime.now())
            session.add(usr)
            session.commit()
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
