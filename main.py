from flask import Flask, request, redirect, render_template
import cgi
import os
 
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('form.html', title="Signup Form")

def signin_email(char):
    if len(char) > 3 or len(char) < 21:
        return True

    empty_field = char.count(" ")
    if empty_field == 0:
        return True

    at_field = char.count("@")
    if at_field == 1:
        return True

    period_field = char.count(".")
    if period_field == 1:
        return True

    else:
        return False

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
    

    if username.count(" ") < 1:
        username_error = "Password cannot have spaces."
        password = ""
        verify = ""
    if len(username) < 3 or len(username) > 20:
        username_error = 'Username must be between 3 and 20 characters.'
        password = ''
        verify = ''

    if len(password) < 3 or len(password) > 20:
        password_error = 'Password must be between 3 and 20 characters.'
        password = ''
        verify = ''
    if password.count(" ") < 1:
        password_error = "Password cannot have spaces."
        password = ''
        verify = ''
    if verify != password:
        verify_error = "Please verify password."
        password = ''
        verify = '' 

    if len(email) != 0:
        if signin_email(email) == False:
            email_error = "Please enter a valid email."
            password = ''
            verify = ''

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