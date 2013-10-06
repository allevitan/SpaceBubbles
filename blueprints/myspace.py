from flask.views import MethodView
from flask import Blueprint, render_template, request, session, jsonify, redirect
from models import User

myspace = Blueprint('myspace', __name__, template_folder="../templates")

class MySpace(MethodView):

    def get(self):
        if not (session and session.get('uid')):
            return redirect('/login')
        return render_template('my_spaces.html')

myspace.add_url_rule("/my_spaces", view_func=MySpace.as_view('myspace'))
