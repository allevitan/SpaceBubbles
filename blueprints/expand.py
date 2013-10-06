from flask.views import MethodView
from flask import Blueprint, render_template, request, redirect, session
import SButils
from models import User

expand = Blueprint('expand', __name__, template_folder="../templates")

class Expand(MethodView):
    def write_form(self, space="", url=""):
        return render_template("expand.html", 
                                space = space,
                                turl=url)

    def get(self):
        return self.write_form()

    def post(self):
        input_space = str(request.form.get("space"))
        input_url = str(request.form.get("url"))
        
        print input_space
        print input_url

        return redirect("/")

expand.add_url_rule("/expand", view_func=Expand.as_view('expand'))
