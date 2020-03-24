from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello():
     return "Hello world"

@app.route('/')
def hello_world():
   return 'Hello'

if __name__ == '__main__':
   app.run()
