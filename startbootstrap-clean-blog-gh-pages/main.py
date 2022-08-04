from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

 
config = {
  "apiKey": "AIzaSyCgAeORTX5FNlLfsUs4sRpJ5hfDrowx7rk",
  "authDomain": "cs-ella-s-blog.firebaseapp.com",
  "projectId": "cs-ella-s-blog",
  "storageBucket": "cs-ella-s-blog.appspot.com",
  "messagingSenderId": "599549052654",
  "appId": "1:599549052654:web:7fb783e54cf0dceb36d5ff",
  "measurementId": "G-HF5RQ6FZLB",
  "databaseURL" : "https://cs-ella-s-blog-default-rtdb.firebaseio.com/"
} 

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       # try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('about'))
       # except:
       #      error = "Authentication failed"
       #      return render_template("signup.html")
    return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
           login_session['user'] = auth.sign_in_with_email_and_password(email, password)
           return redirect(url_for('about'))
       except:
           error = "Authentication failed"
           return render_template("signin.html")
    return render_template("signin.html")


@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/contact', methods = ['GET', 'POST']) 
def contact():
    error = ""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        try:
            post = {"name":request.form["name"], "messege" : request.form["messege"]}
            db.child("posts").push(post)
            return render_template("contact.html", messege=post["messege"])
        except:
           error = "Authentication failed" 
    return render_template('contact.html')

@app.route('/post')
def post():
    return render_template('post.html')
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/messege', methods=['GET','POST'])
def messege():
    if request.method == 'GET':
       try:
            print('here')
            message = db.child("posts").get().val()
            print(message)
            return render_template('messege.html', message=message)
       except:
           print("Couldn't add message")
    return render_template('messege.html')    



app.run(debug = True)