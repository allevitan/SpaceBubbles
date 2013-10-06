from flask.views import MethodView
from flask import Blueprint, render_template, request, jsonify, session
from models import User, Space, Node, Page, Comment
from bson.objectid import ObjectId

api = Blueprint('api', __name__, template_folder="../templates")

class GetSpaces(MethodView):
    
    def get(self):
        if not (session and session.get('uid')):
            return jsonify({'error': 'Not logged in'})
        
        user = User.objects(id=ObjectId(session.get('uid')))[0]
        output = [{'title': space.title,
                   'sid': space.id,
                   'creation': space.creation,
                   'users': [{'uid': user.id,
                              'name': user.name}
                             for user in space.users]}
                  for space in user.spaces]
        return jsonify({'spaces':output})


class GetSpace(MethodView):
    def get(self):
        if not (session and session.get('uid')):
            return jsonify({'error': 'Not logged in'})
        if not request.args.get('sid'):
            return jsonify({'error': 'No space id provided'})
        user = User.objects(id=ObjectId(session.get('uid')))[0]
        spaces = user.spaces(id=ObjectId(request.args['sid']))
        if len(spaces) == 0:
            return jsonify({'error': 'No spaces found'})
        nodes = spaces[0].nodes
        output = [{'name': node.title,
                   'url': node.url,
                   'score': node.score,
                   'pages': [{'slug':page.slug,
                              'url': page.url,
                              'author': page.author,
                              'readby': [{'uid':user.id,
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
        if not (session and session.get('uid')):
            return jsonify({'error': 'Not logged in'})
        space = Space(title=request.form['title']).save()
        user = User.objects(id=ObjectId(session.get('uid')))[0]
        user.spaces.append(space)
        user.save(cascade=True)
    	return jsonify({'success':1})

class AddNode(MethodView):
    def post(self):
        if not (session and session.get('uid')):
            return jsonify({'error': 'Not logged in'})
        node = Node(title=request.form['title'])
        node.url = request.form['url']
        node.score = 1
        node.save()
        space = Space.objects(id=ObjectId(request.form['sid']))[0]
        space.nodes.append(node)
        space.save(cascade=True)
        
    	return jsonify({'success':1})

class AddPage(MethodView):
    def post(self):
        if not (session and session.get('uid')):
            return jsonify({'error': 'Not logged in'})
        page = Page(slug=request.form['slug'])
        page.url = request.form['url']
        page.author = User.objects(id=ObjectId(session.get('uid')))
        page.save()
        node = Node.objects(id=ObjectId(request.form['nid']))[0]
        nodes.pages.append(page)
        node.save(cascade=True)
        
    	return jsonify({'success':1})

class AddComment(MethodView):
    def post(self):
        if not (session and session.get('uid')):
            return jsonify({'error': 'Not logged in'})
        comment = Comment(text=request.form['text'])
        comment.author = User.objects(id=ObjectId(session.get('uid')))
        comment.save()
        node = Node.objects(id=ObjectId(request.form['nid']))[0]
        nodes.comments.append(comment)
        node.save(cascade=True)
        
    	return jsonify({'success':1})

api.add_url_rule("/api/get/spaces", view_func=GetSpaces.as_view('get_spaces'))
api.add_url_rule("/api/get/space", view_func=GetSpace.as_view('get_space'))
api.add_url_rule("/api/add/space", view_func=AddSpace.as_view('add_space'))
api.add_url_rule("/api/add/node", view_func=AddNode.as_view('add_node'))
api.add_url_rule("/api/add/page", view_func=AddPage.as_view('add_page'))
api.add_url_rule("/api/add/comment", view_func=AddComment.as_view('add_comment'))
