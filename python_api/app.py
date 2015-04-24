import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import Connection, MongoClient
import logging
from flask import request, abort, Flask, jsonify, url_for
from functools import wraps
import time
from flask.ext.pymongo import PyMongo
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
# import ujson
# import memcache
# import redis
# from passlib.apps import custom_app_context as pwd_context
# import hashlib
# from logging.handlers import RotatingFileHandler


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# app.config['DEBUG'] = True
# app.debug = True
# app.run(debug=True)


""" root or index page view functions here"""
@app.route('/')
def index():
    return 'Flask is running!'


"""
 The actual decorator function using api_key to verify calls to api
"""
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        if request.values.get('apikey') and str(request.values.get('apikey')) in ['api2014arcgate', 'api2014mobilearcgate']:
            return view_function(*args, **kwargs)
        else:
            final = {'result': {'status': False, 'msg': "Invalid apikey", 'data': None}}
            json_results = json.dumps(final, default=json_util.default)
            return json_results, 200, {'Content-Type': 'application/json'}
            # abort(401)
    return decorated_function


# """ verify the user is logged in or not """
def verify_token(token):
    """ here verify id to where cake php saves the userid"""
    if token:
        return True
    else:
        return False


""" test response (json data) from api """
@app.route('/data')
def names():
    data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)


# """ converts the data to json data"""
# def toJson(data):
#     """Convert Mongo object(s) to JSON
#     :rtype : json object
#     """
#     return json.dumps(data, default=json_util.default)


def make_db_connection():
    """
        MongoDB connection
        connection_string = 'mongodb://192.168.4.86:27017/'
    """
    # connection_string = 'mongodb://10.184.172.70:27017'
    # [username, password, host, port, db] = ['livedbuser',
    # 'WeCnI8VjEiFg4AzX3BjOg4W2R6Q8D', '54.80.251.254', '27017', 'mobapi']
    # mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)

    # print "mongo uri: ", mongo_uri
    # client = MongoClient(mongo_uri)
    """ testing database """
    connection_string = 'mongodb://192.168.4.86:27017/'
    client = MongoClient(connection_string)
    # db = client['mobapi']
    db = client['mobapi_live']
    """ test db connection """
    print "user count: ", db.users.count()
    return db


app.config['MONGO_URI'] = 'mongodb://192.168.4.86:27017/mobapi_live'
mongo = PyMongo(app, config_prefix='MONGO')


"""==================================================================================================================
    Api call for getStream which returns json
   ==================================================================================================================
"""
@app.route('/api/stream/getStreams.json', methods=['GET'])
@require_appkey
def get_stream():
    """ storing the start of time for api"""
    start_time = time.time()
    db = mongo.db
    """ import for the view fuction"""
    # from ast import literal_eval
    # app.logger.warning('A warning occurred (%d apples)', 42)
    # app.logger.error('An error occurred')
    # app.logger.info('Info')

    # connecting to local memcache server
    # mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    # redis server
    # r = redis.StrictRedis(host='localhost', port=6379, db=0)

    # getting the parameters from the request
    streamtype = request.args.get('streamtype', "Stream")
    id = request.args.get('id', "5386f7d8bbe855db0e8b45d8")
    # loggedinUser['_id'] =
    # query = request.args.get('query')

    query_dict = {"status": "active", "company_id": id}
    query = json.dumps(query_dict)

    fields = request.args.get('fields', '[]')
    limit = request.args.get('limit', '1')
    page = request.args.get('page', '1')

    order = request.args.get('order', 1)
    order_dict = {order: -1}
    order = json.dumps(order_dict)

    comment = request.args.get('comment', '0')
    showpromocards = request.args.get('showpromocards', '1')
    apikey = request.args.get('apikey')
    logging.debug('A info (query: %s)', query)

    # if query:
    #     query_dict = literal_eval(query)
    # else:
    #     abort(404)

    # """ making memcache or redis key """
    # key = str(id + "_" + query_dict['company_id'])
    # print "key: ", key

    # """ looking for key in memcache server"""
    # json_results = mc.get(key)

    # """ looking for key in redis server """
    # json_results = r.get(key)

    json_results = None
    """ cache miss logic """
    if not json_results:
        # memcache miss call
        # json_results = []
        str1 = 'getStream(' + '"' + streamtype + '"' + ',"' + id + '",' + ' "" ' + ',' + query + ',' + '"' +\
               fields + '"' + ',' + '"' + limit + '"' + ',' + '"' + page + '"' + ',' + order + ',' + '"' + comment +\
               '"' + ',' + '"' + showpromocards + '"' + ',' + '"' + apikey + '"' + ')'
        # result = db.system_js.getStream(streamtype, id, "", query, fields, limit, page, order, comment,
        #  showpromocards, apikey)

        query_js = db.eval(str1)

        result = {'Total': query_js['total'], 'status': True, 'msg': "list of streams", 'data': query_js}
        format_result = {'result': result}
        json_results = json.dumps(format_result, default=json_util.default)

        # setting the memcache in local server
        # mc.set(memcache_key, json_results)

        # setting value in redis
        # r.set(memcache_key, json_results)
    end_time = time.time()
    # time_take = end_time - start_time
    # logging.info("time take: %s for url: %s", time_take, request.url)
    # print "time take: ", time_take  #, "for url: ", request.url
    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
     Api to get company profile
   ==================================================================================================================
