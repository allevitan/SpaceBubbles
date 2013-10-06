from flask.views import MethodView
from flask import Blueprint, render_template, request, session, jsonify, redirect
from models import User, Graph
from bson.objectid import ObjectId
from data_processing import process_history
import json
import os
import sqlite3

process_data = Blueprint('process_data', __name__, template_folder="../templates")

#Sketch as fuck over here
config = {};
config['UPLOAD_FOLDER'] = 'uploads'

class ProcessData(MethodView):

    def post(self):
        if not (session and session.get('uid')):
            return redirect('/login')
        
        raw_data = request.files['history']
        user = User.objects.get(id=ObjectId(session.get('uid')))
        filename=user.name
        if 'sql' in raw_data.filename.split('.')[-1]:
            filename += '.sqlite'
        raw_data.save(os.path.join(config['UPLOAD_FOLDER'], filename))
        processed_data = process_history(config['UPLOAD_FOLDER'], filename)
        processed_data = json.loads(processed_data)
        Graph(data=processed_data, user=user).save()
        os.remove(os.path.join(config['UPLOAD_FOLDER'], filename))
        return redirect('my_graph')

process_data.add_url_rule("/process_data", view_func=ProcessData.as_view('process_data'))
