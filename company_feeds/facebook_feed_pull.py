import multiprocessing
import time

__author__ = 'stonex'
from pymongo import MongoClient
from facepy import GraphAPI
from facepy import utils
import facepy
from operator import itemgetter
import sys


def get_access_token():
    app_id = 431502770337118 # must be integer
    app_secret = "da89270e98a88a1a56fd9a71b1985b95"
    access_token = utils.get_application_access_token(app_id, app_secret)
    return access_token


def get_collection(collection_name):
    connection_string = 'mongodb://192.168.4.86:27017/'

    client = MongoClient(connection_string)
    db = client['mobapi']
    collection_name = db[collection_name]
    return collection_name


def get_facebook_update(each):
    print "\n\n\ncurrent_count: "  #, current_count
    if each['facebook']:
        facebook_url = each['facebook']
        company_name = facebook_url.split("/")[-1]

        if 'www.facebook.com' in facebook_url.split("/"):
            # company_name = '195175413819'
            # company_posts = company_name + '/posts'

            # graph_data = graph.get(company_posts)
            try:
                # import ipdb
                # ipdb.set_trace()
                graph_data = graph.get(company_name+'?fields=posts.limit(20)')
                if not graph_data.get('posts'):
                    # if 'data' not in graph_data.get('posts'):
                    print "no updates for face url: ", facebook_url
                    # current_count -= 1
                    return None
                    # continue
                posts = graph_data['posts']['data']
                # import ipdb
                # ipdb.set_trace()
                for post in posts:
                    if 'likes' in post:
                        post['likes_count'] = len(post['likes']['data'])
                    else:
                        post['likes_count'] = None

                sorted_x = sorted(posts, key=itemgetter('likes_count'))

                # get only top ten of 20 posts pulled from facebook
                for item in sorted_x[:9]:
                    print "\n"
                    print item
                # import ipdb
                # ipdb.set_trace()
            except facepy.exceptions.OAuthError as error:
                if 'object does not exist' == error.message:
                    print "got exception: ", sys.exc_info()[0]
                    print "facebook url: ", facebook_url

                elif 'Hit API rate limit' == error.message:
                    print "got exception: ", sys.exc_info()[0]
                    print "facebook url: ", facebook_url

                else:
                   raise

            except:
                print "got exception: ", sys.exc_info()[0]
                print "facebook url: ", facebook_url
                # exception_list.append(facebook_url)
                # import ipdb
                # ipdb.set_trace()
        # current_count -= 1
        return None


def start_process():
    print 'Starting', multiprocessing.current_process().name


if __name__ == "__main__":
    start_time = time.time()
    oath_access_token = get_access_token()
    graph = GraphAPI(oath_access_token)

    queue_sociallinks = get_collection(collection_name='queue_sociallinks')
    facebook = queue_sociallinks.find({'facebook': {'$ne': ''}}, {'facebook'}, timeout=False)
    facebook_link_list = [x for x in facebook]
    current_count = facebook.count()

    pool_start_time = time.time()

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size,
                                initializer=start_process,
                                )
    pool_output = pool.map(get_facebook_update, facebook_link_list)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    pool_end_time = time.time()

    print "Pool time taken: %s" % (pool_end_time - pool_start_time)
    # 18.27620079477778 hours
    import ipdb
    ipdb.set_trace()

    get_facebook_update(facebook_link_list[0], current_count)

    exception_list = []
    for each in facebook:
        print "\n\n\ncurrent_count: ", current_count
        if each['facebook']:
            facebook_url = each['facebook']
            company_name = facebook_url.split("/")[-1]

            if 'www.facebook.com' in facebook_url.split("/"):
                # company_name = '195175413819'
                # company_posts = company_name + '/posts'

                # graph_data = graph.get(company_posts)
                try:
                    # import ipdb
                    # ipdb.set_trace()
                    graph_data = graph.get(company_name+'?fields=posts.limit(20)')
                    if not graph_data.get('posts'):
                        # if 'data' not in graph_data.get('posts'):
                        current_count -= 1
                        continue
                    posts = graph_data['posts']['data']
                    # import ipdb
                    # ipdb.set_trace()
                    for post in posts:
                        if 'likes' in post:
                            post['likes_count'] = len(post['likes']['data'])
                        else:
                            post['likes_count'] = None

                    sorted_x = sorted(posts, key=itemgetter('likes_count'))

                    # get only top ten of 20 posts pulled from facebook
                    for item in sorted_x[:9]:
                        print "\n"
                        print item
                    # import ipdb
                    # ipdb.set_trace()

                except:
                    # facepy.exceptions.OAuthError
                    # facepy.exceptions.FacebookError
                    print "got exception: ", sys.exc_info()[0]
                    print "facebook url: ", facebook_url
                    exception_list.append(facebook_url)
                    # import ipdb
                    # ipdb.set_trace()
        current_count -= 1
    end_time = time.time()

    time_taken = end_time - start_time

    print exception_list
    print "\n\n count: ", len(exception_list)
    print "time taken in secs: ", time_taken
    #