"""
@app.route('/api/company/profile.json', methods=['GET'])
@require_appkey
def get_profile():
    """ get api for company profile """
    # logging.debug('A info (query: %s)', "query")
    # logging.info("testing")

    start_time = time.time()
    db = mongo.db
    # db = make_db_connection()
    fields = None
    result_qs = None
    apikey = request.args.get('apikey', None)
    #     # error codes need to be defined here
    if apikey == 'api2014mobilearcgate':
        #mbile req. handler
        fields = ['address', 'category', 'city', 'companyemployeecount', 'companyfancount', 'description', 'facebook', 'linkedin', 'logo',
                  'name', 'url', 'urlname', 'coverphoto']
    else:
    # elif apikey == 'api2014arcgate':
        #web req. handler
        fields = ['address', 'category', 'city', 'country', 'zip', 'state', 'street', 'phone', 'fax', 'companyemployeecount', 'companyfancount', 'description', 'facebook', 'linkedin', 'logo',
                  'name', 'url', 'urlname', 'meta_title', 'meta_description', 'meta_keyword', 'uid', 'coverphoto', 'address_update', 'facebook_update_date']
    # else:
    #     msg = 'Invalid apikey.'
    #     status = False
    #     final = {'result': {'status': status, 'msg': msg, 'data': None}}
    #     json_results = json.dumps(final, default=json_util.default)
    #     return json_results
    #     # abort()

    _id = request.args.get('_id', None)
    urlname = request.args.get('urlname', None)
    if _id:
        result_qs = db.companies.find_one({'_id': ObjectId(_id)}, fields)
    elif urlname:
        result_qs = db.companies.find_one({'urlname': urlname}, fields)
    else:
        # error codes need to be defined here
        msg = 'Name OR ID required.'
        status = False
        final = {'result': {'status': status, 'msg': msg, 'data': None}}
        json_results = json.dumps(final, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}
        # abort(404)

    if result_qs and result_qs['_id']:
        cid = str(result_qs['_id'])
        # verify current user if verified then make status 'active', depends on user
        status = 'active'
        # check here for scope public or private, depends on user
        scope = 'public'
        groups = db.groups.find({'cid': cid, 'status': status, 'scope': scope}, {'_id': 1})
        groupids = [str(g['_id']) for g in groups]
        # canedit logic still figure out, depends on user
        result_qs['_id'] = cid
        result_qs['category'] = result_qs['category'][0]
        result_qs['groups'] = groupids
        result_qs['groupcount'] = len(groupids) + 1
        status = True
        msg = "company details"
    else:
        status = False
        msg = "company doesn't exist or database issue"
    # result = {'status': 'true', 'msg': 'successfully changed the details', 'data': result_qs}
    final = {'result': {'status': status, 'msg': msg, 'data': result_qs}}
    json_results = json.dumps(final, default=json_util.default)
    end_time = time.time()
    time_take = end_time - start_time
    print "time take: ", time_take, "for url: ", request.url
    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api call for edit User which returns json
   ==================================================================================================================
"""
@app.route('/api/users/edit.json', methods=['POST'])
@require_appkey
def edit_user():
    """ get the tokenId which is session id and verify with other verify function if verified moved to edit part and
     return successfully changed or unsuccessful """

    db = mongo.db
    about = request.args.get('about', None)
    displayname = request.args.get('displayname', None)
    username = request.args.get('username', None)
    email = request.args.get('email', None)
    filedata = request.args.get('filedata', None)
    _id = request.args.get('_id', None)
    token = request.args.get('token', None)
    role = request.args.get('role', None)
    status = request.args.get('status', None)
    fname = request.args.get('fname',None)
    # apikey = request.args.get('apikey', None)

    # Check the user is logged in and have valid session id
    # verify_token(token)

    # Saving the details in db
    db_result = db.users.update({'_id': ObjectId(_id)}, {"$set": {
                                                                  'fname': fname
                                                                  # 'about': about,
                                                                  # 'displayname': displayname,
                                                                  # 'username': username,
                                                                  # 'email': email,
                                                                  # 'token': token,
                                                                  # 'role': role,
                                                                  # 'status': status
    }})

    result = {'status': 'true', 'msg': 'successfully changed the details'}
    print "done"
    json_results = json.dumps(result, default=json_util.default)
    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    API FUNCTION TO GET COMPANY DETAILS BY PARAMETERS  (must refactor for improving the code)
   ==================================================================================================================
