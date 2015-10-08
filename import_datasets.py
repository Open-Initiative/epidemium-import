#!/usr/bin/env python3
from urllib.parse import quote
from urllib.request import Request, urlopen, HTTPError
import json, csv
from settings import *
import ast
import argparse

parser = argparse.ArgumentParser(description='debut / fin / nombres de datasets')
parser.add_argument('-s', '--start', type=int, default=0, help='debut de ligne' )
parser.add_argument('-e', '--end', type=int, default=0, help='s arrete a stop-1 , si O ou null alors le script va a la fin ')
parser.add_argument('-c', '--count', type=int, default=0, help='nombre de boucles a effectuer si 0 ou null alors pas compris en compte' )
args = parser.parse_args()

# LOOP =  17688
# #res count 2
# loop_count_res =  75748

loop_count = 0
loop_count_res = 0
loop_serie = args.count
loop_start = args.start

loop_end = args.end
skip_dataset = False
skip_resource = False
debug_datatset = False
debug_resource = False



for row in csv.DictReader(open("data/dataset_fr.csv", encoding='utf-8'), delimiter=";"):

    print("LOOP = ", loop_count)
    # skip start
    if loop_start > loop_count:
        loop_count += 1
        continue

    # skip end
    if loop_end <= loop_count and loop_end > 0:
        break

    # skip end
    if loop_start + loop_serie <= loop_count and loop_serie > 0:
        break

    dataset_dict = {}
    # pour resources
    package_id = row['id']

    dataset_dict['name'] = package_id
    dataset_dict['title'] = row['title']
    dataset_dict['notes'] = row['description']
    dataset_dict['url'] = row['uri']
    organization = ast.literal_eval(row['organization'])
    dataset_dict['owner_org'] = organization['id']




    if debug_datatset:
        print("----------dataset------------")
        # print(row)
        print(quote(json.dumps(row)))
        print(type(row))
        # dict_keys(['uri', 'description', 'id', 'title', 'resources', 'organization', 'owner'])
        print(row.keys())

        print("----------organization------------")
        print(row['organization'])
        # dict_keys(['class', 'uri', 'name', 'id', 'slug', 'page', 'logo'])
        print(organization.keys())

        print("----------dataset to SEND------------")
        # print(dataset_dict)



    # --------------------------INSERTION / CREATION dataset --------------------------------
    if not skip_dataset:
        request = Request('http://%s/api/action/package_create'%ckan_host)
        request.add_header('Authorization', ckan_api_key)
        data_string = quote(json.dumps(dataset_dict)).encode('utf8')
        try:
            response = urlopen(request, data_string)
            # Use the json module to load CKAN's response into a dictionary.
            response_dict = json.loads(response.read().decode())
            assert response_dict['success'] is True
        except HTTPError as error:
            print("{}: {}".format(row['title'], error.read()))




    resources = ast.literal_eval(row['resources'])

    if debug_resource:
        print("----------resources------------")
        print(row['resources'])
        print(resources[0].keys())
        # dict_keys(['checksum', 'url', 'type', 'description', 'mime', 'created_at', 'id', 'last_modified',
        # 'published', 'is_available', 'format', 'size', 'metrics', 'title'])

    print('#res count', len(resources))
    for res in resources:

        loop_count_res += 1
        res['package_id'] = package_id
        res['resource_type'] = res['type']
        res['mimetype'] = res['mime']
        res['created'] = res['created_at']

        if debug_resource:
            print("----------res------------")
            print(res)


        # --------------------------INSERTION / CREATION resource --------------------------------
        if not skip_resource:
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
    loop_count += 1


print('loop_count_res = ', loop_count_res)


# ----------------------------------------------------------
# request = Request('http://%s/api/action/package_create'%ckan_host)
# request.add_header('Authorization', ckan_api_key)
# try:
#     response = urlopen(request, data_string)
#     # Use the json module to load CKAN's response into a dictionary.
#     response_dict = json.loads(response.read().decode())
#     assert response_dict['success'] is True
# except HTTPError as error:
#     print("{}: {}".format(organization["name"], error.read()))
