from flask.views import MethodView
from flask import Blueprint, render_template, request, session, jsonify
from models import User

home = Blueprint('home', __name__, template_folder="../templates")

class Home(MethodView):

    def get(self):
        return render_template('home.html')

home.add_url_rule("/", view_func=Home.as_view('home'))