"""
@app.route('/api/company/get.json', methods=['GET'])
@require_appkey
def get_company():
    """ get company details by params """

    db = mongo.db
    name = request.args.get('name', None)
    limit_search = request.args.get('limit', 0)
    limit_search = int(limit_search) if limit_search else 0
    page = request.args.get('page', 0)
    orderby = request.args.get('orderby', -1)
    urlname = request.args.get('urlname', None)

    data = {}
    count = 0
    skip_records = 0

    start_time = time.time()
    # logic for getting limit for query from limit and page data

    if page:
        skip_records = page * 10

    # if limit_search and page:
    #     limit_query = limit_search * page
    # else:
    #     limit_query = limit_search

    if name:
        # way 1
        # import re
        # regx = re.compile("^" + name, re.IGNORECASE)
        # test = db.companies.find({'name': regx})
        # check1 = [t['name'] for t in test]
        # end1 = time.time()
        # mongo always runs sort and then apply the limit, with different order the limit results will be also different
        result_crx = db.companies.find({'name': {'$regex': '^' + name, "$options": "-i"}}).limit(limit_search).sort('created', orderby)
        # result_crx = db.companies.find({'name': {'$regex': '^' + name, "$options": "-i"}}).skip(skip_records)\
        #     .limit(limit_search).sort('created', orderby)

        # logic for getting the format as php api does
        # for each in result_crx:
        #     data[count] = {'Company': each}
        #     count += 1

    elif urlname:
        result_crx = db.companies.find({'name': {'$regex': '^' + name, "$options": "-i"}}).skip(skip_records)\
            .limit(limit_search).sort('created', orderby)

    else:
        result1 = {'result': {'status': False, 'msg': 'list of companies', 'Total': None, 'data': None}}
        json_results = json.dumps(result1, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}

    for each in result_crx:
        data[count] = {'Company': each}
        count += 1

    total = result_crx.count()
    result1 = {'result': {'status': True, 'msg': 'list of companies', 'Total': total, 'data': data}}

    json_results = json.dumps(result1, default=json_util.default)
    # end_time1 = time.time()
    # json_results = ujson.dumps(result1, ensure_ascii=False)
    end_time = time.time()
    # log it in logger with the time taken:
    print "api finished working with time(secs) json: ", (end_time - start_time)
    # print "api finished working with time(secs): ujson", (end_time - end_time1)

    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api for getfan for companies
   ==================================================================================================================
"""
@app.route('/api/company/getfans.json', methods=['GET'])
@require_appkey
def get_fans():
    """ get fans for companies """

    db = mongo.db
    # import ipdb
    # ipdb.set_trace()
    page = request.args.get('page', 1)
    limit = int(request.args.get('limit', 1))
    _id = request.args.get('_id', None)
    count = 0
    fans_dict = {}

    start_time = time.time()
    if request.args.get('_id'):
        _id = request.args.get('_id')
    else:
        urlname = request.args.get('urlname')
        _id = db.companies.find_one({'urlname': urlname}, {'_id': 1})

    fields = ('username', 'fname', 'lname', 'picture', 'followers', 'companiesfan')
    # _id = '5386f7d8bbe855db0e8b45d8'
    fans = db.users.find({'companiesfan.cid': _id}, fields).limit(limit)
    # count the no. of compaines user follwoing
    # count the followers user has

    for each in fans:
        each['companycount'] = len(each.get('companiesfan')) if each.get('companiesfan') else 0
        each['followerscount'] = len(each.get('followers')) if each.get('followers') else 0

        if each.get('followers'):
            del each['followers']
        if each.get('companiesfan'):
            del each['companiesfan']

        # *** find current user is fan of the each (user) here ???

        cureent_userId = None

        # if cureent_userId in each.get('followers'):
        #     each['isFollow'] = True
        # else:
        #     each['isFollow'] = False

        fans_dict[count] = {'User': each}
        count += 1
    result = {'Total': count, 'data': fans_dict, 'status': True, 'msg': 'list of company fans'}
    json_data = {'result': result}
    json_results = json.dumps(json_data, default=json_util.default)
    end_time = time.time()
    # log it in logger with the time taken:
    logging.debug("api finished working with time(secs): json %s", (end_time - start_time))
    # print "api finished working with time(secs): json", (end_time - start_time)

    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api for get group Stream
   ==================================================================================================================
