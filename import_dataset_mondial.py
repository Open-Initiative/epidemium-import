__author__ = 'PC-DD-10'
# !/usr/bin/env python3
from urllib.parse import quote
from urllib.request import Request, urlopen, HTTPError
import json, csv, re, uuid
from settings import *

# Put the details of the dataset we're going to create into a dict.

strFile = "data/mondial_dataset.csv"
strOrg = "data/mondial_orga.csv"

dataset_unique = []
list_org = []

for row in csv.DictReader(open(strOrg, encoding='utf-8'), delimiter=";"):
    list_org.append(row['name'])

print(list_org)

count = 0
max = 0
for row in csv.DictReader(open(strFile, encoding='utf-8'), delimiter=";"):
    # Use the json module to dump the dictionary to a string for posting.
    if count > max and max > 0:
        continue


    if not str(row['organization']) in list_org:
        continue



    count += 1
    row['organization'] = re.sub(r'\W', '-', row['organization']).lower()

    dataset_dict = {}
    # pour resources
    dataset_dict['name'] = re.sub(r'\W', '-', row['category'] + row['sub_category']).lower()
    dataset_dict['title'] = row['category'] + " / " + row['sub_category']
    dataset_dict['owner_org'] = row['organization']
    dataset_dict['license_id'] = 'License Open'



    # We'll use the row_create function to create a new row.

    if not row['organization']+dataset_dict['name'] in dataset_unique:
        dataset_unique.append(row['organization']+dataset_dict['name'])
        data_string = quote(json.dumps(dataset_dict)).encode('utf8')
        print(data_string)
        request = Request('http://%s/api/action/package_create'%ckan_host)
        request.add_header('Authorization', ckan_api_key)
        try:
            response = urlopen(request, data_string)
            # Use the json module to load CKAN's response into a dictionary.
            response_dict = json.loads(response.read().decode())
            assert response_dict['success'] is True
        except HTTPError as error:
            print("{}: {}".format(dataset_dict["name"], error.read()))

    res = {}
    res['id'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, row['organization']+row['url']))
    res['package_id'] = dataset_dict['name']
    res['url'] = row['url']
    res['name'] = row['resource']
    res['description'] = row['resource']
    # res['title'] = row['uri']
    res['mimetype'] = 'application/xls'

    print(res)
    # --------------------------INSERTION / CREATION resource --------------------------------
    request_res = Request('http://%s/api/action/resource_create'%ckan_host)
    request_res.add_header('Authorization', ckan_api_key)
    data_string = quote(json.dumps(res)).encode('utf8')
    try:
        response = urlopen(request_res, data_string)
        # Use the json module to load CKAN's response into a dictionary.
        response_dict = json.loads(response.read().decode())
        assert response_dict['success'] is True
    except HTTPError as error:
        print("{}: {}".format(res['description'], error.read()))


print(count)