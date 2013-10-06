from flask.views import MethodView
from flask import Blueprint, render_template, request, session, jsonify, redirect
from models import User

my_graph = Blueprint('my_graph', __name__, template_folder="../templates")

class MyGraph(MethodView):

    def get(self):
        if not (session and session.get('uid')):
            return redirect('/login')
        return render_template('my_graph.html')

my_graph.add_url_rule("/my_graph", view_func=MyGraph.as_view('my_graph'))
