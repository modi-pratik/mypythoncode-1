__author__ = 'stonex'
from pymongo import MongoClient


def get_collection(collection_name):
    # connection_string = 'mongodb://192.168.4.86:27017/'
    connection_string = 'mongodb://livedbuser:WeCnI8VjEiFg4AzX3BjOg4W2R6Q8D@54.80.251.254:27017/mobapi'

    client = MongoClient(connection_string)
    # import ipdb
    # ipdb.set_trace()
    db = client['mobapi']
    collection_name = db[collection_name]
    # import ipdb
    # ipdb.set_trace()
    return collection_name


if __name__ == "__main__":
    system = get_collection(collection_name='system')
    # getting profile data
    quires = system.profile.find().sort('millis', -1)
    # import ipdb
    # ipdb.set_trace()
    summary_dict = {}

    for each in quires:
        # if the query is command
        if 'command' in each and each['millis']:
            # find which command is used
            if "$eval" in each['command']:
                # print each['command']['$eval']
                cmd_list = each['command']['$eval'].split("(")
                # counting the command used
                if cmd_list[0] == 'db.eval':
                    cmd = cmd_list[1].strip("'")
                    if cmd in summary_dict:
                        cmd_count = summary_dict[cmd]
                        summary_dict.update({cmd: cmd_count + 1})
                    else:
                        summary_dict[cmd] = 1
                        # summary_dict.update({cmd_list[1]: int(summary_dict[cmd_list[1]])+1})
                else:
                    cmd = cmd_list[0]
                    if cmd in summary_dict:
                        cmd_count = summary_dict[cmd]
                        summary_dict[cmd] = cmd_count + 1
                    else:
                        summary_dict[cmd] = 1

                        # import ipdb
                        # ipdb.set_trace()
        else:
            # import ipdb
            # ipdb.set_trace()
            print "slow collection: ", each['ns'], each['millis'], each['op'], each.get('query')
            ns = each['ns']
            # if each['op'] == 'query':
            #     # import ipdb
            #     # ipdb.set_trace()
            #     print "query :", each['query']
            if ns in summary_dict:
                ns_count = summary_dict[ns]
                summary_dict[ns] = ns_count + 1
            else:
                summary_dict[ns] = 1
                # print each

    sorted_summary_list = sorted(summary_dict, key=lambda a: summary_dict[a])
    sorted_summary_data = [(x, summary_dict[x]) for x in sorted_summary_list]

    # print sorted_summary_data
    import ipdb
    ipdb.set_trace()
    for each in sorted_summary_data:
        print each
        # print summary_dict


# {u'allUsers': [],
# u'lockStats':
#               {u'timeAcquiringMicros':
#                                        {u'r':
#                                              0L, u'R': 0L, u'w': 6L, u'W': 2L},
#                u'timeLockedMicros': {u'R': 0L, u'W': 3565253L}
#               },
#  u'responseLength':415884,
#  u'millis': 3565,
#  u'ts': datetime.datetime(2015, 2, 3, 12, 53, 28, 500000),
#  u'client': u'192.168.2.248',
#  u'execStats': {},
#  u'numYield': 0,
#  u'command': {u'$eval': Code('db.eval(\'getUserFriends("5386f3bff1989db2116e5bf6")\');', {}),
#  u'args': []},
#  u'user': u'',
#  u'keyUpdates': 0,
#  u'ns': u'mobapi.$cmd',
#  u'op': u'command'}
