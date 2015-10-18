#!/usr/bin/env python3
from urllib.parse import quote
from urllib.request import Request, urlopen, HTTPError
import json, csv, re
from settings import *

# Put the details of the dataset we're going to create into a dict.

strFile = "data/mondial_orga.csv"

count = 0
for organization in csv.DictReader(open(strFile, encoding='utf-8'), delimiter=";"):
    # Use the json module to dump the dictionary to a string for posting.
    organization['name'] = re.sub(r'\W', '-', organization['name']).lower()
    data_string = quote(json.dumps(organization)).encode('utf8')

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