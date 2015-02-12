__author__ = 'stonex'

import demjson

file_name = "dex_output_50_ms"
fp = open(file_name)

data = fp.read()
fp.close()

json_data = demjson.decode(data)

print json_data['runStats']

for each in json_data['results']:
    print "\navgTimeMillis: ", each['details']['avgTimeMillis'], " namespace: ", each['namespace'], " recommendation: ",\
    each['recommendation']['shellCommand']
