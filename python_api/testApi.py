__author__ = 'stonex'

import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import Connection
import memcache
from functools import wraps
from flask import request, abort, Flask, jsonify
from passlib.apps import custom_app_context as pwd_context


class User(object):
    __tablename__ = 'users'
    # id =
    # username =
    password_hash = None

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


# auth using user_name and password
def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# The actual decorator function using api_key
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == 'APPKEY_HERE':
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


# Flask
app = Flask(__name__)

# MongoDB connection
connection = Connection('localhost', 27017)
db = connection.blog


def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default)


# @app.route('/sightings/', methods=['GET'])
# def sightings():
#     """Return a list of all UFO sightings
#     ex) GET /sightings/?limit=10&offset=20
#     """
#     if request.method == 'GET':
#         lim = int(request.args.get('limit', 10))
#         off = int(request.args.get('offset', 0))
#         results = db['posts'].find().skip(off).limit(lim)
#         import ipdb
#         ipdb.set_trace()
#         mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#         json_results = mc.get('json_results')
#         if not json_results:
#             json_results = []
#             for result in results:
#                 json_results.append(result)
#             mc.set('json_results', json_results)
#     return toJson(json_results)


@app.route('/posts/', methods=['GET', 'POST'])
# @requires_auth
# @require_appkey
def posts():
    """Return a list of all UFO sightings
    ex) GET /sightings/?limit=10&offset=20
    """
    # import ipdb
    # ipdb.set_trace()
    if request.method == 'GET':
        lim = int(request.args.get('limit', 10))
        off = int(request.args.get('offset', 0))
        results = db['posts'].find().skip(off).limit(lim)
        # import ipdb
        # ipdb.set_trace()
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        json_results = mc.get('json_results')
        if not json_results:
            json_results = []
            for result in results:
                json_results.append(result)
            mc.set('json_results', json_results,)
    if request.method == 'POST':
        data = request.args
        import ipdb
        ipdb.set_trace()
        if 'name' in data:
            msg = 'hi, '+str(data['name'])
            return msg

        # import ipdb
        # ipdb.set_trace()

    return toJson(json_results)


@app.route('/posts/<post_id>', methods=['GET'])
def post(post_id):
    """Return specific UFO sighting
    ex) GET /posts/50ab0f8bbcf1bfe2536dc3f8
    """
    if request.method == 'GET':
        result = db['posts'].find_one({'_id': ObjectId(post_id)})
        return toJson(result)


# @app.route('/sightings/<sighting_id>', methods=['GET'])
# def sighting(sighting_id):
#     """Return specific UFO sighting
#     ex) GET /sightings/123456
#     """
#     if request.method == 'GET':
#         result = db['ufo'].find_one({'_id': ObjectId(sighting_id)})
#         return toJson(result)

if __name__ == '__main__':
    app.run(debug=True)