from flask import Flask, request, redirect, render_template
import cgi
import os
 
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('register.html', title="Signup Form")

def signin_email(char):
    if len(char) == 0:
        return True

    elif len(char) < 3 or len(char) > 20:
        return False
 
    elif char.count(" ") != 0:
      return False

    elif char.count("@") != 1:
      return False

    elif char.count(".") != 1:
      return False    

    else:
      return True
      
@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email'] 

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if username.count(" ") >= 1:
        username_error = "Username cannot have spaces."

    if len(username) < 3 or len(username) > 20:
        username_error = 'Username must be between 3 and 20 characters.'

    if len(password) < 3 or len(password) > 20:
        password_error = 'Password must be between 3 and 20 characters.'
        password = ''
        verify = ''

    if password.count(" ") >= 1:
        password_error = "Password cannot have spaces."
        password = ''
        verify = ''

    if verify != password:
        verify_error = "Password don't match."
        password = ''
        verify = '' 

    if signin_email(email) == False:
        email_error = "Please enter a valid email."

    if not username_error and not password_error and not verify_error and not email_error:
        username = request.form['username']
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('register.html', title="Registration Form",
            username=username, username_error=username_error,
            password=password, password_error=password_error,
            verify=verify, verify_error=verify_error,
            email=email, email_error=email_error)

@app.route("/welcome")
def welcome():
    user = request.args.get('username')
    return render_template('welcome.html', title="Welcome Page", user=user)

app.run()