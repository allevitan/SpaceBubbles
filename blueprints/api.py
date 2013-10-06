from flask.views import MethodView
from flask import Blueprint, render_template, request, jsonify, session
from models import User, Space, Node, Page, Comment

api = Blueprint('api', __name__, template_folder="../templates")

class GetSpaces(MethodView):
    
    def get(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
        
        user = User.objects(uid=session.uid)[0]
        output = [{'title': space.title,
                   'sid': space.sid,
                   'creation': space.creation,
                   'users': [{'uid': user.uid,
                              'name': user.name}
                             for user in space.users]}
                  for space in user.spaces]
        return jsonify({'spaces':output})


class GetSpace(MethodView):
    def get(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
        user = User.objects(uid=session.uid)[0]
        spaces = user.spaces(title=request.form['space'])
        if len(spaces) == 0:
            return jsonify({'error': 'No spaces found'})
        nodes = spaces[0].nodes
        output = [{'name': node.title,
                   'url': node.url,
                   'score': node.score,
                   'pages': [{'slug':page.slug,
                              'url': page.url,
                              'author': page.author,
                              'readby': [{'uid':user.uid,
                                          'name':user.name}
                                         for user in page.readby]} 
                             for page in node.pages],
                   'comments': [{'author': {'uid':comment.author.id,
                                            'name':comment.author.name},
                                 'text': comment.text,
                                 'creation': comment.creation}
                                for comment in node.comments]}
                  for node in nodes]
    	return jsonify({'nodes':output})

class AddSpace(MethodView):
    def post(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
        space = Space(title=request.form['title']).save()
        user = User.objects(uid=session.uid)[0]
        user.spaces.append(space)
        user.save(cascade=True)
    	return jsonify('success')

class AddNode(MethodView):
    def post(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
        node = Node(title=request.form['title'])
        node.url = request.form['url']
        node.score = 1
        node.save()
        space = Space.objects(sid=int(request.form['sid']))[0]
        space.nodes.append(node)
        space.save(cascade=True)
        
    	return jsonify({'this is': {'fake' : 'data'}})

class AddPage(MethodView):
    def post(self):
        if not (session and session.uid):
            return jsonify({'error': 'Not logged in'})
        page = Page(slug=request.form['slug'])
        page.url = request.form['url']
        page.author = User.objects(uid=session.uid)
        page.save()
        node = Node.objects(sid=int(request.form['nid']))[0]
        nodes.pages.append(page)
        node.save(cascade=True)
        
    	return jsonify({'this is': {'fake' : 'data'}})

api.add_url_rule("/api/get/spaces/", view_func=GetSpaces.as_view('get_spaces'))
api.add_url_rule("/api/get/space/", view_func=GetSpace.as_view('get_space'))
api.add_url_rule("/api/add/space/", view_func=AddSpace.as_view('add_space'))
api.add_url_rule("/api/add/node/", view_func=AddNode.as_view('add_node'))
api.add_url_rule("/api/add/page/", view_func=AddPage.as_view('add_page'))
