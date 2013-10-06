from flask.views import MethodView
from flask import Blueprint, render_template, request, session, jsonify, redirect
from models import User

home = Blueprint('home', __name__, template_folder="../templates")

class Home(MethodView):

    def get(self):
        if not (session and session.get('uid')):
            return redirect('/login')
        return redirect('my_graph')

#home.add_url_rule("/user_data/<str:user_json>", view_func=Home.as_view('home'))
home.add_url_rule("/", view_func=Home.as_view('home'))
