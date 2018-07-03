import facebook
import requests
import json
from diets import get_diets, write_data


token = ''

graph = facebook.GraphAPI(token)

post_id = graph.request('v3.0/2042915845959990_2045708582347383')
post_link = graph.request('v3.0/2042915845959990_2045715489013359?fields=link')
info = []
data = graph.request('v3.0/2042915845959990/feed?fields=link,updated_time,id') # get link, updated_time, id

for x in data['data']:
    try:
        name = graph.request('v3.0/{}?fields=story'.format(x['id']))['story'].split()[:2]
        name = '{} {}'.format(name[0],name[1])
        url = x['link']
        date = x['updated_time']
        if url.find('127.0.0.1:8000') == -1:
            info = get_diets(url,name)
            write_data(info)

    except Exception as e:
        print("ERROR : {}".format(e))
