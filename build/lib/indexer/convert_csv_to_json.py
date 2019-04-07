import csv
import json

CSV_PATH = "../data/04-Feb-2019_with_sentiment.csv"
OUTPUT_PATH = "../data/data.json"

_list = []
csvfile = open(CSV_PATH, 'r', encoding='utf-8', newline='')
jsonfile = open(OUTPUT_PATH, 'w')
fieldnames = ("Username", "Full name", "URL", "Timestamp", "Content",
              "No. replies", "No. retweets", "No. likes", "Sentiment")
reader = csv.DictReader(csvfile, fieldnames)
for index,row in enumerate(reader):
    if index == 0:
        continue
    _list.append(dict(row))
    # json.dump(row, jsonfile)
    # jsonfile.write('\n')

json.dump(_list, jsonfile)
