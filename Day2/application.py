from flask import Flask, redirect, url_for, request
app = Flask(__name__)
from flask import render_template
 
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

      return redirect(url_for('success',name = user, pwd = pwd))
   else:
      return render_template('/Register.html')
 
if __name__ == '__main__':
   app.run(debug = True)
