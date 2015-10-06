#!/usr/bin/env python3
from urllib import request
import json, csv

columns = ['private', 'featured', 'frequency', 'owner', 'id', 'badges', 'title', 'spatial', 'supplier', 'resources', 'description', 'tags', 'deleted', 'metrics', 'last_modified', 'community_resources', 'slug', 'frequency_date', 'license', 'created_at', 'uri', 'temporal_coverage', 'extras', 'organization', 'page']
organizations = [line.strip() for line in open('organisations.txt')]
url = "https://www.data.gouv.fr/api/1/datasets/"

csvout = csv.writer(open('out.csv', 'w'), delimiter=';')
csvout.writerow(columns)

while url:
    response = request.urlopen(url)
    data = json.loads(response.read().decode())
    url = data['next_page']
    for dataset in data['data']:
        if dataset['organization'] and dataset['organization']['name'] in organizations:
            print(dataset['organization']['name'])
            line = [dataset[column] for column in columns]
            csvout.writerow(line)

