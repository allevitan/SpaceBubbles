from flask.views import MethodView
from flask import Blueprint, render_template, request, redirect, session
import SButils
from models import User

logout = Blueprint('logout', __name__, template_folder="../templates")

class Logout(MethodView):
    def post(self):
        session.pop("uid")
        return redirect("/")

logout.add_url_rule("/logout", view_func=Logout.as_view('logout'))
