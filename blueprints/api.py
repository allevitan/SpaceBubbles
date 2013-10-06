from flask.views import MethodView
from flask import Blueprint, render_template, request, jsonify, session
from models import User, Space, Node, Page, Comment

api = Blueprint('api', __name__, template_folder="../templates")

class GetSpaces(MethodView):
    
    def get(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
        
        user = User.objects(uid=session.uid)[0]
        spaces = user.spaces
        return jsonify([{'title': space.title} for space in spaces])


class GetSpace(MethodView):
    def get(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
    	return jsonify({'this is': {'fake' : 'data'}})

class AddSpace(MethodView):
    def post(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
    	return jsonify({'this is': {'fake' : 'data'}})

class AddNode(MethodView):
    def post(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
    	return jsonify({'this is': {'fake' : 'data'}})

class AddPage(MethodView):
    def post(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
    	return jsonify({'this is': {'fake' : 'data'}})	
    
api.add_url_rule("/api/get/spaces/", view_func=GetSpaces.as_view('get_spaces'))
api.add_url_rule("/api/get/space/", view_func=GetSpace.as_view('get_space'))
api.add_url_rule("/api/add/space/", view_func=AddSpace.as_view('add_space'))
api.add_url_rule("/api/add/node/", view_func=AddNode.as_view('add_node'))
api.add_url_rule("/api/add/page/", view_func=AddPage.as_view('add_page'))
