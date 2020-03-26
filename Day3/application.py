from flask import Flask, redirect, url_for, request,render_template
from sqlalchemy.orm import sessionmaker
from users import *
import os
from datetime import datetime

app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Session = sessionmaker(bind = engine)
session = Session()
 
@app.route("/")
def default():
   return redirect(url_for('register'))

@app.route('/success/<name>?<pwd>')
def success(name, pwd):
   print("name ", name)
   print("pwd", pwd)
   return 'welcome ' + name + " "+ pwd
 
@app.route('/register',methods = ['POST', 'GET'])
def register():
   if request.method == 'POST':
      user = request.form['email']
      pwd = request.form['psw']
      pwdcheck = request.form['psw-repeat']
      print(user,pwd,pwdcheck)
      # return render_template('/Register.html')
      if(pwd == pwdcheck): 
         usr = User(user_id = user, pwd = pwd, timestamp = datetime.now())
         session.add(usr)
         session.commit()
      return redirect(url_for('success',name = user, pwd = pwd))
   else:
      return render_template('/Register.html')
 

if __name__ == '__main__':
   app.run(debug = True)
