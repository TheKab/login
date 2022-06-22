from login_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re	# the regex EMAIL_REGEX module
from flask_bcrypt import Bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__( self , data ):
        self.id         = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.email      = data['email']
        self.password   = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# ------------------ GET ONE USER ---------------------------
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        #result is a dictionary
        result = connectToMySQL('login_users').query_db(query, data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None





# ------------------ SAVE ONE USER ---------------------------
    @classmethod
    def save(cls, data):
        query =     " INSERT INTO users ( first_name, last_name, email, password) VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s ) ;"
        
        # data is a dictionary that will be passed into the save method from server.py
        user_id = connectToMySQL('login_users').query_db(query, data)
        return user_id


# ------------------ VALIDATE USER ---------------------------
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", "error_first_name")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "error_last_name")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "error_email_register")
            is_valid = False
        if len(user['password']) < 3:
            flash("Password is invalid.", "error_password_register")
            is_valid = False
        if (user['confirm_password'] != (user['password'])):
            flash("Password is invalid.", "error_confirm_password")
            is_valid = False
        return is_valid


# ------------------ VALIDATE LOGIN ---------------------------

    @staticmethod
    def validate_login(data):
        isValid = True
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide your email.", "error_email")
            isValid = False
        if data['email'] == "":
            flash("Please provide your email.", "error_email")
            isValid = False
        if data['password'] =="":
            flash("Please provide your password.", "error_password")
            isValid = False
        return isValid


# -----------------  VALIDATE SESSION  -------------------------

    @staticmethod
    def validate_session():
        #id comes from users controller user_login() -> session['id']
        if "id" in session:
            return True
        else:
            flash("You are not logged in.", "error_not_loggedin")
            return False









# # ------------------ SHOW USER PAGE ---------------------------
#     @classmethod
#     def show(cls, data):
#         query = " SELECT * FROM users WHERE  id = %(user_id)s ;"  

#         #result in a list
#         result = connectToMySQL('login_users').query_db(query, data)

#         return cls(result[0])