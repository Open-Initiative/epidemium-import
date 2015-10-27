import sys

__author__ = 'PC-DD-10'

from urllib.parse import quote
from urllib.request import Request, urlopen, HTTPError
import json, csv, re, uuid
from settings import *

strFile = "data/ocde_dataset_resource.csv"

dict_orga = {}
dict_orga['name'] = 'ocde'
dict_orga['title'] = 'OCDE'

request = Request('http://%s/api/action/organization_create' % ckan_host)
data_string = quote(json.dumps(dict_orga)).encode('utf8')
request.add_header('Authorization', ckan_api_key)
try:
    response = urlopen(request, data_string)
    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read().decode())
    assert response_dict['success'] is True
except HTTPError as error:
    print("{}: {}".format(dict_orga["name"], error.read()))

dict_dataset = {}
dict_dataset['owner_org'] = 'ocde'
dict_dataset['name'] = 'etatdesante'
dict_dataset['title'] = "État de santé"
dict_dataset['description'] = "L'état de santé inclut la durée de vie des personnes et leur santé physique et mentale, qui peut être affectée par des maladies infectieuses, des affections chroniques et des blessures."


request = Request('http://%s/api/action/package_create' % ckan_host)
data_string = quote(json.dumps(dict_dataset)).encode('utf8')

print(data_string)

request.add_header('Authorization', ckan_api_key)
try:
    response = urlopen(request, data_string)
    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read().decode())
    assert response_dict['success'] is True
except HTTPError as error:
    print("{}: {}".format(dict_dataset["name"], error.read()))

# sys.exit()

for row in csv.DictReader(open(strFile, encoding='utf-8'), delimiter=";"):
    dict_res = {}
    dict_res['id'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, row['url']))
    dict_res['package_id'] = 'etatdesante'
    dict_res['url'] = row['url']
    dict_res['title'] = row['indicator_name']
    dict_res['name'] = row['indicator_name']

    request_res = Request('http://%s/api/action/resource_create' % ckan_host)
    request_res.add_header('Authorization', ckan_api_key)
    data_string = quote(json.dumps(dict_res)).encode('utf8')
    try:
        response = urlopen(request_res, data_string)
        # Use the json module to load CKAN's response into a dictionary.
        response_dict = json.loads(response.read().decode())
        assert response_dict['success'] is True
    except HTTPError as error:
        print("{}: {}".format(dict_res['description'], error.read()))
