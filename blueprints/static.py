from flask.views import MethodView
from flask import Blueprint, render_template, send_from_directory

static = Blueprint('static', __name__, template_folder="../templates")

class Static(MethodView):

    def get(self, filename):
        return send_from_directory('static',filename)

static.add_url_rule('/static/<path:filename>', view_func=Static.as_view('static'))
