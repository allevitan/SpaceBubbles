from flask.views import MethodView
from flask import Blueprint, render_template, request, redirect, session
import SButils
from models import User

login = Blueprint('login', __name__, template_folder="../templates")

class Login(MethodView):
    def write_form(self, username="", password="", loginerror=""):
        return render_template('login.html', 
                                username=username,
                                password=password,
                                loginerror=loginerror)

    def get(self):
        return self.write_form()

    def post(self):
        login_input_username = str(request.form.get("username"))
        login_input_pw = str(request.form.get("password"))
        
        try:
            u = User.objects.get(name=login_input_username)
            if u: 
                stored_hashed_pw = u.hashedpass
                if SButils.valid_pw(login_input_pw, stored_hashed_pw):
                    session['uid'] = str(u.id)
                    return redirect("/")
                else:
                    loginerror = "Invalid username and password combination."
                    return self.write_form(username=login_input_username, loginerror=loginerror)
            else:
                loginerror="derp"
                return self.write_form(loginerror=loginerror)
        except:
            loginerror = "Username does not exist in database."
            return self.write_form(loginerror=loginerror)

login.add_url_rule("/login", view_func=Login.as_view('login'))
