from flask.views import MethodView
from flask import Blueprint, render_template, request
import SButils
from models import User

signup = Blueprint('signup', __name__, template_folder="../templates")

class Signup(MethodView):
    def write_form(self, errors, username="", 
                         password="", 
                         verify="", 
                         email=""):
        username_error = errors[0] 
        password_error = errors[1] 
        verify_error = errors[2] 
        email_error = errors[3] 

        return render_template('signup.html', username=username,
                                              password=password,
                                              verify=verify,
                                              email=email,
                                              username_error=username_error, 
                                              password_error=password_error, 
                                              verify_error=verify_error, 
                                              email_error=email_error)
    

    def get(self):
        #Maybe add an error - if you're already logged in, 
        #raise an error message and ask the user if s/he 
        #would like to logout before proceeding.
        return self.write_form(["", "", "", ""])

    def post(self):
        input_username = str(request.form.get("username"))
        input_password = str(request.form.get("password"))
        input_verify = str(request.form.get("verify"))
        input_email = str(request.form.get("email"))
        print input_email

        valid_username = SButils.valid_username(input_username)
        valid_password = SButils.valid_password(input_password)
        valid_verify = SButils.valid_verify(input_password, input_verify)
        valid_email =  SButils.valid_email(input_email)

        errors = ["", "", "", ""]

        if not valid_username:
            errors[0] = "That's not a valid username."
        if not valid_password:
            errors[1] = "That wasn't a valid password."
        if not valid_verify:
            errors[2] = "Your passwords didn't match."
        if not valid_email or input_email == "":
            errors[3] = "That's not a valid email."
        
        if errors != ["", "", "", ""]:
            return self.write_form(errors, input_username, "", "", input_email)
        else:
            user_existence = User.objects(email=str(input_email))
            if len(user_existence) != 0:
                errors[0] = "That user already exists."
                return self.write_form(errors, input_username, "", "", input_email)
            else:
                #create hashed pw + salt
                hashed_pw = SButils.make_pw_hash(str(input_password))
                #create gravatar profile picture URL
                gravatarURL = SButils.obtain_gravatar(input_email)
                #save the user into database
                u = User(hashedpass=hashed_pw, 
                         name=str(input_username), 
                         email=str(input_email), 
                         avatar=gravatarURL).save()
                u.save()
                return redirect('/')
                #LOGIN!! WOOT
                #self.login(username=str(input_username), secret=secret)
                
signup.add_url_rule("/signup", view_func=Signup.as_view('signup'))

