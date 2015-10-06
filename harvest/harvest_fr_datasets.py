#!/usr/bin/env python3
from urllib import request
import json, csv

columns = ['owner', 'id', 'title', 'resources', 'description', 'uri', 'organization']
organizations = [org['name'] for org in csv.DictReader(open("../data/organizations.csv"), delimiter=";")]
url = "https://www.data.gouv.fr/api/1/datasets/?page_size=200"

csvout = csv.writer(open('../data/dataset_fr.csv', 'w'), delimiter=';')
csvout.writerow(columns)

while url:
    response = request.urlopen(url)
    data = json.loads(response.read().decode())
    url = data['next_page']
    for dataset in data['data']:
        if dataset['organization'] and dataset['organization']['id'] in organizations:
            line = [dataset[column] for column in columns]
            csvout.writerow(line)

