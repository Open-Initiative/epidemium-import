#!/usr/bin/env python3
from urllib import request
import json, csv
from settings import *

columns = ['owner_org', 'id', 'title', 'description', 'url', 'organization']
groups = ckan_eu_groups
base_url = "http://open-data.europa.eu/data/api/3/action/package_search"

csvout = csv.writer(open('../data/datasets_eu.csv', 'w'), delimiter=';')
csvout.writerow(columns)

for group in groups:
    url = "{}?q=groups:{}".format(base_url, group)
    while url:
        response = request.urlopen(url)
        data = json.loads(response.read().decode())
        url = data.get('next_page')
        for dataset in data['result']['results']:
            line = [dataset[column] for column in columns]
            csvout.writerow(line)
