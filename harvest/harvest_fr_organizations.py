#!/usr/bin/env python3
from urllib import request
import json, csv
from settings import *

headers = ['description', 'name', 'logo', 'title', 'page']
columns = ['description', 'id', 'logo', 'name', 'page']
url = "https://www.data.gouv.fr/api/1/organizations/"

csvout = csv.writer(open('../data/organizations.csv', 'w', encoding='utf-8'), delimiter=';')
csvout.writerow(headers)

count = 0

while url:
    response = request.urlopen(url)
    data = json.loads(response.read().decode())
    url = data['next_page']
    for organization in data['data']:
        if organization['name'] in ckan_fr_organizations:
            print(organization['name'])
            line = [organization[column] for column in columns]
            csvout.writerow(line)

            count = count + 1

print('count', count)
