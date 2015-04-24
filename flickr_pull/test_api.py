import flickrapi
from pprint import pprint

api_key = u'c0736923769319e5134c600d7a2254ba'
api_secret = u'71035e4390914c6b'

#flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

resp = flickr.urls.lookupGroup(url = "https://www.flickr.com/groups/caterpillarequipment/pool/")

group_id = resp['group']['id']

response = flickr.groups.pools.getPhotos(group_id=group_id, per_page=3)
pprint(response)




#import ipdb
#ipdb.set_trace()
#flickr.authenticate_via_browser(perms='read')


flickr.photos_getInfo(photo_id='123')
