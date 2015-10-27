#!/usr/bin/env python3
import ast
from urllib.parse import quote
from urllib.request import Request, urlopen, HTTPError
from urllib import request
import json, csv
from settings import *

# Put the details of the dataset we're going to create into a dict.
count = 0
max = 0
insert_org = True
insert_dataset = True
insert_resource = True

dataset_dump = []
for row in csv.DictReader(open("data/datasets_datahub_normal.csv"), delimiter=";"):

    if count >= max and max > 0:
        continue

    if len(row['organization']) == 0:
        continue

    print(row)
    # if len(row['organization']) == 0:
    #     continue




    organization  = ast.literal_eval(row['organization'])
    resources_list = ast.literal_eval(row['resources'])

    dict_dataset = {}
    dict_dataset = row

    dict_dataset.pop('organization', None)
    dict_dataset.pop('resources', None)

    if insert_org:
        data_string = quote(json.dumps(organization)).encode('utf8')
        print(organization)
        # We'll use the organization_create function to create a new organization.
        request = Request('http://%s/api/action/organization_create' %ckan_host)
        request.add_header('Authorization', ckan_api_key)
        try:
            response = urlopen(request, data_string)
            # Use the json module to load CKAN's response into a dictionary.
            response_dict = json.loads(response.read().decode())
            assert response_dict['success'] is True
            count += 1
        except HTTPError as error:
            print("{}: {}".format(organization["name"], error.read()))

        print(count)

    if insert_dataset:
        dict_dataset['name'] = dict_dataset['name'].lower()
        # ajout
        dict_dataset['description'] = dict_dataset['notes']
        data_string = quote(json.dumps(dict_dataset)).encode('utf8')
        print(dict_dataset)
        # We'll use the organization_create function to create a new organization.
        request = Request('http://%s/api/action/package_create' %ckan_host)
        request.add_header('Authorization', ckan_api_key)
        try:
            dataset_dump.append(dict_dataset["id"])
            response = urlopen(request, data_string)
            # Use the json module to load CKAN's response into a dictionary.
            response_dict = json.loads(response.read().decode())
            assert response_dict['success'] is True

        except HTTPError as error:
            print("{}: {}".format(dict_dataset["id"], error.read()))

        count += 1
        print(count)


    if insert_resource:
        for resource in resources_list:
            resource['package_id'] = row['id']
            data_string = quote(json.dumps(resource)).encode('utf8')
            request = Request('http://%s/api/action/resource_create' %ckan_host)
            request.add_header('Authorization', ckan_api_key)
            try:
                response = urlopen(request, data_string)
                # Use the json module to load CKAN's response into a dictionary.
                response_dict = json.loads(response.read().decode())
                assert response_dict['success'] is True

            except HTTPError as error:
                print("{}: {}".format(resource["name"], error.read()))

            count += 1
            print(count)

print(count)

