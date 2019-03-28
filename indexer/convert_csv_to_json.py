import csv
import json

_list = []
csvfile = open('data/04-Feb-2019.csv', 'r', encoding='utf-8', newline='')
jsonfile = open('data/data.json', 'w')
fieldnames = ("Username", "Full name", "URL", "Timestamp", "Content", "No. replies", "No. retweets", "No. likes")
reader = csv.DictReader(csvfile, fieldnames)
for index,row in enumerate(reader):
    if index == 0:
        continue
    _list.append(dict(row))
    # json.dump(row, jsonfile)
    # jsonfile.write('\n')

json.dump(_list, jsonfile)
