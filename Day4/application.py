import os
from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, session
from sqlalchemy import desc, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
from users import *

APP = Flask(__name__)
APP.config["SESSION_PERMANENT"] = False
APP.config["SESSION_TYPE"] = "filesystem"
Session(APP)


ENGINE = create_engine(os.getenv("DATABASE_URL"), echo=True)
DB = scoped_session(sessionmaker(bind=ENGINE))

@APP.route("/admin")
def admin():
    usrs = DB.query(User).order_by(desc(User.timestamp)).all()
    return render_template("/Admin.html", data=usrs)

@APP.route("/")
def default():
    if(session.get("user_id") is not None and session.get("password") is not None):
        return render_template('User.html', user=session.get("user_id"))
    return redirect(url_for('register'))

@APP.route('/success/<name>')
def success(name):
    return render_template("/Success.html", data=name)

@APP.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['email']
        pwd = request.form['psw']
        data = DB.query(User).filter_by(user_id=user).all()
        if len(data) > 0:
            return "User already exists"
        if("@" in user and "." in user):
            try:
                usr = User(user_id=user, pwd=pwd, timestamp=datetime.now())
                DB.add(usr)
                DB.commit()
                return redirect(url_for('success', name=user))
            except Exception(E):
                return redirect(url_for('error'))
        return render_template('/Register.html', message="Email invalid")
    return render_template('/Register.html')

@APP.route('/error')
def error():
    return render_template('/Fail.html')

@APP.route('/auth', methods=['POST'])
def auth():
    user = request.form['email']
    pwd = request.form['psw']
    if("@" not in user or "." not in user):
        return render_template('/Register.html', message="Email invalid")
    data = DB.query(User).filter_by(user_id=user).all()
    if len(data) <= 0:
        return render_template('/Register.html', message="User does not exist")
    if data[0].pwd == pwd:
        session['user_id'] = user
        session['password'] = pwd
        return render_template("/User.html", user=user)
    return render_template('/Register.html', message="Invalid credentials")

@APP.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("password", None)
    #Alternatively we can use session.clear()
    return "Logged out"

if __name__ == '__main__':
    APP.run(debug=True)