"""
@app.route('/api/group/get.json', methods=['GET'])
@require_appkey
def get_groupstream():
    """ get stream for group """

    db = mongo.db
    # db = make_db_connection()
    member_id = request.args.get("members_uid")
    members_role = [request.args.get("members_role[0]"), request.args.get("members_role[1]")]
    admindetails = request.args.get("admindetails")
    memberdetails = request.args.get("memberdetails")

    page = int(request.args.get("page", 1)) - 1
    limit = int(request.args.get("limit"))
    apikey = request.args.get("apikey")

    # from flask_restful import reqparse
    # parser = reqparse.RequestParser()
    # parser.add_argument(u'apikey', type=unicode, action='append')
    #
    # args = parser.parse_args()

    skip = page * limit
    # db.groups.find( {"members.uid":"53863567f1989d196402b2db",
    # "members":{
    # "$elemMatch":{
    # "uid":"53863567f1989d196402b2db","role":{"$in":["fan","admin"]}}},
    # "scope":{"$in":["public","open"]}}, [] ).
    # sort( {"created":-1} ).
    # limit( "15" ).
    # skip( 0 )

    crx_groupList = db.groups.find({"members.uid": member_id,
                                    "members": {"$elemMatch":
                                                    {
                                                        "uid": member_id, "role": {"$in": ["fan", "admin"]}
                                                    }
                                                },
                                    "scope": {"$in": [
                                                        "open",
                                                        "public",
                                                        # "private"
                                                        ]},
                                    }).sort("created", -1).limit(limit).skip(skip)
    groupList = []

    for group in crx_groupList:

        group["_id"] = str(group["_id"])
        group['membercount'] += 1
        members = db.users.find({"_id": {"$in": [ObjectId(x["uid"]) for x in group["members"]]}}, ["username", "fname", "lname", "picture", "email"])
        member_dict = {str(x['_id']): x for x in members}
        for member in group["members"]:
            member["User"] = member_dict.get(str(member["uid"]))
            if member.get("User"):
                member['User']['_id'] = str(member['User']['_id'])

        groupList.append({"Group": group})

    result = {"status": True, "msg": "list of groups", "data": groupList, "Total": crx_groupList.count()}
    format_result = {"result": result}
    json_results = json.dumps(format_result, default=json_util.default)

    # print args

    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api for get followers for users
   ==================================================================================================================
"""
@app.route('/api/users/getFollowers.json', methods=['GET'])
@require_appkey
def getFollowers():
    """ get followers for users """

    db = mongo.db

    usernname = request.args.get("username")
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 8))
    apikey = request.args.get("apikey")
    skip = limit * page
    user_id_dict = db.users.find_one({"username": usernname}, {"_id": 1})
    user_id = user_id_dict["_id"]
    # db.users.find( {"_id":ObjectId ("53863567f1989d196402b2db"),"companiesmember.status":"current"}, ["companiesmember.$"] ).sort( [] ).limit( 0 ).skip( 0 )
    # db.companies.find( {"_id":ObjectId ("5386f7d8bbe855db0e8b45d8")}, ["_id","logo","name","urlname","description"] ).sort( [] ).limit( 0 ).skip( 0 )
    # db.groups.find( {"members.uid":"53863567f1989d196402b2db"}, ["_id","group","isDisplay","members.$"] ).sort( {"created":-1} ).limit( 0 ).skip( 0 )

    crx_follower = db.users.find({"follow.uid": str(user_id)}, ["username", "fname", "lname", "picture", "followers",
                                                                "companiesfan", "status"]).limit(limit).skip(skip)

    user_count = 0
    data = {}
    for user in crx_follower:
        data[user_count] = {"User": user}
        user_count += 1

    result = {"status": True, "msg": "list of followers", "data": data, "Total": crx_follower.count()}
    format_result = {"result": result}
    json_results = json.dumps(format_result, default=json_util.default)
    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api for get following for users and company
   ==================================================================================================================
