from flask.views import MethodView
from flask import Blueprint, render_template, request, session, jsonify, redirect
from models import User

outer_space = Blueprint('outer_space', __name__, template_folder="../templates")

class OuterSpace(MethodView):

    def get(self):
        if not (session and session.get('uid')):
            return redirect('/login')
        return render_template('outer_space.html')

outer_space.add_url_rule("/outer_space", view_func=OuterSpace.as_view('outer_space'))
