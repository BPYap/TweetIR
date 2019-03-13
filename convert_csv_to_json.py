import csv
import json
list=[]
csvfile = open('data/04-Feb-2019.csv', 'r')
jsonfile = open('data/data.json', 'w')
fieldnames = ("Username","Full name","URL","Timestamp","Content","No. replies","No. retweets","No. likes")
reader = csv.DictReader( csvfile, fieldnames)
for index,row in enumerate(reader):
    if index==0:continue
    list.append(dict(row))
    #json.dump(row, jsonfile)
    #jsonfile.write('\n')
json.dump(list,jsonfile)
