__author__ = 'PC-DD-10'

from urllib import request
import json, csv
from settings import *

columns = ['owner_org', 'id', 'title', 'name', 'resources', 'notes', 'url', 'organization']
base_url = "http://datahub.io/api/3/action/package_search"

csvout = csv.writer(open('../data/datasets_datahub_normal.csv', 'w'), delimiter=';')
csvout.writerow(columns)

data_json = json.load(open('../data/datahub_normal.json', 'r', encoding='utf-8'))

for dataset in data_json['result']['results']:
    line = [dataset[column] for column in columns]
    csvout.writerow(line)
