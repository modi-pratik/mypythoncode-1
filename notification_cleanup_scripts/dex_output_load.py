from pymongo import MongoClient

__author__ = 'Snehal'

# from work_scrap import scrap_data_page, scrap_data_page_part2
import json

# connection_string = 'mongodb://192.168.4.86:27017/'
#
# client = MongoClient(connection_string)
# db = client['mobapi']
# dex_output.json
with open("dex_output_profile_86.json") as json_file:
    json_data = json.load(json_file)
    print(json_data)

cmd_list = []
for each in json_data['results']:
    if each['details']['avgTimeMillis'] >= 20:
        print "\n"
        print each['details']['avgTimeMillis'], " ", each['recommendation']['namespace'], " ",\
            each['recommendation']['index'],  " \n"
        cmd_list.append(each['recommendation']['shellCommand'])

print "\n\n"

for cmd in cmd_list[1:]:
    print cmd, "\n"
    # collection_name = (cmd.split(".")[0].split("\"")[1])
    # cmd_string = cmd.split(".")[1]
    #
    # import ipdb
    # ipdb.set_trace()
    # db.collection_name.command(cmd_string)





