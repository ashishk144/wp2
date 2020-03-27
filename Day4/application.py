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


engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))
 
@app.route("/admin")
def admin():
    usrs =   db.query(User).order_by(desc(User.timestamp)).all()
    return render_template("/Admin.html", data = usrs)

@app.route("/")
def default():
    if(session.get("user_id") != None and session.get("password") != None):
        return render_template('User.html', user = session.get("user_id"))
    return redirect(url_for('register'))

@app.route('/success/<name>')
def success(name):
    return render_template("/Success.html", data = name)
 
@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['email']
        pwd = request.form['psw']
        data = db.query(User).filter_by(user_id=user).all()
        if(len(data) > 0):
            return "User already exists"
        if("@" in user and "." in user):
            try:
                usr = User(user_id = user, pwd = pwd, timestamp = datetime.now())
                db.add(usr)
                db.commit()
                return redirect(url_for('success',name = user))
            except Exception(e):
                return redirect(url_for('error'))
        return render_template('/Register.html', message = "Email invalid")
    else:
        return render_template('/Register.html')

@app.route('/error')
def error():
    return render_template('/Fail.html')

@app.route('/auth', methods = ['POST'])
def auth():
    user = request.form['email']
    pwd = request.form['psw']
    if("@" not in user or "." not in user):
        return render_template('/Register.html', message = "Email invalid")
    data = db.query(User).filter_by(user_id=user).all()
    if(len(data) <= 0):
        return render_template('/Register.html', message = "User does not exist")
    if(data[0].pwd == pwd):
        session['user_id'] = user
        session['password'] = pwd
        return render_template("/User.html", user = user)
    return render_template('/Register.html', message = "Invalid credentials")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("password", None)
    return "Logged out"

if __name__ == '__main__':
    app.run(debug = True)