"""
@app.route('/api/users/getFollowinguserscompany.json', methods=['GET'])
@require_appkey
def get_followingusercompany():
    """ get followers for users """

    db = mongo.db

    usernname = request.args.get("username")
    _id = request.args.get("id")

    page = int(request.args.get("page", 0))
    limit = request.args.get("limit", None)
    if limit:
        limit = int(limit)
    apikey = request.args.get("apikey")

    # import ipdb
    # ipdb.set_trace()
    # db.eval('getfollowing("53863567f1989d196402b2db","","5")');
    str1 = 'getfollowing("' + _id + '"' + ',"","' + unicode(limit) + '");'
    query_js = db.eval(str1)

    result = {"status": True, "msg": "list of following", "data": query_js}
    format_result = {"result": result}
    json_results = json.dumps(format_result, default=json_util.default)
    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api for add group ( post call)
   ==================================================================================================================
"""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# import base64
# def decode_base64(data):
#     """Decode base64, padding being optional.
#
#     :param data: Base64 data as an ASCII byte string
#     :returns: The decoded byte string.
#
#     """
#     missing_padding = 4 - len(data) % 4
#     if missing_padding:
#         data += b'='* missing_padding
#     return base64.b64decode(data)


@app.route('/api/group/add.json', methods=['POST'])
@require_appkey
def add_group():
    """ get followers for users (refactoring must done)"""

    db = mongo.db

    scope = request.values.get("scope")
    group = request.values.get("group")
    groupurl = request.values.get("groupurl")
    token = request.values.get("token")
    uid = request.values.get("uid")
    cid = request.values.get("cid")
    apikey = request.values.get("apikey")

    status = "active"
    isDisplay = True

    result = {"status": True, "msg": "list of following", "data": None}

    if not status:
        result['msg'] = {"status": "You must select a status."}
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}

    if not scope:
        result['msg'] = {"scope": "You must select a scope."}
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}


    if not (group or groupurl):
        result['msg'] = {
                         "group": ["You must enter a group name."],
                         "groupurl": ["You must enter a groupurl."]
                        }
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}

    if not cid:
        result['msg'] = {"cid": ["You must enter a cid"]}
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}

    if not uid:
        result['msg'] = {"uid": ["You must enter a uid"]}
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}


    # import ipdb
    # ipdb.set_trace()
    groupurl_found = bool(db.companies.find_one({"urlname": groupurl}) or\
                     db.groups.find_one({"groupurl": groupurl}) or\
                     db.users.find_one({"username": groupurl}))

    if groupurl_found:
        result['msg'] = {"groupurl": "This groupurl already taken."}
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}

    # import ipdb
    # ipdb.set_trace()
    notsupported = ('about', 'undefined', 'login', 'contact', 'faq', 'terms', 'privacy', 'invite', 'logout')
    shouldnotstartwith = "emp-"

    if groupurl in notsupported or groupurl.startswith(shouldnotstartwith):
        result['msg'] = {"groupurl": "Group URL already exists."}
        format_result = {"result": result}
        json_results = json.dumps(format_result, default=json_util.default)
        return json_results, 200, {'Content-Type': 'application/json'}

    # import ipdb
    # ipdb.set_trace()
    coverphoto = 'files/coverphoto/group/groupdefault_1.jpg'

    if request.values.get('image') and request.values.get('filedata'):
        from utils import validatephoto
        # validatefile = {'error': error, 'img_type': img_type, 'file_like': file_like}
        validatefile = validatephoto(request)

        if not validatefile['error']:
            gid = db.groups.find_one({'groupurl': groupurl}, {'_id': 1})
            if gid:
                from config_data import GROUP_IMAGES, APP_PATH
                str_gid = str(gid['_id'])
                img_type = validatefile['img_type']
                img_path_name = APP_PATH + GROUP_IMAGES + str_gid + '.' + img_type

                from utils import uploadImage
                file_like = validatefile['file_like']
                uploadImageStatus = uploadImage(file_like)
    else:
        groupsort = group.lower()
        post_data = {'scope': scope, 'group': group, 'groupurl': groupurl, 'uid': uid, 'cid': cid,
                         'status': status, 'isDisplay': isDisplay, 'coverphoto': coverphoto, 'groupsort': groupsort,
                         'token': token, 'apikey': apikey}
        try:
            group_insert = db.groups.insert(post_data)
            group_id = str(group_insert)
            post_data['group_id'] = group_id
            result = {"status": True, "msg": "Group Added Successfully", "data": post_data}
            format_result = {"result": result}
            json_results = json.dumps(format_result, default=json_util.default)
            return json_results, 200, {'Content-Type': 'application/json'}

        except:
            logging.error("error in inserting into the db for add group api call")
            result = {"status": False, "msg": "error in inserting into the db for add group api call", "data": post_data}
            format_result = {"result": result}
            json_results = json.dumps(format_result, default=json_util.default)
            return json_results, 200, {'Content-Type': 'application/json'}



    # ''' send file to s3 bucket '''
    # import boto
    # from boto.s3.key import Key
    # from boto.s3.connection import S3Connection
    #
    # conn = S3Connection('AKIAIQMFRF3T3OGGT63Q', 'pfNgxSW+ZVTNghluSAT24nMaZuFtmOli+Cjzinej')
    #
    # bucket = conn.get_bucket('workmob-dev')
    #
    # key_image = Key(bucket)
    # try:
    #     key_image.send_file(file_like)
    # except:
    #     print "error in uploading file to server"
    #
    # img_file = request.files['file']
    #
    # if file and allowed_file(img_file.filename):
    #         filename = secure_filename(img_file.filename)
    #         img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # else:
    #     result['msg'] = {"groupurl": "Group URL already exists."}
    #     format_result = {"result": result}
    #     json_results = json.dumps(format_result, default=json_util.default)
    #     return json_results, 200, {'Content-Type': 'application/json'}
    # query_js = None
    #
    # result = {"status": True, "msg": "list of following", "data": query_js}
    # format_result = {"result": result}
    # json_results = json.dumps(format_result, default=json_util.default)
    # return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    Api for edit group ( post call)
   ==================================================================================================================
