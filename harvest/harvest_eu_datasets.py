#!/usr/bin/env python3
from urllib import request
import json, csv
from settings import *

columns = ['owner_org', 'id', 'title', 'name', 'resources', 'description', 'url', 'organization']
ckan_eu_groups = ["eurovoc_domain_100142", "eurovoc_domain_100143", "eurovoc_domain_100144", "eurovoc_domain_100145", "eurovoc_domain_100146", "eurovoc_domain_100147", "eurovoc_domain_100148", "eurovoc_domain_100149", "eurovoc_domain_100150", "eurovoc_domain_100151", "eurovoc_domain_100152", "eurovoc_domain_100153", "eurovoc_domain_100154", "eurovoc_domain_100155", "eurovoc_domain_100156", "eurovoc_domain_100157", "eurovoc_domain_100158", "eurovoc_domain_100159", "eurovoc_domain_100160", "eurovoc_domain_100161", "eurovoc_domain_100162"]
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
