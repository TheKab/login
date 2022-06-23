# Controller ---- ROUTES

from flask import render_template, redirect, request, session, flash
from login_app import app
from login_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# -----------------  LOGIN USER -------------------------

@app.route("/")
@app.route('/login')
def display_login():

        return render_template("register_user.html")


@app.route('/login', methods=["POST"])
def user_login():
    #Use validate_login staticmethod to validate login form
    if User.validate_login(request.form) == False:
        return redirect("/")
    #Else get user from DB
    else:
        result = User.get_one(request.form)

        #If not in DB 
        if result == None:
            flash("Wrong credentials", "error_login")
            return redirect("/")
        #Else through session pass credentials to open homepage
        else:
            session['email']    = result.email
            session['id']       = result.id
            session['first_name'] = result.first_name

            return redirect("/homepage")


# -----------------  LOGGED IN HOMEPAGE -------------------------

@app.route('/homepage')
def homepage():
    if User.validate_session() == False:
        return redirect("/")
    else:
        data = {
            'email' : session['email']
        }
        one_user = User.get_one(data)
        return render_template("homepage.html", one_user = one_user)


# -----------------  REGISTER NEW USER WITH VALIDATION -------------------------

@app.route("/users/register_user", methods=["POST"])
def register_user():
    #Use validate_login staticmethod to validate register form = flash messages
    if User.validate_user(request.form) == False:
        return redirect("/")
    #Else get user from DB
    else:
        result = User.get_one(request.form)

        #If not in DB 
        if result is not None:
            flash("Email is taken.", "error_login")
            return redirect("/")
        #Else through pass credentials to create user
        else:
            data = {
                "first_name"    : request.form["first_name"],
                "last_name"     : request.form["last_name"],
                "email"         : request.form["email"],
                "password"      : bcrypt.generate_password_hash(request.form['password'])
            }
            new_user_id = User.save(data)

            #create session to pass through to homepage - New Registered User is logged in.
            session['email']    = data['email']
            session['id']       = new_user_id

        return redirect('/homepage')


# -----------------  LOGOUT -------------------------

@app.route("/logout", methods = ["POST"])
def user_logout():
    session.clear()
    return redirect("/login")