"""
@app.route('/api/group/edit.json', methods=['POST'])
@require_appkey
def edit_group():
    """ get followers for users """
    # import ipdb
    # ipdb.set_trace()
    db = mongo.db

    apikey = request.values.get("apikey")
    image_data_binary = request.values.get('image')
    category = request.values.get("category")
    description = request.values.get("description")
    token = request.values.get("token")
    _id = request.values.get("_id")
    uid = request.values.get("uid")

    group = db.groups.find_one({'_id': ObjectId(_id)})
    group_id = _id
    category_dict = db.categories.find_one({'_id': ObjectId(category)}, {'category': 1})
    # category_name = category_dict.get('category')

    if request.values.get('image'): #and request.values.get('filedata'):
        from utils import validatephoto
        # validatefile = {'error': error, 'img_type': img_type, 'file_like': file_like}
        validatefile = validatephoto(request)

        if not validatefile['error']:
            # gid = db.groups.find_one({'groupurl': groupurl}, {'_id': 1})
            if group_id:
                from config_data import GROUP_IMAGES, APP_PATH
                # str_gid = str(gid['_id'])
                img_type = validatefile['img_type']
                ext_type = validatefile['img_type'].split('/')[-1]
                # if img_type == 'jpeg':
                #     img_type = 'jpg'

                img_path_name = GROUP_IMAGES + group_id + '.' + ext_type
                local_img_path_name = APP_PATH + '/' + img_path_name
                from utils import uploadImage
                file_like = validatefile['file_like']
                # import ipdb
                # ipdb.set_trace()
                fp = open(local_img_path_name, 'wb')
                file_like.seek(0)
                fp.write(file_like.read())
                fp.close()
                uploadImageStatus = uploadImage(file_like, img_path_name, img_type)
                if uploadImageStatus:
                    pass

    query_js = None
    result = {"status": True, "msg": "list of following", "data": query_js}
    format_result = {"result": result}
    json_results = json.dumps(format_result, default=json_util.default)
    return json_results, 200, {'Content-Type': 'application/json'}


@app.route('/api/users/login.json', methods=['POST'])
#@require_appkey
def user_login():
    """ user login only for testing """
    import ipdb
    ipdb.set_trace()
    db = mongo.db
    #print "getting here"
    test = request.values['testing']
    result = {"status": True, "msg": "login post call", "data": test}
    format_result = {"result": result}
    json_results = json.dumps(format_result, default=json_util.default)
    return json_results, 200, {'Content-Type': 'application/json'}


"""==================================================================================================================
    End of api part
   ==================================================================================================================
"""


if __name__ == '__main__':

    # logging.basicConfig(filename='flask_app.log', level=logging.DEBUG)

    # handler = RotatingFileHandler('/home/www/logs/flask_app.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.DEBUG)
    # app.logger.addHandler(handler)
    # app.debug = True

    # app.run(debug=True, host='127.0.0.1', port=5500)
    # app.run(host='127.0.0.1', port=5500)
    # app.run(debug=True)

    app.run(
        host="192.168.4.242",
        port=int("5000"),
        debug=True
    )