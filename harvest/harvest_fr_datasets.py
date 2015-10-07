#!/usr/bin/env python3
from urllib import request
import json, csv
import sys
columns = ['owner', 'id', 'title', 'resources', 'description', 'uri', 'organization']
organizations = [org['name'] for org in csv.DictReader(open("../data/organizations.csv", encoding='utf-8'), delimiter=";")]
url = "https://www.data.gouv.fr/api/1/datasets/?page_size=200"

csvout = csv.writer(open('../data/dataset_fr_1.csv', 'w', encoding='utf-8'), delimiter=';')
csvout.writerow(columns)

count = 0

while url:
    response = request.urlopen(url)
    data = json.loads(response.read().decode())
    url = data['next_page']
    for dataset in data['data']:
        if dataset['organization'] and dataset['organization']['id'] in organizations:
            line = [dataset[column] for column in columns]
            csvout.writerow(line)
            count = count+1
            sys.exit(1)
            if count%10 == 0:
                print('count', count)
                sys.exit(1)

            if count > 100:
                sys.exit(1)


print('count', count)

