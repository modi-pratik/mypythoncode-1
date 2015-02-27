import hashlib

__author__ = 'stonex'
import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import Connection, MongoClient
import memcache
from flask import request, abort, Flask, jsonify, url_for
import redis
from functools import wraps
from passlib.apps import custom_app_context as pwd_context
# from passlib.hash import sha256_crypt


# import ipdb
# ipdb.set_trace()
# class User(object):
#     __tablename__ = 'users'
#     # id =
#     # username =
#     password_hash = None
#
#     def hash_password(self, password):
#         self.password_hash = sha256_crypt.encrypt(password)
#
#     def verify_password(self, password):
#         return sha256_crypt.verify(password, self.password_hash)
#
#
# def hash_password(self, password):
#     self.password_hash = sha256_crypt.encrypt(password)
#
# def verify_password(self, password):
#     return sha256_crypt.verify(password, self.password_hash)


# Flask
app = Flask(__name__)

# MongoDB connection
connection_string = 'mongodb://192.168.4.86:27017/'
client = MongoClient(connection_string)
db = client['mobapi']


def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default)


# Api call for getStream which returns json
@app.route('/api/getstream', methods=['GET'])
def get_stream():
    from ast import literal_eval

    # connecting to local memcache server
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    # redis server
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    # getting the parameters from the request
    streamtype = request.args.get('streamtype', None)
    id = request.args.get('id')
    # loggedinUser['_id'] =
    query = request.args.get('query')
    fields = request.args.get('fields')
    limit = request.args.get('limit')
    page = request.args.get('page')
    order = request.args.get('order')
    comment = request.args.get('comment')
    showpromocards = request.args.get('showpromocards')
    apikey = request.args.get('apikey')
    query_dict = literal_eval(query)

    # making memcache key
    memcache_key = str(id + "_" + query_dict['company_id'])
    print "memcache_key: ", memcache_key

    # looking for memcache_key in server
    # json_results = mc.get(memcache_key)

    # redis read
    json_results = r.get(memcache_key)
    if not json_results:
        # memcache miss call
        # import ipdb
        # ipdb.set_trace()
        json_results = []
        str1 = 'getStream('+'"'+streamtype+'"'+','+'"'+id+'"'+','+'""'+','+query+','+'"'+fields+'"'+','+'"'+limit+'"'+','+'"'+page+'"'+','+order+','+'"'+comment+'"'+','+'"'+showpromocards+'"'+','+'"'+apikey+'"'+')'
        # result = db.system_js.getStream(streamtype, id, "", query, fields, limit, page, order, comment, showpromocards, apikey)
        query_js = db.eval(str1)
        json_results = json.dumps(query_js, default=json_util.default)

        # setting the memcache in local server
        # mc.set(memcache_key, json_results)

        # setting value in redis
        r.set(memcache_key, json_results)

    return json_results




@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    users_collection = db['users']
    if users_collection.find_one({'username': username}) is not None:


        hash_passwd = 'DYhG93b0qyJfIxfs2guVoUubWwvniR2G0FgaC9mi12'+password
        user_pwd_db = str(users_collection.find_one({'username': username})['password'])

        user_hashed_pwd = hashlib.sha1(hash_passwd).hexdigest()
        if user_pwd_db == user_hashed_pwd:
            # success
            print "user is valid user"
            import ipdb
            ipdb.set_trace()
        else:
            abort(400) # existing user
    # user = User(username=username)
    # user.hash_password(password)
    # db.session.add(user)
    # db.session.commit()
    return jsonify({'username': username}), 201, {'Location': url_for('get_user', id = id, _external = True)}


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

if __name__ == '__main__':
    app.run(debug=True)