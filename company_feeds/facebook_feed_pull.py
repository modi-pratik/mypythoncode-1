__author__ = 'stonex'
from facepy import GraphAPI
from facepy import utils

from operator import itemgetter

access_token = 'da89270e98a88a1a56fd9a71b1985b95'
app_id = 431502770337118 # must be integer
app_secret = "da89270e98a88a1a56fd9a71b1985b95"
oath_access_token = utils.get_application_access_token(app_id, app_secret)

graph = GraphAPI(oath_access_token)
company_name = 'CharlesSchwab'
company_posts = company_name + '/posts'
graph_data = graph.get(company_posts)
posts = graph_data['data']
for each in posts:
    if 'description' in each:
        each['likes_count'] = len(each['likes']['data'])
    else:
        each['likes_count'] = None

sorted_x = sorted(posts, key=itemgetter('likes_count'))

for item in sorted_x:
    print "\n"
    print item
